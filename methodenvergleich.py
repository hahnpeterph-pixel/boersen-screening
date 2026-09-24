"""
methodenvergleich.py - Vergleich zweier Lesarten der Tiefzaehlung.
Angelegt 24.09.2026 (Peter: "Methodik einmal ueberpruefen").

  dow          heutiger Standard: ein Hoch ueber der Referenz beendet die Serie,
               auch wenn nur der Docht darueber liegt.
  dow_schluss  Vergleich: die Serie endet erst mit einem TAGESSCHLUSS ueber der
               Referenz.

Gemessen je Tiefposition (1 bis 6, 7+), 7 Jahre, alle Werte des Universums:
  - Fortsetzung: Anteil der Tiefs, nach denen die Serie noch ein weiteres Tief
    machte (nur abgeschlossene Serien).
  - Halten 63 T: Anteil der Tiefs, nach denen der Kurs in den naechsten 63
    Handelstagen NICHT tiefer fiel als Tief minus p x ATR (p = 2, 3, 4).
Alles zusaetzlich getrennt nach erster und zweiter Haelfte des Zeitraums.

Entscheidungsregel (Stoppregel 17.09.2026): Umstellen nur, wenn sich die
Werte um mindestens 8-10 Prozentpunkte unterscheiden, der Unterschied in
beiden Haelften gilt und ein plausibler Mechanismus dahintersteht.

Schreibt nur docs/methodenvergleich.md. Rechnet ausschliesslich mit
oeffentlichen Kursdaten, kennt keine Positionen.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import historie
import tiefs_regel as regel

VARIANTEN = ("dow", "dow_schluss")
PUFFER = (2.0, 3.0, 4.0)
TAGE = 63
MIN_TAGE = 200
AUS = historie.DOCS / "methodenvergleich.md"


def pos_klasse(k: int) -> str:
    return str(k) if k <= 6 else "7+"


def faelle(df: pd.DataFrame, variante: str, mitte: pd.Timestamp) -> list[dict]:
    a = historie.atr(df)
    tief = df["Low"].values
    n = len(df)
    out = []
    for s in regel.sequenzen(df, variante):
        for k, i in enumerate(s["tiefs"], start=1):
            if not np.isfinite(a[i]) or a[i] <= 0:
                continue
            f = {"pos": pos_klasse(k), "haelfte": 1 if df.index[i] < mitte else 2,
                 "weiter": None, "benoetigt": None}
            if not s["laufend"] or k < s["anzahl"]:
                f["weiter"] = k < s["anzahl"]
            if i + TAGE < n:
                f["benoetigt"] = max(0.0, (tief[i] - tief[i + 1:i + 1 + TAGE].min()) / a[i])
            out.append(f)
    return out


def kennzahlen(fs: list[dict]) -> dict:
    w = [f["weiter"] for f in fs if f["weiter"] is not None]
    b = np.array([f["benoetigt"] for f in fs if f["benoetigt"] is not None])
    r = {"n": len(fs), "weiter": (100 * np.mean(w) if w else None), "n_w": len(w)}
    for p in PUFFER:
        r[p] = 100 * np.mean(b < p) if len(b) else None
    return r


def z(x):
    return "-" if x is None else f"{x:.0f} %"


def d(a, b):
    if a is None or b is None:
        return "-"
    x = b - a
    s = f"{x:+.0f}".replace("-", "−")
    return f"**{s}**" if abs(x) >= 8 else s


def main() -> int:
    jahre = int(sys.argv[sys.argv.index("--jahre") + 1]) if "--jahre" in sys.argv else 7
    daten = historie.lade(historie.universum(), jahre)
    alle = {v: [] for v in VARIANTEN}
    serien = {v: 0 for v in VARIANTEN}
    for t, df in daten.items():
        df = df.dropna(subset=["High", "Low", "Close"])
        if len(df) < MIN_TAGE:
            continue
        mitte = df.index[len(df) // 2]
        for v in VARIANTEN:
            fs = faelle(df, v, mitte)
            for f in fs:
                f["ticker"] = t
            alle[v] += fs
            serien[v] += len(regel.sequenzen(df, v))

    klassen = ["1", "2", "3", "4", "5", "6", "7+"]
    zeilen = [f"# Methodenvergleich Tiefzaehlung ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)", "",
              f"{len(daten)} Werte, {jahre} Jahre. Serien gesamt: Standard {serien['dow']}, "
              f"Schlusskurs-Regel {serien['dow_schluss']}"
              + (f" ({(serien['dow_schluss'] / serien['dow'] - 1) * 100:+.1f} %)." if serien['dow'] else "."), "",
              "Δ = Schlusskurs-Regel minus Standard in Prozentpunkten, **fett** ab 8.", ""]
    for titel, filt in (("Gesamt", None), ("Erste Hälfte", 1), ("Zweite Hälfte", 2)):
        zeilen += [f"## {titel}", "",
                   "| Tief | Fälle Std/Schl | Fortsetzung Std | Schl | Δ | Halten 2 ATR Std | Schl | Δ | Halten 3 ATR Std | Schl | Δ | Halten 4 ATR Std | Schl | Δ |",
                   "|---" * 14 + "|"]
        for kl in klassen:
            k = {}
            for v in VARIANTEN:
                fs = [f for f in alle[v] if f["pos"] == kl and (filt is None or f["haelfte"] == filt)]
                k[v] = kennzahlen(fs)
            a, b = k["dow"], k["dow_schluss"]
            zeilen.append(f"| {kl} | {a['n']}/{b['n']} | {z(a['weiter'])} | {z(b['weiter'])} | {d(a['weiter'], b['weiter'])} | "
                          + " | ".join(f"{z(a[p])} | {z(b[p])} | {d(a[p], b[p])}" for p in PUFFER) + " |")
        zeilen.append("")
    AUS.write_text("\n".join(zeilen), encoding="utf-8")
    print("\n".join(zeilen))
    print(f"Geschrieben: {AUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
