"""bruch.py - Seit wann verhaelt sich ein Wert anders? (Version 1, 27.09.2026)

Peter 27.09.2026: "Einmal schauen, seit wann hat sich der Wert veraendert, und wie ist es seit der
Veraenderung - unabhaengig davon, wie lange das her ist." Wird halbjaehrlich neu gerechnet
(erstes Wochenende im Januar und im Juli) oder mit --erzwingen.

Grundlage: docs/puffer_je_tief.csv.gz (20 Jahre, historie.py). Je Wert werden alle Tiefs ab Tief 2
mit mind. 63 Tagen Beobachtung genommen. Jedes Jahr 2011-2023 wird als Bruchpunkt getestet: Wie tief
liefen die Kurse nach den Tiefs vorher und nachher weiter (benoetigt_atr)? Rangtest (Mann-Whitney,
Normalnaeherung). Bruch nur, wenn p < 0,003 (streng, weil 13 Jahre getestet werden) und mind. 10 Faelle
auf jeder Seite. Die Finanzkrise 2008 zaehlt bewusst NICHT als Bruch (Marktphase, bleibt in den 20 Jahren).

Ausgabe: docs/bruch_je_wert.csv (ticker, bruch_jahr leer = kein Bruch, p, n_vor, n_nach,
haelt2_vor, haelt2_nach, haelt3_vor, haelt3_nach, stand).
"""
from __future__ import annotations

import math
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

HIER = os.path.dirname(os.path.abspath(__file__))
EIN = os.path.join(HIER, "docs", "puffer_je_tief.csv.gz")
AUS = os.path.join(HIER, "docs", "bruch_je_wert.csv")
JAHRE_TEST = range(2011, 2024)
MIN_FAELLE = 10
P_GRENZE = 0.003


def mw_p(a: np.ndarray, b: np.ndarray) -> float:
    """Zweiseitiger Mann-Whitney-Test mit Normalnaeherung und Bindungskorrektur."""
    n1, n2 = len(a), len(b)
    alle = np.concatenate([a, b])
    r = pd.Series(alle).rank().values
    u = r[:n1].sum() - n1 * (n1 + 1) / 2
    _, t = np.unique(alle, return_counts=True)
    n = n1 + n2
    var = n1 * n2 / 12 * ((n + 1) - (t ** 3 - t).sum() / (n * (n - 1)))
    if var <= 0:
        return 1.0
    z = (u - n1 * n2 / 2) / math.sqrt(var)
    return math.erfc(abs(z) / math.sqrt(2))


def faellig() -> bool:
    if "--erzwingen" in sys.argv or not os.path.exists(AUS):
        return True
    h = date.today()
    return h.month in (1, 7) and h.day <= 10


def main() -> int:
    if not faellig():
        print("bruch.py: nicht faellig (halbjaehrlich Jan/Jul) - nichts zu tun.")
        return 0
    F = pd.read_csv(EIN, usecols=["ticker", "datum", "position", "beobachtet", "benoetigt_atr"])
    F = F[(F.position >= 2) & (F.beobachtet >= 63)].copy()
    F["j"] = pd.to_datetime(F.datum).dt.year
    rows = []
    for t, g in F.groupby("ticker"):
        best = None
        for b in JAHRE_TEST:
            a, n = g[g.j < b].benoetigt_atr.values, g[g.j >= b].benoetigt_atr.values
            if len(a) < MIN_FAELLE or len(n) < MIN_FAELLE:
                continue
            p = mw_p(a, n)
            if best is None or p < best[1]:
                best = (b, p, a, n)
        z = {"ticker": t, "bruch_jahr": "", "p": "", "n_vor": "", "n_nach": "",
             "haelt2_vor": "", "haelt2_nach": "", "haelt3_vor": "", "haelt3_nach": ""}
        if best:
            b, p, a, n = best
            z.update(p=round(p, 5), n_vor=len(a), n_nach=len(n),
                     haelt2_vor=round((a <= 2).mean() * 100), haelt2_nach=round((n <= 2).mean() * 100),
                     haelt3_vor=round((a <= 3).mean() * 100), haelt3_nach=round((n <= 3).mean() * 100))
            if p < P_GRENZE:
                z["bruch_jahr"] = b
        rows.append(z)
    R = pd.DataFrame(rows)
    R["stand"] = date.today().isoformat()
    R.to_csv(AUS, index=False)
    print(f"bruch.py: {len(R)} Werte, davon {int((R.bruch_jahr != '').sum())} mit Bruch -> {AUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
