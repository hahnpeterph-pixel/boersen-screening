"""Indizes und Index-Abhaengigkeit je Wert (Peter 26.09.2026).

Laeuft taeglich im Screening (Schritt "Indizes ausfuehren") und woechentlich
im Workflow Stimmung-Auswertung. Kein Kaufwert, nur Einordnung.

1. Holt S&P 500, Nasdaq 100, Dow Jones und DAX (Yahoo, 7 Jahre Schlusskurse)
   nach docs/indizes.csv und schreibt eine Kurzzeile nach docs/indizes.md.
2. Rechnet je Wert aus docs/markthistorie.csv.gz gegen seinen Heimatindex
   (US-Werte: S&P 500, .DE-Werte: DAX):
   - korr_125 / beta_125: Gleichlauf und Mitnahme der letzten 125 Handelstage
     (gleiches Fenster wie die Zeile "Abhaengigkeit" der Kaufvorlage)
   - beta_250: dasselbe ueber 250 Tage
   - beta_abwaerts: Mitnahme nur an Tagen, an denen der Index faellt
     (250 Tage) - fuer Einbrueche die ehrlichere Zahl
   - einbruch_faktor: Wie stark fiel der Wert im Median, wenn der Index in
     20 Handelstagen mindestens 8 % verlor (alle Faelle seit 2019, je Wert).
     Faelle = Anzahl solcher 20-Tage-Fenster (ueberlappend, grobe Groesse).
   Ergebnis: docs/index_beta.csv. Positionsdaten bleiben lokal (E58) -
   der Stresstest fuers Depot rechnet Claude mit dem Orderbuch.
"""
from __future__ import annotations

import datetime as dt
import gzip
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf

DOCS = "docs"
INDIZES = {"^GSPC": "S&P 500", "^NDX": "Nasdaq 100", "^DJI": "Dow Jones", "^GDAXI": "DAX"}
HEIMAT_US, HEIMAT_DE = "^GSPC", "^GDAXI"
START = "2011-01-01"  # seit 26.09.2026 ab 2011 (vorher 2019)


def de(x, n=1):
    return "–" if x is None or pd.isna(x) else f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hole() -> pd.DataFrame:
    pfad = os.path.join(DOCS, "indizes.csv")
    alt = pd.read_csv(pfad, index_col=0, parse_dates=True) if os.path.exists(pfad) else None
    reihen = {}
    for t in INDIZES:
        try:
            roh = yf.Ticker(t).history(start=START, interval="1d", auto_adjust=False)
            s = roh["Close"].dropna()
            s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
            reihen[t] = s[~s.index.duplicated(keep="last")]
            print(f"  {t}: {len(s)} Tage bis {s.index[-1].date()}")
        except Exception as e:  # noqa: BLE001
            print(f"  {t}: Abruf fehlgeschlagen ({e})")
    df = pd.DataFrame(reihen)
    if alt is not None:
        df = df.combine_first(alt)
    df.index.name = "datum"
    df.sort_index().to_csv(pfad, float_format="%.2f")
    return df.sort_index()


def kurzzeile(df: pd.DataFrame) -> str:
    teile = []
    for t, name in INDIZES.items():
        s = df[t].dropna() if t in df else pd.Series(dtype=float)
        if len(s) < 21:
            continue
        hoch = s.iloc[-250:].max()
        teile.append(f"{name} {de(s.iloc[-1], 0)} ({'+' if s.iloc[-1] >= s.iloc[-6] else ''}{de((s.iloc[-1]/s.iloc[-6]-1)*100)} % 5T, "
                     f"{de((s.iloc[-1]/hoch-1)*100)} % vom Jahreshoch)")
    return " · ".join(teile)


def beta(r, m):
    ok = r.notna() & m.notna()
    r, m = r[ok], m[ok]
    if len(r) < 60 or m.var() == 0:
        return np.nan, np.nan
    return float(np.corrcoef(r, m)[0, 1]), float(np.cov(r, m)[0, 1] / m.var())


def abhaengigkeit(idx: pd.DataFrame) -> pd.DataFrame:
    mh = pd.read_csv(gzip.open(os.path.join(DOCS, "markthistorie.csv.gz"))).set_index("ticker")
    mh.columns = pd.to_datetime(mh.columns)
    zeilen = []
    for t, z in mh.iterrows():
        if any(c in t for c in "=^"):
            continue
        heimat = HEIMAT_DE if t.endswith(".DE") else HEIMAT_US
        if heimat not in idx:
            continue
        s = z.dropna().astype(float)
        i = idx[heimat].dropna()
        gem = s.index.intersection(i.index)
        s, i = s.loc[gem], i.loc[gem]
        if len(s) < 260:
            continue
        rs, ri = np.log(s).diff(), np.log(i).diff()
        k125, b125 = beta(rs.iloc[-125:], ri.iloc[-125:])
        _, b250 = beta(rs.iloc[-250:], ri.iloc[-250:])
        ab = ri.iloc[-250:] < 0
        _, bab = beta(rs.iloc[-250:][ab], ri.iloc[-250:][ab])
        # Einbrueche: 20-Tage-Fenster mit Index <= -8 %
        i20 = i.pct_change(20)
        s20 = s.pct_change(20)
        fall = i20 <= -0.08
        faktor = float(np.median(s20[fall] / i20[fall])) if fall.sum() >= 5 else np.nan
        zeilen.append({"ticker": t, "index": INDIZES[heimat], "korr_125": round(k125, 2),
                       "beta_125": round(b125, 2), "beta_250": round(b250, 2),
                       "beta_abwaerts": round(bab, 2), "einbruch_faktor": round(faktor, 2),
                       "einbruch_faelle": int(fall.sum())})
    return pd.DataFrame(zeilen).sort_values("ticker")


def main() -> int:
    idx = hole()
    zeile = kurzzeile(idx)
    ab = abhaengigkeit(idx)
    ab.to_csv(os.path.join(DOCS, "index_beta.csv"), index=False)
    md = ["# Indizes", "", f"Stand Abruf: {dt.datetime.utcnow():%d.%m.%Y %H:%M} UTC", "", f"**Indizes:** {zeile}", "",
          "## Index-Abhaengigkeit je Wert (docs/index_beta.csv)", "",
          "Beta = um wie viel Prozent der Wert im Schnitt mitgeht, wenn sein Index 1 % bewegt "
          "(US-Werte gegen S&P 500, deutsche gegen DAX). Einbruch-Faktor = Median des Wertverlusts "
          "geteilt durch den Indexverlust in 20-Tage-Fenstern mit mindestens 8 % Indexminus seit 2019.", ""]
    for name in ("S&P 500", "DAX"):
        t = ab[ab["index"] == name]
        if t.empty:
            continue
        md += [f"**{name}:** {len(t)} Werte · Median Beta (250 T) {de(t.beta_250.median(), 2)} · "
               f"abwaerts {de(t.beta_abwaerts.median(), 2)} · Einbruch-Faktor {de(t.einbruch_faktor.median(), 2)} · "
               f"Gleichlauf (125 T) {de(t.korr_125.median(), 2)}", ""]
    with open(os.path.join(DOCS, "indizes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(zeile)
    print(f"index_beta.csv: {len(ab)} Werte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
