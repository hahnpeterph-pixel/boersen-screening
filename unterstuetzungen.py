"""
unterstuetzungen.py - Unterstuetzungen unter dem Kurs, zwei Sorten.
Angelegt 20.09.2026.

1. VOLUMENSPITZEN aus Stundenkerzen (1 Jahr).
   Peter: "wenn er eine Volumenspitze unterschritten hat, kommt darunter
   irgendwann noch eine - das waere die naechste Unterstuetzung".
   Die erste Fassung (marktdaten.py, Tageskerzen) war unbrauchbar: das
   Volumen eines ganzen Tages ueber die Tagesspanne verteilt verschmiert
   scharfe Spitzen zu breiten Huegeln, kleinere Spitzen gingen neben der
   groessten unter (GE Aerospace: Sockel 287 fehlte, Sherwin-Williams:
   ganzer Handelsbereich 303-320 fehlte). Stundenkerzen sind rund
   sieben Mal feiner und liefern Spitzen wie ein Chartprogramm.

2. CHART-TIEFS aus Wochenkerzen (5 Jahre).
   Umkehrtiefs, wie Peter sie als Linie zieht (Costco 845, Sherwin-
   Williams 290). Dort wird kaum gehandelt - ein Volumenprofil zeigt sie
   deshalb gerade NICHT. Gezaehlt nach derselben Umkehr-Regel wie die
   Tagestiefs (tiefs_regel.pivots), nur auf Wochenkerzen. Tiefs, die
   naeher als 1 ATR beieinander liegen, sind eine Linie; die Zahl der
   Beruehrungen steht dabei.

Ausgabe: docs/unterstuetzungen.csv
  ticker, vp_poc, vp_spitzen ("preis:staerke;..."), chart_tiefs
  ("preis:beruehrungen:juengstes_datum;...")
heute.py liest die Datei; fehlt sie, bleibt die Zeile leer.

Laeuft im Screening nach marktdaten.py mit continue-on-error: ein
Yahoo-Aussetzer bei Stundenkerzen darf den Tagesbericht nicht gefaehrden.
"""
from __future__ import annotations

import csv
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yfinance as yf

import tiefs_regel as regel

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
AUS = os.path.join(DOCS, "unterstuetzungen.csv")

VP_PERIODE = "1y"
VP_BIN_ATR = 0.25      # Preisstufe in ATR - fein genug fuer Stundenkerzen
VP_SPITZE_MIN = 0.20   # Spitze zaehlt ab 20 % der groessten
VP_ABSTAND_ATR = 1.0   # Spitzen enger als 1 ATR = eine (die staerkere bleibt)
CT_PERIODE = "5y"
CT_ABSTAND_ATR = 1.0   # Wochentiefs enger als 1 ATR = eine Linie
BATCH = 40


def _laden(tickers, period, interval):
    """Batch-Download, Rueckgabe {ticker: DataFrame}. Fehlende Werte fehlen."""
    aus = {}
    for i in range(0, len(tickers), BATCH):
        teil = tickers[i:i + BATCH]
        try:
            d = yf.download(teil, period=period, interval=interval,
                            auto_adjust=False, group_by="ticker",
                            threads=True, progress=False)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! Abruf {interval} {teil[0]}..: {exc}")
            continue
        for t in teil:
            try:
                x = d[t] if isinstance(d.columns, pd.MultiIndex) else d
            except KeyError:
                continue
            x = x.dropna(subset=["High", "Low"])
            if len(x):
                aus[t] = x
    return aus


def volumenspitzen(df: pd.DataFrame, atr: float) -> tuple:
    """Volumenprofil aus Stundenkerzen. Rueckgabe (poc, [(preis, staerke%)])."""
    if df is None or atr in (None, 0) or "Volume" not in df.columns:
        return None, []
    d = df[(df["Volume"] > 0)]
    if len(d) < 200:
        return None, []
    unten, oben = float(d["Low"].min()), float(d["High"].max())
    breite = max(VP_BIN_ATR * atr, (oben - unten) / 600)
    n = int(np.ceil((oben - unten) / breite)) + 1
    grenzen = unten + breite * np.arange(n + 1)
    vol = np.zeros(n)
    for lo, hi, v in zip(d["Low"].values, d["High"].values, d["Volume"].values):
        i0 = int((lo - unten) / breite)
        i1 = min(int((hi - unten) / breite), n - 1)
        if hi <= lo or i0 == i1:
            vol[i0] += v
            continue
        for i in range(i0, i1 + 1):
            anteil = (min(hi, grenzen[i + 1]) - max(lo, grenzen[i])) / (hi - lo)
            if anteil > 0:
                vol[i] += v * anteil
    glatt = np.convolve(vol, np.ones(3) / 3, mode="same")
    mitte = grenzen[:-1] + breite / 2
    spitze = glatt.max()
    if spitze <= 0:
        return None, []
    kand = [i for i in range(n)
            if glatt[i] >= VP_SPITZE_MIN * spitze
            and glatt[i] >= (glatt[i - 1] if i > 0 else -1)
            and glatt[i] > (glatt[i + 1] if i < n - 1 else -1)]
    gew = []
    for i in sorted(kand, key=lambda k: -glatt[k]):
        if all(abs(mitte[i] - mitte[j]) >= VP_ABSTAND_ATR * atr for j in gew):
            gew.append(i)
    gew.sort()
    poc = float(mitte[int(np.argmax(glatt))])
    return poc, [(float(mitte[i]), int(round(100 * glatt[i] / spitze))) for i in gew]


def chart_tiefs(df: pd.DataFrame, atr: float) -> list:
    """Umkehrtiefs auf Wochenkerzen. Rueckgabe [(preis, beruehrungen, datum)]."""
    if df is None or atr in (None, 0) or len(df) < 60:
        return []
    w = df.resample("W-FRI").agg({"Open": "first", "High": "max",
                                  "Low": "min", "Close": "last"}).dropna()
    if len(w) < 10:
        return []
    tiefs = [(float(w["Low"].iloc[i]), w.index[i])
             for art, i in regel.pivots(w) if art == "tief"]
    tiefs.sort(key=lambda x: x[0])
    linien = []            # [preis_min, anzahl, juengstes_datum]
    for preis, datum in tiefs:
        if linien and preis - linien[-1][0] < CT_ABSTAND_ATR * atr:
            linien[-1][1] += 1
            linien[-1][2] = max(linien[-1][2], datum)
        else:
            linien.append([preis, 1, datum])
    return [(p, n, d) for p, n, d in linien]


def main() -> int:
    m = pd.read_csv(os.path.join(DOCS, "marktdaten.csv"))
    m = m[m["art"] == "Aktie"] if "art" in m.columns else m
    tickers = [t for t in m["ticker"] if isinstance(t, str)]
    atr = dict(zip(m["ticker"], m["atr14"]))
    print(f"Unterstuetzungen fuer {len(tickers)} Werte ...")
    stunden = _laden(tickers, VP_PERIODE, "1h")
    print(f"  Stundenkerzen: {len(stunden)} Werte")
    tage = _laden(tickers, CT_PERIODE, "1d")
    print(f"  Tageskerzen 5 Jahre: {len(tage)} Werte")
    zeilen = []
    for t in tickers:
        a = atr.get(t)
        poc, sp = volumenspitzen(stunden.get(t), a)
        ct = chart_tiefs(tage.get(t), a)
        zeilen.append({
            "ticker": t,
            "vp_poc": round(poc, 2) if poc is not None else "",
            "vp_spitzen": ";".join(f"{p:.2f}:{s}" for p, s in sp),
            "chart_tiefs": ";".join(f"{p:.2f}:{n}:{d:%Y-%m-%d}" for p, n, d in ct),
        })
    os.makedirs(DOCS, exist_ok=True)
    with open(AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "vp_poc", "vp_spitzen", "chart_tiefs"])
        w.writeheader()
        w.writerows(zeilen)
    leer_vp = sum(1 for z in zeilen if not z["vp_spitzen"])
    leer_ct = sum(1 for z in zeilen if not z["chart_tiefs"])
    print(f"Geschrieben: {AUS} ({len(zeilen)} Werte, ohne Volumenspitzen {leer_vp}, "
          f"ohne Chart-Tiefs {leer_ct}) - {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC")
    return 0


if __name__ == "__main__":
    sys.exit(main())
