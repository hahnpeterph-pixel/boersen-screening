"""lauf20.py - TESTLAUF 20 Jahre (Peter 27.09.2026: "erst mal testen").

Startet ein bestehendes Skript unveraendert, biegt aber jede Kursabfrage mit Zeitraum "Ny"
(z. B. "7y", "20y") auf 20 Jahre um: Abruf mit "max", danach auf die letzten 20 Jahre gekuerzt.
Nur fuer den Test-Workflow test20.yml - das taegliche Screening nutzt diese Datei nicht.
Aufruf: python lauf20.py SKRIPT.py [Argumente ...]
"""
import re, runpy, sys
import pandas as pd
import kurse

JAHRE = 20
_kb, _k = kurse.kerzen_batch, kurse.kerzen


def _kurz(df):
    if df is None or len(df) == 0:
        return df
    ab = pd.Timestamp.today().normalize() - pd.DateOffset(years=JAHRE)
    idx = df.index.tz_localize(None) if getattr(df.index, "tz", None) else df.index
    return df[idx >= ab]


def kerzen_batch(tickers, period="400d", auto_adjust=False):
    if re.fullmatch(r"\d+y", str(period)):
        return {t: _kurz(d) for t, d in _kb(tickers, period="max", auto_adjust=auto_adjust).items()}
    return _kb(tickers, period=period, auto_adjust=auto_adjust)


def kerzen(ticker, period="400d", auto_adjust=False):
    if re.fullmatch(r"\d+y", str(period)):
        return _kurz(_k(ticker, period="max", auto_adjust=auto_adjust))
    return _k(ticker, period=period, auto_adjust=auto_adjust)


kurse.kerzen_batch, kurse.kerzen = kerzen_batch, kerzen
skript = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(skript, run_name="__main__")
