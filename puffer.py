#!/usr/bin/env python3
"""
Puffer-Analyse - wie viel ATR-Abstand braucht die KO-Schwelle wirklich?

Die Wette der Strategie lautet: ein bestaetigtes Tief haelt, oder es wird nur
leicht unterschritten. Dieses Skript misst, ob das stimmt - und wenn ja, wie
leicht "leicht" ist.

TEIL A - die eigenen Trades. Fuer jede geschlossene Position: welches Tief war
das Bezugstief, wie tief ging der Basiswert waehrend der Haltedauer darunter,
gemessen in ATR(14) zum Kaufzeitpunkt. Aussagekraft begrenzt: 13 Tranchen ohne
einen einzigen Knock-out liefern nur eine Untergrenze.

TEIL B - die eigentliche Antwort. Ueber das ganze Universum und mehrere Jahre
wird JEDES bestaetigte Swing-Tief gesucht und gemessen, wie weit der Kurs in
den Tagen danach darunter gerutscht ist. Das ergibt eine Verteilung mit
mehreren tausend Faellen statt dreizehn. Daraus laesst sich ablesen, welcher
Puffer welchen Anteil der Faelle abdeckt.

Getrennt ausgewiesen wird die Teilmenge, die der Strategie entspricht: Tiefs,
die TIEFER liegen als das vorherige Tief - also nicht das erste Tief eines
Abwaertstrends, sondern das zweite oder dritte.

Ausgabe: docs/puffer.md

Aufruf:  python3 puffer.py
         python3 puffer.py --jahre 5

KEINE Anlageberatung. Das Skript misst historische Kursverlaeufe.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
AUSGABE = DOCS / "puffer.md"

LINKS = RECHTS = 3      # Swing-Tief: tiefer als 3 Tage davor und 3 danach
ATR_TAGE = 14
HALTE_FENSTER = (5, 10, 20)   # Handelstage nach dem Tief, die geprueft werden
JAHRE = 3

# ── Geschlossene Positionen aus dem Orderbuch (Blatt Transaktionen) ────
# name, yfinance-Ticker, Kaufdatum, Verkaufsdatum (letzte Tranche)
TRADES = [
    ("Microsoft",         "MSFT",     "2026-07-22", "2026-08-10"),
    ("Oracle",            "ORCL",     "2026-07-21", "2026-08-10"),
    ("NVIDIA",            "NVDA",     "2026-08-03", "2026-08-21"),
    ("Rheinmetall",       "RHM.DE",   "2026-08-11", "2026-08-17"),
    ("Gold",              "XAUUSD=X", "2026-08-14", "2026-08-20"),
    ("ASML",              "ASML",     "2026-08-20", "2026-08-21"),
    ("Applied Materials", "AMAT",     "2026-08-20", "2026-08-21"),
    ("Take-Two",          "TTWO",     "2026-08-20", "2026-08-21"),
    ("Micron",            "MU",       "2026-08-20", "2026-08-21"),
    ("Gold II",           "XAUUSD=X", "2026-08-21", "2026-08-21"),
]


def atr(df: pd.DataFrame, tage: int = ATR_TAGE) -> pd.Series:
    """ATR nach Wilder auf echten Hoch/Tief/Schluss-Werten."""
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vor = schluss.shift(1)
    spanne = pd.concat([hoch - tief, (hoch - vor).abs(), (tief - vor).abs()], axis=1).max(axis=1)
    return spanne.ewm(alpha=1 / tage, adjust=False).mean()


def swing_tiefs(df: pd.DataFrame) -> list[int]:
    """Positionen aller bestaetigten Swing-Tiefs. Bestaetigt heisst: die
    RECHTS Tage danach existieren bereits und liegen hoeher - ein Tief am
    Rand der Zeitreihe zaehlt nicht mit."""
    tief = df["Low"].values
    n = len(tief)
    treffer = []
    for i in range(LINKS, n - RECHTS):
        links = tief[i - LINKS:i]
        rechts = tief[i + 1:i + 1 + RECHTS]
        if tief[i] < links.min() and tief[i] < rechts.min():
            treffer.append(i)
    return treffer


def lade(tickers: list[str], jahre: int) -> dict[str, pd.DataFrame]:
    import yfinance as yf
    print(f"Lade {len(tickers)} Werte, {jahre} Jahre ...")
    daten: dict[str, pd.DataFrame] = {}
    schritt = 40
    for i in range(0, len(tickers), schritt):
        teil = tickers[i:i + schritt]
        try:
            roh = yf.download(teil, period=f"{jahre}y", interval="1d",
                              auto_adjust=True, group_by="ticker",
                              threads=True, progress=False)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! Abruf fehlgeschlagen ({teil[0]} ...): {exc}")
            continue
        for t in teil:
            try:
                df = roh[t] if isinstance(roh.columns, pd.MultiIndex) else roh
                df = df.dropna(subset=["Low", "High", "Close"])
                if len(df) > 60:
                    daten[t] = df
            except Exception:  # noqa: BLE001
                continue
    print(f"  {len(daten)} Werte geladen.")
    return daten


# ── Teil A: die eigenen Trades ────────────────────────────────────────
def teil_a(daten: dict) -> list[dict]:
    zeilen = []
    for name, ticker, kauf, verkauf in TRADES:
        df = daten.get(ticker)
        z = {"name": name, "ticker": ticker, "kauf": kauf, "verkauf": verkauf,
             "bezugstief": None, "atr": None, "tiefstes": None,
             "unterschritten_atr": None, "hinweis": ""}
        if df is None:
            z["hinweis"] = "keine Kursdaten"
            zeilen.append(z)
            continue

        idx = df.index.tz_localize(None) if df.index.tz is not None else df.index
        df = df.copy()
        df.index = idx
        d_kauf = pd.Timestamp(kauf)
        d_verk = pd.Timestamp(verkauf)

        vor = df[df.index < d_kauf]
        if len(vor) < 30:
            z["hinweis"] = "zu wenig Vorlauf"
            zeilen.append(z)
            continue

        # Bezugstief: das juengste bestaetigte Swing-Tief VOR dem Kauf
        pos = swing_tiefs(vor)
        if not pos:
            z["hinweis"] = "kein bestaetigtes Tief vor dem Kauf"
            zeilen.append(z)
            continue
        i = pos[-1]
        bezug = float(vor["Low"].iloc[i])
        a = float(atr(vor).iloc[-1])
        z["bezugstief"] = round(bezug, 2)
        z["atr"] = round(a, 2)
        z["tief_datum"] = str(vor.index[i].date())

        halte = df[(df.index >= d_kauf) & (df.index <= d_verk)]
        if halte.empty:
            z["hinweis"] = "keine Kurse in der Haltedauer"
            zeilen.append(z)
            continue
        tiefstes = float(halte["Low"].min())
        z["tiefstes"] = round(tiefstes, 2)
        z["unterschritten_atr"] = round(max(0.0, (bezug - tiefstes) / a), 2) if a > 0 else None
        zeilen.append(z)
    return zeilen


# ── Teil B: alle Swing-Tiefs im Universum ─────────────────────────────
def teil_b(daten: dict) -> dict:
    faelle: list[dict] = []
    for ticker, df in daten.items():
        a = atr(df)
        tief = df["Low"].values
        atr_w = a.values
        # Die Tiefs EINMAL bestimmen. Der Vorgaenger eines Tiefs ist einfach der
        # vorherige Eintrag dieser Liste - dafuer noch einmal zu suchen waere
        # bei 159 Werten x mehreren Jahren unnoetig teuer.
        stellen = swing_tiefs(df)
        for k, i in enumerate(stellen):
            if not np.isfinite(atr_w[i]) or atr_w[i] <= 0:
                continue
            # Erstes Tief eines Abwaertstrends oder schon ein tieferes?
            tiefer_als_vorher = k > 0 and tief[i] < tief[stellen[k - 1]]
            eintrag = {"ticker": ticker, "tiefer_als_vorher": tiefer_als_vorher}
            for w in HALTE_FENSTER:
                spanne = tief[i + 1:i + 1 + w]
                if len(spanne) == 0:
                    eintrag[w] = None
                    continue
                eintrag[w] = max(0.0, (tief[i] - spanne.min()) / atr_w[i])
            faelle.append(eintrag)
    return {"faelle": faelle}



# ── Teil C: welches Bezugstief? ───────────────────────────────────────
# Zwei Vorgehensweisen stehen im Depot nebeneinander: die KO-Schwelle unter
# das JUENGSTE Tief des laufenden Abwaertstrends legen (wenig Abstand, viel
# Hebel), oder unter ein aelteres, deutlich tieferes Tief (viel Abstand,
# wenig Hebel). Hier wird beides an denselben historischen Faellen
# gegeneinander gerechnet - Ausfallquote UND Hebelkosten, denn ohne die
# zweite Zahl gewinnt der grosse Abstand immer.
BEZUEGE = (("juengstes Tief", 0), ("tiefstes 60 Tage", 60), ("tiefstes 90 Tage", 90))
PUFFER_VARIANTEN = (1.0, 2.0, 3.0)
AUSSTIEG_TAGE = 5      # realistische Haltedauer, nicht der Zielhorizont
PRUEF_TAGE = 10        # Fenster, in dem ein Knock-out zaehlt


def teil_c(daten: dict) -> list[dict]:
    """Fuer jedes bestaetigte Swing-Tief einen fiktiven Trade rechnen:
    Einstieg am Bestaetigungstag, KO je nach Bezug und Puffer, Ausstieg
    nach AUSSTIEG_TAGE Handelstagen. Ein Knock-out zaehlt als -100%."""
    treffer = {(b, p): {"ko": 0, "n": 0, "abstand": [], "rendite": []}
               for b, _ in BEZUEGE for p in PUFFER_VARIANTEN}

    for _, df in daten.items():
        a = atr(df).values
        tief = df["Low"].values
        schluss = df["Close"].values
        n = len(df)
        for i in swing_tiefs(df):
            e = i + RECHTS                      # Bestaetigungstag = Einstieg
            if e + PRUEF_TAGE >= n or not np.isfinite(a[e]) or a[e] <= 0:
                continue
            einstieg = schluss[e]
            tiefstes_danach = tief[e + 1:e + 1 + PRUEF_TAGE].min()
            ausstieg = schluss[min(e + AUSSTIEG_TAGE, n - 1)]

            for name, fenster in BEZUEGE:
                if fenster == 0:
                    bezug = tief[i]
                else:
                    start = max(0, i - fenster + 1)
                    bezug = tief[start:i + 1].min()
                for p in PUFFER_VARIANTEN:
                    ko = bezug - p * a[e]
                    if einstieg <= ko:          # kann nicht gekauft werden
                        continue
                    s = treffer[(name, p)]
                    s["n"] += 1
                    s["abstand"].append((einstieg - ko) / a[e])
                    if tiefstes_danach <= ko:
                        s["ko"] += 1
                        s["rendite"].append(-1.0)
                    else:
                        # Hebelwirkung: der Schein bildet den Abstand zum KO ab
                        s["rendite"].append((ausstieg - einstieg) / (einstieg - ko))

    zeilen = []
    for (name, p), s in treffer.items():
        if s["n"] == 0:
            continue
        r = np.array(s["rendite"])
        zeilen.append({
            "bezug": name, "puffer": p, "n": s["n"],
            "ausfall": s["ko"] / s["n"] * 100,
            "abstand": float(np.mean(s["abstand"])),
            "rendite_ueberlebt": float(r[r > -1].mean() * 100) if (r > -1).any() else 0.0,
            "erwartung": float(r.mean() * 100),
        })
    return zeilen



# ── Teil D: woran erkennt man ein Tief, das haelt? ────────────────────
# Die eigentliche Frage der Strategie. Nicht "wie viel Puffer brauche ich",
# sondern "welche Tiefs werden nur minimal unterschritten". Fuer jedes
# bestaetigte Swing-Tief werden Merkmale gemessen, die am Einstiegstag
# BEKANNT sind - kein Blick in die Zukunft - und dagegen gehalten, ob das
# Tief anschliessend gehalten hat.
HAELT_GRENZE = 1.0     # Unterschreitung bis 1 ATR gilt als "haelt"
D_FENSTER = 10         # Handelstage nach der Bestaetigung


def rsi(werte: pd.Series, tage: int = 14) -> pd.Series:
    """RSI nach Wilder."""
    diff = werte.diff()
    auf = diff.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    ab = (-diff.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    return 100 - 100 / (1 + auf / ab.replace(0, np.nan))


def teil_d(daten: dict) -> list[dict]:
    faelle = []
    for _, df in daten.items():
        if len(df) < 260:
            continue
        a = atr(df).values
        tief = df["Low"].values
        hoch = df["High"].values
        schluss = df["Close"].values
        offen = df["Open"].values if "Open" in df else schluss
        vol = df["Volume"].values if "Volume" in df else np.full(len(df), np.nan)
        r = rsi(df["Close"]).values
        ema200 = df["Close"].ewm(span=200, adjust=False).mean().values
        n = len(df)

        stellen = swing_tiefs(df)
        for k, i in enumerate(stellen):
            e = i + RECHTS
            if e + D_FENSTER >= n or i < 200 or not np.isfinite(a[i]) or a[i] <= 0:
                continue

            # Das wievielte Tief einer absteigenden Folge ist es?
            nr = 1
            j = k
            while j > 0 and tief[stellen[j]] < tief[stellen[j - 1]]:
                nr += 1
                j -= 1

            # RSI-Divergenz: tieferes Tief im Kurs, hoeheres im RSI
            divergenz = False
            if k > 0:
                v = stellen[k - 1]
                divergenz = bool(tief[i] < tief[v] and np.isfinite(r[i])
                                 and np.isfinite(r[v]) and r[i] > r[v])

            fenster = slice(max(0, i - 59), i + 1)
            falltiefe = (hoch[fenster].max() - tief[i]) / a[i]

            vrel = np.nan
            if np.isfinite(vol[i]) and i >= 21:
                schnitt = np.nanmean(vol[i - 20:i])
                if schnitt and schnitt > 0:
                    vrel = vol[i] / schnitt

            koerper = abs(schluss[i] - offen[i])
            lunte = min(schluss[i], offen[i]) - tief[i]
            hammer = bool(koerper > 0 and lunte >= 2 * koerper)

            unterschritten = max(0.0, (tief[i] - tief[e + 1:e + 1 + D_FENSTER].min()) / a[i])
            faelle.append({
                "haelt": unterschritten <= HAELT_GRENZE,
                "nr": nr,
                "rsi": r[i] if np.isfinite(r[i]) else None,
                "divergenz": divergenz,
                "falltiefe": falltiefe,
                "vrel": vrel if np.isfinite(vrel) else None,
                "ema200": (tief[i] - ema200[i]) / a[i] if np.isfinite(ema200[i]) else None,
                "hammer": hammer,
                "anstieg": (schluss[e] - tief[i]) / a[i],
            })
    return faelle


def d_gruppen(faelle: list[dict]) -> list[tuple]:
    """Merkmal in Klassen schneiden und je Klasse die Haltequote ausweisen."""
    def quote(teil):
        return (len(teil), sum(1 for x in teil if x["haelt"]) / len(teil) * 100) if teil else (0, 0)

    zeilen = []
    def add(merkmal, klasse, teil):
        n, q = quote(teil)
        if n >= 50:
            zeilen.append((merkmal, klasse, n, q))

    add("Alle Faelle", "Grundquote", faelle)

    for lo, hi, name in ((1, 1, "1. Tief der Folge"), (2, 2, "2. Tief"),
                         (3, 3, "3. Tief"), (4, 99, "4. Tief oder spaeter")):
        add("Stellung in der Tiefpunktfolge", name,
            [x for x in faelle if lo <= x["nr"] <= hi])

    for lo, hi, name in ((0, 30, "unter 30"), (30, 40, "30 bis 40"),
                         (40, 50, "40 bis 50"), (50, 101, "ueber 50")):
        add("RSI am Tief", name,
            [x for x in faelle if x["rsi"] is not None and lo <= x["rsi"] < hi])

    for wert, name in ((True, "ja"), (False, "nein")):
        add("RSI-Divergenz", name, [x for x in faelle if x["divergenz"] is wert])
        add("Hammer-Kerze", name, [x for x in faelle if x["hammer"] is wert])

    for lo, hi, name in ((0, 3, "unter 3 ATR"), (3, 6, "3 bis 6 ATR"),
                         (6, 10, "6 bis 10 ATR"), (10, 999, "ueber 10 ATR")):
        add("Falltiefe vom 60-Tage-Hoch", name,
            [x for x in faelle if lo <= x["falltiefe"] < hi])

    for lo, hi, name in ((0, 1.0, "unter Schnitt"), (1.0, 1.5, "1,0 bis 1,5x"),
                         (1.5, 2.5, "1,5 bis 2,5x"), (2.5, 999, "ueber 2,5x")):
        add("Volumen am Tief", name,
            [x for x in faelle if x["vrel"] is not None and lo <= x["vrel"] < hi])

    for lo, hi, name in ((-999, -2, "mehr als 2 ATR darunter"), (-2, 0, "bis 2 ATR darunter"),
                         (0, 999, "ueber der EMA(200)")):
        add("Lage zur EMA(200)", name,
            [x for x in faelle if x["ema200"] is not None and lo <= x["ema200"] < hi])

    for lo, hi, name in ((0, 0.5, "unter 0,5 ATR"), (0.5, 1.0, "0,5 bis 1 ATR"),
                         (1.0, 2.0, "1 bis 2 ATR"), (2.0, 999, "ueber 2 ATR")):
        add("Anstieg bis zur Bestaetigung", name,
            [x for x in faelle if lo <= x["anstieg"] < hi])
    return zeilen


def verteilung(werte: list[float]) -> dict:
    if not werte:
        return {}
    s = pd.Series(werte)
    return {
        "n": int(s.size),
        "haelt": float((s <= 0.001).mean() * 100),
        "p50": float(s.quantile(0.50)), "p75": float(s.quantile(0.75)),
        "p90": float(s.quantile(0.90)), "p95": float(s.quantile(0.95)),
        "p99": float(s.quantile(0.99)),
        "abgedeckt_1": float((s <= 1.0).mean() * 100),
        "abgedeckt_2": float((s <= 2.0).mean() * 100),
        "abgedeckt_3": float((s <= 3.0).mean() * 100),
        "abgedeckt_4": float((s <= 4.0).mean() * 100),
    }


def bericht(a_zeilen: list, b: dict, c_zeilen: list, d_zeilen: list, jahre: int) -> str:
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    L = ["# Puffer-Analyse - wie viel ATR braucht die KO-Schwelle?", "",
         f"_Erstellt {jetzt} UTC. Swing-Tief = tiefer als die {LINKS} Tage davor "
         f"und die {RECHTS} danach. Puffer immer in ATR({ATR_TAGE}) zum Zeitpunkt "
         f"des Tiefs._", ""]

    # Teil A
    L += ["## Teil A - die eigenen Trades", "",
          "_Bezugstief ist das juengste bestaetigte Swing-Tief vor dem Kauf. "
          "'Unterschritten' misst, wie weit der Basiswert waehrend der Haltedauer "
          "darunter ging. 0,00 heisst: das Tief hat gehalten._", "",
          "| Position | Basiswert | Kauf | Verkauf | Bezugstief | ATR | tiefster Kurs | unterschritten |",
          "|---|---|---|---|---|---|---|---|"]
    werte_a = []
    for z in a_zeilen:
        if z["unterschritten_atr"] is None:
            L.append(f"| {z['name']} | {z['ticker']} | {z['kauf']} | {z['verkauf']} | - | - | - | {z['hinweis']} |")
            continue
        werte_a.append(z["unterschritten_atr"])
        L.append(f"| {z['name']} | {z['ticker']} | {z['kauf']} | {z['verkauf']} | "
                 f"{z['bezugstief']} | {z['atr']} | {z['tiefstes']} | "
                 f"**{z['unterschritten_atr']:.2f} ATR** |")
    L.append("")
    if werte_a:
        L.append(f"Von {len(werte_a)} Trades haben "
                 f"{sum(1 for x in werte_a if x <= 0.001)} das Bezugstief gehalten. "
                 f"Groesste Unterschreitung: {max(werte_a):.2f} ATR.")
        L.append("")

    # Teil B
    alle = [f[10] for f in b["faelle"] if f.get(10) is not None]
    setup = [f[10] for f in b["faelle"] if f.get(10) is not None and f["tiefer_als_vorher"]]
    L += ["## Teil B - alle Swing-Tiefs im Universum", "",
          f"_{jahre} Jahre Kurshistorie. Gemessen wird die tiefste Unterschreitung "
          "innerhalb der naechsten 10 Handelstage - das entspricht ungefaehr der "
          "realen Haltedauer._", ""]
    L.append("| Menge | Faelle | Tief haelt | Median | 75% | 90% | 95% | 99% |")
    L.append("|---|---|---|---|---|---|---|---|")
    for name, w in (("alle Tiefs", alle), ("nur tiefer als das vorherige Tief", setup)):
        v = verteilung(w)
        if not v:
            continue
        L.append(f"| {name} | {v['n']} | {v['haelt']:.0f}% | {v['p50']:.2f} | "
                 f"{v['p75']:.2f} | {v['p90']:.2f} | {v['p95']:.2f} | {v['p99']:.2f} |")
    L.append("")

    L += ["### Welcher Puffer deckt wie viel ab?", "",
          "| Puffer | alle Tiefs | nur tiefer als das vorherige |", "|---|---|---|"]
    va, vs = verteilung(alle), verteilung(setup)
    for p in (1, 2, 3, 4):
        L.append(f"| {p},0 ATR | {va.get(f'abgedeckt_{p}', 0):.0f}% | "
                 f"{vs.get(f'abgedeckt_{p}', 0):.0f}% |")
    L.append("")

    L += ["### Nach Haltedauer", "",
          "_Je laenger gehalten wird, desto mehr Zeit hat der Kurs, das Tief zu "
          "testen. Deshalb haengt der noetige Puffer an der Haltedauer._", "",
          "| Fenster | Median | 90% | 95% | 2 ATR decken ab |", "|---|---|---|---|---|"]
    for w in HALTE_FENSTER:
        v = verteilung([f[w] for f in b["faelle"] if f.get(w) is not None and f["tiefer_als_vorher"]])
        if v:
            L.append(f"| {w} Handelstage | {v['p50']:.2f} | {v['p90']:.2f} | "
                     f"{v['p95']:.2f} | {v['abgedeckt_2']:.0f}% |")
    L.append("")
    L.append("_Ein Knock-out ist ein Totalverlust, kein Teilverlust. Ein Puffer, der "
             "80% der Faelle abdeckt, heisst: jeder fuenfte Trade endet bei null._")
    L.append("")

    # Teil C
    L += ["## Teil C - welches Bezugstief lohnt sich?", "",
          f"_Fiktiver Trade je Swing-Tief: Einstieg am Bestaetigungstag, Ausstieg nach "
          f"{AUSSTIEG_TAGE} Handelstagen, Knock-out zaehlt als -100%. Die Rendite ist "
          "die des Scheins, nicht des Basiswerts - sie ergibt sich aus dem Abstand "
          "zum KO. 'Abstand' ist der Weg vom Einstieg bis zur Schwelle in ATR und "
          "misst den Hebelverlust: je groesser, desto traeger der Schein._", "",
          "| Bezugstief | Puffer | Faelle | Ausfallquote | Abstand Einstieg-KO | Rendite der Ueberlebenden | Erwartungswert |",
          "|---|---|---|---|---|---|---|"]
    for z in sorted(c_zeilen, key=lambda x: -x["erwartung"]):
        L.append(f"| {z['bezug']} | {z['puffer']:.0f} ATR | {z['n']} | "
                 f"{z['ausfall']:.1f}% | {z['abstand']:.2f} ATR | "
                 f"{z['rendite_ueberlebt']:+.1f}% | **{z['erwartung']:+.1f}%** |")
    L.append("")

    # Teil D
    grund = next((q for m, k, n, q in d_zeilen if m == "Alle Faelle"), 0.0)
    L += ["## Teil D - woran erkennt man ein Tief, das haelt?", "",
          f"_Ein Tief 'haelt', wenn es in den {D_FENSTER} Handelstagen nach der "
          f"Bestaetigung um hoechstens {HAELT_GRENZE:.1f} ATR unterschritten wird. "
          "Alle Merkmale sind am Einstiegstag bekannt - kein Blick in die Zukunft. "
          "'Unterschied' zeigt die Abweichung von der Grundquote: nur wo er deutlich "
          "positiv ist, hilft das Merkmal bei der Auswahl._", "",
          "| Merkmal | Auspraegung | Faelle | Haltequote | Unterschied |",
          "|---|---|---|---|---|"]
    for m, k, n, q in d_zeilen:
        d = q - grund
        kennz = "**" if abs(d) >= 3 and m != "Alle Faelle" else ""
        L.append(f"| {m} | {k} | {n} | {kennz}{q:.1f}%{kennz} | "
                 f"{'' if m == 'Alle Faelle' else f'{d:+.1f} Punkte'} |")
    L.append("")
    L.append("_Ein Merkmal mit wenigen Punkten Unterschied ist bei mehreren tausend "
             "Faellen noch kein Vorteil, sondern Rauschen. Erst zweistellige "
             "Unterschiede taugen als Auswahlkriterium._")
    L.append("")
    L.append("_Vorsicht bei 'Anstieg bis zur Bestaetigung': ein Teil des Effekts ist "
             "reine Geometrie. Wer weiter oben einsteigt, hat mehr Abstand nach unten "
             "und unterschreitet das Tief seltener - dafuer sitzt der KO weiter weg "
             "und der Hebel ist kleiner. Der Vorteil ist also nicht geschenkt, "
             "sondern bezahlt._")
    L.append("")
    L.append("_Der Erwartungswert ist eine Rechengroesse, keine Prognose: er unterstellt "
             f"festen Ausstieg nach {AUSSTIEG_TAGE} Tagen ohne Verkaufssignal, ohne "
             "Gebuehren und ohne Auswahl nach RSI oder Analysten. Er taugt zum Vergleich "
             "der Varianten untereinander, nicht als erwartete Depotrendite._")
    return "\n".join(L)


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])

    universum: list[str] = []
    datei = BASE / "universe.json"
    if datei.exists():
        roh = json.loads(datei.read_text(encoding="utf-8"))
        for gruppe in roh.get("benchmarks", {}):
            universum += roh.get(gruppe, [])
    tickers = sorted(set(universum) | {t for _, t, _, _ in TRADES})

    daten = lade(tickers, jahre)
    if len(daten) < 10:
        print("Zu wenige Kursdaten - Abbruch.")
        return 1

    print("Teil A: eigene Trades ...")
    a_zeilen = teil_a(daten)
    print("Teil B: alle Swing-Tiefs ...")
    b = teil_b(daten)
    print(f"  {len(b['faelle'])} Swing-Tiefs gefunden.")
    print("Teil C: Bezugstief-Varianten ...")
    c_zeilen = teil_c(daten)
    print("Teil D: Merkmale haltender Tiefs ...")
    d_faelle = teil_d(daten)
    print(f"  {len(d_faelle)} auswertbare Tiefs.")
    d_zeilen = d_gruppen(d_faelle)

    text = bericht(a_zeilen, b, c_zeilen, d_zeilen, jahre)
    DOCS.mkdir(parents=True, exist_ok=True)
    AUSGABE.write_text(text, encoding="utf-8")
    print(f"\nGeschrieben: {AUSGABE}\n")
    print(text[:1800])
    return 0


if __name__ == "__main__":
    sys.exit(main())
