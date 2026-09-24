"""
methodenvergleich.py - Vergleich verschiedener Lesarten der Tiefzaehlung.
Angelegt 24.09.2026, erweitert am selben Tag (Peter: "schau von dem Hoch zum
naechsten Tief oder irgendwie anders, was fuer eine Zaehlung wirklich
sinnvoll sein koennte").

Wann endet eine Abwaertsserie? Verglichene Regeln:
  dow          Standard: ein Hoch (auch nur der Docht) ueber dem Zwischenhoch
               vor dem tiefsten Tief.
  schluss      wie dow, aber ein TAGESSCHLUSS muss darueber liegen.
  schwelle05   wie dow, das Hoch muss mindestens 0,5 ATR darueber liegen.
  schwelle10   dasselbe mit 1,0 ATR.
  halb         Erholung: ein Tagesschluss holt mindestens die HAELFTE des
               Rueckgangs vom Starthoch bis zum tiefsten Tief zurueck.
  starthoch    ein Hoch ueber dem Hoch, an dem die ganze Serie begann
               ("vom Hoch bis zum naechsten Tief" im weitesten Sinn).

Neue Tiefs zaehlen in allen Regeln gleich: bestaetigte Wendepunkt-Tiefs aus
tiefs_regel.pivots(), die unter dem bisher tiefsten Tief der Serie liegen.

Gemessen je Regel (7 Jahre, alle Werte):
  Fehlabbruch  Anteil der beendeten Serien, bei denen der Kurs binnen 63
               Handelstagen nach dem Ende doch noch unter das tiefste Tief der
               alten Serie faellt. Genau der UnitedHealth-Fall: die Serie war
               in Wahrheit nicht vorbei. Niedriger ist besser.
  Fortsetzung  je Tiefposition: Anteil, nach dem noch ein weiteres Tief kam.
  Halten 3 ATR je Tiefposition: Anteil, bei dem ein KO 3 ATR unter dem Tief
               die naechsten 63 Handelstage ueberlebt.
  Trennschaerfe  Abstand zwischen Tief 1 und Tief 5 bei "Halten 3 ATR" - je
               groesser, desto mehr sagt die Tiefposition ueber das Risiko aus.
Alles auch getrennt nach erster und zweiter Haelfte des Zeitraums.

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

REGELN = ("dow", "schluss", "schwelle05", "schwelle10", "halb", "starthoch")
NAMEN = {"dow": "Standard (Docht)", "schluss": "Schlusskurs", "schwelle05": "+0,5 ATR",
         "schwelle10": "+1,0 ATR", "halb": "Halbe Erholung", "starthoch": "Über Starthoch"}
TAGE = 63
MIN_TAGE = 200
AUS = historie.DOCS / "methodenvergleich.md"
KLASSEN = ["1", "2", "3", "4", "5", "6", "7+"]


def serien(df: pd.DataFrame, regelname: str, a: np.ndarray) -> list[dict]:
    """Abwaertsserien nach der gewaehlten Endregel. Rueckgabe je Serie:
    tiefs (Zeilennummern), tiefstand, ende_i (Zeile, an der sie endete, oder
    None), laufend."""
    hoch, tief, schl = df["High"].values, df["Low"].values, df["Close"].values
    pv = regel.pivots(df)
    out: list[dict] = []
    seq = {"tiefs": [], "tiefstand": None, "ref": None, "start": None}
    letztes_hoch = None
    letztes_ende = 0

    def schliessen(ende):
        if seq["tiefs"]:
            out.append({"tiefs": list(seq["tiefs"]), "tiefstand": seq["tiefstand"],
                        "ende_i": ende, "laufend": ende is None})

    for k, (art, i) in enumerate(pv):
        von = pv[k - 1][1] + 1 if k > 0 else 0
        bis = pv[k + 1][1] if k + 1 < len(pv) else len(df)
        if art == "hoch":
            h = float(hoch[i])
            ende = None
            if seq["tiefs"]:
                ref = seq["ref"] if seq["ref"] is not None else h
                if seq["ref"] is None:
                    seq["ref"] = h
                atr_i = a[i] if np.isfinite(a[i]) else 0.0
                if regelname == "dow" and regel._ueber(h, ref):
                    ende = i
                elif regelname == "schwelle05" and h > ref + 0.5 * atr_i:
                    ende = i
                elif regelname == "schwelle10" and h > ref + 1.0 * atr_i:
                    ende = i
                elif regelname == "schluss":
                    for j in range(von, bis):
                        if regel._ueber(float(schl[j]), ref):
                            ende = j; break
                elif regelname == "halb" and seq["start"] is not None:
                    grenze = seq["tiefstand"] + 0.5 * (seq["start"] - seq["tiefstand"])
                    for j in range(von, bis):
                        if schl[j] >= grenze:
                            ende = j; break
                elif regelname == "starthoch" and seq["start"] is not None and regel._ueber(h, seq["start"]):
                    ende = i
            if ende is not None:
                schliessen(ende)
                seq = {"tiefs": [], "tiefstand": None, "ref": None, "start": h}
                letztes_ende = ende
            elif not seq["tiefs"]:
                # vor dem ersten Tief: Starthoch ist das hoechste Hoch
                seq["start"] = h if seq["start"] is None else max(seq["start"], h)
            letztes_hoch = h
        else:
            t = float(tief[i])
            if seq["tiefstand"] is None or regel._unter(t, seq["tiefstand"]):
                if not seq["tiefs"]:
                    # Starthoch = hoechstes Hoch seit dem Ende der vorigen Serie
                    seq["start"] = float(hoch[letztes_ende:i + 1].max())
                seq["tiefs"].append(i)
                seq["tiefstand"] = t
                seq["ref"] = letztes_hoch
    schliessen(None)
    return out


def auswerten(df: pd.DataFrame, regelname: str, mitte) -> dict:
    a = historie.atr(df)
    tief = df["Low"].values
    n = len(df)
    ss = serien(df, regelname, a)
    faelle, abbr = [], []
    for s in ss:
        for k, i in enumerate(s["tiefs"], start=1):
            if not np.isfinite(a[i]) or a[i] <= 0:
                continue
            f = {"pos": str(k) if k <= 6 else "7+", "h": 1 if df.index[i] < mitte else 2,
                 "weiter": None, "b": None}
            if not s["laufend"] or k < len(s["tiefs"]):
                f["weiter"] = k < len(s["tiefs"])
            if i + TAGE < n:
                f["b"] = max(0.0, (tief[i] - tief[i + 1:i + 1 + TAGE].min()) / a[i])
            faelle.append(f)
        e = s["ende_i"]
        if e is not None and e + TAGE < n:
            abbr.append({"h": 1 if df.index[e] < mitte else 2,
                         "fehl": bool(tief[e + 1:e + 1 + TAGE].min() < s["tiefstand"])})
    laengen = [len(s["tiefs"]) for s in ss]
    return {"faelle": faelle, "abbr": abbr, "serien": len(ss), "laenge": laengen}


def q(xs):
    xs = [x for x in xs if x is not None]
    return 100 * np.mean(xs) if xs else None


def z(x):
    return "-" if x is None else f"{x:.0f}"


def main() -> int:
    jahre = int(sys.argv[sys.argv.index("--jahre") + 1]) if "--jahre" in sys.argv else 7
    daten = historie.lade(historie.universum(), jahre)
    erg = {r: {"faelle": [], "abbr": [], "serien": 0, "laenge": []} for r in REGELN}
    werte = 0
    for t, df in daten.items():
        df = df.dropna(subset=["High", "Low", "Close"])
        if len(df) < MIN_TAGE:
            continue
        werte += 1
        mitte = df.index[len(df) // 2]
        for r in REGELN:
            x = auswerten(df, r, mitte)
            for k in ("faelle", "abbr", "laenge"):
                erg[r][k] += x[k]
            erg[r]["serien"] += x["serien"]

    L = [f"# Methodenvergleich Tiefzählung ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)", "",
         f"{werte} Werte, {jahre} Jahre. Alle Zahlen in Prozent.", "",
         "## Überblick", "",
         "| Regel | Serien | Ø Tiefs je Serie | Fehlabbruch gesamt | 1. Hälfte | 2. Hälfte | Trennschärfe (Halten 3 ATR, Tief 5 minus Tief 1) | 1. Hälfte | 2. Hälfte |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in REGELN:
        e = erg[r]
        fehl = [q([a["fehl"] for a in e["abbr"] if h is None or a["h"] == h]) for h in (None, 1, 2)]
        tr = []
        for h in (None, 1, 2):
            f1 = [f["b"] < 3 for f in e["faelle"] if f["pos"] == "1" and f["b"] is not None and (h is None or f["h"] == h)]
            f5 = [f["b"] < 3 for f in e["faelle"] if f["pos"] == "5" and f["b"] is not None and (h is None or f["h"] == h)]
            tr.append(q(f5) - q(f1) if f1 and f5 else None)
        L.append(f"| {NAMEN[r]} | {e['serien']} | {np.mean(e['laenge']):.2f} | " +
                 " | ".join(z(x) for x in fehl) + " | " + " | ".join(("-" if x is None else f"{x:+.0f}") for x in tr) + " |")
    for titel, feld in (("Fortsetzung je Tiefposition (noch ein weiteres Tief)", "weiter"),
                        ("Halten 3 ATR je Tiefposition (63 Handelstage)", "b")):
        L += ["", f"## {titel}", "", "| Regel | " + " | ".join(f"Tief {k}" for k in KLASSEN) + " |",
              "|---" * (len(KLASSEN) + 1) + "|"]
        for r in REGELN:
            zellen = []
            for kl in KLASSEN:
                fs = [f for f in erg[r]["faelle"] if f["pos"] == kl]
                if feld == "weiter":
                    xs = [f["weiter"] for f in fs if f["weiter"] is not None]
                else:
                    xs = [f["b"] < 3 for f in fs if f["b"] is not None]
                zellen.append(f"{z(q(xs))} ({len(xs)})")
            L.append(f"| {NAMEN[r]} | " + " | ".join(zellen) + " |")
    L += ["", "Lesehilfe: Fehlabbruch = Serie galt als beendet, der Kurs fiel binnen 63 Tagen aber doch "
          "unter ihr tiefstes Tief. Trennschärfe = wie viel sicherer ein KO an Tief 5 ist als an Tief 1; "
          "je größer, desto mehr taugt die Zählung für die Risikoeinschätzung."]
    AUS.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"Geschrieben: {AUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
