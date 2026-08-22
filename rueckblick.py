#!/usr/bin/env python3
"""
Rueckblick — haetten die abgeschlossenen Trades nach den heutigen Regeln
gekauft werden duerfen?

Rekonstruiert fuer jeden Kauf den Stand AM KAUFTAG, mit ausschliesslich
Daten, die zu diesem Zeitpunkt vorlagen. Kein Blick in die Zukunft.

Geprueft wird, was sich aus Kursdaten rekonstruieren laesst:

  - Tief 1 nach der Umkehr-Regel, Datum und Bestaetigung
  - Abstand des Einstiegs zum Bezugstief in ATR
  - Laufende Tiefserie: das wievielte absteigende Tief war es
  - Laufende Korrektur ab dem letzten bestaetigten Hoch, in ATR und Tagen
  - Bodenbildung: Falltiefe, Tiefabstand, Volumendruck
  - RSI(14)
  - Die Sollwerte dieses Wertes, gerechnet NUR aus der Zeit VOR dem Kauf

Nicht rekonstruierbar sind Analystenurteil und Kursziel - beides liegt
historisch nicht vor. Der Score hier ist deshalb ein TECHNISCHER Score von
maximal 70 Punkten (Bodenbildung 30, RSI 20 bzw. 10, Einstieg nah am Tief
15, Tief bestaetigt 5) und nicht mit den 100 Punkten der Empfehlungsliste
vergleichbar.

Zehn Trades sind eine sehr kleine Stichprobe. Das Ergebnis zeigt Muster,
es beweist nichts.

Ausgabe: docs/rueckblick.md

Aufruf:  python3 rueckblick.py

KEINE Anlageberatung.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
AUSGABE = DOCS / "rueckblick.md"

ATR_TAGE = 14
FENSTER_TAGE = 90

# name, ticker, kaufdatum, verkaufsdatum, ergebnis in Prozent (aus dem Orderbuch)
TRADES = [
    ("Microsoft",         "MSFT",     "2026-07-22", "2026-08-10", 160.8),
    ("Oracle",            "ORCL",     "2026-07-21", "2026-08-10",  30.0),
    ("NVIDIA",            "NVDA",     "2026-08-03", "2026-08-21",   None),
    ("Rheinmetall",       "RHM.DE",   "2026-08-11", "2026-08-17",   None),
    ("Gold",              "GC=F",     "2026-08-14", "2026-08-20",  75.7),
    ("ASML",              "ASML",     "2026-08-20", "2026-08-21", -17.6),
    ("Applied Materials", "AMAT",     "2026-08-20", "2026-08-21", -12.2),
    ("Take-Two",          "TTWO",     "2026-08-20", "2026-08-21",  55.9),
    ("Micron",            "MU",       "2026-08-20", "2026-08-21",   4.6),
    ("Gold II",           "GC=F",     "2026-08-21", "2026-08-21",  12.0),
]


def atr_reihe(df: pd.DataFrame, tage: int = ATR_TAGE) -> pd.Series:
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vor = schluss.shift(1)
    spanne = pd.concat([hoch - tief, (hoch - vor).abs(), (tief - vor).abs()], axis=1).max(axis=1)
    return spanne.ewm(alpha=1 / tage, adjust=False).mean()


def rsi_reihe(df: pd.DataFrame, tage: int = 14) -> pd.Series:
    d = df["Close"].diff()
    g = d.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    v = (-d.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    return 100 - 100 / (1 + g / v.replace(0, np.nan))


def pivots(df: pd.DataFrame) -> tuple[list[int], list[int]]:
    """Tiefs und Hochs nach der Umkehr-Regel, identisch zu marktdaten.py."""
    hoch, tief = df["High"].values, df["Low"].values
    tiefs, hochs = [], []
    richtung, kandidat, gipfel = "ab", 0, 0
    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i
            elif hoch[i] > hoch[kandidat]:
                tiefs.append(kandidat)
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i
            elif tief[i] < tief[gipfel]:
                hochs.append(gipfel)
                richtung, kandidat = "ab", i
    if richtung == "ab" and kandidat not in tiefs:
        tiefs.append(kandidat)
    return tiefs, hochs


def soll_werte(df: pd.DataFrame) -> dict:
    """Median-Kennzahlen dieses Wertes, gerechnet nur auf den uebergebenen
    Daten - beim Aufruf enthalten sie nur die Zeit vor dem Kauf."""
    tiefs, hochs = pivots(df)
    a = atr_reihe(df).values
    tief = df["Low"].values
    hoch = df["High"].values
    if len(tiefs) < 4:
        return {}

    anzahl, tiefen = [], []
    k = 0
    while k < len(tiefs) - 1:
        start = k
        while k < len(tiefs) - 1 and tief[tiefs[k + 1]] < tief[tiefs[k]]:
            k += 1
        anzahl.append(k - start + 1)
        vor = [i for i in hochs if i < tiefs[start]]
        if vor and np.isfinite(a[tiefs[k]]) and a[tiefs[k]] > 0:
            tiefen.append((hoch[vor[-1]] - tief[tiefs[k]]) / a[tiefs[k]])
        k += 1
    return {"tiefs_soll": float(np.median(anzahl)) if anzahl else None,
            "korr_soll": float(np.median(tiefen)) if tiefen else None}


def stand_am_kauftag(df: pd.DataFrame) -> dict:
    """Alles, was am Kauftag bekannt war. df endet am Kauftag."""
    a = float(atr_reihe(df).iloc[-1])
    r = float(rsi_reihe(df).iloc[-1])
    kurs = float(df["Close"].iloc[-1])
    tiefs, hochs = pivots(df)
    if not tiefs or a <= 0:
        return {}

    grenze = df.index[-1] - pd.Timedelta(days=FENSTER_TAGE)
    im_fenster = [i for i in tiefs if df.index[i] >= grenze]
    if not im_fenster:
        return {}
    letzte = sorted(im_fenster, reverse=True)
    i1 = letzte[0]
    t1 = float(df["Low"].values[i1])

    # Laufende Serie absteigender Tiefs
    lauf = 1
    for k in range(1, len(letzte)):
        if float(df["Low"].values[letzte[k]]) > float(df["Low"].values[letzte[k - 1]]):
            lauf += 1
        else:
            break
    beginn = letzte[lauf - 1]

    vor = [i for i in hochs if i < beginn]
    korr_atr = korr_tage = None
    if vor:
        korr_atr = (float(df["High"].values[vor[-1]]) - t1) / a
        korr_tage = i1 - vor[-1]

    # Bodenbildung wie in der Excel
    fenster60 = df["High"].tail(60)
    falltiefe = (float(fenster60.max()) - t1) / a
    tiefabstand = None
    if len(letzte) > 1:
        tiefabstand = abs(t1 - float(df["Low"].values[letzte[1]])) / a
    druck = None
    if "Volume" in df.columns and len(df) > 7:
        d5 = df["Close"].diff().tail(5)
        v5 = df["Volume"].tail(5)
        auf, ab = float(v5[d5 > 0].sum()), float(v5[d5 <= 0].sum())
        druck = auf / ab if ab > 0 else None
    boden = bool(falltiefe >= 4 and tiefabstand is not None and tiefabstand <= 1
                 and druck is not None and druck > 1)

    einstieg = (kurs - t1) / a
    punkte = (30 if boden else 0)
    punkte += 20 if r < 30 else (10 if r < 40 else 0)
    punkte += 15 if 0 <= einstieg <= 1.5 else 0
    punkte += 5   # Tief bestaetigt - die Umkehr-Regel liefert nur bestaetigte

    return {"kurs": kurs, "atr": a, "rsi": r, "tief1": t1,
            "tief1_datum": df.index[i1].date(), "einstieg": einstieg,
            "tiefs_lauf": lauf, "korr_atr": korr_atr, "korr_tage": korr_tage,
            "falltiefe": falltiefe, "tiefabstand": tiefabstand, "druck": druck,
            "boden": boden, "score": punkte}


def main() -> int:
    import yfinance as yf
    tickers = sorted({t for _, t, _, _, _ in TRADES})
    print(f"Lade {len(tickers)} Basiswerte ...")
    roh = yf.download(tickers, period="3y", interval="1d", auto_adjust=True,
                      group_by="ticker", threads=True, progress=False)
    daten = {}
    for t in tickers:
        try:
            d = roh[t] if isinstance(roh.columns, pd.MultiIndex) else roh
            d = d.dropna(subset=["High", "Low", "Close"])
            d.index = pd.to_datetime(d.index).tz_localize(None)
            daten[t] = d
        except Exception:  # noqa: BLE001
            pass
    print(f"  {len(daten)} geladen.")

    zeilen = []
    for name, ticker, kauf, verkauf, erg in TRADES:
        df = daten.get(ticker)
        if df is None:
            zeilen.append({"name": name, "hinweis": "keine Kursdaten"})
            continue
        bis = df[df.index <= pd.Timestamp(kauf)]
        if len(bis) < 260:
            zeilen.append({"name": name, "hinweis": "zu wenig Vorlauf"})
            continue
        stand = stand_am_kauftag(bis)
        soll = soll_werte(bis.iloc[:-1])
        if not stand:
            zeilen.append({"name": name, "hinweis": "kein Tief im Fenster"})
            continue
        zeilen.append({"name": name, "ticker": ticker, "kauf": kauf,
                       "ergebnis": erg, **stand, **soll})

    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    L = ["# Rueckblick - haetten die Trades nach heutigen Regeln gekauft werden duerfen?", "",
         f"_Erstellt {jetzt} UTC. Rekonstruiert den Stand am Kauftag, ausschliesslich mit "
         "Daten, die damals vorlagen. Analystenurteil und Kursziel sind historisch nicht "
         "verfuegbar, der Score ist deshalb TECHNISCH und geht nur bis 70 Punkte: "
         "Bodenbildung 30, RSI unter 30 zwanzig bzw. unter 40 zehn, Einstieg hoechstens "
         "1,5 ATR ueber dem Bezugstief 15, Tief bestaetigt 5._", "",
         "| Position | Kauf | RSI | Bezugstief | Einstieg | Tiefs jetzt (üblich) | "
         "Korrektur jetzt (üblich) | Boden | Score | Ergebnis |",
         "|---|---|---|---|---|---|---|---|---|---|"]

    def z(v, nk=2, einheit=""):
        return "-" if v is None else f"{v:.{nk}f}{einheit}"

    for e in zeilen:
        if e.get("hinweis"):
            L.append(f"| {e['name']} | - | - | - | - | - | - | - | - | {e['hinweis']} |")
            continue
        tiefs = f"{e['tiefs_lauf']} ({z(e.get('tiefs_soll'), 0)})"
        korr = f"{z(e.get('korr_atr'))} ({z(e.get('korr_soll'))})"
        L.append(f"| {e['name']} | {e['kauf']} | {e['rsi']:.0f} | "
                 f"{e['tief1']:.2f} vom {e['tief1_datum']:%d.%m.} | "
                 f"{z(e['einstieg'])} ATR | {tiefs} | {korr} | "
                 f"{'ja' if e['boden'] else 'nein'} | **{e['score']}** | "
                 f"{z(e.get('ergebnis'), 1, '%')} |")

    gute = [e for e in zeilen if e.get("score") is not None and e["score"] >= 35]
    schwache = [e for e in zeilen if e.get("score") is not None and e["score"] < 35]
    L += ["", "## Auswertung", "",
          f"- Trades mit technischem Score ab 35: {len(gute)}",
          f"- Trades unter 35: {len(schwache)}", ""]
    for gruppe, titel in ((gute, "Ab 35 Punkten"), (schwache, "Unter 35 Punkten")):
        werte = [e["ergebnis"] for e in gruppe if e.get("ergebnis") is not None]
        if werte:
            L.append(f"- {titel}: {len(werte)} mit bekanntem Ergebnis, "
                     f"Median {np.median(werte):+.1f}%, Spanne {min(werte):+.1f}% bis {max(werte):+.1f}%")
    L += ["", "_Zehn Trades sind eine sehr kleine Stichprobe, und die Ergebnisse haengen "
          "zusaetzlich am Verkaufszeitpunkt, der hier gar nicht geprueft wird. Die Tabelle "
          "zeigt, welche Kaeufe die heutigen Kriterien erfuellt haetten - sie beweist nicht, "
          "dass die Kriterien funktionieren._"]

    DOCS.mkdir(parents=True, exist_ok=True)
    AUSGABE.write_text("\n".join(L), encoding="utf-8")
    print(f"\nGeschrieben: {AUSGABE}\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
