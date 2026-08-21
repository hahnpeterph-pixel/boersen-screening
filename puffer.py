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


def bericht(a_zeilen: list, b: dict, jahre: int) -> str:
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

    text = bericht(a_zeilen, b, jahre)
    DOCS.mkdir(parents=True, exist_ok=True)
    AUSGABE.write_text(text, encoding="utf-8")
    print(f"\nGeschrieben: {AUSGABE}\n")
    print(text[:1800])
    return 0


if __name__ == "__main__":
    sys.exit(main())