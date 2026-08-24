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
import shutil
from datetime import date

import pandas as pd
import yfinance as yf

HIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HIER, ".kurse_cache")

# Version im Dateinamen: aendert sich das Format oder die Aufbereitung,
# darf ein alter Cache nicht stillschweigend weiterbenutzt werden. Genau
# dieser Fehler ist beim Fundamentaldaten-Cache schon einmal passiert.
CACHE_VERSION = 1

MINDESTKERZEN = 30

_MEM: dict[tuple, pd.DataFrame] = {}


def _pfad(ticker: str, period: str) -> str:
    sicher = "".join(c if c.isalnum() or c in "-_" else "_" for c in ticker)
    return os.path.join(CACHE, f"v{CACHE_VERSION}_{sicher}_{period}.csv")


def aufraeumen() -> None:
    """Cache-Dateien von frueheren Tagen oder Versionen entfernen."""
    if not os.path.isdir(CACHE):
        return
    heute = date.today().isoformat()
    for name in os.listdir(CACHE):
        pfad = os.path.join(CACHE, name)
        try:
            alt = date.fromtimestamp(os.path.getmtime(pfad)).isoformat()
            if alt != heute or not name.startswith(f"v{CACHE_VERSION}_"):
                os.remove(pfad)
        except OSError:
            pass


def leeren() -> None:
    """Cache vollstaendig verwerfen - fuer Tests."""
    _MEM.clear()
    shutil.rmtree(CACHE, ignore_errors=True)


def _aufbereiten(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < MINDESTKERZEN:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def kerzen(ticker: str, period: str = "400d") -> pd.DataFrame | None:
    """Tageskerzen fuer einen Ticker. None, wenn keine brauchbaren Daten.

    Reihenfolge: Arbeitsspeicher, dann Tagescache auf der Platte, dann
    Yahoo. Ein Fehlschlag wird als None gemerkt, damit ein toter Ticker
    nicht bei jedem Aufruf erneut abgefragt wird.
    """
    key = (ticker, period)
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    pfad = _pfad(ticker, period)
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {ticker}: Cache unlesbar ({e}), hole neu")

    try:
        roh = yf.Ticker(ticker).history(period=period, interval="1d",
                                        auto_adjust=False)
    except Exception as e:
        print(f"  {ticker}: Abruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _aufbereiten(roh)
    _MEM[key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {ticker}: Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()
