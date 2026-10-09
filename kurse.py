"""
kurse.py - ein Abruf, ein Cache, alle Skripte bedienen sich daraus.

Vorher holten screener.py, tiefs.py und marktdaten.py dieselben Kerzen
getrennt: sechs Abrufe plus einer plus einer, dreimal ueber die Leitung.
Das kostet Laufzeit im 30-Minuten-Fenster und provoziert Rate-Limits bei
Yahoo, die dann als "keine Daten" durchschlagen.

Weil die drei Skripte als getrennte Workflow-Schritte laufen, also in
getrennten Prozessen, reicht ein Cache im Arbeitsspeicher nicht - er muss
auf die Platte. Der Runner behaelt das Verzeichnis ueber alle Schritte
eines Laufs hinweg.

Der Cache liegt bewusst NICHT in state/, weil der Workflow "git add docs
state" macht und die Kursdateien sonst jeden Tag ins Repository wandern.
.kurse_cache/ gehoert in .gitignore.

Frische: ein Kalendertag. Ein zweiter Lauf am selben Tag liest aus dem
Cache, der naechste Morgen holt neu.
"""

from __future__ import annotations

import os
import time
import shutil
import json
import statistics
from datetime import date, datetime, timedelta, timezone
from io import StringIO

import pandas as pd
import requests
import re
import yfinance as yf
from dateutil.easter import easter

HIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HIER, ".kurse_cache")

# Version im Dateinamen: aendert sich das Format oder die Aufbereitung,
# darf ein alter Cache nicht stillschweigend weiterbenutzt werden. Genau
# dieser Fehler ist beim Fundamentaldaten-Cache schon einmal passiert.
CACHE_VERSION = 2   # 03.10.2026: Heimatboerse/Pence-Umrechnung - alte Caches ungueltig

MINDESTKERZEN = 30

# ── Abweichende Kursquellen ────────────────────────────────────────
# Einige Werte notieren an mehreren Boersen, und der Report rechnete
# bisher auf der falschen. ASML steht im Universum als "ASML" und wurde
# damit von der New Yorker Registry-Notierung in USD geholt - waehrend der
# Knock-out-Schein auf die Euro-Notierung lautet und der Chart im
# Orderbuch (Frage 9: Kurs 1508,00, Wochentief 1489,40) ebenfalls in Euro
# gelesen wurde. Der ausgewiesene Puffer war deshalb frei erfunden; bei
# ASML war er sechsmal zu gross.
#
# Der Ticker als Name bleibt unveraendert, damit alle Verknuepfungen mit
# analysten.csv und universe.json halten. Getauscht wird nur, WOHER die
# Kerzen kommen. Betroffen sind Kurs, ATR und Tiefs, also alles, was
# marktdaten.py und tiefs.py rechnen - screener.py holt seine Kurse
# getrennt und vergleicht dort Kurs und Kursziel weiter in derselben
# Waehrung, bleibt also in sich stimmig.
#
# BEWUSST OHNE RUECKFALL auf die andere Notierung: ein stiller Wechsel
# zurueck in eine fremde Waehrung wuerde genau den Fehler wieder
# einbauen, den diese Liste behebt. Liefert die Quelle nichts, faellt der
# Wert mit Meldung aus - sichtbar statt falsch.
#
# Der Quellencheck vom 24.08.2026 hat geprueft, welche Werte ueberhaupt
# betroffen sind: NXPI.AS kennt Yahoo nicht, NXP ist also kein
# Zweitnotierungsfall. AZN und CCEP haben ihre Ratings ohnehin auf der
# US-Seite. Bleibt ASML.
KURSQUELLE: dict[str, dict] = {
    "ASML": {
        "ticker": "ASML.AS",
        "waehrung": "EUR",
        "grund": "Schein und Chart laufen auf der Euro-Notierung, "
                 "nicht auf der New Yorker Registry-Notierung",
    },
}

# ── HEIMATBOERSE (03.10.2026, Peter: "Ja, ich haette nicht gedacht, dass wir die Heimatboerse ausgeschlossen haben.
# Das betraf ja eigentlich nur ASML" · Umbau "Jetzt"). Werte, deren Haupthandel NICHT in den USA liegt, werden an der
# Heimatboerse ausgewertet - Kurs, ATR, Tiefs, KO-Statistik in Heimatwaehrung. Anlass: BAT 02.10.2026 - London mit
# 74 Mio. Stueck Volumen zeigte eine gruene Kerze, die US-Notierung nur einen Mini-Hammer; Trade Republic fuehrt
# Turbos direkt auf die Londoner Notierung (SG DE000FA62HF8, KO in GBP). Der Name (US-Ticker) bleibt, damit alle
# Verknuepfungen halten; Analysten-Kursziele rechnet screener.py in die Heimatwaehrung um.
# "faktor": Yahoo notiert London in Pence (GBp) - 0,01 macht daraus Pfund wie bei Trade Republic.
for _name, _q, _w, _f in (
        ("BTI", "BATS.L", "GBP", 0.01), ("SHEL", "SHEL.L", "GBP", 0.01), ("HSBC", "HSBA.L", "GBP", 0.01),
        ("UL", "ULVR.L", "GBP", 0.01), ("AZN", "AZN.L", "GBP", 0.01), ("GSK", "GSK.L", "GBP", 0.01),
        ("BP", "BP.L", "GBP", 0.01), ("RIO", "RIO.L", "GBP", 0.01),
        ("NVO", "NOVO-B.CO", "DKK", 1.0), ("NVS", "NOVN.SW", "CHF", 1.0), ("UBS", "UBSG.SW", "CHF", 1.0),
        ("SNY", "SAN.PA", "EUR", 1.0), ("TTE", "TTE.PA", "EUR", 1.0), ("ING", "INGA.AS", "EUR", 1.0),
        ("SAN", "SAN.MC", "EUR", 1.0), ("BBVA", "BBVA.MC", "EUR", 1.0), ("EQNR", "EQNR.OL", "NOK", 1.0),
        ("TSM", "2330.TW", "TWD", 1.0), ("TM", "7203.T", "JPY", 1.0), ("SONY", "6758.T", "JPY", 1.0),
        ("MUFG", "8306.T", "JPY", 1.0), ("SMFG", "8316.T", "JPY", 1.0), ("MFG", "8411.T", "JPY", 1.0),
        ("BABA", "9988.HK", "HKD", 1.0), ("BHP", "BHP.AX", "AUD", 1.0), ("HDB", "HDFCBANK.NS", "INR", 1.0),
        ("IBN", "ICICIBANK.NS", "INR", 1.0), ("PBR", "PETR3.SA", "BRL", 1.0), ("SKHY", "000660.KS", "KRW", 1.0)):
    KURSQUELLE[_name] = {"ticker": _q, "waehrung": _w, "faktor": _f, "grund": "Heimatboerse (Peter 03.10.2026)"}


def faktor(ticker: str) -> float:
    """Umrechnung der Yahoo-Kurse in die Handelswaehrung (London: Pence -> Pfund)."""
    return float(KURSQUELLE.get(ticker, {}).get("faktor", 1.0))


def _skalieren(df, ticker):
    """Open/High/Low/Close mit faktor() multiplizieren (Volumen bleibt). Nur EINMAL je Abruf aufrufen."""
    f = faktor(ticker)
    if df is None or f == 1.0:
        return df
    df = df.copy()
    for sp in ("Open", "High", "Low", "Close", "Adj Close"):
        if sp in df.columns:
            df[sp] = df[sp] * f
    return df


def _ohne_rueckfall(ticker: str) -> bool:
    """Heimatboerse ohne Stooq/Twelve-Data-Rueckfall (andere Waehrung/Einheit waere still falsch)."""
    return ticker in KURSQUELLE and ticker != "ASML"


def quelle(ticker: str) -> str:
    """Von welchem Yahoo-Ticker die Kerzen dieses Wertes kommen."""
    return KURSQUELLE.get(ticker, {}).get("ticker", ticker)


def waehrung(ticker: str) -> str:
    """Waehrung der Kursreihe, leer wenn keine Ausnahme hinterlegt ist."""
    return KURSQUELLE.get(ticker, {}).get("waehrung", "")


def quellen(tickers: list[str]) -> dict[str, str]:
    """Name auf Quellticker fuer einen ganzen Stapel.

    Fuer historie.py, tagesreaktion.py und phasen.py: die drei holen ihre
    Kerzen aus Zeitgruenden gebuendelt ueber yf.download statt einzeln
    ueber kerzen(), brauchen aber dieselbe Zuordnung. Ohne sie rechneten
    die Halteraten und Puffer-Verteilungen fuer ASML weiter auf der
    Dollar-Reihe, waehrend der Tagesbericht in Euro rechnet - und ein Tief
    in Dollar ist keines in Euro, wenn der Wechselkurs dazwischenlaeuft.

    Angefragt wird beim Quellticker, abgelegt unter dem Namen.
    """
    zuordnung = {t: quelle(t) for t in tickers}
    for name, q in zuordnung.items():
        if q != name:
            print(f"  {name}: Kurse von {q} ({waehrung(name)})")
    return zuordnung


_MEM: dict[tuple, pd.DataFrame] = {}

# Merker fuer die Stooq-Diagnose (15.09.2026): Die Antwort wird nur EINMAL
# pro Lauf ausgegeben. Bei 219 Tickern waere das Log sonst unbrauchbar -
# genau das war am 09. und 15.09.2026 das Problem, als 219 identische
# Parser-Fehler die eigentliche Ursache verdeckten.
_STOOQ_GEMELDET = False


def _pfad(ticker: str, period: str, auto_adjust: bool = False) -> str:
    sicher = "".join(c if c.isalnum() or c in "-_" else "_" for c in ticker)
    suffix = "_adj" if auto_adjust else ""
    return os.path.join(CACHE, f"v{CACHE_VERSION}_{sicher}_{period}{suffix}.csv")


# Hoechstalter einer Cache-Datei in Stunden. Loest die frueherere Regel
# "Kalendertag muss heute sein" ab (Fund vom 09.09.2026).
#
# Warum: Der 22:15-UTC-Lauf beginnt vor Mitternacht und endet danach.
# marktdaten.py fuellte den Cache am 08.09.2026 um 22:1x - kursverlauf.py
# rief aufraeumen() um 00:14 des Folgetags auf, verglich Kalendertage und
# loeschte damit den gesamten, wenige Minuten alten Cache. Anschliessend
# holte es 218 Ticker in 16 Sekunden neu, lief bei Yahoo in die Bremse und
# schrieb einen Stand vom 04.09. Die Tage 07.09. (1 Wert) und 08.09.
# (13 Werte) fielen danach unter MINDESTBESETZUNG und flogen aus der
# Tagesachse - unbemerkt, weil der Schritt continue-on-error hat.
#
# Zwoelf Stunden sind kurz genug, damit ein Lauf am naechsten Morgen
# frische Kerzen holt, und lang genug, dass ein Lauf ueber Mitternacht
# seinen eigenen Cache behaelt.
CACHE_MAX_STUNDEN = 12


def aufraeumen() -> None:
    """Cache-Dateien entfernen, die aelter als CACHE_MAX_STUNDEN sind
    oder aus einer frueheren Cache-Version stammen."""
    if not os.path.isdir(CACHE):
        return
    grenze = time.time() - CACHE_MAX_STUNDEN * 3600
    for name in os.listdir(CACHE):
        pfad = os.path.join(CACHE, name)
        try:
            if (os.path.getmtime(pfad) < grenze
                    or not name.startswith(f"v{CACHE_VERSION}_")):
                os.remove(pfad)
        except OSError:
            pass


def leeren() -> None:
    """Cache vollstaendig verwerfen - fuer Tests."""
    _MEM.clear()
    shutil.rmtree(CACHE, ignore_errors=True)


def _platzhalter_weg(df: pd.DataFrame, letzte_behalten: bool = True) -> pd.DataFrame:
    """PLATZHALTER-KERZEN (03.10.2026, Peter: "Wenn Fehler vorhanden sind, muessen die sofort korrigiert
    werden"). Yahoo liefert an manchen Tagen statt der echten Kerze einen Platzhalter: Eroeffnung = Hoch =
    Tief = Schluss = Vortagesschluss, Volumen 0 (z. B. 25.06.2026 bei 13 deutschen Werten - Rheinmetall
    fiel an dem Tag intraday bis rund 893, im Platzhalter stand 949). Solche Zeilen sind KEIN Kurs, sie
    werden verworfen; der Tag gilt dann als fehlend und _loecher_fuellen baut ihn aus Stundenkerzen neu.
    Die juengste Zeile bleibt stehen (sonst haengt der Wert in der Vollstaendigkeitspruefung zurueck);
    datenpruefung.py meldet sie. Dazu werden unlogische Kerzen bereinigt (Schluss/Eroeffnung ausserhalb
    von Hoch/Tief): Hoch = groesster, Tief = kleinster der vier Werte."""
    if df is None or df.empty or not {"Open", "High", "Low", "Close"} <= set(df.columns):
        return df
    v = df["Volume"] if "Volume" in df.columns else pd.Series(0.0, index=df.index)
    platz = ((df["Open"] == df["High"]) & (df["High"] == df["Low"]) & (df["Low"] == df["Close"])
             & ((v == 0) | v.isna()))
    if letzte_behalten and len(platz):
        platz.iloc[-1] = False
    if platz.any():
        print(f"  Platzhalter verworfen: {', '.join(str(d)[:10] for d in df.index[platz])}")
    df = df[~platz].copy()
    vier = df[["Open", "High", "Low", "Close"]]
    df["High"] = vier.max(axis=1)
    df["Low"] = vier.min(axis=1)
    return df


def _aufbereiten(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    df = _platzhalter_weg(df)
    if len(df) < MINDESTKERZEN:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def stooq_symbol(ticker: str) -> str:
    """Yahoo-Ticker auf Stooqs Schreibweise uebersetzt.

    Aus screener.py verschoben (30.08.2026, Fragen 43/44) - dort lief das
    bereits als Fallback fuer Aktien. Neu dazugekommen: die "=X"-Endung
    fuer FX- und Edelmetall-Spotpaare (XAUUSD=X -> xauusd). Stooq fuehrt
    diese Paare ohne Praefix oder Laenderendung.
    """
    if ticker.startswith("^"):
        return {"^NDX": "^ndq", "^DJI": "^dji", "^GDAXI": "^dax"}.get(ticker, ticker.lower())
    if ticker.endswith("=X"):
        return ticker[:-2].lower()
    if ticker.endswith(".DE"):
        return ticker[:-3].replace(".", "-").lower() + ".de"
    return ticker.replace(".", "-").lower() + ".us"


def kerzen_stooq(ticker: str) -> pd.DataFrame | None:
    """Fallback ueber Stooq, wenn Yahoo nichts liefert.

    Bisher nur in screener.py als Fallback fuer einzelne Aktien genutzt.
    Am 30.08.2026 hierher verschoben und fuer Edelmetall-Spotpaare
    erweitert (Frage 44): Yahoo liefert fuer XAUUSD=X/XAGUSD=X/XPTUSD=X/
    XPDUSD=X nachweislich keine Daten, marktdaten.py faellt seither direkt
    auf die Future-Notierung zurueck (Contango, nicht 1:1 mit dem Spot).
    Ob Stooq hier taugt, zeigt sich am naechsten Lauf von selbst - dieser
    Fallback greift nur, wenn Yahoo bereits gescheitert ist, kann also
    nichts verschlechtern.

    Wie bei kerzen() zaehlt die Quelle, nicht der Name - ASML wird intern
    ueber ASML.AS abgerufen, nicht ueber das US-Kuerzel, das auf Stooq
    kein sinnvolles Ergebnis liefern wuerde.

    Eigener Cache-Praefix ("stooq_"), damit ein Yahoo-Fehlschlag von
    heute nicht mit einer erfolgreichen Stooq-Reihe von gestern verwechselt
    wird - beide landen unter unterschiedlichen Dateinamen.
    """
    if _ohne_rueckfall(ticker):   # 03.10.2026: Heimatboerse - kein Rueckfall in fremder Einheit
        return None
    holen = quelle(ticker)
    key = (ticker, "stooq")
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    pfad = _pfad(f"stooq_{holen}", "voll")
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {ticker}: Stooq-Cache unlesbar ({e}), hole neu")

    # HTTP Error 404 beim ersten Praxistest (30.08.2026, Actions-Log,
    # Screening-Lauf 12:48 UTC) - fuer alle vier Edelmetalle, exakt bei
    # dieser URL, die in externer Dokumentation (Stand Januar 2026) als
    # funktionierend beschrieben war. Wahrscheinlichste Erklaerung: pandas
    # ruft pd.read_csv(url) intern ueber urllib auf, das einen generischen
    # Python-User-Agent mitschickt ("Python-urllib/3.x") - eine
    # gaengige, einfache Sperre vieler Seiten gegen genau dieses Muster,
    # auch ohne robots.txt-Pruefung. Deshalb hier ueber requests mit einem
    # browserartigen User-Agent statt direkt ueber pandas. Ob das der
    # tatsaechliche Grund war, zeigt erst der naechste Lauf - von hier aus
    # nicht testbar, stooq.com steht nicht auf der Netzwerk-Freigabeliste
    # dieser Umgebung.
    url = f"https://stooq.com/q/d/l/?s={stooq_symbol(holen)}&i=d"
    try:
        antwort = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36"})
        antwort.raise_for_status()

        # DIAGNOSE, eingebaut am 15.09.2026.
        #
        # Am 09.09. und erneut am 15.09.2026 scheiterte JEDER Stooq-Abruf -
        # 219 von 219, auch die US-Werte - mit derselben Meldung:
        # "Missing column provided to 'parse_dates': 'Date'". Das ist ein
        # Parser-Fehler, kein Netzwerkfehler: raise_for_status() ging
        # durch, Stooq antwortet also mit HTTP 200. Der Inhalt ist nur
        # keine CSV mit Date-Spalte.
        #
        # Der alte Code las die Antwort blind als CSV und meldete den
        # Folgefehler statt der Ursache. Was Stooq tatsaechlich schickt -
        # eine Limitmeldung, eine Sperrseite, eine HTML-Weiterleitung -
        # war aus dem Log nicht erkennbar. Deshalb wird der Anfang der
        # Antwort jetzt EINMAL pro Lauf ausgegeben, nicht 219-mal.
        kopf = antwort.text.lstrip()[:200].replace("\n", " | ")
        if not antwort.text.lstrip().startswith("Date,"):
            global _STOOQ_GEMELDET
            if not _STOOQ_GEMELDET:
                _STOOQ_GEMELDET = True
                print(f"  STOOQ ANTWORTET NICHT MIT CSV. HTTP "
                      f"{antwort.status_code}, Content-Type "
                      f"{antwort.headers.get('Content-Type', '?')}, "
                      f"{len(antwort.text)} Zeichen.")
                print(f"    Anfang der Antwort: {kopf}")
                print(f"    Abgerufene URL: {url}")
            raise ValueError("Antwort ist keine CSV")

        roh = pd.read_csv(StringIO(antwort.text), parse_dates=["Date"]).set_index("Date")
    except Exception as e:
        print(f"  {ticker}: Stooq-Abruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _aufbereiten(roh)
    _MEM[key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {holen}: Stooq-Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()


def kerzen_twelvedata(ticker: str, tage: int = 30) -> pd.DataFrame | None:
    """Fallback ueber Twelve Data (01.09.2026, weiter zu Fragen 43/44) -
    eine echte REST-API mit API-Key statt einer Webseite, die man mit
    einem Skript nachahmt. Stooq blockierte Anfragen aus GitHub Actions
    offenbar pauschal (Cloud-IP-Bereiche werden von vielen Seiten so
    behandelt, unabhaengig vom User-Agent) - eine echte API mit Key
    umgeht genau dieses Problem.

    Key kommt AUSSCHLIESSLICH aus der Umgebungsvariable TWELVEDATA_API_KEY
    (GitHub Secret) - steht nirgends im Quelltext. Fehlt die Variable,
    liefert diese Funktion sauber None, kein Fehler.

    Nur fuer Tageskerzen gedacht, deshalb bewusst kurzes Standardfenster
    (30 Tage) - reicht, um "wie aktuell ist die letzte Kerze" zu pruefen
    und im Bedarfsfall die letzten paar Tage nachzuliefern. Fuer eine
    vollstaendige 400-Tage-Historie waere das Gratis-Kontingent
    (800 Anfragen/Tag, 8/Minute) zu knapp bemessen.
    """
    if _ohne_rueckfall(ticker):   # 03.10.2026: Heimatboerse - kein Rueckfall in fremder Einheit
        return None
    key = os.environ.get("TWELVEDATA_API_KEY")
    if not key:
        return None

    holen = quelle(ticker)
    mem_key = (ticker, "twelvedata", tage)
    if mem_key in _MEM:
        wert = _MEM[mem_key]
        return None if wert is None else wert.copy()

    pfad = _pfad(f"twelvedata_{holen}", f"{tage}d")
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= 5:
                    _MEM[mem_key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {ticker}: Twelve-Data-Cache unlesbar ({e}), hole neu")

    basis = holen[:-3] if holen.endswith(".DE") else holen
    params = {"symbol": basis, "interval": "1day", "outputsize": tage,
              "order": "ASC", "apikey": key}
    if holen.endswith(".DE"):
        params["mic_code"] = "XETR"
    try:
        antwort = requests.get("https://api.twelvedata.com/time_series",
                               params=params, timeout=15)
        antwort.raise_for_status()
        roh = antwort.json()
    except Exception as e:
        print(f"  {ticker}: Twelve-Data-Abruf fehlgeschlagen ({e})")
        _MEM[mem_key] = None
        return None

    if roh.get("status") == "error" or "values" not in roh:
        print(f"  {ticker}: Twelve Data meldet Fehler ({roh.get('message', roh)})")
        _MEM[mem_key] = None
        return None

    df = pd.DataFrame(roh["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").rename(columns={
        "open": "Open", "high": "High", "low": "Low", "close": "Close",
        "volume": "Volume"})
    for c in ("Open", "High", "Low", "Close", "Volume"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # Kein _aufbereiten() hier - das verlangt MINDESTKERZEN (30) Zeilen,
    # gedacht fuer die lange 400-Tage-Reihe. Dieser Abruf ist bewusst kurz
    # (Standard 30 Kalendertage, das sind eher 20 Handelstage), soll nur
    # die letzten paar frischen Tage liefern - eine einfache Pruefung
    # reicht.
    if "Low" not in df.columns or "Close" not in df.columns:
        df = None
    else:
        df = df.dropna(subset=["Low", "Close"])
        if df.empty:
            df = None

    _MEM[mem_key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {holen}: Twelve-Data-Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()


# ── Lange Zeitraeume (27.09.2026, Peter: Historie 20 statt 7 Jahre) ──
# Yahoo kennt feste Zeitraeume wie "10y" oder "max" sicher, "20y" nicht
# verlaesslich. Zeitraeume ueber 10 Jahre werden deshalb mit "max" geholt und
# danach auf die gewuenschte Laenge gekuerzt. Getestet im Testlauf test20.yml.
def _abruf_zeitraum(period: str) -> tuple[str, int | None]:
    m = re.fullmatch(r"(\d+)y", str(period))
    if m and int(m.group(1)) > 10:
        return "max", int(m.group(1))
    return period, None


def _kuerzen(df, jahre: int | None):
    if df is None or jahre is None or len(df) == 0:
        return df
    ab = pd.Timestamp.today().normalize() - pd.DateOffset(years=jahre)
    idx = df.index.tz_localize(None) if getattr(df.index, "tz", None) else df.index
    return df[idx >= ab]


def kerzen(ticker: str, period: str = "400d", auto_adjust: bool = False) -> pd.DataFrame | None:
    """Tageskerzen fuer einen Ticker. None, wenn keine brauchbaren Daten.

    Reihenfolge: Arbeitsspeicher, dann Tagescache auf der Platte, dann
    Yahoo. Ein Fehlschlag wird als None gemerkt, damit ein toter Ticker
    nicht bei jedem Aufruf erneut abgefragt wird.

    auto_adjust=False ist die Voreinstellung und bleibt es fuer alle
    bisherigen Aufrufer (marktdaten.py, tiefs.py, phasen.py, historie.py,
    hochs.py, ruecksetzer.py) unveraendert. screener.py rechnete bisher
    mit auto_adjust=True (dividenden-/split-bereinigt) - beim Umzug auf
    diese Funktion (30.08.2026) bewusst NICHT stillschweigend
    vereinheitlicht, das waere eine Methodikaenderung, keine reine
    Code-Zusammenlegung. Beide Varianten leben nebeneinander im Cache
    (Dateiname mit "_adj"-Endung fuer die angepasste Reihe), sodass sie
    sich nicht gegenseitig ueberschreiben.
    """
    key = (ticker, period, auto_adjust)
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    # Ab hier zaehlt die Quelle, nicht der Name. Cache und Abruf laufen
    # unter dem Quellticker, damit zwei Namen auf dieselbe Reihe nicht
    # zwei Abrufe ausloesen.
    holen = quelle(ticker)
    if holen != ticker:
        print(f"  {ticker}: Kurse von {holen} ({waehrung(ticker)})")

    pfad = _pfad(holen, period, auto_adjust)
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {holen}: Cache unlesbar ({e}), hole neu")

    try:
        abruf, lang = _abruf_zeitraum(period)
        roh = yf.Ticker(holen).history(period=abruf, interval="1d",
                                       auto_adjust=auto_adjust)
    except Exception as e:
        print(f"  {holen}: Abruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _skalieren(_kuerzen(_aufbereiten(roh), lang), ticker)
    # LOECHER FUELLEN (19.09.2026). Siehe Abschnitt "Handelskalender und
    # Lueckenfuellung" weiter unten.
    bericht = {}
    if df is not None:
        df, bericht = _loecher_fuellen(ticker, holen, df, auto_adjust)
    _MEM[key] = df
    _FUELLUNG[key] = bericht
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
            with open(_fuell_pfad(holen, period, auto_adjust), "w", encoding="utf-8") as f:
                json.dump(bericht, f)
        except OSError as e:
            print(f"  {holen}: Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()


def kerzen_batch(tickers: list[str], period: str = "400d",
                  auto_adjust: bool = False) -> dict[str, pd.DataFrame]:
    """Tageskerzen fuer VIELE Ticker in einem Rutsch statt einzeln.

    Fuer screener.py entstanden (30.08.2026): das Skript braucht alle
    ~200 Werte auf einmal fuer die 10-Jahres-Historie zum Allzeithoch. Ein
    Abruf je Ticker ueber kerzen() waere hier falsch - erst recht ohne
    Cache-Treffer aus einem anderen Skript, weil kein anderes Skript mit
    demselben Zeitraum arbeitet. Genau das Problem, das kurse.py
    eigentlich verhindern soll (Laufzeit im 30-Minuten-Fenster,
    Rate-Limits bei Yahoo), waere durch einen naiven Umstieg auf
    kerzen() zurueckgekommen, nur diesmal in screener.py statt verteilt
    auf drei Skripte.

    Nutzt denselben Cache wie kerzen() - ein spaeterer einzelner
    kerzen()-Aufruf fuer denselben Ticker, Zeitraum und dieselbe
    auto_adjust-Einstellung liest den hier gefuellten Cache, und
    umgekehrt.

    Anders als kerzen() merkt sich das hier NICHT einzeln, welcher Ticker
    fehlgeschlagen ist - eine Batch-Anfrage soll selten laufen (einmal
    pro Skriptlauf ueber das ganze Universum), wiederholte Fehlschlaege
    sind dabei kein Problem.
    """
    ergebnis: dict[str, pd.DataFrame] = {}
    frisch: list[str] = []
    quelle_von = {t: quelle(t) for t in tickers}

    for t in tickers:
        key = (t, period, auto_adjust)
        if key in _MEM:
            wert = _MEM[key]
            if wert is not None:
                ergebnis[t] = wert.copy()
            continue
        pfad = _pfad(quelle_von[t], period, auto_adjust)
        if os.path.exists(pfad):
            try:
                if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                    df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                    if len(df) >= MINDESTKERZEN:
                        _MEM[key] = df
                        ergebnis[t] = df.copy()
                        continue
            except Exception as e:
                print(f"  {t}: Cache unlesbar ({e}), hole neu")
        frisch.append(t)

    quellticker = sorted({quelle_von[t] for t in frisch})
    roh_je_quelle: dict[str, pd.DataFrame] = {}
    chunk = 40
    for i in range(0, len(quellticker), chunk):
        batch = quellticker[i:i + chunk]
        try:
            data = yf.download(batch, period=_abruf_zeitraum(period)[0], interval="1d",
                                auto_adjust=auto_adjust, group_by="ticker",
                                threads=True, progress=False)
        except Exception as e:
            print(f"  ! Batch-Download fehlgeschlagen ({batch[0]}...): {e}")
            continue
        for q in batch:
            try:
                roh_je_quelle[q] = (data[q] if isinstance(data.columns, pd.MultiIndex)
                                     else data)
            except Exception:
                continue

    os.makedirs(CACHE, exist_ok=True)
    for t in frisch:
        q = quelle_von[t]
        df = _skalieren(_kuerzen(_aufbereiten(roh_je_quelle.get(q)), _abruf_zeitraum(period)[1]), t)
        _MEM[(t, period, auto_adjust)] = df
        if df is not None:
            ergebnis[t] = df.copy()
            try:
                df.to_csv(_pfad(q, period, auto_adjust))
            except OSError as e:
                print(f"  {q}: Cache nicht schreibbar ({e})")
    return ergebnis


# ── Stundenkerzen ──────────────────────────────────────────────────
# Bewusst eine eigene Funktion statt eines interval-Parameters an
# kerzen(): die Stundenreihe hat andere Eigenschaften und darf die
# Tagesreihe nirgends versehentlich ersetzen.
#
#   - Yahoo liefert 1h nur rund zwei Jahre zurueck, nicht 400 Tage
#     plus Reserve wie bei 1d. Fuer Halteraten und Puffer-Verteilungen
#     taugt sie deshalb NICHT (siehe Gespraech vom 25.08.2026) - sie ist
#     ausschliesslich fuer den Blick auf den laufenden Tag gedacht.
#   - MINDESTKERZEN aus der Tageslogik passt nicht: ein einzelner
#     US-Handelstag hat rund 7 Stundenkerzen. Ein Tag mit Feiertag oder
#     verkuerztem Handel haette danach "keine Daten".
#
# Der Cache laeuft ueber denselben Tagesmechanismus wie die Tagesreihe,
# mit eigenem Praefix im Dateinamen.
STUNDEN_MINDESTKERZEN = 3


def _aufbereiten_stunden(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < STUNDEN_MINDESTKERZEN:
        return None
    # Zeitzone behalten waere ehrlicher, macht aber jeden Vergleich mit
    # der Tagesreihe zum Sonderfall. Stattdessen auf die Boersenzeit des
    # jeweiligen Wertes normalisiert und dann tz-frei - wie bei kerzen().
    df.index = pd.to_datetime(df.index)
    try:
        df.index = df.index.tz_localize(None)
    except TypeError:
        df.index = df.index.tz_convert(None)
    return df


def stundenkerzen(ticker: str, period: str = "5d", auto_adjust: bool = False) -> pd.DataFrame | None:
    """Stundenkerzen fuer einen Ticker. None, wenn keine brauchbaren Daten.

    Fuenf Handelstage reichen fuer den laufenden Tag samt Vergleich zu
    den Vortagen und halten die Antwort klein. Wer mehr braucht, gibt
    period ausdruecklich groesser an - Yahoo deckelt bei rund zwei Jahren.

    auto_adjust wie bei kerzen(): Voreinstellung False bleibt fuer
    bisherige Aufrufer unveraendert, screener.py ruft mit True auf, um
    sein bisheriges Verhalten zu erhalten (30.08.2026).
    """
    key = (ticker, period, "1h", auto_adjust)
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    holen = quelle(ticker)
    pfad = _pfad(f"h_{holen}", period, auto_adjust)
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= STUNDEN_MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {holen}: Stunden-Cache unlesbar ({e}), hole neu")

    try:
        roh = yf.Ticker(holen).history(period=period, interval="1h",
                                       auto_adjust=auto_adjust)
    except Exception as e:
        print(f"  {holen}: Stundenabruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _skalieren(_aufbereiten_stunden(roh), ticker)
    _MEM[key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {holen}: Stunden-Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()



# ── Handelskalender und Lueckenfuellung ────────────────────────────
# Eingebaut am 19.09.2026 auf Peters Vorgabe ("wenn keine vollstaendigen
# Daten vorliegen, kann man das Tief nicht richtig bestimmen").
#
# ANLASS: Yahoo lieferte fuer alle 40 deutschen Werte und ASML nie eine
# Kerze vom 17.09.2026 - in keinem Lauf, auch nicht nachtraeglich. Drei
# Schwaechen kamen zusammen:
#   1. Die Pruefung in kursverlauf.py schaute nur, ob der LETZTE Tag da
#      ist. Ein Loch mitten in der Reihe (17.09. fehlt, 18.09. da) fiel
#      niemandem auf.
#   2. Die Zweitquelle Twelve Data deckt im Gratistarif NUR US-Boersen ab,
#      kein XETRA (Preisseite, geprueft 19.09.2026). Der Notnagel, der fuer
#      die deutschen Werte gedacht war, griff bei ihnen nie.
#   3. Der Kalender wurde aus den gelieferten Daten abgeleitet. Fehlt ein
#      Tag bei ALLEN Werten einer Boerse, sieht er aus wie ein Feiertag.
# Folge: Luecken falsch als geschlossen gewertet (Infineon), Folgekerze
# und Bezugstief der EU-Werte ungeprueft.
#
# DIE LOESUNG in drei Stufen, hier an der Quelle, damit ALLE Skripte, die
# kerzen() nutzen, dieselben vollstaendigen Reihen bekommen:
#   a) Fester Boersenkalender je Handelsplatz statt Ableitung aus Daten.
#   b) Fehlender Tag zuerst aus dem ARCHIV (docs/kursverlauf*.csv aus dem
#      letzten Lauf) - eine Kerze, die einmal da war, geht nicht mehr
#      verloren, auch wenn Yahoo sie spaeter nicht mehr liefert.
#   c) Sonst aus Yahoos STUNDENKERZEN nachgebaut: Eroeffnung der ersten
#      Stunde, Hoch und Tief ueber alle Stunden, Schluss der letzten
#      Stunde, Volumen als Summe. Anderer Abrufweg als die Tagesreihe und
#      in der Praxis meist vollstaendig. Yahoo hat Stundenkerzen nur rund
#      zwei Jahre zurueck, deshalb die Grenze STUNDEN_FUELLGRENZE_TAGE.
# Was danach noch fehlt, bleibt ein ehrliches Loch. heute.py nimmt einen
# Wert mit Loch in den letzten PRUEF_TAGE Handelstagen aus Block 1 (harte
# Sperre, Peters Entscheidung vom 19.09.2026).
#
# Rohstoffe und Devisen (=F, =X) sind ausgenommen: sie handeln fast rund
# um die Uhr, ein Tageskalender passt nicht, und sie kommen fuer Block 1
# ohnehin nicht in Frage.

# Unplanmaessige Boersenschliessungen, die kein Regelkalender kennt.
# Fehlt ein solcher Tag hier, gilt er bei ALLEN Werten der Boerse als Loch
# - das faellt im Protokoll sofort auf ("offen" bei jedem Wert desselben
# Tages) und wird dann hier nachgetragen.
SONDERSCHLIESSTAGE: dict[str, set] = {
    "USA": {date(2025, 1, 9)},       # Staatstrauer Jimmy Carter
    "XETRA": set(),
    "Euronext": set(),
}

# Ab wann (UTC) ein Handelstag als abgeschlossen gilt - dieselben
# Schwellen wie unfertige_heutige_kerze_verwerfen() in kursverlauf.py.
SCHLUSS_UTC = {"XETRA": 17, "Euronext": 17, "USA": 21,
               # 03.10.2026 Heimatboersen (Stunde UTC, ab der der Tag sicher geschlossen ist)
               "LSE": 17, "SIX": 17, "BME": 17, "CPH": 17, "OSL": 17, "TSE": 8, "TWSE": 7, "HKEX": 9,
               "ASX": 7, "NSE": 11, "B3": 21, "KRX": 8}
# Kalender der Heimatboersen aus exchange_calendars (Feiertage je Boerse, auch Asien) - 03.10.2026
_XKAL = {}
_KAL_FEHLER: set = set()
XCAL = {"LSE": "XLON", "SIX": "XSWX", "BME": "XMAD", "CPH": "XCSE", "OSL": "XOSL", "TSE": "XTKS", "TWSE": "XTAI",
        "HKEX": "XHKG", "ASX": "XASX", "NSE": "XBOM", "B3": "BVMF", "KRX": "XKRX"}

# 03.10.2026: Schliesstage, die exchange_calendars (noch) nicht kennt - je Fall belegt.
# KRX 03.06.2026 Kommunalwahl, 17.07.2026 Verfassungstag (2026 wieder Feiertag); TWSE 10.07.2026 Taifun Bavi.
HEIMAT_SONDERSCHLUSS = {
    "KRX": {date(2026, 6, 3), date(2026, 7, 17)},
    "TWSE": {date(2026, 7, 10)},
}

STUNDEN_FUELLGRENZE_TAGE = 720
MIN_STUNDEN_JE_TAG = 5
# Obergrenze fuer Stundenabrufe je Prozess. Ein unbekannter Schliesstag
# wuerde sonst bei jedem US-Wert einen Abruf ausloesen und Yahoo bremsen.
MAX_FUELL_ANFRAGEN = 120
_FUELL_ANFRAGEN = 0

# Wie viele Handelstage zurueck ein Loch zur Kaufsperre fuehrt. 63 Tage
# sind drei Monate - derselbe Horizont wie die Halteraten, und weit genug,
# um jede laufende Korrektur samt ihrer Tiefs abzudecken.
PRUEF_TAGE = 63

_FUELLUNG: dict[tuple, dict] = {}
_ARCHIV: dict[str, "pd.DataFrame"] | None = None


def boerse(ticker: str) -> str | None:
    """Handelsplatz fuer den Kalender, None fuer Rohstoffe/Devisen."""
    if ticker.endswith("=F") or ticker.endswith("=X"):
        return None
    q = quelle(ticker)
    if q.endswith(".DE"):
        return "XETRA"
    if q.endswith(".AS") or q.endswith(".PA"):
        return "Euronext"
    if "." not in q:
        return "USA"
    # 03.10.2026: Heimatboersen, Kalender ueber exchange_calendars
    return {".L": "LSE", ".SW": "SIX", ".MC": "BME", ".CO": "CPH", ".OL": "OSL", ".T": "TSE", ".TW": "TWSE",
            ".HK": "HKEX", ".AX": "ASX", ".NS": "NSE", ".SA": "B3", ".KS": "KRX"}.get("." + q.rsplit(".", 1)[-1])


def _feiertage(b: str, jahr: int) -> set:
    ostern = easter(jahr)
    karfreitag = ostern - timedelta(days=2)
    ostermontag = ostern + timedelta(days=1)
    if b == "XETRA":
        return {date(jahr, 1, 1), karfreitag, ostermontag, date(jahr, 5, 1),
                date(jahr, 12, 24), date(jahr, 12, 25), date(jahr, 12, 26),
                date(jahr, 12, 31)}
    if b == "Euronext":
        # 24.12. und 31.12. sind in Amsterdam verkuerzte Handelstage, keine
        # Feiertage.
        return {date(jahr, 1, 1), karfreitag, ostermontag, date(jahr, 5, 1),
                date(jahr, 12, 25), date(jahr, 12, 26)}
    if b == "USA":
        def nter(monat, wochentag, n):
            d = date(jahr, monat, 1)
            d += timedelta(days=(wochentag - d.weekday()) % 7)
            return d + timedelta(days=7 * (n - 1))

        def letzter(monat, wochentag):
            d = (date(jahr, monat + 1, 1) - timedelta(days=1)) if monat < 12 else date(jahr, 12, 31)
            return d - timedelta(days=(d.weekday() - wochentag) % 7)

        def beobachtet(d):
            if d.weekday() == 5:
                return d - timedelta(days=1)
            if d.weekday() == 6:
                return d + timedelta(days=1)
            return d

        tage = {nter(1, 0, 3), nter(2, 0, 3), karfreitag, letzter(5, 0),
                nter(9, 0, 1), nter(11, 3, 4), beobachtet(date(jahr, 6, 19)),
                beobachtet(date(jahr, 7, 4)), beobachtet(date(jahr, 12, 25))}
        # Faellt Neujahr auf einen Samstag, schliesst die NYSE am Freitag
        # davor NICHT.
        if date(jahr, 1, 1).weekday() != 5:
            tage.add(beobachtet(date(jahr, 1, 1)))
        return tage
    return set()


def handelstage(b: str, von: date, bis: date) -> list[date]:
    """Alle regulaeren Handelstage eines Handelsplatzes von..bis."""
    if b in XCAL:   # 03.10.2026: Heimatboersen
        try:
            import exchange_calendars as xc
            schl = (XCAL[b], von.year)
            if schl not in _XKAL:
                _XKAL[schl] = xc.get_calendar(XCAL[b], start=pd.Timestamp(date(von.year, 1, 1)))
            kal = _XKAL[schl]
            s = kal.sessions_in_range(pd.Timestamp(von), pd.Timestamp(bis))
            zu = HEIMAT_SONDERSCHLUSS.get(b, set())
            return [d.date() for d in s if d.date() not in zu]
        except Exception as e:  # noqa: BLE001
            # 03.10.2026: OHNE Kalender keine Lueckenpruefung fuer diese Boerse (None) - Montag bis Freitag hatte die
            # Feiertage der Heimatboersen als "fehlend" gefuellt (mit Kursen der US-Notierung, Fund Shell 06.04.).
            global _KAL_FEHLER
            if b not in _KAL_FEHLER:
                print(f"  !!! KALENDER {b} NICHT VERFUEGBAR ({e!r}) - keine Lueckenpruefung fuer diese Boerse")
                _KAL_FEHLER.add(b)
            return None
    tage, feiertage, d = [], {}, von
    while d <= bis:
        if d.weekday() < 5:
            if d.year not in feiertage:
                feiertage[d.year] = _feiertage(b, d.year) | SONDERSCHLIESSTAGE.get(b, set())
            if d not in feiertage[d.year]:
                tage.append(d)
        d += timedelta(days=1)
    return tage


def letzter_fertiger_tag(b: str, jetzt: datetime | None = None) -> date:
    jetzt = jetzt or datetime.now(timezone.utc)
    return jetzt.date() if jetzt.hour >= SCHLUSS_UTC.get(b, 21) else jetzt.date() - timedelta(days=1)


def _fuell_pfad(holen: str, period: str, auto_adjust: bool) -> str:
    return _pfad(f"fuell_{holen}", period, auto_adjust)[:-4] + ".json"


def _archiv(ticker: str) -> "pd.DataFrame | None":
    """Kerzen dieses Wertes aus den zuletzt geschriebenen docs/kursverlauf*."""
    global _ARCHIV
    if _ARCHIV is None:
        _ARCHIV = {}
        docs = os.path.join(HIER, "docs")
        teile = {"Open": "kursverlauf_eroeffnung.csv", "High": "kursverlauf_hoch.csv",
                 "Low": "kursverlauf_tief.csv", "Close": "kursverlauf.csv",
                 "Volume": "kursverlauf_volumen.csv"}
        try:
            frames = {sp: pd.read_csv(os.path.join(docs, datei), index_col=0)
                      for sp, datei in teile.items()}
        except Exception as e:
            print(f"  Archiv docs/kursverlauf* nicht lesbar ({e}) - ohne Archiv weiter")
            return None
        for t in frames["Close"].index:
            teil = pd.DataFrame({sp: f.loc[t] if t in f.index else float("nan")
                                 for sp, f in frames.items()})
            teil.index = pd.to_datetime(teil.index)
            teil = teil.dropna(subset=["Open", "High", "Low", "Close"])
            teil = _platzhalter_weg(teil, letzte_behalten=False)   # 03.10.2026: Platzhalter nie als Fuellkerze nutzen
            _ARCHIV[t] = teil
    return _ARCHIV.get(ticker)


def _volumen_faktor(df: "pd.DataFrame | None", h: "pd.DataFrame | None") -> float:
    """09.10.2026: Verhaeltnis echtes Tagesvolumen / Summe der Stundenvolumen an Tagen, fuer die beides vorliegt
    (Median der letzten bis zu 10 Tage, mindestens 3). Ohne brauchbare Vergleichstage 1.0 (unveraendert)."""
    try:
        if df is None or h is None or "Volume" not in df.columns or "Volume" not in h.columns:
            return 1.0
        sh = h.groupby(h.index.date)["Volume"].agg(["sum", "count"])
        sh = sh[(sh["count"] >= MIN_STUNDEN_JE_TAG) & (sh["sum"] > 0)]
        dv = df["Volume"].copy(); dv.index = dv.index.date
        dv = dv[~dv.index.duplicated(keep="first")]
        gem = [d for d in sh.index if d in dv.index and dv[d] == dv[d] and dv[d] > 0]
        r = [float(dv[d]) / float(sh.loc[d, "sum"]) for d in gem[-10:]]
        if len(r) < 3:
            return 1.0
        f = float(statistics.median(r))
        return f if 0.8 <= f <= 6.0 else 1.0
    except Exception:  # noqa: BLE001
        return 1.0


def _loecher_fuellen(ticker: str, holen: str, df: "pd.DataFrame",
                     auto_adjust: bool) -> tuple["pd.DataFrame", dict]:
    """Fehlende Handelstage erkennen und fuellen. Liefert die ergaenzte
    Reihe und einen Bericht {"gefuellt": {tag: quelle}, "offen": [tage]}."""
    global _FUELL_ANFRAGEN
    b = boerse(ticker)
    if b is None or df is None or df.empty:
        return df, {}
    vorhanden = set(df.index.date)
    kal = handelstage(b, df.index[0].date(), letzter_fertiger_tag(b))
    if kal is None:   # 03.10.2026: Kalender fehlt - nichts fuellen statt falsch fuellen
        return df, {}
    fehlend = [d for d in kal if d not in vorhanden]
    if not fehlend:
        return df, {}

    gefuellt: dict[str, str] = {}
    neue = []

    def _zeile(d, o, h, l, c, v):
        z = pd.DataFrame({"Open": [o], "High": [h], "Low": [l], "Close": [c],
                          "Volume": [v]}, index=[pd.Timestamp(d)])
        for sp in ("Dividends", "Stock Splits"):
            if sp in df.columns:
                z[sp] = 0.0
        return z

    # b) Archiv - nur fuer die unbereinigte Reihe, das Archiv ist unbereinigt.
    if not auto_adjust and not _ohne_rueckfall(ticker):   # 03.10.2026: Archiv kann US-Kurse enthalten - Heimatwerte nur aus Stunden
        arch = _archiv(ticker)
        if arch is not None:
            for d in fehlend:
                ts = pd.Timestamp(d)
                if ts in arch.index:
                    r = arch.loc[ts]
                    neue.append(_zeile(d, r.Open, r.High, r.Low, r.Close, r.Volume))
                    gefuellt[str(d)] = "archiv"

    # c) Stundenkerzen
    rest = [d for d in fehlend if str(d) not in gefuellt
            and d >= date.today() - timedelta(days=STUNDEN_FUELLGRENZE_TAGE)]
    if rest and _FUELL_ANFRAGEN < MAX_FUELL_ANFRAGEN:
        _FUELL_ANFRAGEN += 1
        try:
            # 09.10.2026 (Peter, Fund Infineon 08.10.: Stunden 1,36 Mio. gegen 2,70 Mio. laut stock3): Stundenkerzen enthalten
            # die Schlussauktion und Teile des Handels nicht - die Summe lag bei Heimatwerten bei 35-55 % des Tagesvolumens.
            # Deshalb 20 Kalendertage frueher abrufen und das Volumen mit dem wertspezifischen Verhaeltnis Tag/Stundensumme
            # der Vortage (Median, mindestens 3 Tage) hochrechnen. Kurse bleiben unveraendert; der naechste Lauf mit echter
            # Tageskerze ersetzt die Fuellkerze wie bisher.
            roh = yf.Ticker(holen).history(start=min(rest) - timedelta(days=20), end=max(rest) + timedelta(days=1),
                                           interval="1h", auto_adjust=auto_adjust)
            h = _skalieren(_aufbereiten_stunden(roh), ticker)
        except Exception as e:
            print(f"  {holen}: Stundenabruf zum Fuellen fehlgeschlagen ({e})")
            h = None
        vfak = _volumen_faktor(df, h)
        if h is not None:
            for d in rest:
                tag = h[h.index.date == d]
                if len(tag) >= MIN_STUNDEN_JE_TAG:
                    vol = float(tag["Volume"].sum()) * vfak if "Volume" in tag.columns else float("nan")
                    neue.append(_zeile(d, float(tag["Open"].iloc[0]), float(tag["High"].max()),
                                       float(tag["Low"].min()), float(tag["Close"].iloc[-1]), vol))
                    gefuellt[str(d)] = "stunden"
    elif rest:
        print(f"  {holen}: Obergrenze {MAX_FUELL_ANFRAGEN} Stundenabrufe erreicht - "
              f"{len(rest)} Tage bleiben offen")

    if neue:
        df = pd.concat([df] + neue).sort_index()
        df = df[~df.index.duplicated(keep="first")]
    offen = [str(d) for d in fehlend if str(d) not in gefuellt]
    if gefuellt:
        print(f"  {ticker}: {len(gefuellt)} fehlende Tage gefuellt - "
              + ", ".join(f"{t} ({q})" for t, q in sorted(gefuellt.items())))
    if offen:
        print(f"  {ticker}: {len(offen)} Tage weiterhin OFFEN - " + ", ".join(offen[-10:]))
    return df, {"gefuellt": gefuellt, "offen": offen}


def fuellbericht(ticker: str, period: str = "400d", auto_adjust: bool = False) -> dict:
    """Bericht zur Lueckenfuellung aus dem letzten kerzen()-Aufruf - auch
    wenn der in einem frueheren Workflow-Schritt (anderer Prozess) lief."""
    key = (ticker, period, auto_adjust)
    if key in _FUELLUNG:
        return _FUELLUNG[key]
    pfad = _fuell_pfad(quelle(ticker), period, auto_adjust)
    try:
        with open(pfad, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def fehlende_tage(ticker: str, vorhandene_tage, pruef_tage: int = PRUEF_TAGE,
                  jetzt: datetime | None = None) -> list[str]:
    """Regulaere Handelstage der letzten pruef_tage, die in
    vorhandene_tage fehlen - bis einschliesslich zum letzten
    abgeschlossenen Handelstag. Grundlage der harten Kaufsperre."""
    b = boerse(ticker)
    if b is None:
        return []
    bis = letzter_fertiger_tag(b, jetzt)
    kalender = handelstage(b, bis - timedelta(days=int(pruef_tage * 1.6) + 10), bis)
    if kalender is None:   # 03.10.2026: ohne Kalender keine Aussage
        return []
    kalender = kalender[-pruef_tage:]
    da = {d if isinstance(d, date) else pd.Timestamp(d).date() for d in vorhandene_tage}
    if not da:
        return [str(d) for d in kalender]
    # Tage VOR der ersten Kerze sind kein Loch, sondern ein Wert, der
    # damals noch nicht notierte (z. B. HONA nach der Abspaltung).
    erster = min(da)
    return [str(d) for d in kalender if d >= erster and d not in da]


def wochenkontrolle(ticker: str, tag: date, tagestiefs: dict) -> str:
    """Kontrolle ueber die Wochenkerze fuer einen fehlenden Tag.

    Liegt das Wochentief unter allen bekannten Tagestiefs derselben Woche,
    muss der fehlende Tag das tiefere Tief gemacht haben. Einschraenkung:
    Die Wochenkerze kommt von derselben Quelle. Fehlt der Tag dort
    ebenfalls, sagt ein gleiches Tief nichts - deshalb "kein Hinweis",
    nie "sicher kein neues Tief".
    """
    montag = tag - timedelta(days=tag.weekday())
    try:
        w = yf.Ticker(quelle(ticker)).history(start=montag, end=montag + timedelta(days=7),
                                              interval="1wk")
    except Exception as e:
        return f"Wochenkerze nicht abrufbar ({e})"
    if w is None or w.empty:
        return "Wochenkerze nicht verfuegbar"
    wtief = float(w["Low"].min()) * faktor(ticker)
    bekannt = [v for d, v in tagestiefs.items()
               if montag <= pd.Timestamp(d).date() < montag + timedelta(days=5)
               and v is not None and v == v]
    if not bekannt:
        return f"Wochentief {wtief:.2f}, keine Tagestiefs der Woche bekannt"
    btief = min(bekannt)
    if wtief < btief * 0.999:
        return (f"Wochentief {wtief:.2f} liegt UNTER allen bekannten Tagestiefs "
                f"({btief:.2f}) - der fehlende Tag hatte ein tieferes Tief")
    return (f"Wochentief {wtief:.2f} = bekanntes Tief - kein Hinweis auf ein "
            f"tieferes Tief am fehlenden Tag (Kontrolle aus derselben Quelle)")
