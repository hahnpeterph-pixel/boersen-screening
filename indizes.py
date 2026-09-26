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


# ── Marktlage mit 40-Tage-Blick und Warnfeldern (Peter 26.09.2026) ──────
# Test 26.09.2026 (S&P 500, 2011-2026, getrennt 2011-18 / 2019-26 bestaetigt):
# 40 Handelstage Rueckblick sagen am meisten ueber Einbrueche >= 10 % in den
# naechsten 63 Tagen: Index unterstes Fuenftel 22 % gegen 9 %, VIX oberstes
# Fuenftel 16 % gegen 8 %, Fear & Greed unterstes Fuenftel 16 % gegen 8 %.
# Warnfelder: VIX ruhig (< 16) + F&G < 25 -> 43 % Einbrueche >= 10 %;
# VIX normal (16-22) + F&G < 25 -> 29 %. Durchschnitt aller Tage 12 %.
BLICK = 40
SATZ = ""


def marktlage(idx: pd.DataFrame) -> tuple[str, list[str]]:
    st = pd.read_csv(os.path.join(DOCS, "stimmung.csv"), parse_dates=["datum"]).set_index("datum")
    sp = idx["^GSPC"].dropna()
    d = pd.DataFrame({"k": sp})
    d["v"] = st["vix"].reindex(d.index).ffill()
    d["fg"] = st["fg"].reindex(d.index).ffill()
    reihen = {"S&P": (d.k / d.k.shift(BLICK) - 1) * 100, "VIX": d.v - d.v.shift(BLICK), "F&G": d.fg - d.fg.shift(BLICK)}
    teile, fuenftel = [], {}
    for name, x in reihen.items():
        x = x.dropna()
        grenzen = x.quantile([0.2, 0.4, 0.6, 0.8]).to_numpy()
        heute = x.iloc[-1]
        q = int((heute > grenzen).sum()) + 1
        fuenftel[name] = q
        wert = f"{'+' if heute >= 0 else ''}{de(heute)}{' %' if name == 'S&P' else ''}"
        teile.append(f"{name} {wert} ({q}/5)")
    v, fg = d.v.dropna().iloc[-1], d.fg.dropna().iloc[-1]
    # Einbruch >= 4 % in den naechsten 10 Handelstagen (Peter 26.09.2026):
    # Anteil der frueheren Tage mit gleicher VIX- und F&G-Lage.
    c = d.k.to_numpy()
    tief = np.full(len(c), np.nan)
    for i in range(len(c) - 10):
        tief[i] = c[i + 1:i + 11].min() / c[i] - 1
    d["tief10"] = tief
    vl = lambda x: 0 if x < 16 else (1 if x < 22 else 2)
    fl = lambda x: 0 if x < 25 else (1 if x < 45 else (2 if x < 55 else (3 if x < 75 else 4)))
    e = d.dropna(subset=["tief10", "v", "fg"])
    gleich = e[(e.v.map(vl) == vl(v)) & (e.fg.map(fl) == fl(fg))]
    p4 = (gleich.tief10 <= -0.04).mean() * 100 if len(gleich) >= 30 else np.nan
    schnitt = (e.tief10 <= -0.04).mean() * 100
    vtext = ["ruhig", "normal", "unruhig"][vl(v)]
    ftext = ["extreme Angst", "Angst", "neutral", "Gier", "extreme Gier"][fl(fg)]
    global SATZ
    # Einstufung (Peter 26.09.2026, Variante 1): niedrig < 2/3 des Schnitts,
    # erhoeht > 1,5-fach, sonst normal.
    stufe = ("–" if np.isnan(p4) else "niedrig" if p4 < schnitt * 2 / 3
             else "erhöht" if p4 > schnitt * 1.5 else "normal")
    SATZ = (f"VIX {de(v)} {vtext} · Fear & Greed {de(fg, 0)} {ftext} – Risiko für einen Rückgang um 4 % "
            f"in den nächsten 2 Wochen: **{stufe} ({de(p4, 0)} von 100, sonst {de(schnitt, 0)})**")
    alarme = []
    if fg < 25 and v < 16:
        alarme.append(f"Warnfeld VIX ruhig + Fear & Greed extreme Angst (VIX {de(v)}, F&G {de(fg, 0)}): früher 43 % Einbrüche ≥ 10 % in 63 Tagen")
    elif fg < 25 and v < 22:
        alarme.append(f"Warnfeld VIX normal + Fear & Greed extreme Angst (VIX {de(v)}, F&G {de(fg, 0)}): früher 29 % Einbrüche ≥ 10 % in 63 Tagen")
    if fuenftel["S&P"] == 1:
        alarme.append("S&P 500 über 40 Tage im untersten Fünftel: früher 22 % Einbrüche ≥ 10 % (Schnitt 12 %)")
    if fuenftel["VIX"] == 5:
        alarme.append("VIX über 40 Tage im obersten Fünftel: früher 16 % Einbrüche ≥ 10 % (Schnitt 12 %)")
    if fuenftel["F&G"] == 1:
        alarme.append("Fear & Greed über 40 Tage im untersten Fünftel: früher 16 % Einbrüche ≥ 10 % (Schnitt 12 %)")
    return "40 T: " + " · ".join(teile), alarme


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
    try:
        blick, alarme = marktlage(idx)
    except Exception as e:  # noqa: BLE001
        blick, alarme = f"40 T: nicht berechenbar ({e})", []
    md[4:4] = [f"**Marktlage S&P 500:** {SATZ}", "", "**Marktlage-Alarm:** " + ("; ".join(alarme) if alarme else "keiner"), "",
               f"(intern, nur für die Alarme: {blick}; Fünftel 1 = stärkster Rückgang, 5 = stärkster Anstieg seit 2011)", ""]
    print(blick, alarme)
    with open(os.path.join(DOCS, "indizes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(zeile)
    print(f"index_beta.csv: {len(ab)} Werte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
