#!/usr/bin/env python3
"""
Boersen-Screening: NASDAQ-100, Dow Jones 30, DAX 40.
Version 20 (2026-08-20): Kaufen-Anteil Analysten komplett neu berechnet -
nicht mehr Yahoos eigene "aktueller Konsens"-Zahl (deren genaue Aktualitaet
nicht nachvollziehbar war), sondern eigene Berechnung aus den rohen
Einzel-Ratings: pro Bank zaehlt NUR die zeitlich juengste Einstufung
(Dedupe), aelter als CONSENSUS_MAX_AGE_DAYS (120 Tage, ca. 4 Monate) faellt
die Bank komplett raus. Freitext-Grades (Overweight, Outperform,
Equal-Weight, Underperform etc.) werden ueber eine Mapping-Tabelle zu
Kaufen/Halten/Verkaufen zusammengefasst; nicht zuordenbare Begriffe zaehlen
nicht mit. Nutzt dieselbe schon geladene Tabelle, kein Mehraufwand - die
alte, separate Yahoo-Konsens-Abfrage in get_fundamentals ist entfernt
(spart sogar einen Netzwerkaufruf pro Wert).

Version 19: RSI auf drei Zeitebenen (Tag/Woche/Stunde) in der
Analysten-Filter-Tabelle, jede Ebene ECHT neu berechnet auf echten Kerzen
dieser Zeitebene (RSI Woche: Wochenschlusskurse resampled aus den
Tagesdaten; RSI Stunde: echte 60-Minuten-Kerzen, nur fuer die
Filtertreffer geladen, um den taeglichen Lauf nicht zu verlangsamen).

Version 18: Radikal vereinfacht - der Bericht zeigt jetzt nur noch den
Analysten-Filter (Kursziel >=X%, Kaufen-Anteil >=Y%) plus die zugehoerige
Einzelaufstellung der Ratingaenderungen. Die frueheren Turnaround-/
Momentum-/Value-Top-10-Tabellen, die Rohstoffe/Krypto-Uebersicht und die
taeglichen Veraenderungsmeldungen sind entfernt. Score-Berechnung laeuft
intern unveraendert weiter (u.a. fuer den Value-Trap-Ausschluss im
Filter), wird aber nicht mehr angezeigt.

Erzeugt drei getrennte Ranglisten (Turnaround, Momentum, Value/Qualitaet),
vergleicht sie mit dem Vortag und schreibt einen Report, der NUR
Veraenderungen zeigt.

Ausgabe:
  docs/report.md      -> der Morgen-Report (wird vom Claude-Task gelesen)
  docs/report.json    -> gleiche Inhalte maschinenlesbar
  state/state.json    -> Zustand von heute (Basis fuer den Vergleich morgen)
  state/fundamentals.json -> Cache langsamer Fundamentaldaten (max. 7 Tage alt)
  state/analyst.json      -> Cache der Analysten-Ratingaenderungen (max. 1 Tag alt)
  state/rank_history.json -> rollierende Rang-Historie (12 Tage, Tiefe 40 je Liste)

KEINE Anlageberatung. Das Skript sortiert Kennzahlen, mehr nicht.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import kurse

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent
UNIVERSE_FILE = BASE / "universe.json"
DOCS_DIR = BASE / "docs"
EXTERN_RATINGS_FILE = DOCS_DIR / "analysten_extern.csv"
STATE_DIR = BASE / "state"
STATE_FILE = STATE_DIR / "state.json"
FUND_FILE = STATE_DIR / "fundamentals.json"
ANALYST_FILE = STATE_DIR / "analyst.json"
HISTORY_FILE = STATE_DIR / "rank_history.json"

TOP_N = 15             # Groesse jeder angezeigten Rangliste
TRACK_N = 40            # Tiefe der intern gefuehrten Liste (fuer Rang-Historie)
HISTORY_KEEP_DAYS = 12  # Rollierendes Fenster - deckt auch Feiertage/Brueckentage ab
SECTOR_CAP = 3         # maximal so viele Werte je Sektor pro Rangliste
RANK_JUMP = 5         # ab wie vielen Plaetzen eine Bewegung gemeldet wird
HISTORY_PERIOD = "10y"  # Basis fuer das Allzeithoch
FUND_MAX_AGE_DAYS = 7    # langsame Fundamentaldaten (KGV, Marge, Schulden) hoechstens so alt
ANALYST_MAX_AGE_DAYS = 1  # Ratingaenderungen taeglich frisch - das ist das kurzfristige Signal
# Bei jeder Erweiterung der gespeicherten Felder hier hochzaehlen. Ein Cache
# mit abweichender Version wird ignoriert (sofort neu geholt), egal wie
# frisch er nach dem Alter waere - sonst benutzt ein neuer Programmlauf
# unbemerkt einen Cache mit alter, unvollstaendiger Datenstruktur.
FUND_CACHE_VERSION = 5   # 5 ab 24.08.2026: Feld "country" ergaenzt
ANALYST_CACHE_VERSION = 4
REVISION_WINDOW_DAYS = 30  # Fenster fuer "kurzfristige" Analysten-Ratingaenderungen
TARGET_FRESH_DAYS = 14     # Kursziel gilt als "frisch", wenn eine Ratingaenderung diese Zeit nicht ueberschreitet
CONSENSUS_MAX_AGE_DAYS = 120  # ~4 Monate: aeltere Einzelwertungen zaehlen nicht mehr mit
ANALYST_FILTER_MIN_UPSIDE = 15    # Mindest-Kurspotenzial zum Analysten-Kursziel, in Prozent
ANALYST_FILTER_MIN_KAUFEN_PCT = 75  # Mindestanteil "Kaufen"-Einstufungen, in Prozent
ANALYST_FILTER_TOP_N = 20
EARNINGS_WARN_DAYS = 5  # Warnung vor Quartalszahlen

LISTS = ("turnaround", "momentum", "value")
LIST_TITLES = {
    "turnaround": "Turnaround (Bodenbildung nach Absturz)",
    "momentum": "Momentum (Staerke nahe Allzeithoch)",
    "value": "Value / Qualitaet",
}


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def ramp(x: float, lo: float, hi: float) -> float:
    """0.0 bei lo, 1.0 bei hi, linear dazwischen. lo>hi kehrt die Richtung um."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return 0.0
    if lo == hi:
        return 1.0 if x >= hi else 0.0
    v = (x - lo) / (hi - lo)
    return float(min(1.0, max(0.0, v)))


def plateau(x: float, lo: float, opt_lo: float, opt_hi: float, hi: float) -> float:
    """Trapez: 0 unter lo, 1 zwischen opt_lo und opt_hi, 0 ueber hi."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return 0.0
    if x < opt_lo:
        return ramp(x, lo, opt_lo)
    if x > opt_hi:
        return ramp(x, hi, opt_hi)
    return 1.0


# Zuordnung der von Banken verwendeten Freitext-Begriffe zu Kaufen/Halten/
# Verkaufen. Nicht erschoepfend (jede Bank hat eigene Begriffe) - unbekannte
# Begriffe werden NICHT geraten, sondern als "nicht zuordenbar" ausgewiesen
# und aus der Prozentrechnung rausgehalten, um die Zahl nicht zu verfaelschen.
GRADE_BUY_TERMS = {
    "buy", "strong buy", "outperform", "overweight", "accumulate", "add",
    "positive", "conviction buy", "top pick", "sector outperform",
}
GRADE_HOLD_TERMS = {
    "hold", "neutral", "equal-weight", "equalweight", "equal weight",
    "market perform", "sector perform", "in-line", "inline", "peer perform",
    "perform", "market weight",
}
GRADE_SELL_TERMS = {
    "sell", "underperform", "underweight", "reduce", "negative",
    "strong sell", "sector underperform",
}


def classify_grade(grade: str | None) -> str | None:
    """Ordnet einen Freitext-Grade (z.B. 'Overweight') in Kaufen/Halten/
    Verkaufen ein. Gibt None zurueck, wenn der Begriff nicht sicher
    zuordenbar ist - lieber ausschliessen als falsch einordnen."""
    if not grade:
        return None
    g = grade.strip().lower()
    if g in GRADE_BUY_TERMS:
        return "buy"
    if g in GRADE_HOLD_TERMS:
        return "hold"
    if g in GRADE_SELL_TERMS:
        return "sell"
    return None


def compute_consensus_from_actions(ud: pd.DataFrame, date_col: str, cutoff) -> dict:
    """Eigene, saubere Kaufen/Halten/Verkaufen-Aufteilung statt Yahoos
    undurchsichtiger 'aktueller Konsens'-Zahl: pro Bank NUR die juengste
    Einstufung, und nur wenn diese nicht aelter als CONSENSUS_MAX_AGE_DAYS
    ist - eine Bank, die vor 5 Monaten zuletzt bewertet hat, zaehlt gar
    nicht mehr mit (nicht nur "die alte Wertung ignorieren", sondern die
    Bank faellt komplett raus, wie gewuenscht)."""
    recent = ud[ud[date_col] >= cutoff]
    if recent.empty or "Firm" not in recent.columns:
        return {"kaufen_pct": None, "halten_pct": None, "verkaufen_pct": None,
                "total": 0, "unclassified": 0, "firmen": []}

    # Pro Bank die zeitlich juengste Zeile behalten
    latest_per_firm = recent.sort_values(date_col).groupby("Firm", as_index=False).last()

    buy = hold = sell = unclassified = 0
    for _, r in latest_per_firm.iterrows():
        grade = r.get("ToGrade")
        cls = classify_grade(grade)
        if cls == "buy":
            buy += 1
        elif cls == "hold":
            hold += 1
        elif cls == "sell":
            sell += 1
        else:
            unclassified += 1

    firmen = []
    for _, r in latest_per_firm.iterrows():
        firmen.append({"firm": str(r.get("Firm")),
                       "date": str(r[date_col].date()),
                       "grade": (str(r.get("ToGrade")) if pd.notna(r.get("ToGrade")) else None),
                       "target": None, "quelle": "Yahoo"})

    total = buy + hold + sell
    if total == 0:
        return {"kaufen_pct": None, "halten_pct": None, "verkaufen_pct": None,
                "total": 0, "unclassified": unclassified}
    return {
        "kaufen_pct": round(buy / total * 100),
        "halten_pct": round(hold / total * 100),
        "verkaufen_pct": round(sell / total * 100),
        "total": total,
        "unclassified": unclassified,
    }


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def clean_name(name: str | None, ticker: str) -> str:
    """Yahoo liefert deutsche Namen fest breitenformatiert mit angehaengtem
    Aktiengattungs-Kuerzel (z.B. 'Bayer AG                      N').
    Mehrfache Leerzeichen zusammenziehen und das einzelne Buchstabenkuerzel
    am Ende entfernen."""
    if not name:
        return ticker
    n = " ".join(name.split())
    n = re.sub(r"\s[A-Z]$", "", n)
    return n or ticker


def safe(d: dict, key: str, default=None):
    v = d.get(key, default)
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return v


# ---------------------------------------------------------------------------
# Datenbeschaffung
# ---------------------------------------------------------------------------

def load_universe() -> tuple[dict, dict, dict]:
    raw = json.loads(UNIVERSE_FILE.read_text(encoding="utf-8"))
    benchmarks = raw["benchmarks"]
    members: dict[str, list[str]] = {}
    for idx in benchmarks:
        for t in raw.get(idx, []):
            members.setdefault(t, []).append(idx)
    # Rohstoffe/Krypto: bewusst getrennt von den Aktien-Ranglisten. Sie haben
    # keine Fundamentaldaten, keinen Sektor und keinen Index - der Value-Score
    # und der Sektor-Deckel ergeben fuer sie keinen Sinn. Sie laufen technisch
    # (Turnaround-/Momentum-Kriterien) mit, werden aber nur informativ gezeigt.
    extras: dict[str, str] = {}
    extras.update(raw.get("COMMODITIES", {}))
    extras.update(raw.get("CRYPTO", {}))
    return members, benchmarks, extras


def fetch_yahoo(tickers: list[str]) -> dict[str, pd.DataFrame]:
    """Kursdaten von Yahoo ueber den gemeinsamen Cache in kurse.py.

    Bis 29.08.2026 rief dieses Skript yf.download() direkt auf - der
    dritte von sechs getrennten Kursabrufen im Repo (Frage 40, Fragen-
    Blatt). Umgestellt auf kurse.kerzen_batch() am 30.08.2026: dieselbe
    Bündelung wie vorher (40er-Chunks, Threads), aber jetzt im selben
    Plattencache wie marktdaten.py/tiefs.py/phasen.py - ein Wert, der
    heute schon fuer denselben Zeitraum UND dieselbe auto_adjust-
    Einstellung geladen wurde, kostet keinen zweiten Abruf.

    auto_adjust=True bewusst erhalten (kurse.py selbst nutzt False) -
    sonst wuerde die Umstellung nicht nur Code zusammenlegen, sondern
    still die Kursbasis fuer das Allzeithoch und alle Kennzahlen dieses
    Skripts aendern.

    kerzen_batch() akzeptiert schon ab 30 Kerzen (kurse.MINDESTKERZEN) -
    zu wenig fuer ein 10-Jahres-Allzeithoch. Die alte Schwelle von hier
    (260 Kerzen, gut ein Jahr) bleibt deshalb als eigene Nachpruefung
    erhalten, sonst wuerden neu gelistete Werte mit duenner Historie
    durchrutschen, wo sie vorher ausgeschlossen waren.
    """
    roh = kurse.kerzen_batch(tickers, period=HISTORY_PERIOD, auto_adjust=True)
    return {t: df for t, df in roh.items() if len(df) > 260}


def fetch_stooq(ticker: str) -> pd.DataFrame | None:
    """Fallback, falls Yahoo einen Wert nicht liefert.

    stooq_symbol() und der eigentliche Abruf leben seit 30.08.2026 in
    kurse.py (Frage 44) - hier nur noch die 260-Tage-Nachpruefung, die
    dieses Skript schon vorher hatte und kurse.kerzen_stooq() nicht kennt.
    """
    df = kurse.kerzen_stooq(ticker)
    if df is None or "Close" not in df.columns or len(df) < 260:
        return None
    if "Volume" not in df.columns:
        df["Volume"] = np.nan
    return df


def get_prices(tickers: list[str]) -> dict[str, pd.DataFrame]:
    print(f"Lade Kursdaten fuer {len(tickers)} Werte ...")
    prices = fetch_yahoo(tickers)
    missing = [t for t in tickers if t not in prices]
    if missing:
        print(f"  {len(missing)} Werte fehlen, versuche Stooq-Fallback ...")
        for t in missing:
            df = fetch_stooq(t)
            if df is not None:
                prices[t] = df
            time.sleep(0.3)
    print(f"  {len(prices)} von {len(tickers)} Werten geladen.")
    if len(prices) < len(tickers) * 0.5:
        print("  ! Weniger als die Haelfte geladen - Datenquelle vermutlich gestoert.")
    return prices


def get_hourly_rsi(tickers: list[str]) -> dict[str, float | None]:
    """Echter Stunden-RSI, NEU berechnet auf echten Stundenkerzen - kein
    Umrechnen des Tages-RSI. Bewusst nur fuer eine kleine, bereits gefilterte
    Tickerliste (nicht das ganze Universum), da Yahoo dafuer einen eigenen,
    zusaetzlichen Datenabruf je Ticker braucht (Intraday-Daten sind separat
    von den Tagesdaten). Laut Datenlage geht das bei Yahoo bis zu ca. 730
    Tage zurueck fuer 60-Minuten-Kerzen - fuer einen 14-Perioden-RSI reicht
    ein deutlich kuerzeres Fenster locker aus."""
    if not tickers:
        return {}
    print(f"Lade Stundendaten fuer {len(tickers)} Filtertreffer ...")

    out: dict[str, float | None] = {}
    for t in tickers:
        try:
            # kurse.stundenkerzen() statt eigenem yf.download() (30.08.2026,
            # Frage 40) - war hier schon vorher ein Aufruf je Ticker ohne
            # Threads, also keine Batching-Effizienz zu verlieren. Gewinn:
            # gemeinsamer Cache mit anderen Skripten, KURSQUELLE-Routing
            # (ASML) automatisch dabei. auto_adjust=True erhaelt das
            # bisherige Verhalten dieses Skripts.
            df = kurse.stundenkerzen(t, period="60d", auto_adjust=True)
            if df is None or df.empty:
                out[t] = None
                continue
            close = df["Close"].dropna()
            if len(close) < 20:
                out[t] = None
                continue
            rsi_h = rsi(close)
            out[t] = round(float(rsi_h.iloc[-1]), 1)
        except Exception:  # noqa: BLE001
            out[t] = None
        time.sleep(0.3)
    ok = sum(1 for v in out.values() if v is not None)
    print(f"  Stunden-RSI fuer {ok}/{len(tickers)} Werte erhalten.")
    return out


def get_fundamentals(tickers: list[str]) -> dict:
    """Fundamentaldaten, hoechstens FUND_MAX_AGE_DAYS alt (Cache)."""
    cache = {"updated": None, "data": {}}
    if FUND_FILE.exists():
        try:
            cache = json.loads(FUND_FILE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass

    age_days = 999.0
    if cache.get("updated"):
        try:
            upd = datetime.fromisoformat(cache["updated"])
            age_days = (datetime.now(timezone.utc) - upd).total_seconds() / 86400
        except Exception:  # noqa: BLE001
            pass

    if (age_days < FUND_MAX_AGE_DAYS and cache.get("data")
            and cache.get("version") == FUND_CACHE_VERSION):
        print(f"Fundamentaldaten aus Cache ({age_days:.1f} Tage alt).")
        return cache["data"]
    if cache.get("data") and cache.get("version") != FUND_CACHE_VERSION:
        print("Cache-Format veraltet (neue Version) - hole Fundamentaldaten neu.")

    print("Aktualisiere Fundamentaldaten (dauert einige Minuten) ...")
    import yfinance as yf

    # PEG-Ratio bewusst nicht mehr genutzt: bei Yahoo haeufig aus nicht
    # zusammenpassenden Zeitraeumen berechnet und dadurch irrefuehrend
    # (z.B. PEG 0.14 bei Werten mit moderatem Wachstum). Zielpreis und
    # Analystenmeinung liefert die separate, taeglich aktualisierte
    # get_analyst_data(), damit sie nicht eine Woche alt werden.
    keys = (
        "trailingPE", "forwardPE", "priceToBook", "profitMargins",
        "operatingMargins", "revenueGrowth", "earningsGrowth", "debtToEquity",
        "freeCashflow", "returnOnEquity", "dividendYield", "earningsTimestamp",
        "shortName", "sector", "country",
        "targetMeanPrice", "numberOfAnalystOpinions", "recommendationKey",
    )
    data: dict[str, dict] = {}
    for n, t in enumerate(tickers, 1):
        try:
            tk = yf.Ticker(t)
            info = tk.info or {}
            data[t] = {k: info.get(k) for k in keys}
            try:
                isin = tk.isin
                data[t]["isin"] = isin if isin and isin != "-" else None
            except Exception:  # noqa: BLE001
                data[t]["isin"] = None
        except Exception:  # noqa: BLE001
            data[t] = {}
        if n % 25 == 0:
            print(f"  {n}/{len(tickers)}")
        time.sleep(0.25)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    FUND_FILE.write_text(json.dumps(
        {"updated": datetime.now(timezone.utc).isoformat(), "version": FUND_CACHE_VERSION, "data": data},
        indent=1), encoding="utf-8")
    return data


def get_analyst_data(tickers: list[str]) -> dict:
    """Analysten-Ratingaenderungen der letzten REVISION_WINDOW_DAYS Tage.

    Bewusst taeglich frisch (1-Tage-Cache), waehrend die traegen
    Fundamentaldaten wochenweise gecacht werden: eine Herauf- oder
    Herabstufung von gestern ist genau das kurzfristige Signal, das
    eine Woche alter Cache verschlucken wuerde. Der Abruf ist dafuer
    bewusst schlank (nur die Ratingtabelle, nicht der komplette
    Kennzahlensatz), um den taeglichen Lauf nicht unnoetig zu verlangsamen.
    """
    cache = {"updated": None, "data": {}}
    if ANALYST_FILE.exists():
        try:
            cache = json.loads(ANALYST_FILE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass

    age_days = 999.0
    if cache.get("updated"):
        try:
            upd = datetime.fromisoformat(cache["updated"])
            age_days = (datetime.now(timezone.utc) - upd).total_seconds() / 86400
        except Exception:  # noqa: BLE001
            pass

    if (age_days < ANALYST_MAX_AGE_DAYS and cache.get("data")
            and cache.get("version") == ANALYST_CACHE_VERSION):
        print(f"Analysten-Ratings aus Cache ({age_days * 24:.1f} Std. alt).")
        return cache["data"]
    if cache.get("data") and cache.get("version") != ANALYST_CACHE_VERSION:
        print("Cache-Format veraltet (neue Version) - hole Analysten-Ratings neu.")

    print("Aktualisiere Analysten-Ratingaenderungen ...")
    import yfinance as yf

    # Bewusst NUR die Ratingtabelle (leichter Abruf) - Zielpreis, Analystenzahl
    # und Empfehlung kommen aus derselben .info-Abfrage wie die uebrigen
    # Fundamentaldaten (siehe get_fundamentals), um den teuren vollen
    # Datenabruf nicht zusaetzlich taeglich zu wiederholen.
    cutoff = datetime.now(timezone.utc) - pd.Timedelta(days=REVISION_WINDOW_DAYS)
    cutoff_consensus = datetime.now(timezone.utc) - pd.Timedelta(days=CONSENSUS_MAX_AGE_DAYS)
    data: dict[str, dict] = {}
    for n, t in enumerate(tickers, 1):
        entry = {
            "upgrades_30d": 0, "downgrades_30d": 0, "net_30d": 0,
            "last_action": None, "last_firm": None, "last_date": None,
            "actions": [],  # bis zu 5 juengste Einzelaktionen, neueste zuerst
            "consensus": {"kaufen_pct": None, "halten_pct": None, "verkaufen_pct": None,
                          "total": 0, "unclassified": 0, "firmen": []},
            "quelle": "keine",
            "price_targets": {},
            "konsens_firmen": [],
            "merged_firmen": [],
            "merged_ziele": {},
        }
        try:
            tk = yf.Ticker(t)
            ud = tk.upgrades_downgrades
            if ud is not None and not ud.empty:
                ud = ud.reset_index()
                date_col = "GradeDate" if "GradeDate" in ud.columns else ud.columns[0]
                ud[date_col] = pd.to_datetime(ud[date_col], utc=True, errors="coerce")

                # Eigene Kaufen/Halten/Verkaufen-Aufteilung: pro Bank nur die
                # juengste Wertung, aeltere als CONSENSUS_MAX_AGE_DAYS zaehlen
                # nicht mehr mit. Nutzt dieselbe schon geladene Tabelle wie
                # unten - kein zusaetzlicher Datenabruf.
                entry["consensus"] = compute_consensus_from_actions(ud, date_col, cutoff_consensus)
                if entry["consensus"]["total"] > 0:
                    entry["quelle"] = "Einzelratings"
                entry["konsens_firmen"] = entry["consensus"].pop("firmen", [])

                recent = ud[ud[date_col] >= cutoff].sort_values(date_col)
                if not recent.empty:
                    actions = recent["Action"].astype(str).str.lower()
                    entry["upgrades_30d"] = int(actions.isin(["up", "init"]).sum())
                    entry["downgrades_30d"] = int((actions == "down").sum())
                    entry["net_30d"] = entry["upgrades_30d"] - entry["downgrades_30d"]
                    last = recent.iloc[-1]
                    entry["last_action"] = str(last.get("Action"))
                    entry["last_firm"] = str(last.get("Firm"))
                    entry["last_date"] = str(last[date_col].date())

                    newest_first = recent.sort_values(date_col, ascending=False).head(5)
                    for _, r in newest_first.iterrows():
                        entry["actions"].append({
                            "date": str(r[date_col].date()),
                            "firm": (str(r.get("Firm")) or None) if pd.notna(r.get("Firm")) else None,
                            "action": (str(r.get("Action")).lower() or None) if pd.notna(r.get("Action")) else None,
                            "to_grade": (str(r.get("ToGrade")) or None) if pd.notna(r.get("ToGrade")) else None,
                            "from_grade": (str(r.get("FromGrade")) or None) if pd.notna(r.get("FromGrade")) else None,
                        })
        except Exception:  # noqa: BLE001
            pass

        # Kaskade: Die Eigenberechnung aus den Einzelratings ist erste Wahl.
        # Findet sie nichts (Ratingtabelle leer oder alles aelter als
        # CONSENSUS_MAX_AGE_DAYS - z.B. META, RHM.DE), greift Yahoos
        # aggregierte Zaehlung. Die Herkunft steht in entry['quelle'],
        # damit beides nie verwechselt wird.
        if entry['consensus']['total'] == 0:
            try:
                agg = consensus_from_recommendations(yf.Ticker(t))
                if agg['total'] > 0:
                    entry['consensus'] = agg
                    entry['quelle'] = 'Aggregat'
            except Exception:  # noqa: BLE001
                pass
        try:
            entry['price_targets'] = yf.Ticker(t).analyst_price_targets or {}
        except Exception:  # noqa: BLE001
            entry['price_targets'] = {}

        data[t] = entry
        if n % 25 == 0:
            print(f"  {n}/{len(tickers)}")
        time.sleep(0.2)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    ANALYST_FILE.write_text(json.dumps(
        {"updated": datetime.now(timezone.utc).isoformat(), "version": ANALYST_CACHE_VERSION, "data": data},
        indent=1), encoding="utf-8")
    return data


# ---------------------------------------------------------------------------
# Kennzahlen
# ---------------------------------------------------------------------------

def compute_metrics(df: pd.DataFrame, bench: pd.Series | None) -> dict | None:
    close = df["Close"].dropna()
    if len(close) < 260:
        return None
    vol = df["Volume"].reindex(close.index) if "Volume" in df else pd.Series(index=close.index, dtype=float)

    last = float(close.iloc[-1])
    ath = float(close.max())
    ath_date = close.idxmax()
    dd_ath = (last / ath - 1) * 100
    days_since_ath = int((close.index[-1] - ath_date).days)

    w52 = close.iloc[-252:]
    hi52, lo52 = float(w52.max()), float(w52.min())
    range_pos = (last - lo52) / (hi52 - lo52) * 100 if hi52 > lo52 else 50.0

    sma50_s = close.rolling(50).mean()
    sma100_s = close.rolling(100).mean()
    sma200_s = close.rolling(200).mean()
    sma50 = float(sma50_s.iloc[-1])
    sma100 = float(sma100_s.iloc[-1]) if len(close) >= 100 else None
    sma200 = float(sma200_s.iloc[-1])
    sma50_slope = (sma50_s.iloc[-1] / sma50_s.iloc[-21] - 1) * 100
    sma200_slope = (sma200_s.iloc[-1] / sma200_s.iloc[-21] - 1) * 100

    low_recent = float(close.iloc[-30:].min())
    low_prev = float(close.iloc[-90:-30].min())
    higher_low = low_recent > low_prev
    higher_low_pct = (low_recent / low_prev - 1) * 100 if low_prev > 0 else None

    rsi_s = rsi(close)
    rsi14 = float(rsi_s.iloc[-1])
    rsi_min60 = float(rsi_s.iloc[-60:].min())

    # Wochen-RSI: ECHTE Neuberechnung auf echten Wochenschlusskursen (letzter
    # Handelstag jeder Woche), kein Umrechnen des Tages-RSI. Nutzt dieselben
    # Tagesdaten, die wir ohnehin schon geladen haben - keine zusaetzliche
    # Datenquelle noetig.
    rsi_week = None
    weekly_close = close.resample("W").last().dropna()
    if len(weekly_close) >= 20:
        rsi_week_s = rsi(weekly_close)
        rsi_week = float(rsi_week_s.iloc[-1])

    perf = {}
    for label, n in (("m1", 21), ("m3", 63), ("m6", 126), ("m12", 252)):
        if len(close) > n:
            perf[label] = (last / float(close.iloc[-n - 1]) - 1) * 100

    rs6 = None
    if bench is not None and len(bench) > 126 and "m6" in perf:
        b = bench.dropna()
        bench_perf = (float(b.iloc[-1]) / float(b.iloc[-127]) - 1) * 100
        rs6 = perf["m6"] - bench_perf

    # Volumen-Ausbruch: heutiges Volumen vs. Durchschnitt der 20 Handelstage
    # DAVOR (heute bewusst ausgeschlossen, sonst verzerrt ein Ausbruchstag
    # seinen eigenen Referenzwert). Beantwortet "gibt es gerade einen
    # Ausbruch", nicht "hat die Aktie generell hohes Volumen" - letzteres war
    # die alte, zu lange (60 Tage) und falsch beantwortete Frage.
    vol_breakout = None
    if vol.notna().sum() > 21:
        vol_today = float(vol.iloc[-1])
        vol_avg20 = float(vol.iloc[-21:-1].mean())
        if vol_avg20 > 0:
            vol_breakout = vol_today / vol_avg20

    # Kauf-/Verkaufsdruck der letzten 5 Handelstage: Verhaeltnis des Volumens
    # an Anstiegstagen zu Ruecksetzertagen. Kein Short/Long-Wert (echte
    # Leerverkaufsdaten haben ca. 2 Wochen Meldeverzug und keine 7-Tage-
    # Aufloesung) - stattdessen ein taeglich verfuegbarer Ersatz aus den
    # Kursdaten, die ohnehin schon geladen sind.
    vol_pressure_5d = None
    if vol.notna().sum() > 6:
        diff_all = close.diff()
        up5 = (diff_all > 0).tail(5)
        vol5 = vol.tail(5)
        v_up5 = float(vol5[up5].sum())
        v_dn5 = float(vol5[~up5].sum())
        if v_dn5 > 0:
            vol_pressure_5d = v_up5 / v_dn5

    return {
        "last": round(last, 2),
        "dd_ath": round(dd_ath, 1),
        "days_since_ath": days_since_ath,
        "range_pos": round(range_pos, 1),
        "above_sma50": last > sma50,
        "above_sma100": (last > sma100) if sma100 is not None else None,
        "above_sma200": last > sma200,
        "pct_above_sma50": (last / sma50 - 1) * 100 if sma50 else None,
        "pct_above_sma100": (last / sma100 - 1) * 100 if sma100 else None,
        "pct_above_sma200": (last / sma200 - 1) * 100 if sma200 else None,
        "sma50_slope": round(float(sma50_slope), 2),
        "sma200_slope": round(float(sma200_slope), 2),
        "higher_low": bool(higher_low),
        "higher_low_pct": round(higher_low_pct, 1) if higher_low_pct is not None else None,
        "rsi14": round(rsi14, 1),
        "rsi_min60": round(rsi_min60, 1),
        "rsi_week": round(rsi_week, 1) if rsi_week is not None else None,
        "perf": {k: round(v, 1) for k, v in perf.items()},
        "rs6": round(rs6, 1) if rs6 is not None else None,
        "vol_pressure_5d": round(vol_pressure_5d, 2) if vol_pressure_5d is not None else None,
        "vol_breakout": round(vol_breakout, 2) if vol_breakout is not None else None,
    }


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------

def pressure_score(vp: float | None, weight: float) -> tuple[float, str]:
    """Kauf-/Verkaufsdruck: Verhaeltnis von Volumen an Anstiegs- zu
    Ruecksetzertagen. 1.0 = ausgeglichen. PLATEAU auf Log-Skala:

    - unter 0.6x: klar mehr Verkaufs- als Kaufvolumen -> 0 Punkte
    - 0.6x-1.2x: Uebergangszone, steigt linear von 0 auf voll
    - 1.2x-2.5x: die "gute" Zone -> volle Punktzahl
    - ueber 2.5x: faellt wieder leicht ab, Sockel bei 55% (Grund: ein
      Vielfaches wie 4x oder 6x an nur 5 Tagen ist bei Einzelwerten oft ein
      einzelner Ausreissertag statt breiter Kaufbereitschaft)
    """
    if vp is None:
        return weight * 0.5, "keine Daten"
    if vp <= 0:
        return 0.0, "keine Daten"

    lv = math.log(vp)
    lo, opt_lo, opt_hi, hi = math.log(0.6), math.log(1.2), math.log(2.5), math.log(6.0)
    floor = 0.55

    if lv <= lo:
        frac = 0.0
    elif lv < opt_lo:
        frac = (lv - lo) / (opt_lo - lo)
    elif lv <= opt_hi:
        frac = 1.0
    elif lv < hi:
        frac = 1.0 - (1.0 - floor) * (lv - opt_hi) / (hi - opt_hi)
    else:
        frac = floor

    label = "mehr Kaeufer als Verkaeufer" if vp > 1.15 else (
        "mehr Verkaeufer als Kaeufer" if vp < 0.87 else "ausgeglichen")
    return weight * frac, f"{label} ({vp:.2f}x)"


def breakout_score(vb: float | None, weight: float) -> tuple[float, str]:
    """Heutiges Volumen vs. 20-Tage-Durchschnitt davor. ACHTUNG andere Zone
    als pressure_score: hier bedeutet 1.0 = genau Durchschnittsvolumen, also
    KEIN Ausbruch. Die "gute" Zone beginnt daher erst deutlich darueber -
    ein Wert von 0.9 (unterdurchschnittliches Volumen) darf keine
    nennenswerten Punkte bekommen, auch wenn er "nah an 1" liegt.

    - bis 1.0x (Durchschnitt oder darunter): 0 Punkte
    - 1.0x-1.5x: leichter Anstieg, aber noch kein echter Ausbruch
    - 2.0x-4.0x: die "gute" Zone -> volle Punktzahl (klarer Ausbruch)
    - ueber 4.0x: faellt wieder leicht ab, Sockel bei 60% (moeglicherweise
      ein einzelnes Sonderereignis wie ein Index-Rebalancing statt echtes
      neues Kaufinteresse)
    """
    if vb is None:
        return weight * 0.5, "keine Daten"
    if vb <= 0:
        return 0.0, "keine Daten"

    lv = math.log(vb)
    lo, opt_lo, opt_hi, hi = math.log(1.0), math.log(2.0), math.log(4.0), math.log(8.0)
    floor = 0.60

    if lv <= lo:
        frac = 0.0
    elif lv < opt_lo:
        frac = (lv - lo) / (opt_lo - lo)
    elif lv <= opt_hi:
        frac = 1.0
    elif lv < hi:
        frac = 1.0 - (1.0 - floor) * (lv - opt_hi) / (hi - opt_hi)
    else:
        frac = floor

    if vb < 1.0:
        label = "unterdurchschnittlich"
    elif vb < 2.0:
        label = "leicht erhoeht"
    else:
        label = "Ausbruch"
    return weight * frac, f"{label} ({vb:.2f}x Ø20T)"


def ma_distance_score(pct_above: float | None, weight: float, ma_label: str) -> tuple[float, str]:
    """Abstand des Kurses zur gleitenden Linie in Prozent, graduell statt
    starrem Ja/Nein - ein Kurs knapp UNTER der Linie (kurz vor Durchbruch)
    bekommt so noch Teilpunkte, ein Kurs weit darueber die volle Punktzahl,
    ein Kurs weit darunter 0."""
    if pct_above is None:
        return weight * 0.5, "keine Daten"
    frac = ramp(pct_above, -3, 3)
    status = "darueber" if pct_above > 0 else "darunter"
    return weight * frac, f"{pct_above:+.1f}% {status} {ma_label}"


def rsi_recovery_score(rsi14: float, rsi_min60: float, weight_base: float,
                        weight_bonus: float) -> tuple[float, str]:
    """RSI-Erholung, stufenlos statt Ja/Nein-Sprung.

    Optimum bewusst bei 40-50, nicht "je niedriger desto besser" und nicht
    bei 50-58: nach Constance Browns "RSI Range Shift" (Standardwerk
    "Technical Analysis for the Trading Professional", vielfach bestaetigt
    von Chart-Technikern) pendelt der RSI starker Aktien in einem echten
    Aufwaertstrend eher zwischen 40 und 80-90 statt zwischen 30 und 70 - die
    40-50-Zone wirkt dort als Unterstuetzung und ist der zuverlaessigere
    Einstieg als der klassische 30er-Bounce, der eher in noch nicht
    trendbestaetigten, seitwaertslaufenden Werten funktioniert. Deshalb
    Optimum bei 40-50, mit Abfall nach oben (ab RSI 70 ueberkauft, egal in
    welchem Regime) UND nach unten (unter 25 ggf. noch im freien Fall, keine
    bestaetigte Wende). "Kam aus einem echten Tief" bleibt ein kleiner Bonus:
    genau das ist der eigentliche Range-Shift-Moment (Wechsel von
    Baeren- auf Bullen-Spanne), aber kein Alles-oder-Nichts-Schalter.
    """
    base = weight_base * plateau(rsi14, 25, 40, 50, 70)
    came_from_low = rsi_min60 < 35
    bonus = weight_bonus if came_from_low else 0.0
    detail = f"RSI {rsi14:.0f}" + (", aus Ueberverkauft" if came_from_low else "")
    return base + bonus, detail


def score_turnaround(m: dict) -> tuple[float, list[str], list[dict]]:
    """Gefallen, aber Boden erkennbar UND die Wende passiert erkennbar JETZT
    (nicht nur "war mal ueberverkauft"). Gewichte summieren sich zu 100.
    Abstand zum Allzeithoch fliesst NICHT mehr ein (siehe Notiz am
    Berichtsende: keine belegte Schwelle, wird nur noch angezeigt).
    Gibt (Gesamt-Score, Kurzbegruendungen, Einzelscore-Aufschluesselung) zurueck."""
    why = []
    b: list[dict] = []

    # Basis (18.75) fuer "ueberhaupt ein hoeheres Tief", plus Bonus (bis 6.25)
    # je nachdem WIE VIEL hoeher (Vergleich: Tiefpunkt der letzten 30
    # Handelstage vs. Tiefpunkt der 90 Tage davor).
    hl_pct = m.get("higher_low_pct")
    if m["higher_low"]:
        bonus = 6.25 * ramp(hl_pct, 0, 15) if hl_pct is not None else 0.0
        p = 18.75 + bonus
        detail = f"ja, 30T-Tief liegt {hl_pct:.1f}% ueber dem 90T-Tief davor" if hl_pct is not None else "ja"
    else:
        p, detail = 0.0, (f"nein, 30T-Tief liegt {hl_pct:.1f}% unter dem 90T-Tief davor" if hl_pct is not None else "nein")
    b.append({"label": "Hoeheres Tief", "points": round(p, 1), "max": 25, "detail": detail})
    if m["higher_low"]:
        why.append("hoeheres Tief")

    p, detail = ma_distance_score(m.get("pct_above_sma50"), 10, "50T-Linie")
    b.append({"label": "Abstand 50T-Linie", "points": round(p, 1), "max": 10, "detail": detail})
    if m["above_sma50"]:
        why.append("ueber 50-Tage-Linie")

    # 100-Tage-Linie als Zwischenschritt zwischen dem kurzfristigen 50T- und
    # dem langfristigen 200T-Trend.
    a100 = m.get("above_sma100")
    p = 5.0 if a100 else 0.0
    b.append({"label": "Ueber 100T-Linie", "points": p, "max": 5,
              "detail": "ja" if a100 else ("nein" if a100 is False else "keine Daten")})

    # Steigt die 50-Tage-Linie SELBST (nicht der Kurs) - ein traeger
    # Trendwende-Fruehindikator, unabhaengig von "Abstand 50T-Linie" oben.
    p = 10 * ramp(m["sma50_slope"], -1, 3)
    b.append({"label": "50T-Linie im Aufwaertstrend", "points": round(p, 1), "max": 10,
              "detail": f"{m['sma50_slope']:+.1f}% Veraenderung der Linie in 21 Tagen"})
    if p > 6:
        why.append("50-Tage-Linie dreht nach oben")

    # RSI aus der Ueberverkauftheit heraus - stufenlos, siehe rsi_recovery_score
    p, detail = rsi_recovery_score(m["rsi14"], m["rsi_min60"], 12, 3)
    b.append({"label": "RSI-Erholung", "points": round(p, 1), "max": 15, "detail": detail})
    if p > 10:
        why.append("RSI erholt sich aus dem ueberverkauften Bereich")

    # Volumen-Ausbruch: heutiges Volumen vs. 20-Tage-Durchschnitt.
    vb = m.get("vol_breakout")
    p, detail = breakout_score(vb, 5)
    b.append({"label": "Volumen-Ausbruch", "points": round(p, 1), "max": 5, "detail": detail})

    p = 10 * plateau(m["range_pos"], 5, 15, 55, 75)
    b.append({"label": "Position 52W-Spanne", "points": round(p, 1), "max": 10,
              "detail": f"{m['range_pos']:.0f}% der Jahres-Spanne (0%=Jahrestief, 100%=Jahreshoch)"})

    # Bestaetigt der Handel der letzten 5 Tage die Wende JETZT, oder wird
    # trotz guter Vorgeschichte gerade verkauft? Unbekannt (None) bekommt
    # neutralen Halbwert statt Abzug. Log-Skala siehe pressure_score.
    vp = m.get("vol_pressure_5d")
    p, detail = pressure_score(vp, 20)
    b.append({"label": "Kauf-/Verkaufsdruck 5T", "points": round(p, 1), "max": 20, "detail": detail})
    if vp is not None and p > 13:
        why.append("Kaufdruck der letzten 5 Tage bestaetigt die Wende")
    elif vp is not None and p < 7:
        why.append("aber: Verkaufsdruck diese Woche - Wende noch nicht bestaetigt")

    total = round(min(sum(x["points"] for x in b), 100.0), 1)
    return total, why, b


def score_momentum(m: dict) -> tuple[float, list[str], list[dict]]:
    """Staerke, nahe am Hoch UND der Ausbruch wird gerade JETZT bestaetigt.
    Gewichte summieren sich zu 100. Abstand zum Allzeithoch fliesst NICHT
    mehr ein (siehe Notiz am Berichtsende), wird nur noch angezeigt."""
    why = []
    b: list[dict] = []

    if m["rs6"] is not None:
        p = 28 * ramp(m["rs6"], -5, 25)
        detail = f"{m['rs6']:+.0f}% staerker/schwaecher als der Index"
        if p > 17:
            why.append(f"relative Staerke +{m['rs6']:.0f}% vs. Index")
    else:
        p, detail = 0.0, "keine Daten"
    b.append({"label": "Rel. Staerke 6M", "points": round(p, 1), "max": 28, "detail": detail})

    p, detail = ma_distance_score(m.get("pct_above_sma50"), 10, "50T-Linie")
    b.append({"label": "Abstand 50T-Linie", "points": round(p, 1), "max": 10, "detail": detail})

    p, detail = ma_distance_score(m.get("pct_above_sma200"), 10, "200T-Linie")
    b.append({"label": "Abstand 200T-Linie", "points": round(p, 1), "max": 10, "detail": detail})
    if m["above_sma50"] and m["above_sma200"]:
        why.append("ueber 50- und 200-Tage-Linie")

    # 100-Tage-Linie als Zwischenschritt.
    a100 = m.get("above_sma100")
    p = 5.0 if a100 else 0.0
    b.append({"label": "Ueber 100T-Linie", "points": p, "max": 5,
              "detail": "ja" if a100 else ("nein" if a100 is False else "keine Daten")})

    p = 10 * ramp(m["sma200_slope"], 0, 4)
    b.append({"label": "200T-Linie im Aufwaertstrend", "points": round(p, 1), "max": 10,
              "detail": f"{m['sma200_slope']:+.1f}% Veraenderung der Linie in 21 Tagen"})
    if p > 6:
        why.append("200-Tage-Linie steigt")

    p = 15 * ramp(m["range_pos"], 60, 90)
    b.append({"label": "Position 52W-Spanne", "points": round(p, 1), "max": 15,
              "detail": f"{m['range_pos']:.0f}% der Jahres-Spanne (0%=Jahrestief, 100%=Jahreshoch)"})

    vb = m.get("vol_breakout")
    p, detail = breakout_score(vb, 4)
    b.append({"label": "Volumen-Ausbruch", "points": round(p, 1), "max": 4, "detail": detail})

    # Bestaetigt der Handel der letzten 5 Tage die Staerke JETZT?
    vp = m.get("vol_pressure_5d")
    p, detail = pressure_score(vp, 18)
    b.append({"label": "Kauf-/Verkaufsdruck 5T", "points": round(p, 1), "max": 18, "detail": detail})
    if vp is not None and p > 10:
        why.append("Kaufdruck der letzten 5 Tage bestaetigt die Staerke")
    elif vp is not None and p < 5:
        why.append("aber: Verkaufsdruck diese Woche trotz Naehe zum Hoch")

    total = round(min(sum(x["points"] for x in b), 100.0), 1)
    return total, why, b


# Gewichte fuer score_value - summieren sich zu genau 100, damit der Score
# nie ueber 100 hinauslaufen kann. PEG bewusst nicht enthalten: bei Yahoo
# haeufig aus nicht zusammenpassenden Zeitraeumen berechnet (siehe Notiz
# in get_fundamentals) und damit irrefuehrend statt hilfreich.
W_PE_IMPROVE = 10   # erwartetes KGV liegt unter dem aktuellen
W_PE_LEVEL = 10     # absolutes Niveau des erwarteten KGV
W_FCF = 15          # positiver Free Cashflow
W_MARGIN = 10       # Nettomarge
W_GROWTH = 15       # Umsatzwachstum
W_ROE = 10          # Eigenkapitalrendite
W_DEBT = 10         # Verschuldungsgrad (niedrig ist besser)
W_STRUCTURE = 5     # Kurs ueber 200-Tage-Linie
W_REVISIONS = 10    # Analysten-Ratingaenderungen, letzte 30 Tage
W_UPSIDE = 5        # Abstand zum mittleren Analysten-Kursziel


def score_value(m: dict, f: dict, a: dict) -> tuple[float, list[str], list[dict]]:
    """Bewertung und Qualitaet, 0-100. Grobe Vorsortierung - Fundamentaldaten
    sind lueckenhaft, siehe SETUP.md Teil D."""
    why: list[str] = []
    b: list[dict] = []

    def add(label: str, points: float, max_: float, detail: str) -> None:
        b.append({"label": label, "points": round(points, 1), "max": max_, "detail": detail})

    if not f:
        for label, max_ in (("KGV verbessert", W_PE_IMPROVE), ("KGV Niveau", W_PE_LEVEL),
                            ("Free Cashflow", W_FCF), ("Marge", W_MARGIN),
                            ("Umsatzwachstum", W_GROWTH), ("Eigenkapitalrendite", W_ROE),
                            ("Verschuldung", W_DEBT), ("Ueber 200T-Linie", W_STRUCTURE),
                            ("Analysten-Revisionen", W_REVISIONS), ("Kursziel-Abstand", W_UPSIDE)):
            add(label, 0.0, max_, "k.A.")
        return 0.0, ["keine Fundamentaldaten"], b

    tpe = safe(f, "trailingPE")
    fpe = safe(f, "forwardPE")
    margin = safe(f, "profitMargins")
    rev_growth = safe(f, "revenueGrowth")
    d2e = safe(f, "debtToEquity")
    fcf = safe(f, "freeCashflow")
    roe = safe(f, "returnOnEquity")
    target = safe(f, "targetMeanPrice")

    if fpe and tpe and 0 < fpe < tpe:
        add("KGV verbessert", W_PE_IMPROVE, W_PE_IMPROVE, f"{fpe:.1f} < {tpe:.1f}")
        why.append("erwartetes KGV unter aktuellem")
    else:
        add("KGV verbessert", 0.0, W_PE_IMPROVE, "nein" if fpe or tpe else "k.A.")

    if fpe and fpe > 0:
        p = W_PE_LEVEL * ramp(fpe, 30, 10)
        add("KGV Niveau", p, W_PE_LEVEL, f"{fpe:.1f}")
    else:
        add("KGV Niveau", 0.0, W_PE_LEVEL, "k.A.")

    if fcf and fcf > 0:
        add("Free Cashflow", W_FCF, W_FCF, "positiv")
        why.append("positiver Free Cashflow")
    else:
        add("Free Cashflow", 0.0, W_FCF, "negativ/k.A.")

    if margin and margin > 0:
        p = W_MARGIN * ramp(margin, 0, 0.20)
        add("Marge", p, W_MARGIN, f"{margin * 100:.1f}%")
    else:
        add("Marge", 0.0, W_MARGIN, "k.A.")

    if rev_growth and rev_growth > 0:
        p = W_GROWTH * ramp(rev_growth, 0, 0.15)
        add("Umsatzwachstum", p, W_GROWTH, f"{rev_growth * 100:.0f}%")
        if p > W_GROWTH * 0.6:
            why.append(f"Umsatzwachstum {rev_growth * 100:.0f}%")
    else:
        add("Umsatzwachstum", 0.0, W_GROWTH, "k.A.")

    if roe and roe > 0:
        p = W_ROE * ramp(roe, 0.05, 0.25)
        add("Eigenkapitalrendite", p, W_ROE, f"{roe * 100:.1f}%")
    else:
        add("Eigenkapitalrendite", 0.0, W_ROE, "k.A.")

    if d2e is not None:
        p = W_DEBT * ramp(d2e, 200, 40)
        add("Verschuldung", p, W_DEBT, f"{d2e:.0f}")
    else:
        add("Verschuldung", 0.0, W_DEBT, "k.A.")

    add("Ueber 200T-Linie", W_STRUCTURE if m["above_sma200"] else 0.0, W_STRUCTURE,
        "ja" if m["above_sma200"] else "nein")

    net_rev = safe(a, "net_30d", 0)
    p = W_REVISIONS * ramp(net_rev, -2, 2)
    add("Analysten-Revisionen", p, W_REVISIONS, f"{net_rev:+d}" if net_rev else "0")
    if net_rev and net_rev != 0:
        richtung = "hochgestuft" if net_rev > 0 else "herabgestuft"
        why.append(f"Analysten zuletzt netto {abs(net_rev)}x {richtung} (30 Tage)")

    if target and target > 0 and m["last"] > 0:
        upside = (target / m["last"] - 1) * 100
        p = W_UPSIDE * ramp(upside, 0, 20)
        add("Kursziel-Abstand", p, W_UPSIDE, f"{upside:.0f}%")
        if upside > 8:
            why.append(f"{upside:.0f}% Abstand zum mittleren Kursziel")
    else:
        add("Kursziel-Abstand", 0.0, W_UPSIDE, "k.A.")

    total = round(min(sum(x["points"] for x in b), 100.0), 1)
    return total, why, b


def format_revision(a: dict) -> str | None:
    """Kurzform der letzten Ratingaenderung, fuer die Anzeige bei jedem Wert."""
    net = safe(a, "net_30d", 0)
    if not net:
        return None
    firm = safe(a, "last_firm")
    date = safe(a, "last_date")
    richtung = "↑" if net > 0 else "↓"
    tail = f" ({firm}, {date})" if firm and date else ""
    return f"Analysten {richtung}{abs(net)} in 30T{tail}"


def target_price_info(f: dict, a: dict, last: float) -> dict:
    """Kursziel-Informationen: absoluter Wert, Abstand zum Kurs in Prozent,
    Kaufen/Halten/Verkaufen-Aufteilung, Aktualitaets-Kennzeichnung.

    Die Kaufen/Halten/Verkaufen-Aufteilung kommt aus a["consensus"]
    (compute_consensus_from_actions) - eine eigene Berechnung aus den
    rohen Einzel-Ratings (pro Bank nur die juengste, maximal
    CONSENSUS_MAX_AGE_DAYS alt), NICHT aus Yahoos eigener "aktueller
    Konsens"-Zahl (deren genaue Aktualitaet nicht nachvollziehbar war).

    Yahoo liefert keinen Zeitstempel dafuer, wann das Kursziel zuletzt gesetzt
    wurde. Als Naeherung: gab es innerhalb der letzten TARGET_FRESH_DAYS Tage
    eine Analysten-Ratingaenderung (die typischerweise mit einer Kurszielbe-
    staetigung/-anpassung einhergeht), gilt das Kursziel als "frisch". Sonst
    wird trotzdem das vorhandene Kursziel gezeigt (besser als nichts), aber
    klar als moeglicherweise aelter gekennzeichnet - lieber ehrlich unsicher
    als falsch sicher.
    """
    empfehlung_text = {
        "strong_buy": "klar kaufen", "buy": "kaufen", "hold": "halten",
        "sell": "verkaufen", "strong_sell": "klar verkaufen",
        "none": "keine Angabe", "underperform": "unterdurchschnittlich",
        "outperform": "ueberdurchschnittlich",
    }
    target = safe(f, "targetMeanPrice")
    n_analysts = safe(f, "numberOfAnalystOpinions")
    empfehlung = empfehlung_text.get(safe(f, "recommendationKey"), None)
    rec_breakdown = safe(a, "consensus")

    if not target or target <= 0 or not last or last <= 0:
        return {"target_abs": None, "upside_pct": None, "fresh": None,
                "n_analysts": n_analysts, "empfehlung": empfehlung, "rec_breakdown": rec_breakdown}

    upside = (target / last - 1) * 100
    fresh = None
    last_action_date = safe(a, "last_date")
    if last_action_date:
        try:
            d = datetime.strptime(last_action_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - d).total_seconds() / 86400
            fresh = age_days <= TARGET_FRESH_DAYS
        except Exception:  # noqa: BLE001
            fresh = None
    return {"target_abs": round(target, 2), "upside_pct": round(upside, 1), "fresh": fresh,
            "n_analysts": n_analysts, "empfehlung": empfehlung, "rec_breakdown": rec_breakdown}


def action_phrase(action: str | None, to_grade: str | None) -> str:
    """Vollstaendige, grammatisch korrekte Phrase fuer eine Analysten-Aktion.
    Frueher wurde ein Richtungswort + 'gestuft' zusammengeklebt - das ergab
    bei allem ausser hoch/runter kaputte Woerter (z.B. 'maingestuft' fuer den
    Yahoo-Aktionstyp 'main' = Rating unveraendert bestaetigt)."""
    templates = {
        "up": "hochgestuft" + (f" auf {to_grade}" if to_grade else ""),
        "down": "abgestuft" + (f" auf {to_grade}" if to_grade else ""),
        "init": "neu bewertet" + (f" mit {to_grade}" if to_grade else ""),
        "reit": "Rating bestaetigt" + (f": {to_grade}" if to_grade else ""),
        "main": "Rating bestaetigt" + (f": {to_grade}" if to_grade else ""),
    }
    return templates.get(action, (action or "Aenderung") + (f" ({to_grade})" if to_grade else ""))


def kaufen_pct_cell(info: dict) -> str:
    """NUR der Kaufen-Anteil der Analysten, als eigene, kompakte Spalte -
    Halten/Verkaufen interessieren hier nicht extra, die stecken implizit
    im Rest."""
    rb = info.get("rec_breakdown")
    if rb and rb.get("kaufen_pct") is not None:
        return f"{rb['kaufen_pct']}% ({rb['total']} Banken, \u2264{CONSENSUS_MAX_AGE_DAYS}T)"
    emp = info.get("empfehlung")
    return (emp + " (kein aktueller Konsens)") if emp else "keine aktuelle Bewertung (>4 Monate)"


def kursziel_cell(info: dict) -> str:
    """Nur der Kurszielwert + Abstand - kompakt, ohne Kaufen/Halten/Verkaufen
    (das steht jetzt in einer eigenen Spalte)."""
    if info.get("target_abs") is None:
        return "kein Kursziel verfuegbar"
    richtung = "unter" if info["upside_pct"] < 0 else "ueber"
    return f"{info['target_abs']:.2f} ({abs(info['upside_pct']):.0f}% {richtung} Kurs)"


def letztes_rating_cell(actions: list | None) -> str:
    """Nur die EINE juengste Ratingaenderung, kompakt: Datum, Bank, Aktion."""
    if not actions:
        return "keine in 30T"
    act = actions[0]
    firm = act.get("firm") or "unbekannte Bank"
    date = act.get("date") or "?"
    return f"{date} {firm}: {action_phrase(act.get('action'), act.get('to_grade'))}"


def exclusions(m: dict, f: dict) -> list[str]:
    """Value-Trap-Filter. Wer hier auffaellt, fliegt aus allen Listen."""
    flags = []
    rev = safe(f, "revenueGrowth")
    d2e = safe(f, "debtToEquity")
    if rev is not None and d2e is not None and rev < 0 and d2e > 150:
        flags.append("fallender Umsatz bei hoher Verschuldung")
    if not m["above_sma200"] and m["sma200_slope"] < -2:
        flags.append("200-Tage-Linie faellt steil")
    if m["dd_ath"] < -80:
        flags.append("mehr als 80% unter ATH")
    fcf = safe(f, "freeCashflow")
    if fcf is not None and fcf < 0 and (safe(f, "profitMargins") or 0) < 0:
        flags.append("negativer Cashflow und Verlust")
    return flags


def earnings_in_days(f: dict) -> int | None:
    ts = safe(f, "earningsTimestamp")
    if not ts:
        return None
    try:
        d = datetime.fromtimestamp(float(ts), tz=timezone.utc)
    except Exception:  # noqa: BLE001
        return None
    days = (d - datetime.now(timezone.utc)).days
    return days if 0 <= days <= 30 else None


# ---------------------------------------------------------------------------
# Auswertung und Report
# ---------------------------------------------------------------------------

def build_extras(prices: dict, extras: dict) -> dict:
    """Rohstoffe/Krypto: rein technische Auswertung (Turnaround-/Momentum-
    Score), keine Fundamentaldaten noetig - beide Score-Funktionen brauchen
    nur die Kursmetriken. Kein Sektor-Deckel, keine Ausschlusskriterien, kein
    Value-Score (dafuer fehlen KGV, Marge etc. bei Rohstoffen komplett)."""
    rows = {}
    for t, name in extras.items():
        df = prices.get(t)
        if df is None:
            continue
        m = compute_metrics(df, None)  # kein Index-Benchmark fuer rel. Staerke
        if m is None:
            continue
        s_turn, w_turn, bd_turn = score_turnaround(m)
        s_mom, w_mom, bd_mom = score_momentum(m)
        rows[t] = {
            "name": name,
            "metrics": m,
            "scores": {"turnaround": s_turn, "momentum": s_mom},
            "why": {"turnaround": w_turn, "momentum": w_mom},
        }
    return rows


def build_state(prices, fundamentals, analyst, members, benchmarks) -> dict:
    bench_series = {}
    for idx, sym in benchmarks.items():
        if sym in prices:
            bench_series[idx] = prices[sym]["Close"].dropna()

    rows = {}
    for t, idxs in members.items():
        df = prices.get(t)
        if df is None:
            continue
        primary = idxs[0]
        m = compute_metrics(df, bench_series.get(primary))
        if m is None:
            continue
        f = fundamentals.get(t, {}) or {}
        a = analyst.get(t, {}) or {}
        flags = exclusions(m, f)
        s_turn, w_turn, bd_turn = score_turnaround(m)
        s_mom, w_mom, bd_mom = score_momentum(m)
        s_val, w_val, bd_val = score_value(m, f, a)
        rows[t] = {
            "name": clean_name(safe(f, "shortName"), t),
            # Datum der letzten Kerze dieses Wertes. Ohne diese Angabe
            # laesst sich nicht erkennen, ob ein Wert zurueckhaengt -
            # siehe die Standwarnung weiter unten.
            "stand": str(df.index[-1].date()),
            "isin": safe(f, "isin"),
            "index": "/".join(idxs),
            "sector": safe(f, "sector", "unbekannt"),
            # Land ab 24.08.2026: Grundlage der Depot-Streuung im Orderbuch.
            # Der Index taugt dafuer nicht - ASML, AstraZeneca, PDD und
            # MercadoLibre notieren an der Nasdaq, sitzen aber woanders.
            "country": safe(f, "country", "unbekannt"),
            "metrics": m,
            "flags": flags,
            "earnings_in": earnings_in_days(f),
            "analyst": a,
            "revision_note": format_revision(a),
            "target": target_price_info(f, a, m["last"]),
            "scores": {"turnaround": s_turn, "momentum": s_mom, "value": s_val},
            "why": {"turnaround": w_turn, "momentum": w_mom, "value": w_val},
            "breakdown": {"turnaround": bd_turn, "momentum": bd_mom, "value": bd_val},
        }

    ranks = {}
    ranks_full = {}
    for name in LISTS:
        eligible = [(t, r["scores"][name]) for t, r in rows.items() if not r["flags"]]
        eligible.sort(key=lambda x: x[1], reverse=True)
        picked: list[str] = []
        sector_count: dict[str, int] = {}
        for t, _ in eligible:
            if len(picked) >= TRACK_N:
                break
            sector = rows[t]["sector"]
            if sector_count.get(sector, 0) >= SECTOR_CAP:
                continue
            picked.append(t)
            sector_count[sector] = sector_count.get(sector, 0) + 1
        # Falls der Sektor-Deckel die Liste kuerzer laesst als TRACK_N erlaubt,
        # mit den naechstbesten (auch ueber dem Deckel) auffuellen.
        if len(picked) < TRACK_N:
            for t, _ in eligible:
                if len(picked) >= TRACK_N:
                    break
                if t not in picked:
                    picked.append(t)
        ranks_full[name] = picked      # Tiefe TRACK_N, nur fuer die Rang-Historie
        ranks[name] = picked[:TOP_N]   # angezeigte Rangliste (Top 15)

    missing = sorted(set(members.keys()) - set(rows.keys()))

    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ranks": ranks,
        "ranks_full": ranks_full,
        "rows": rows,
        "missing": missing,
    }


def diff_lists(today: dict, prev: dict) -> dict:
    changes = {}
    for name in LISTS:
        cur = today["ranks"][name]
        old = prev["ranks"].get(name, []) if prev else []
        old_pos = {t: i for i, t in enumerate(old)}
        entries, exits, moves = [], [], []
        for i, t in enumerate(cur):
            if t not in old_pos:
                entries.append({"ticker": t, "rank": i + 1})
            else:
                delta = old_pos[t] - i
                if abs(delta) >= RANK_JUMP:
                    moves.append({"ticker": t, "rank": i + 1, "delta": delta})
        for t in old:
            if t not in cur:
                exits.append({"ticker": t, "old_rank": old_pos[t] + 1})
        changes[name] = {"entries": entries, "exits": exits, "moves": moves}

    # Analysten-Sentiment: fuer alle heute gelisteten Werte pruefen, ob sich
    # das Vorzeichen der Netto-Ratingaenderungen gegenueber gestern gedreht hat.
    # Das ist unabhaengig von der Rangliste selbst das eigentliche
    # "kurzfristige" Signal aus den Analystendaten.
    flips = []
    if prev:
        listed_today = sorted({t for n in LISTS for t in today["ranks"][n]})
        for t in listed_today:
            now_net = safe(today["rows"][t]["analyst"], "net_30d", 0)
            prev_row = prev.get("rows", {}).get(t)
            if prev_row is None:
                continue
            old_net = safe(prev_row.get("analyst", {}), "net_30d", 0)
            if now_net != 0 and (old_net == 0 or (old_net > 0) != (now_net > 0)):
                flips.append({"ticker": t, "now": now_net, "old": old_net})
    changes["analyst_flips"] = flips
    return changes


def score_label(score: float) -> str:
    """Grobe Einordnung des Scores in Textform. Ausdruecklich eine Beschreibung,
    wie gut die hinterlegten Kriterien erfuellt sind - keine statistisch
    ermittelte Erfolgswahrscheinlichkeit (dafuer fehlt ein Backtest)."""
    if score >= 80:
        return "sehr hoch"
    if score >= 65:
        return "hoch"
    if score >= 50:
        return "mittel"
    return "niedrig"


def pressure_label(x: float | None) -> str:
    """Textform des 5-Tage-Kauf-/Verkaufsdrucks (Volumen an Anstiegs- vs.
    Ruecksetzertagen). Kein Short/Long-Indikator, siehe Notiz in compute_metrics."""
    if x is None:
        return "unbekannt"
    if x >= 1.3:
        return "klarer Kaufdruck"
    if x >= 1.1:
        return "leichter Kaufdruck"
    if x <= 1 / 1.3:
        return "klarer Verkaufsdruck"
    if x <= 1 / 1.1:
        return "leichter Verkaufsdruck"
    return "ausgeglichen"


def load_rank_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return sorted(data, key=lambda e: e["date"])
    except Exception:  # noqa: BLE001
        return []


def save_rank_history(history: list[dict], today_entry: dict) -> None:
    history = [e for e in history if e["date"] != today_entry["date"]]
    history.append(today_entry)
    cutoff = (datetime.now(timezone.utc) - pd.Timedelta(days=HISTORY_KEEP_DAYS)).strftime("%Y-%m-%d")
    history = [e for e in history if e["date"] >= cutoff]
    history.sort(key=lambda e: e["date"])
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=1, ensure_ascii=False), encoding="utf-8")


def nearest_entry_at_or_before(history: list[dict], target_date: str) -> dict | None:
    """History ist aufsteigend nach Datum sortiert - das letzte Element mit
    Datum <= target_date ist der naechste verfuegbare Handelstag davor."""
    candidates = [e for e in history if e["date"] <= target_date]
    return candidates[-1] if candidates else None


def build_rank_lookup(history: list[dict], today_date: str):
    """Liefert eine Funktion get_rank(kategorie, ticker, 'yesterday'|'lastweek'),
    die den Rang aus der gespeicherten Historie (Tiefe TRACK_N) nachschlaegt."""
    yesterday_entry = history[-1] if history else None
    lastweek_target = (datetime.strptime(today_date, "%Y-%m-%d") - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
    lastweek_entry = nearest_entry_at_or_before(history, lastweek_target)

    def get_rank(name: str, ticker: str, when: str) -> int | None:
        entry = yesterday_entry if when == "yesterday" else lastweek_entry
        if not entry:
            return None
        lst = entry.get("ranks_full", {}).get(name, [])
        return lst.index(ticker) + 1 if ticker in lst else None

    return get_rank


def stand_je_wert(today: dict) -> dict[str, str]:
    """Ticker auf Datum der letzten Kerze, leere Angaben uebersprungen."""
    return {t: r["stand"] for t, r in today["rows"].items() if r.get("stand")}


def stand_satz(today: dict) -> str:
    """Der Kopfsatz sagt, WELCHER Handelstag im Bericht steht.

    Bis 25.08.2026 stand hier fest "Schlusskurse vom Vortag". Das war
    falsch, sobald der Lauf am Abend des Handelstages selbst laeuft - und
    es war auch vorher schon falsch fuer die europaeischen Werte, die
    ueber Nacht ihre Tageskerze verlieren koennen. Jetzt kommt die Angabe
    aus den Daten.
    """
    staende = stand_je_wert(today)
    if not staende:
        return "unbekannt."
    neuester = max(staende.values())
    zurueck = sum(1 for d in staende.values() if d < neuester)
    if not zurueck:
        return f"Schlusskurse vom {neuester}."
    return (f"Schlusskurse vom {neuester}, "
            f"aber {zurueck} Werte haengen zurueck - siehe Standwarnung.")


def build_standwarnung(today: dict) -> str:
    """Listet jeden Wert, dessen letzte Kerze aelter ist als die neueste.

    Anlass war der 25.08.2026: alle 39 DAX-Werte und ASML standen im
    Morgenbericht auf dem Schlusskurs vom Freitag, waehrend die 120
    US-Werte den Montag trugen. Sichtbar war das nirgends - der Kopf des
    Berichts behauptete unveraendert "Schlusskurse vom Vortag". Eine
    Kaufentscheidung haette auf einem drei Tage alten Kurs beruht.

    Die Warnung nennt jeden betroffenen Wert einzeln mit seinem Datum,
    ohne Sammelklassen. Sie steht ganz oben, weil sie alles darunter
    entwertet.
    """
    staende = stand_je_wert(today)
    if not staende:
        return ""
    neuester = max(staende.values())
    alt = sorted(((d, t) for t, d in staende.items() if d < neuester))
    if not alt:
        return ""
    L = [f"> **Standwarnung: {len(alt)} von {len(staende)} Werten haengen "
         f"zurueck.** Neuester Handelstag im Bericht ist {neuester}.",
         ">",
         "> Ursache ist in aller Regel Yahoo: die vorlaeufige Tageskerze "
         "einer Boerse wird ueber Nacht durch die offizielle Abrechnung "
         "ersetzt, und solange die fehlt, faellt der Tag weg. Betroffen "
         "sind meist die europaeischen Notierungen. Fuer diese Werte "
         "gelten Kurs, ATR, RSI und Tiefs unten NICHT fuer den neuesten "
         "Handelstag.",
         ">",
         "> | Wert | letzte Kerze |", "> |---|---|"]
    for d, t in alt:
        L.append(f"> | {t} | {d} |")
    return "\n".join(L)


def build_glossary() -> str:
    return "\n".join([
        "## \U0001F4D6 Glossar (was die Spalten bedeuten)", "",
        "- **Kurs**: letzter Schlusskurs.",
        "- **Abstand ATH**: wie weit der Kurs unter dem Allzeithoch liegt. "
        "Rein informativ, dient nur der Einordnung.",
        "- **Kaufen-Anteil Analysten**: EIGENE Berechnung (nicht Yahoos "
        "eigene 'aktueller Konsens'-Zahl, deren genaue Aktualitaet nicht "
        "nachvollziehbar war): pro Bank zaehlt NUR die juengste Einstufung, "
        f"und nur wenn diese nicht aelter als {CONSENSUS_MAX_AGE_DAYS} Tage "
        "(ca. 4 Monate) ist - eine Bank, die seit ueber 4 Monaten nichts "
        "Neues gesagt hat, faellt komplett raus. Freitext-Einstufungen wie "
        "'Overweight' oder 'Outperform' werden zu Kaufen/Halten/Verkaufen "
        "zusammengefasst; nicht sicher zuordenbare Begriffe zaehlen NICHT "
        "mit (lieber ausschliessen als falsch einordnen). Format z.B. "
        "\"75% (12 Banken, \u2264120T)\" heisst: von 12 Banken mit einer "
        "Wertung juenger als 120 Tage empfehlen 75% den Kauf.",
        "- **Kursziel**: mittleres Kursziel aller Analysten (Durchschnitt, keine "
        "Einzelmeinung) und Abstand zum aktuellen Kurs, z.B. \"67% unter "
        "aktuellem Kurs\" heisst: das Kursziel liegt 67% UNTER dem, was die "
        "Aktie gerade kostet.",
        "- **RSI Tag / Woche / Stunde**: Momentum-Indikator (0-100) auf drei "
        "Zeitebenen, jeweils ECHT neu berechnet auf echten Kerzen dieser "
        "Zeitebene - nicht rechnerisch aus dem Tages-RSI umgerechnet (das "
        "waere mathematisch nicht zulaessig). RSI Woche nutzt Wochen-"
        "Schlusskurse, RSI Stunde echte Stundenkerzen (nur fuer die "
        "Filtertreffer geladen, um Datenabrufe zu sparen - \"k.A.\" heisst: "
        "keine verwertbaren Stundenkerzen vorhanden). Optimum tendenziell bei "
        "40-50, nicht bei 30 wie oft angenommen (Quelle: Constance Brown, "
        "\"RSI Range Shift\").",
        "- **Letztes Rating**: die juengste namentliche Ratingaenderung mit "
        "Bank und Datum. WICHTIG: welcher Analyst welchen genauen Kurszielwert "
        "genannt hat, liefert die kostenlose Datenquelle nicht (nur den "
        "Durchschnitt aller Analysten) - dafuer braeuchte es einen "
        "kostenpflichtigen Dienst wie TipRanks. Das \"Long/Short\"-Verhaeltnis "
        "aus manchen Broker-Apps (z.B. Trade Republic) ist NICHT enthalten - "
        "das ist brokerinterne Handelsaktivitaet bei Derivaten, nirgendwo "
        "oeffentlich verfuegbar.",
        "",
    ])



def analyst_filter_hits(today: dict) -> list:
    """Ermittelt die Treffer fuer den Analysten-Filter: Kursziel mindestens
    ANALYST_FILTER_MIN_UPSIDE% ueber dem aktuellen Kurs UND mindestens
    ANALYST_FILTER_MIN_KAUFEN_PCT% der Analysten auf Kaufen, ueber ALLE
    ausgewerteten Werte (nicht nur alte Top-10-Listen). Value-Trap-
    Ausschluesse gelten auch hier. Sortiert nach Kaufen-Anteil absteigend,
    bei Gleichstand nach Kurspotenzial absteigend, gedeckelt bei
    ANALYST_FILTER_TOP_N. Gibt Liste von (Ticker, Zeile, Kaufen-Anteil) zurueck."""
    hits = []
    for t, row in today["rows"].items():
        if row["flags"]:
            continue
        target = row.get("target", {})
        upside = target.get("upside_pct")
        rb = target.get("rec_breakdown")
        if upside is None or not rb or rb.get("kaufen_pct") is None:
            continue
        if upside >= ANALYST_FILTER_MIN_UPSIDE and rb["kaufen_pct"] >= ANALYST_FILTER_MIN_KAUFEN_PCT:
            hits.append((t, row, rb["kaufen_pct"], upside))
    hits.sort(key=lambda x: (x[2], x[3]), reverse=True)
    return [(t, row, kp) for t, row, kp, _ in hits[:ANALYST_FILTER_TOP_N]]


def build_analyst_filter_section(today: dict, hits: list, hourly_rsi: dict | None = None) -> str:
    """Darstellung der Analysten-Filter-Treffer (siehe analyst_filter_hits)
    als Tabelle, sortiert nach Kaufen-Anteil absteigend. RSI auf drei
    Zeitebenen: Tag (Standard-14-Tage-RSI), Woche (echte Neuberechnung auf
    Wochenschlusskursen), Stunde (echte Neuberechnung auf Stundenkerzen,
    nur fuer diese Treffer geladen - siehe get_hourly_rsi)."""
    hourly_rsi = hourly_rsi or {}
    L = [f"## \U0001F3AF Analysten-Filter (Kursziel \u2265{ANALYST_FILTER_MIN_UPSIDE}%, "
         f"Kaufen-Anteil \u2265{ANALYST_FILTER_MIN_KAUFEN_PCT}%)", "",
         f"_Ueber alle {len(today['rows'])} ausgewerteten Werte. Sortiert nach "
         "Kaufen-Anteil absteigend, bei Gleichstand nach Kurspotenzial. Maximal "
         f"{ANALYST_FILTER_TOP_N} Treffer. Value-Trap-Ausschluesse gelten auch "
         "hier. RSI auf drei Zeitebenen, jeweils echt neu berechnet (nicht "
         "umgerechnet): Tag, Woche, Stunde. \"k.A.\" bei Stunde heisst: fuer "
         "diesen Wert lagen keine verwertbaren Stundenkerzen vor._", ""]

    if not hits:
        L.append("Heute kein Treffer.")
        L.append("")
        return "\n".join(L)

    L.append("| Rang | Ticker | ISIN | Name | Index | Kurs | Abstand ATH (Info) | "
             "Kaufen-Anteil Analysten | Kursziel | RSI Tag | RSI Woche | RSI Stunde | Letztes Rating |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, (t, row, _) in enumerate(hits, 1):
        m = row["metrics"]
        target = row.get("target", {})
        rsi_d = f"{m['rsi14']:.0f}" if m.get("rsi14") is not None else "k.A."
        rsi_w = f"{m['rsi_week']:.0f}" if m.get("rsi_week") is not None else "k.A."
        rh = hourly_rsi.get(t)
        rsi_h = f"{rh:.0f}" if rh is not None else "k.A."
        L.append(f"| {i} | {t} | {row.get('isin') or '-'} | {row['name']} | {row['index']} | "
                 f"{m['last']:.2f} | {m['dd_ath']:.0f}% | {kaufen_pct_cell(target)} | "
                 f"{kursziel_cell(target)} | {rsi_d} | {rsi_w} | {rsi_h} | "
                 f"{letztes_rating_cell(row.get('analyst', {}).get('actions'))} |")
    L.append("")
    return "\n".join(L)


def build_top10_tables(today: dict, get_rank) -> str:
    L = ["## 📊 Aktuelle Top 10", ""]
    for name in LISTS:
        L.append(f"### {LIST_TITLES[name]}")
        L.append("")
        header = ["Rang", "Ticker", "ISIN", "Name", "Index", "Kurs", "Abstand ATH (Info)",
                   "Kaufen-Anteil Analysten", "Kursziel", "Letztes Rating",
                   "**Gesamt**", "Einordnung", "Rang gestern", "Rang Vorwoche", "Warum (Kurzfassung)"]
        L.append("| " + " | ".join(header) + " |")
        L.append("|" + "---|" * len(header))

        for i, t in enumerate(today["ranks_full"][name][:10], 1):
            row = today["rows"][t]
            m = row["metrics"]
            score = row["scores"][name]
            ry = get_rank(name, t, "yesterday")
            rw = get_rank(name, t, "lastweek")
            ry_s = str(ry) if ry else "neu"
            rw_s = str(rw) if rw else "neu"
            target = row.get("target", {})
            why = "; ".join(row["why"][name][:3]) or "-"
            cells = [str(i), t, row.get("isin") or "-", row["name"], row["index"],
                     f"{m['last']:.2f}", f"{m['dd_ath']:.0f}%",
                     kaufen_pct_cell(target), kursziel_cell(target),
                     letztes_rating_cell(row.get("analyst", {}).get("actions")),
                     f"**{score:.0f}**", score_label(score), ry_s, rw_s, why]
            L.append("| " + " | ".join(cells) + " |")
        L.append("")
    return "\n".join(L)


def build_extras_section(extras_rows: dict) -> str:
    if not extras_rows:
        return ""
    L = ["## 🪙 Rohstoffe & Krypto (informativ, nicht Teil des Rankings)", "",
         "_Rein technisch ausgewertet (Turnaround-/Momentum-Kriterien wie bei "
         "den Aktien) - kein Value-Score moeglich, da Fundamentaldaten wie "
         "KGV oder Umsatzwachstum bei Rohstoffen und Krypto nicht existieren. "
         "Keine Sektor-Regeln, kein Ranking gegen die Aktienlisten._", ""]
    L.append("| Name | Kurs | Abstand ATH | RSI | Turnaround-Score | Momentum-Score |")
    L.append("|---|---|---|---|---|---|")
    for t, row in extras_rows.items():
        m = row["metrics"]
        L.append(f"| {row['name']} ({t}) | {m['last']:.2f} | {m['dd_ath']:.0f}% | "
                 f"{m['rsi14']:.0f} | {row['scores']['turnaround']:.0f}/100 "
                 f"({score_label(row['scores']['turnaround'])}) | "
                 f"{row['scores']['momentum']:.0f}/100 ({score_label(row['scores']['momentum'])}) |")
    L.append("")
    return "\n".join(L)


def build_analyst_section(today: dict, tickers: list) -> str:
    """Klare, eindeutige Liste je Wert: Datum, Bank, konkrete Einstufung.
    Fuer die uebergebenen Ticker (typischerweise die Treffer des
    Analysten-Filters)."""
    tickers = sorted(tickers)
    richtung_text = {
        "up": "Hochstufung", "down": "Herabstufung",
        "init": "Erstbewertung", "reit": "Bestaetigung", "main": "Bestaetigung",
    }
    L = ["## \U0001F9ED Analysten-Einstufungen (Filtertreffer, letzte 30 Tage)", ""]
    if not tickers:
        L.append("Keine Treffer heute, daher keine Einzelaufstellung.")
        L.append("")
        return "\n".join(L)
    for t in tickers:
        row = today["rows"][t]
        L.append(f"**{t}** ({row['name']}, {row['index']})")
        actions = row["analyst"].get("actions") or []
        if not actions:
            L.append("- keine Ratingaenderung in den letzten 30 Tagen")
        else:
            for act in actions:
                grade = None
                if act.get("from_grade") and act.get("to_grade"):
                    grade = f"{act['from_grade']} \u2192 {act['to_grade']}"
                elif act.get("to_grade"):
                    grade = act["to_grade"]
                richtung = richtung_text.get(act.get("action"), act.get("action") or "-")
                firm = act.get("firm") or "unbekannte Bank"
                date = act.get("date") or "-"
                line = f"- {date}: {firm} \u2013 {richtung}"
                if grade:
                    line += f" ({grade})"
                L.append(line)
        L.append("")
    return "\n".join(L)


def fmt_row(t: str, row: dict, list_name: str) -> str:
    m = row["metrics"]
    why = ", ".join(row["why"][list_name][:3]) or "-"
    line = (f"**{t}** ({row['name']}, {row['index']}) - Score {row['scores'][list_name]:.0f} | "
            f"{m['dd_ath']:.0f}% unter ATH, RSI {m['rsi14']:.0f} | {why}")
    if row.get("revision_note"):
        line += f" | {row['revision_note']}"
    return line


def build_report(today: dict, prev: dict, changes: dict, get_rank, extras_rows: dict,
                  hourly_rsi: dict | None = None) -> str:
    """Stark vereinfacht auf Wunsch: nur noch der Analysten-Filter (Kursziel
    >=X%, Kaufen-Anteil >=Y%) plus die zugehoerige Einzelaufstellung der
    Ratingaenderungen. Die frueheren Turnaround-/Momentum-/Value-Top-10-
    Tabellen, die Rohstoffe/Krypto-Uebersicht und die taeglichen
    Veraenderungsmeldungen sind bewusst entfernt - das hier ist jetzt das
    Hauptaugenmerk. Die Score-Berechnung selbst laeuft im Hintergrund
    unveraendert weiter (u.a. fuer den Value-Trap-Ausschluss), wird aber
    nicht mehr angezeigt."""
    L = []
    L.append(f"# Boersen-Screening - {today['date']}")
    L.append("")
    L.append(f"_Stand: {stand_satz(today)} Erstellt {today['generated']} UTC. "
             f"{len(today['rows'])} Werte ausgewertet._")
    L.append("")
    warnung = build_standwarnung(today)
    if warnung:
        L.append(warnung)
        L.append("")
    L.append(build_glossary())

    filter_hits = analyst_filter_hits(today)
    L.append(build_analyst_filter_section(today, filter_hits, hourly_rsi))
    L.append("")
    hit_tickers = [t for t, _, _ in filter_hits]
    L.append(build_analyst_section(today, hit_tickers))
    L.append("")

    L.append("---")
    L.append("")
    if today.get("missing"):
        L.append(f"_Nicht auswertbar heute ({len(today['missing'])}): "
                 f"{', '.join(today['missing'])}_")
        L.append("")
    L.append("_Automatisch erzeugte Kennzahlensortierung, keine Anlageberatung._")
    return "\n".join(L)

GRADE_BUY_TERMS_DE = {"kaufen", "klar kaufen", "aufstocken", "uebergewichten", "übergewichten"}
GRADE_HOLD_TERMS_DE = {"halten", "neutral bewerten", "marktgewichten"}
GRADE_SELL_TERMS_DE = {"verkaufen", "klar verkaufen", "reduzieren", "untergewichten"}

# Schreibweisen desselben Hauses zusammenfuehren. Ohne diese Tabelle waeren
# "Jefferies & Company Inc." und "Jefferies" zwei verschiedene Banken - und
# dieselbe Analyse wuerde doppelt in den Konsens einfliessen.
FIRMEN_ALIAS = {
    "jefferies company inc": "Jefferies",
    "jefferies co": "Jefferies",
    "jefferies": "Jefferies",
    "jp morgan chase co": "JP Morgan",
    "jpmorgan chase co": "JP Morgan",
    "jpmorgan": "JP Morgan",
    "jp morgan": "JP Morgan",
    "ubs ag": "UBS",
    "ubs group": "UBS",
    "ubs": "UBS",
    "rbc capital markets": "RBC Capital",
    "rbc capital": "RBC Capital",
    "barclays capital": "Barclays",
    "barclays": "Barclays",
    "goldman sachs group inc": "Goldman Sachs",
    "goldman sachs": "Goldman Sachs",
    "bernstein research": "Bernstein",
    "bernstein": "Bernstein",
    "sanford c bernstein": "Bernstein",
    "dz bank": "DZ Bank",
    "deutsche bank ag": "Deutsche Bank",
    "deutsche bank": "Deutsche Bank",
    "morgan stanley": "Morgan Stanley",
    "b of a securities": "B of A Securities",
    "bofa securities": "B of A Securities",
    "bank of america": "B of A Securities",
    "merrill lynch": "B of A Securities",
    "wells fargo": "Wells Fargo",
    "wells fargo securities": "Wells Fargo",
    "citigroup": "Citigroup",
    "citi": "Citigroup",
    "bmo capital": "BMO Capital",
    "bmo capital markets": "BMO Capital",
    "td cowen": "TD Cowen",
    "cowen co": "TD Cowen",
    "baird": "Baird",
    "robert w baird": "Baird",
    "needham": "Needham",
    "needham company": "Needham",
    "argus research": "Argus Research",
    "raymond james": "Raymond James",
    "stifel": "Stifel",
    "stifel nicolaus": "Stifel",
    "oppenheimer": "Oppenheimer",
    "wedbush": "Wedbush",
    "piper sandler": "Piper Sandler",
    "guggenheim": "Guggenheim",
    "scotiabank": "Scotiabank",
    "macquarie": "Macquarie",
    "truist securities": "Truist Securities",
    "truist": "Truist Securities",
    "da davidson": "DA Davidson",
    "rosenblatt": "Rosenblatt",
    "bnp paribas": "BNP Paribas",
    "new street research": "New Street Research",
    "craig hallum": "Craig-Hallum",
    "craighallum": "Craig-Hallum",
    "tigress financial": "Tigress Financial",
    "benchmark": "Benchmark",
    "telsey advisory group": "Telsey Advisory Group",
    "b riley securities": "B. Riley Securities",
    "briley securities": "B. Riley Securities",
    "warburg research": "Warburg Research",
    "berenberg": "Berenberg",
    "baader bank": "Baader Bank",
    "hauck aufhaeuser": "Hauck Aufhaeuser",
    "kepler cheuvreux": "Kepler Cheuvreux",
    "jp morgan cazenove": "JP Morgan",
}


def normalize_firm(name: str | None) -> str | None:
    """Bankname auf eine einheitliche Schreibweise bringen."""
    if not name:
        return None
    s = str(name).strip()
    if not s or s.lower() in ("nan", "none"):
        return None
    schluessel = s.lower()
    for zeichen in (".", ",", "&", "'", "-", "/", "(", ")"):
        schluessel = schluessel.replace(zeichen, " ")
    schluessel = " ".join(schluessel.split())
    # Erst mit vollem Schluessel nachsehen, dann schrittweise Rechtsformen
    # abschneiden und erneut pruefen. Andersherum verfehlt man Eintraege wie
    # "jp morgan chase co", die genau so in der Tabelle stehen.
    if schluessel in FIRMEN_ALIAS:
        return FIRMEN_ALIAS[schluessel]
    endungen = (" inc", " llc", " ltd", " gmbh", " ag", " plc", " sa", " co",
                " group", " markets", " securities", " research", " capital markets")
    geaendert = True
    while geaendert:
        geaendert = False
        for endung in endungen:
            if schluessel.endswith(endung):
                kandidat = schluessel[: -len(endung)].strip()
                if not kandidat:
                    continue
                schluessel = kandidat
                geaendert = True
                if schluessel in FIRMEN_ALIAS:
                    return FIRMEN_ALIAS[schluessel]
    return FIRMEN_ALIAS.get(schluessel, s)


def classify_grade_any(grade: str | None) -> str | None:
    """Wie classify_grade, zusaetzlich mit deutschsprachigen Einstufungen."""
    cls = classify_grade(grade)
    if cls:
        return cls
    if not grade:
        return None
    g = str(grade).strip().lower()
    if g in GRADE_BUY_TERMS_DE:
        return "buy"
    if g in GRADE_HOLD_TERMS_DE:
        return "hold"
    if g in GRADE_SELL_TERMS_DE:
        return "sell"
    return None


def load_extern_ratings(pfad) -> dict:
    """docs/analysten_extern.csv einlesen - von Hand gepflegte Einzelratings.

    Bewusst KEIN automatischer Abruf eines zweiten Portals: das waere
    rechtlich heikel und technisch fragil. Stattdessen eine nachvollziehbare
    Datei, in der jede Zeile Quelle und Datum mitbringt.

    Spalten: ticker,bank,datum,einstufung,kursziel,quelle
    """
    daten: dict[str, list] = {}
    if not pfad.exists():
        return daten
    import csv as _csv
    with pfad.open(encoding="utf-8") as f:
        for zeile in _csv.DictReader(f):
            t = (zeile.get("ticker") or "").strip().upper()
            bank = normalize_firm(zeile.get("bank"))
            datum = (zeile.get("datum") or "").strip()
            if not t or not bank or not datum:
                continue
            ziel = None
            roh = (zeile.get("kursziel") or "").strip().replace(",", ".")
            if roh:
                try:
                    ziel = float(roh)
                except ValueError:
                    ziel = None
            daten.setdefault(t, []).append({
                "firm": bank,
                "date": datum,
                "grade": (zeile.get("einstufung") or "").strip(),
                "target": ziel,
                "quelle": (zeile.get("quelle") or "extern").strip(),
            })
    return daten


def merge_firm_ratings(yahoo_firmen: list, extern_firmen: list, cutoff_datum: str) -> list:
    """Beide Listen vereinigen, Doppelte entfernen, Altes ausfiltern.

    Doppelt heisst: gleiche Bank UND Datum hoechstens 3 Tage auseinander -
    dann ist es dieselbe Analyse, nur unterschiedlich erfasst. Behalten wird
    der reichere Eintrag: einer MIT Kursziel schlaegt einen ohne.

    Danach gilt wie gehabt: pro Bank nur die juengste Einstufung, und nur
    wenn sie nicht aelter als das Stichdatum ist.
    """
    from datetime import datetime as _dt

    def als_datum(s):
        try:
            return _dt.strptime(str(s)[:10], "%Y-%m-%d")
        except Exception:  # noqa: BLE001
            return None

    grenze = als_datum(cutoff_datum)
    alle = []
    for eintrag in list(yahoo_firmen or []) + list(extern_firmen or []):
        d = als_datum(eintrag.get("date"))
        if d is None or (grenze and d < grenze):
            continue
        firm = normalize_firm(eintrag.get("firm"))
        if not firm:
            continue
        alle.append({**eintrag, "firm": firm, "_d": d})

    # Doppelte je Bank zusammenfuehren
    je_bank: dict[str, list] = {}
    for e in alle:
        je_bank.setdefault(e["firm"], []).append(e)

    ergebnis = []
    for firm, eintraege in je_bank.items():
        eintraege.sort(key=lambda x: x["_d"], reverse=True)
        behalten: list = []
        for e in eintraege:
            treffer = None
            for b in behalten:
                if abs((b["_d"] - e["_d"]).days) <= 3:
                    treffer = b
                    break
            if treffer is None:
                behalten.append(e)
            else:
                # gleiche Analyse: fehlende Felder auffuellen
                if treffer.get("target") is None and e.get("target") is not None:
                    treffer["target"] = e["target"]
                if not treffer.get("grade") and e.get("grade"):
                    treffer["grade"] = e["grade"]
                if not treffer.get("quelle") and e.get("quelle"):
                    treffer["quelle"] = e["quelle"]
                treffer["doppelt"] = True
        # pro Bank zaehlt nur die juengste
        ergebnis.append(behalten[0])

    ergebnis.sort(key=lambda x: x["_d"], reverse=True)
    for e in ergebnis:
        e.pop("_d", None)
    return ergebnis


def consensus_from_firmen(firmen: list) -> dict:
    """Kaufen/Halten/Verkaufen und Kursziel aus der vereinigten Liste."""
    leer = {"kaufen_pct": None, "halten_pct": None, "verkaufen_pct": None,
            "total": 0, "unclassified": 0, "ziel_mittel": None,
            "ziel_hoch": None, "ziel_tief": None, "anzahl_ziele": 0}
    if not firmen:
        return leer
    buy = hold = sell = unclassified = 0
    ziele = []
    for e in firmen:
        cls = classify_grade_any(e.get("grade"))
        if cls == "buy":
            buy += 1
        elif cls == "hold":
            hold += 1
        elif cls == "sell":
            sell += 1
        else:
            unclassified += 1
        if e.get("target"):
            ziele.append(float(e["target"]))
    total = buy + hold + sell
    if total == 0:
        return leer
    return {
        "kaufen_pct": round(buy / total * 100),
        "halten_pct": round(hold / total * 100),
        "verkaufen_pct": round(sell / total * 100),
        "total": total,
        "unclassified": unclassified,
        "ziel_mittel": round(sum(ziele) / len(ziele), 2) if ziele else None,
        "ziel_hoch": max(ziele) if ziele else None,
        "ziel_tief": min(ziele) if ziele else None,
        "anzahl_ziele": len(ziele),
    }


def apply_extern_ratings(today: dict, extern: dict, cutoff_datum: str) -> int:
    """Externe Ratings in den heutigen Stand einmischen.

    Wirkt auf alle nachgelagerten Auswertungen - auch auf report.md und den
    Analysten-Filter, weil das VOR dem Report-Aufbau passiert.
    Beruehrt wird ein Wert nur, wenn die Zusammenfuehrung tatsaechlich mehr
    Banken ergibt als die reine Yahoo-Berechnung.
    """
    geaendert = 0
    for t, row in (today.get("rows") or {}).items():
        a = row.get("analyst") or {}
        yahoo_firmen = a.get("konsens_firmen") or []
        extern_firmen = extern.get(t, [])
        if not extern_firmen and not yahoo_firmen:
            continue
        merged = merge_firm_ratings(yahoo_firmen, extern_firmen, cutoff_datum)
        kons = consensus_from_firmen(merged)
        if kons["total"] == 0:
            continue
        alt_total = (a.get("consensus") or {}).get("total", 0) or 0
        if extern_firmen and kons["total"] >= alt_total:
            a["consensus"] = {k: kons[k] for k in
                              ("kaufen_pct", "halten_pct", "verkaufen_pct", "total", "unclassified")}
            a["quelle"] = "Zusammengefuehrt" if yahoo_firmen else "extern"
            geaendert += 1
        a["merged_firmen"] = merged
        a["merged_ziele"] = {k: kons[k] for k in
                             ("ziel_mittel", "ziel_hoch", "ziel_tief", "anzahl_ziele")}
        tg = row.get("target") or {}
        tg["rec_breakdown"] = a["consensus"]
        row["target"] = tg
        row["analyst"] = a
    return geaendert


def consensus_from_recommendations(tk) -> dict:
    """Zweite Quelle: Yahoos aggregierte Empfehlungszaehlung.

    Wird NUR benutzt, wenn compute_consensus_from_actions nichts findet -
    also wenn die Ratingtabelle leer ist oder jede Bank laenger als
    CONSENSUS_MAX_AGE_DAYS geschwiegen hat (z.B. META, RHM.DE).

    Yahoo liefert hier eine reine Zaehlung je Monatsfenster ('0m' = laufender
    Monat) ohne Bankennamen und ohne Datum. Weniger sauber als die
    Eigenberechnung, aber deutlich besser als gar nichts. Deshalb steht die
    Herkunft immer in der Spalte 'quelle'.
    """
    leer = {"kaufen_pct": None, "halten_pct": None, "verkaufen_pct": None,
            "total": 0, "unclassified": 0}
    rec = tk.recommendations
    if rec is None or getattr(rec, "empty", True):
        return leer

    rec = rec.reset_index()
    zeile = None
    if "period" in rec.columns:
        treffer = rec[rec["period"].astype(str) == "0m"]
        zeile = treffer.iloc[0] if not treffer.empty else rec.iloc[0]
    else:
        zeile = rec.iloc[0]

    def z(spalte: str) -> int:
        try:
            wert = zeile.get(spalte)
            return int(wert) if wert is not None and not pd.isna(wert) else 0
        except Exception:  # noqa: BLE001
            return 0

    buy = z("strongBuy") + z("buy")
    hold = z("hold")
    sell = z("sell") + z("strongSell")
    total = buy + hold + sell
    if total == 0:
        return leer
    return {"kaufen_pct": round(buy / total * 100),
            "halten_pct": round(hold / total * 100),
            "verkaufen_pct": round(sell / total * 100),
            "total": total, "unclassified": 0}


AKTION_KLARTEXT = {
    "up": "hochgestuft", "down": "abgestuft", "main": "bestaetigt",
    "init": "neu aufgenommen", "reit": "bestaetigt",
}


def rating_klartext(akt: dict) -> str:
    """Aus einer Einzelaktion einen lesbaren Satz bauen.

    'bestaetigt' allein sagt nichts - es muss dabeistehen, WAS bestaetigt
    wurde und wovon aus geaendert wurde.
    """
    if not akt:
        return ""
    aktion = AKTION_KLARTEXT.get((akt.get("action") or "").lower(), akt.get("action") or "")
    von = akt.get("from_grade") or ""
    nach = akt.get("to_grade") or ""
    if von and nach and von != nach:
        return f"{aktion} von {von} auf {nach}"
    if nach:
        return f"{aktion} auf {nach}"
    return aktion


def richtung(neu, alt, schwelle: float = 0.005) -> str:
    """Vergleich gegen den Stand des Vortags aus der State-Datei."""
    if neu is None:
        return ""
    if alt is None:
        return "neu"
    try:
        if neu > alt * (1 + schwelle):
            return "angehoben"
        if neu < alt * (1 - schwelle):
            return "gesenkt"
    except Exception:  # noqa: BLE001
        return ""
    return "bestaetigt"


def csv_feld(v) -> str:
    """Ein einzelnes CSV-Feld sauber maskieren."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "ja" if v else "nein"
    s = str(v)
    if any(c in s for c in (",", '"', "\n", "\r", ";")):
        return '"' + s.replace('"', '""') + '"'
    return s


def build_analysten_csv(today: dict, prev: dict | None = None) -> str:
    """docs/analysten.csv - Analystendaten fuer ALLE ausgewerteten Werte.

    report.md zeigt nur die maximal 20 Filtertreffer. Berechnet werden
    Kaufen-Anteil und Kursziel aber ohnehin fuer jeden Wert im Universum.

    Zusaetzlich zum Stand von heute steht hier die RICHTUNG: wurde das
    Kursziel gegenueber gestern angehoben, gesenkt oder bestaetigt, und
    ebenso der Kaufen-Anteil. Dafuer wird der Vortagesstand aus der
    State-Datei herangezogen. Bei Ratingaenderungen steht Von->Nach dabei -
    ein blosses 'bestaetigt' ohne Angabe der Einstufung ist wertlos.
    """
    kopf = [
        "ticker", "name", "isin", "index", "kurs", "sektor", "land",
        "quelle", "kaufen_pct", "kaufen_pct_vortag", "kaufen_richtung",
        "halten_pct", "verkaufen_pct", "banken", "nicht_zuordenbar",
        "empfehlung_yahoo", "analysten_yahoo",
        "kursziel", "kursziel_vortag", "kursziel_richtung", "potenzial_pct",
        "kursziel_hoch", "kursziel_tief", "kursziel_frisch",
        "ziel_eigen", "ziel_eigen_hoch", "ziel_eigen_tief", "anzahl_einzelziele",
        "hochstufungen_30t", "abstufungen_30t", "netto_30t",
        "letztes_datum", "letzte_bank", "letzte_aktion",
        "letzte_von", "letzte_nach", "letzte_klartext", "aenderungen_30t",
        "einzelratings",
    ]
    zeilen = [",".join(kopf)]
    vorrows = (prev or {}).get("rows", {}) or {}

    for t in sorted(today.get("rows", {})):
        r = today["rows"][t]
        m = r.get("metrics", {}) or {}
        tg = r.get("target", {}) or {}
        rb = tg.get("rec_breakdown") or {}
        a = r.get("analyst", {}) or {}
        pt = a.get("price_targets") or {}
        akts = a.get("actions") or []
        mz = a.get("merged_ziele") or {}
        merged = a.get("merged_firmen") or []
        letzte = akts[0] if akts else {}

        vr = vorrows.get(t, {}) or {}
        v_tg = vr.get("target", {}) or {}
        v_rb = (v_tg.get("rec_breakdown") or {})
        kz_alt = v_tg.get("target_abs")
        kp_alt = v_rb.get("kaufen_pct")

        liste = "; ".join(
            f"{k.get('date', '')} {k.get('firm', '')}: {rating_klartext(k)}".strip()
            for k in akts
        )

        werte = [
            t, r.get("name"), r.get("isin"), r.get("index"), m.get("last"),
            # Sektor und Land ab 24.08.2026: Grundlage der Depot-Streuung im
            # Orderbuch. Der Sektor wurde schon immer abgerufen, aber nie in
            # eine Datei geschrieben; country ist neu in der Feldliste der
            # Fundamentaldaten und im State.
            r.get("sector") or "",
            r.get("country") or "",
            a.get("quelle", "keine"),
            rb.get("kaufen_pct"), kp_alt, richtung(rb.get("kaufen_pct"), kp_alt),
            rb.get("halten_pct"), rb.get("verkaufen_pct"),
            rb.get("total"), rb.get("unclassified"),
            tg.get("empfehlung"), tg.get("n_analysts"),
            tg.get("target_abs"), kz_alt, richtung(tg.get("target_abs"), kz_alt),
            tg.get("upside_pct"), pt.get("high"), pt.get("low"), tg.get("fresh"),
            mz.get("ziel_mittel"), mz.get("ziel_hoch"), mz.get("ziel_tief"),
            mz.get("anzahl_ziele", 0),
            safe(a, "upgrades_30d", 0), safe(a, "downgrades_30d", 0), safe(a, "net_30d", 0),
            safe(a, "last_date"), safe(a, "last_firm"), safe(a, "last_action"),
            letzte.get("from_grade"), letzte.get("to_grade"),
            rating_klartext(letzte), liste,
            "; ".join(
                f"{e.get('date','')} {e.get('firm','')}: {e.get('grade','') or '-'}"
                + (f" Ziel {e['target']}" if e.get("target") else "")
                + f" [{e.get('quelle','')}]"
                for e in merged
            ),
        ]
        zeilen.append(",".join(csv_feld(v) for v in werte))

    return "\n".join(zeilen) + "\n"


def main() -> int:
    members, benchmarks, extras = load_universe()
    tickers = sorted(members.keys())
    extra_tickers = sorted(extras.keys())
    all_symbols = tickers + list(benchmarks.values()) + extra_tickers

    prices = get_prices(all_symbols)
    if len(prices) < 20:
        print("Zu wenige Kursdaten - Abbruch, Zustand bleibt unveraendert.")
        return 1

    fundamentals = get_fundamentals(tickers)
    analyst = get_analyst_data(tickers)

    today = build_state(prices, fundamentals, analyst, members, benchmarks)

    # Externe Einzelratings (von Hand gepflegt) einmischen. Passiert VOR dem
    # Report-Aufbau, damit auch der Analysten-Filter davon profitiert.
    extern = load_extern_ratings(EXTERN_RATINGS_FILE)
    if extern:
        cutoff_txt = (datetime.now(timezone.utc)
                      - pd.Timedelta(days=CONSENSUS_MAX_AGE_DAYS)).strftime("%Y-%m-%d")
        n_ext = apply_extern_ratings(today, extern, cutoff_txt)
        print(f"Externe Ratings eingemischt: {n_ext} Werte aus {EXTERN_RATINGS_FILE.name}")
    extras_rows = build_extras(prices, extras)

    prev = None
    if STATE_FILE.exists():
        try:
            prev = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prev = None
    if prev and prev.get("date") == today["date"]:
        print("Hinweis: heutiger Lauf existiert bereits, vergleiche trotzdem.")

    changes = diff_lists(today, prev) if prev else {}

    rank_history = load_rank_history()
    get_rank = build_rank_lookup(rank_history, today["date"])

    # Stunden-RSI nur fuer die Analysten-Filter-Treffer holen (kleine Liste,
    # spart einen zusaetzlichen Datenabruf je Wert fuer das ganze Universum).
    filter_hits = analyst_filter_hits(today)
    hit_tickers = [t for t, _, _ in filter_hits]
    hourly_rsi = get_hourly_rsi(hit_tickers)

    report = build_report(today, prev, changes, get_rank, extras_rows, hourly_rsi)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "report.md").write_text(report, encoding="utf-8")
    (DOCS_DIR / "analysten.csv").write_text(build_analysten_csv(today, prev), encoding="utf-8")
    (DOCS_DIR / "report.json").write_text(json.dumps(
        {"date": today["date"], "ranks": today["ranks"], "changes": changes},
        indent=1, ensure_ascii=False), encoding="utf-8")
    STATE_FILE.write_text(json.dumps(today, indent=1, ensure_ascii=False), encoding="utf-8")
    save_rank_history(rank_history, {"date": today["date"], "ranks_full": today["ranks_full"]})

    print("\n" + report[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
