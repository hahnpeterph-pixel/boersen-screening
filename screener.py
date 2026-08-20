#!/usr/bin/env python3
"""
Boersen-Screening: NASDAQ-100, Dow Jones 30, DAX 40.

Erzeugt drei getrennte Ranglisten (Turnaround, Momentum, Value/Qualitaet),
vergleicht sie mit dem Vortag und schreibt einen Report, der NUR
Veraenderungen zeigt.

Ausgabe:
  docs/report.md      -> der Morgen-Report (wird vom Claude-Task gelesen)
  docs/report.json    -> gleiche Inhalte maschinenlesbar
  state/state.json    -> Zustand von heute (Basis fuer den Vergleich morgen)
  state/fundamentals.json -> Cache der Fundamentaldaten (max. 7 Tage alt)

KEINE Anlageberatung. Das Skript sortiert Kennzahlen, mehr nicht.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent
UNIVERSE_FILE = BASE / "universe.json"
DOCS_DIR = BASE / "docs"
STATE_DIR = BASE / "state"
STATE_FILE = STATE_DIR / "state.json"
FUND_FILE = STATE_DIR / "fundamentals.json"

TOP_N = 15            # Groesse jeder Rangliste
RANK_JUMP = 5         # ab wie vielen Plaetzen eine Bewegung gemeldet wird
HISTORY_PERIOD = "10y"  # Basis fuer das Allzeithoch
FUND_MAX_AGE_DAYS = 7   # Fundamentaldaten hoechstens so alt
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


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


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

def load_universe() -> tuple[dict, dict]:
    raw = json.loads(UNIVERSE_FILE.read_text(encoding="utf-8"))
    benchmarks = raw["benchmarks"]
    members: dict[str, list[str]] = {}
    for idx in benchmarks:
        for t in raw.get(idx, []):
            members.setdefault(t, []).append(idx)
    return members, benchmarks


def fetch_yahoo(tickers: list[str]) -> dict[str, pd.DataFrame]:
    """Kursdaten von Yahoo. Batch-Download, danach je Ticker aufgeteilt."""
    import yfinance as yf

    out: dict[str, pd.DataFrame] = {}
    chunk = 40
    for i in range(0, len(tickers), chunk):
        batch = tickers[i:i + chunk]
        try:
            data = yf.download(
                batch, period=HISTORY_PERIOD, interval="1d",
                auto_adjust=True, group_by="ticker", threads=True,
                progress=False,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  ! Batch-Download fehlgeschlagen ({batch[0]}...): {exc}")
            continue
        for t in batch:
            try:
                df = data[t] if isinstance(data.columns, pd.MultiIndex) else data
                df = df.dropna(subset=["Close"])
                if len(df) > 260:
                    out[t] = df
            except Exception:  # noqa: BLE001
                continue
        time.sleep(1)
    return out


def stooq_symbol(ticker: str) -> str:
    if ticker.startswith("^"):
        return {"^NDX": "^ndq", "^DJI": "^dji", "^GDAXI": "^dax"}.get(ticker, ticker.lower())
    if ticker.endswith(".DE"):
        return ticker[:-3].replace(".", "-").lower() + ".de"
    return ticker.replace(".", "-").lower() + ".us"


def fetch_stooq(ticker: str) -> pd.DataFrame | None:
    """Fallback, falls Yahoo einen Wert nicht liefert."""
    url = f"https://stooq.com/q/d/l/?s={stooq_symbol(ticker)}&i=d"
    try:
        df = pd.read_csv(url, parse_dates=["Date"]).set_index("Date")
    except Exception:  # noqa: BLE001
        return None
    if df.empty or "Close" not in df.columns or len(df) < 260:
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

    if age_days < FUND_MAX_AGE_DAYS and cache.get("data"):
        print(f"Fundamentaldaten aus Cache ({age_days:.1f} Tage alt).")
        return cache["data"]

    print("Aktualisiere Fundamentaldaten (dauert einige Minuten) ...")
    import yfinance as yf

    keys = (
        "trailingPE", "forwardPE", "pegRatio", "priceToBook", "profitMargins",
        "operatingMargins", "revenueGrowth", "earningsGrowth", "debtToEquity",
        "freeCashflow", "returnOnEquity", "dividendYield", "earningsTimestamp",
        "shortName", "sector",
    )
    data: dict[str, dict] = {}
    for n, t in enumerate(tickers, 1):
        try:
            info = yf.Ticker(t).info or {}
            data[t] = {k: info.get(k) for k in keys}
        except Exception:  # noqa: BLE001
            data[t] = {}
        if n % 25 == 0:
            print(f"  {n}/{len(tickers)}")
        time.sleep(0.25)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    FUND_FILE.write_text(json.dumps(
        {"updated": datetime.now(timezone.utc).isoformat(), "data": data},
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
    sma200_s = close.rolling(200).mean()
    sma50 = float(sma50_s.iloc[-1])
    sma200 = float(sma200_s.iloc[-1])
    sma50_slope = (sma50_s.iloc[-1] / sma50_s.iloc[-21] - 1) * 100
    sma200_slope = (sma200_s.iloc[-1] / sma200_s.iloc[-21] - 1) * 100

    low_recent = float(close.iloc[-30:].min())
    low_prev = float(close.iloc[-90:-30].min())
    higher_low = low_recent > low_prev

    rsi_s = rsi(close)
    rsi14 = float(rsi_s.iloc[-1])
    rsi_min60 = float(rsi_s.iloc[-60:].min())

    perf = {}
    for label, n in (("m1", 21), ("m3", 63), ("m6", 126), ("m12", 252)):
        if len(close) > n:
            perf[label] = (last / float(close.iloc[-n - 1]) - 1) * 100

    rs6 = None
    if bench is not None and len(bench) > 126 and "m6" in perf:
        b = bench.dropna()
        bench_perf = (float(b.iloc[-1]) / float(b.iloc[-127]) - 1) * 100
        rs6 = perf["m6"] - bench_perf

    vol_ratio = None
    if vol.notna().sum() > 60:
        tail_c, tail_v = close.tail(60), vol.tail(60)
        up = tail_c.diff() > 0
        v_up, v_dn = tail_v[up].mean(), tail_v[~up].mean()
        if v_dn and v_dn > 0:
            vol_ratio = float(v_up / v_dn)

    return {
        "last": round(last, 2),
        "dd_ath": round(dd_ath, 1),
        "days_since_ath": days_since_ath,
        "range_pos": round(range_pos, 1),
        "above_sma50": last > sma50,
        "above_sma200": last > sma200,
        "sma50_slope": round(float(sma50_slope), 2),
        "sma200_slope": round(float(sma200_slope), 2),
        "higher_low": bool(higher_low),
        "rsi14": round(rsi14, 1),
        "rsi_min60": round(rsi_min60, 1),
        "perf": {k: round(v, 1) for k, v in perf.items()},
        "rs6": round(rs6, 1) if rs6 is not None else None,
        "vol_ratio": round(vol_ratio, 2) if vol_ratio is not None else None,
    }


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------

def score_turnaround(m: dict) -> tuple[float, list[str]]:
    """Gefallen, aber Boden erkennbar."""
    pts, why = 0.0, []

    # Drawdown-Zone: interessant zwischen 25 und 60 Prozent, optimal 35-50
    p = 25 * plateau(-m["dd_ath"], 15, 30, 55, 75)
    pts += p
    if p > 15:
        why.append(f"{m['dd_ath']:.0f}% unter ATH")

    if m["higher_low"]:
        pts += 20
        why.append("hoeheres Tief")

    if m["above_sma50"]:
        pts += 15
        why.append("ueber 50-Tage-Linie")

    p = 10 * ramp(m["sma50_slope"], -1, 3)
    pts += p
    if p > 6:
        why.append("50-Tage-Linie dreht nach oben")

    # RSI aus der Ueberverkauftheit heraus
    if m["rsi_min60"] < 35 and 40 <= m["rsi14"] <= 70:
        pts += 15
        why.append("RSI erholt sich aus dem ueberverkauften Bereich")
    else:
        pts += 7 * plateau(m["rsi14"], 30, 45, 65, 80)

    if m["vol_ratio"] is not None:
        p = 10 * ramp(m["vol_ratio"], 0.9, 1.3)
        pts += p
        if p > 6:
            why.append("Anstiege auf hoeherem Volumen")

    pts += 5 * plateau(m["range_pos"], 5, 15, 55, 75)
    return round(pts, 1), why


def score_momentum(m: dict) -> tuple[float, list[str]]:
    """Staerke, nahe am Hoch."""
    pts, why = 0.0, []

    p = 25 * ramp(m["dd_ath"], -25, -2)
    pts += p
    if p > 15:
        why.append(f"nur {abs(m['dd_ath']):.0f}% unter ATH")

    if m["rs6"] is not None:
        p = 25 * ramp(m["rs6"], -5, 25)
        pts += p
        if p > 15:
            why.append(f"relative Staerke +{m['rs6']:.0f}% vs. Index")

    if m["above_sma50"] and m["above_sma200"]:
        pts += 20
        why.append("ueber 50- und 200-Tage-Linie")
    elif m["above_sma200"]:
        pts += 8

    p = 10 * ramp(m["sma200_slope"], 0, 4)
    pts += p
    if p > 6:
        why.append("200-Tage-Linie steigt")

    pts += 10 * ramp(m["range_pos"], 60, 90)

    if m["vol_ratio"] is not None:
        pts += 10 * ramp(m["vol_ratio"], 0.9, 1.25)
    return round(pts, 1), why


def score_value(m: dict, f: dict) -> tuple[float, list[str]]:
    """Bewertung und Qualitaet. Grobe Vorsortierung - Fundamentaldaten sind lueckenhaft."""
    pts, why = 0.0, []
    if not f:
        return 0.0, ["keine Fundamentaldaten"]

    tpe = safe(f, "trailingPE")
    fpe = safe(f, "forwardPE")
    peg = safe(f, "pegRatio")
    margin = safe(f, "profitMargins")
    rev_growth = safe(f, "revenueGrowth")
    d2e = safe(f, "debtToEquity")
    fcf = safe(f, "freeCashflow")
    roe = safe(f, "returnOnEquity")

    if fpe and tpe and 0 < fpe < tpe:
        pts += 15
        why.append("erwartetes KGV unter aktuellem")
    if fpe and 0 < fpe < 20:
        pts += 10 * ramp(fpe, 25, 8)
    if peg and 0 < peg < 2.5:
        p = 15 * ramp(peg, 2.5, 0.8)
        pts += p
        if p > 9:
            why.append(f"PEG {peg:.2f}")
    if fcf and fcf > 0:
        pts += 15
        why.append("positiver Free Cashflow")
    if margin and margin > 0:
        pts += 10 * ramp(margin, 0, 0.20)
    if rev_growth and rev_growth > 0:
        p = 15 * ramp(rev_growth, 0, 0.15)
        pts += p
        if p > 9:
            why.append(f"Umsatzwachstum {rev_growth * 100:.0f}%")
    if roe and roe > 0:
        pts += 10 * ramp(roe, 0.05, 0.25)
    if d2e is not None:
        pts += 10 * ramp(d2e, 200, 40)

    # Bewertung nuetzt nichts ohne Bodenbildung: leichter Zuschlag fuer Struktur
    if m["above_sma200"]:
        pts += 5
    return round(pts, 1), why


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

def build_state(prices, fundamentals, members, benchmarks) -> dict:
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
        flags = exclusions(m, f)
        s_turn, w_turn = score_turnaround(m)
        s_mom, w_mom = score_momentum(m)
        s_val, w_val = score_value(m, f)
        rows[t] = {
            "name": safe(f, "shortName", t),
            "index": "/".join(idxs),
            "metrics": m,
            "flags": flags,
            "earnings_in": earnings_in_days(f),
            "scores": {"turnaround": s_turn, "momentum": s_mom, "value": s_val},
            "why": {"turnaround": w_turn, "momentum": w_mom, "value": w_val},
        }

    ranks = {}
    for name in LISTS:
        eligible = [(t, r["scores"][name]) for t, r in rows.items() if not r["flags"]]
        eligible.sort(key=lambda x: x[1], reverse=True)
        ranks[name] = [t for t, _ in eligible[:TOP_N]]

    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ranks": ranks,
        "rows": rows,
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
    return changes


def fmt_row(t: str, row: dict, list_name: str) -> str:
    m = row["metrics"]
    why = ", ".join(row["why"][list_name][:3]) or "-"
    return (f"**{t}** ({row['name']}, {row['index']}) - Score {row['scores'][list_name]:.0f} | "
            f"{m['dd_ath']:.0f}% unter ATH, RSI {m['rsi14']:.0f} | {why}")


def build_report(today: dict, prev: dict, changes: dict) -> str:
    L = []
    L.append(f"# Boersen-Screening - {today['date']}")
    L.append("")
    L.append(f"_Stand: Schlusskurse vom Vortag. Erstellt {today['generated']} UTC. "
             f"{len(today['rows'])} Werte ausgewertet._")
    L.append("")

    if prev is None:
        L.append("## Erstlauf - Baseline angelegt")
        L.append("")
        L.append("Ab morgen werden nur noch Veraenderungen gemeldet. "
                 "Heute einmalig die kompletten Ranglisten:")
        L.append("")
        for name in LISTS:
            L.append(f"### {LIST_TITLES[name]}")
            L.append("")
            for i, t in enumerate(today["ranks"][name], 1):
                L.append(f"{i}. {fmt_row(t, today['rows'][t], name)}")
            L.append("")
        return "\n".join(L)

    any_change = any(
        changes[n]["entries"] or changes[n]["exits"] or changes[n]["moves"] for n in LISTS
    )

    if not any_change:
        L.append("## Keine Veraenderungen")
        L.append("")
        L.append(f"Alle drei Top-{TOP_N}-Listen unveraendert gegenueber {prev['date']}. "
                 "Kein Handlungsbedarf.")
        L.append("")
    else:
        for name in LISTS:
            c = changes[name]
            if not (c["entries"] or c["exits"] or c["moves"]):
                continue
            L.append(f"## {LIST_TITLES[name]}")
            L.append("")
            for e in c["entries"]:
                row = today["rows"][e["ticker"]]
                L.append(f"- ⬆️ **NEU auf Platz {e['rank']}**: {fmt_row(e['ticker'], row, name)}")
            for e in c["exits"]:
                row = today["rows"].get(e["ticker"])
                extra = ""
                if row:
                    extra = (f" - jetzt Score {row['scores'][name]:.0f}"
                             + (f", Ausschluss: {', '.join(row['flags'])}" if row["flags"] else ""))
                L.append(f"- ⬇️ **RAUS** (war Platz {e['old_rank']}): {e['ticker']}{extra}")
            for e in c["moves"]:
                arrow = "↗️" if e["delta"] > 0 else "↘️"
                L.append(f"- {arrow} {e['ticker']}: {abs(e['delta'])} Plaetze "
                         f"{'hoch' if e['delta'] > 0 else 'runter'}, jetzt Platz {e['rank']}")
            L.append("")

    # Termin- und Risikohinweise fuer alle aktuell gelisteten Werte
    watch = sorted({t for n in LISTS for t in today["ranks"][n]})
    earnings = [(t, today["rows"][t]["earnings_in"]) for t in watch
                if today["rows"][t]["earnings_in"] is not None
                and today["rows"][t]["earnings_in"] <= EARNINGS_WARN_DAYS]
    if earnings:
        L.append("## ⚠️ Quartalszahlen in Kuerze")
        L.append("")
        for t, d in sorted(earnings, key=lambda x: x[1]):
            L.append(f"- {t}: in {d} Tag(en)")
        L.append("")

    L.append("---")
    L.append("")
    L.append(f"_Aktuelle Listen: Turnaround {', '.join(today['ranks']['turnaround'][:5])} ... | "
             f"Momentum {', '.join(today['ranks']['momentum'][:5])} ... | "
             f"Value {', '.join(today['ranks']['value'][:5])} ..._")
    L.append("")
    L.append("_Automatisch erzeugte Kennzahlensortierung, keine Anlageberatung._")
    return "\n".join(L)


# ---------------------------------------------------------------------------

def main() -> int:
    members, benchmarks = load_universe()
    tickers = sorted(members.keys())
    all_symbols = tickers + list(benchmarks.values())

    prices = get_prices(all_symbols)
    if len(prices) < 20:
        print("Zu wenige Kursdaten - Abbruch, Zustand bleibt unveraendert.")
        return 1

    fundamentals = get_fundamentals(tickers)

    today = build_state(prices, fundamentals, members, benchmarks)

    prev = None
    if STATE_FILE.exists():
        try:
            prev = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prev = None
    if prev and prev.get("date") == today["date"]:
        print("Hinweis: heutiger Lauf existiert bereits, vergleiche trotzdem.")

    changes = diff_lists(today, prev) if prev else {}
    report = build_report(today, prev, changes)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "report.md").write_text(report, encoding="utf-8")
    (DOCS_DIR / "report.json").write_text(json.dumps(
        {"date": today["date"], "ranks": today["ranks"], "changes": changes},
        indent=1, ensure_ascii=False), encoding="utf-8")
    STATE_FILE.write_text(json.dumps(today, indent=1, ensure_ascii=False), encoding="utf-8")

    print("\n" + report[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
