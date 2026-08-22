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

# Jede abgeschlossene Tranche aus dem Blatt Transaktionen:
# name, ticker, kaufdatum, verkaufsdatum, Scheinkurs Kauf, Scheinkurs Verkauf,
# Rendite des Scheins in Prozent
TRANCHEN = [
    ("Microsoft",         "MSFT",   "2026-07-22", "2026-08-03",  4.85, 11.82, 139.2),
    ("Microsoft",         "MSFT",   "2026-07-22", "2026-08-10",  4.85, 14.85, 199.0),
    ("NVIDIA",            "NVDA",   "2026-08-03", "2026-08-10",  2.37,  3.95,  63.5),
    ("Oracle",            "ORCL",   "2026-07-21", "2026-08-10",  1.03,  3.44, 217.0),
    ("Rheinmetall",       "RHM.DE", "2026-08-11", "2026-08-17",  1.02,  1.64,  44.8),
    ("Gold",              "GC=F",   "2026-08-14", "2026-08-20", 14.33, 25.97,  79.9),
    ("Gold",              "GC=F",   "2026-08-14", "2026-08-20", 14.33, 24.75,  71.4),
    ("ASML",              "ASML",   "2026-08-20", "2026-08-21",  6.33,  5.81,  -9.7),
    ("NVIDIA",            "NVDA",   "2026-08-03", "2026-08-21",  2.37,  3.63,  25.5),
    ("Applied Materials", "AMAT",   "2026-08-20", "2026-08-21",  5.32,  4.74, -12.3),
    ("Take-Two",          "TTWO",   "2026-08-20", "2026-08-21",  0.92,  1.45,  53.2),
    ("Micron",            "MU",     "2026-08-20", "2026-08-21",  8.92,  9.32,   2.8),
    ("Gold II",           "GC=F",   "2026-08-21", "2026-08-21",  3.35,  3.80,  12.0),
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


def zerlege(df, kauf, verkauf, rendite_schein):
    """Zerlegt eine Tranche in ihre zwei Bestandteile.

    Der Gewinn eines Knock-out-Scheins entsteht aus zwei Dingen: wie weit
    sich der Basiswert bewegt hat, und wie stark der Hebel diese Bewegung
    vervielfacht. Ohne diese Trennung sieht ein Trade gut aus, bei dem sich
    der Basiswert kaum bewegte und nur der Hebel extrem war - und genau der
    ist der riskanteste.

    Aus dem Verhaeltnis der beiden Renditen laesst sich der effektive Hebel
    berechnen und daraus rueckwaerts, wo die KO-Schwelle ungefaehr lag:
    Hebel = Kurs / (Kurs - KO), also KO = Kurs x (1 - 1/Hebel). Das ist eine
    Naeherung - Spread, Finanzierungskosten und das Nachziehen der Schwelle
    sind darin nicht enthalten.

    Zusaetzlich: der tiefste Basiskurs waehrend der Haltedauer. Er zeigt,
    wie nah es an der geschaetzten Schwelle war.
    """
    d1, d2 = pd.Timestamp(kauf), pd.Timestamp(verkauf)
    bis_kauf = df[df.index <= d1]
    bis_verk = df[df.index <= d2]
    if bis_kauf.empty or bis_verk.empty:
        return {}
    k = float(bis_kauf["Close"].iloc[-1])
    v = float(bis_verk["Close"].iloc[-1])
    a = float(atr_reihe(bis_kauf).iloc[-1])
    bewegung = (v / k - 1) * 100
    hebel = (rendite_schein / bewegung) if abs(bewegung) > 0.01 else None
    ko = k * (1 - 1 / hebel) if hebel and hebel > 1 else None

    halte = df[(df.index >= d1) & (df.index <= d2)]
    tiefster = float(halte["Low"].min()) if not halte.empty else None
    abstand_ko = ((tiefster - ko) / a) if (ko and tiefster and a > 0) else None

    return {"basis_kauf": k, "basis_verkauf": v, "bewegung": bewegung,
            "hebel": hebel, "ko_geschaetzt": ko, "tiefster": tiefster,
            "puffer_rest": abstand_ko, "atr": a,
            "bewegung_atr": (v - k) / a if a > 0 else None}


def main() -> int:
    import yfinance as yf
    tickers = sorted({t for _, t, _, _, _, _, _ in TRANCHEN})
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
    for name, ticker, kauf, verkauf, sk, sv, rend in TRANCHEN:
        df = daten.get(ticker)
        if df is None:
            zeilen.append({"name": name, "hinweis": "keine Kursdaten"})
            continue
        bis = df[df.index <= pd.Timestamp(kauf)]
        stand = stand_am_kauftag(bis) if len(bis) >= 260 else {}
        soll = soll_werte(bis.iloc[:-1]) if len(bis) >= 260 else {}
        zerl = zerlege(df, kauf, verkauf, rend)
        zeilen.append({"name": name, "ticker": ticker, "kauf": kauf, "verkauf": verkauf,
                       "schein_kauf": sk, "schein_verkauf": sv, "rendite": rend,
                       **stand, **soll, **zerl})

    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    def z(v, nk=2, e=""):
        return "-" if v is None else f"{v:.{nk}f}{e}"

    L = ["# Rueckblick - was hat die erfolgreichen Trades getragen?", "",
         f"_Erstellt {jetzt} UTC. Eine Zeile je abgeschlossener Tranche. Der Stand am Kauftag "
         "ist ausschliesslich aus damals vorliegenden Daten rekonstruiert._", "",
         "## Teil 1 - Zerlegung des Gewinns", "",
         "_Der Gewinn eines Knock-out-Scheins hat zwei Quellen: die Bewegung des Basiswerts "
         "und den Hebel. 'Hebel' ist hier RUECKGERECHNET aus den beiden Renditen, nicht aus "
         "den Papierdaten. 'KO geschaetzt' folgt daraus und ist eine Naeherung ohne Spread "
         "und Finanzierungskosten. 'Rest zum KO' ist der Abstand des tiefsten Kurses waehrend "
         "der Haltedauer zu dieser geschaetzten Schwelle, in ATR - je kleiner, desto knapper "
         "war es._", "",
         "| Position | Kauf | Verkauf | Basis Kauf | Basis Verkauf | Bewegung | in ATR | "
         "Rendite Schein | Hebel | KO geschaetzt | tiefster Kurs | Rest zum KO |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in zeilen:
        if e.get("hinweis"):
            L.append(f"| {e['name']} | " + " | ".join(["-"] * 11) + " |")
            continue
        L.append(f"| {e['name']} | {e['kauf'][5:]} | {e['verkauf'][5:]} | "
                 f"{z(e.get('basis_kauf'))} | {z(e.get('basis_verkauf'))} | "
                 f"{z(e.get('bewegung'), 1, '%')} | {z(e.get('bewegung_atr'))} | "
                 f"**{z(e.get('rendite'), 1, '%')}** | {z(e.get('hebel'), 1, 'x')} | "
                 f"{z(e.get('ko_geschaetzt'))} | {z(e.get('tiefster'))} | "
                 f"{z(e.get('puffer_rest'))} ATR |")

    L += ["", "## Teil 2 - Lage am Kauftag", "",
          "_Technischer Score bis 70 Punkte: Bodenbildung 30, RSI unter 30 zwanzig bzw. unter "
          "40 zehn, Einstieg hoechstens 1,5 ATR ueber dem Bezugstief 15, Tief bestaetigt 5. "
          "Analystenurteil und Kursziel liegen historisch nicht vor._", "",
          "| Position | Kauf | RSI | Bezugstief | Einstieg | Tiefs jetzt (üblich) | "
          "Korrektur jetzt (üblich) | Boden | Score | Rendite |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for e in zeilen:
        if e.get("score") is None:
            continue
        tiefs = f"{e['tiefs_lauf']} ({z(e.get('tiefs_soll'), 0)})"
        korr = f"{z(e.get('korr_atr'))} ({z(e.get('korr_soll'))})"
        L.append(f"| {e['name']} | {e['kauf'][5:]} | {e['rsi']:.0f} | "
                 f"{e['tief1']:.2f} vom {e['tief1_datum']:%d.%m.} | {z(e['einstieg'])} ATR | "
                 f"{tiefs} | {korr} | {'ja' if e['boden'] else 'nein'} | "
                 f"**{e['score']}** | {z(e.get('rendite'), 1, '%')} |")

    gute = [e for e in zeilen if e.get("rendite") is not None and e["rendite"] > 0]
    schlecht = [e for e in zeilen if e.get("rendite") is not None and e["rendite"] <= 0]
    L += ["", "## Teil 3 - was trennt Gewinner von Verlierern?", "",
          "| Kennzahl | Gewinner | Verlierer |", "|---|---|---|"]
    for feld, titel, nk in (("bewegung", "Bewegung Basiswert in %", 2),
                            ("bewegung_atr", "Bewegung in ATR", 2),
                            ("hebel", "Hebel", 1),
                            ("puffer_rest", "Rest zum KO in ATR", 2),
                            ("einstieg", "Einstieg ueber Tief in ATR", 2),
                            ("rsi", "RSI am Kauftag", 0),
                            ("korr_atr", "laufende Korrektur in ATR", 2),
                            ("score", "technischer Score", 0)):
        def m(gruppe):
            w = [e[feld] for e in gruppe if e.get(feld) is not None]
            return f"{np.median(w):.{nk}f}" if w else "-"
        L.append(f"| {titel} | {m(gute)} | {m(schlecht)} |")
    L += ["", f"_{len(gute)} Gewinner, {len(schlecht)} Verlierer. Bei dieser Groesse sind "
          "Mediane Anhaltspunkte, keine Belege. Der Verkaufszeitpunkt wird nicht geprueft - "
          "ein Trade kann die Kaufkriterien erfuellt haben und trotzdem schlecht ausgegangen "
          "sein, weil zu frueh oder zu spaet verkauft wurde._"]

    DOCS.mkdir(parents=True, exist_ok=True)
    AUSGABE.write_text("\n".join(L), encoding="utf-8")
    print(f"\nGeschrieben: {AUSGABE}\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
