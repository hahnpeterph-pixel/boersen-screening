"""rsi_schwellen.py - Wertspezifische Kauf-RSI-Schwellen je Tiefsposition.

Entscheidung 79: RSI-Schwellen sind wertspezifisch, keine festen Zahlen.
Die feste Grenze "RSI unter 50" stammt aus dem Durchschnitt ueber alle
Werte und beschreibt keinen einzigen davon richtig. Synopsys dreht
historisch bei deutlich hoeheren RSI-Staenden nach oben als etwa ein
ruhiger Versorger - dieselbe Zahl auf beide anzuwenden verwirft beim
einen die richtigen Kandidaten und laesst beim anderen zu viele durch.

Gemessen wird der RSI an den TIEFS dieses Wertes nach der Umkehr-Regel
(tiefs_regel.py), getrennt nach der Position des Tiefs in der laufenden
Abwaertsserie. Das ist noetig, weil der RSI mit jedem weiteren Tief einer
Serie systematisch faellt: bei Synopsys liegt das p75 an Tief 1 bei
62,4, an Tief 4 nur noch bei 37,2. Eine ueber alle Positionen gepoolte
Schwelle waere an Tief 1 zu streng und an Tief 4 zu lasch.

Ausgewiesen wird p75, nicht der Median: die Schwelle soll die Grenze des
ueblichen Bereichs markieren, nicht seine Mitte. Ein Kauf beim Median
waere nur bei der Haelfte der historischen Tiefe unauffaellig gewesen.

Kein Pooling ueber Werte (Entscheidung 77) - es gibt bewusst keine
universumsweite Zeile in der Ausgabe.

Eingabe:  docs/puffer_je_tief.csv.gz   (eine Zeile je Tief, aus historie.py)
Ausgabe:  docs/rsi_schwellen.csv       (ticker, position, faelle, Verteilung)

Position 0 bedeutet: alle Tiefspositionen dieses Wertes gepoolt - die
zweite Stufe der Fallback-Kette in tiefs.py, falls eine einzelne Position
zu duenn besetzt ist.

Laeuft direkt nach historie.py im selben Workflow (historie.yml), weil es
dessen Ausgabe liest. Eigenstaendig startbar, solange die gz-Datei da ist.
"""

import csv
import os
import sys

import numpy as np
import pandas as pd

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
EINGABE = os.path.join(DOCS, "puffer_je_tief.csv.gz")
AUSGABE = os.path.join(DOCS, "rsi_schwellen.csv")

# Ab wie vielen Faellen eine Schwelle als belastbar gilt. Duenn besetzte
# Zellen werden NICHT unterdrueckt - sie stehen mit ihrer Fallzahl in der
# Datei und werden dort als nicht belastbar markiert. Die Entscheidung,
# was damit geschieht, faellt in tiefs.py, nicht hier.
MIN_FAELLE = 3

FELDER = ["ticker", "position", "faelle", "belastbar",
          "rsi_min", "rsi_p25", "rsi_median", "rsi_p75", "rsi_max"]


def verteilung(werte: np.ndarray) -> dict:
    """Volle Verteilung statt eines einzelnen Kennwerts - der Median
    allein verschweigt, wie breit die Streuung ist."""
    return {
        "faelle": int(werte.size),
        "belastbar": "ja" if werte.size >= MIN_FAELLE else "nein",
        "rsi_min": round(float(werte.min()), 2),
        "rsi_p25": round(float(np.percentile(werte, 25)), 2),
        "rsi_median": round(float(np.median(werte)), 2),
        "rsi_p75": round(float(np.percentile(werte, 75)), 2),
        "rsi_max": round(float(werte.max()), 2),
    }


def main() -> int:
    if not os.path.exists(EINGABE):
        print(f"FEHLER: {EINGABE} fehlt - erst historie.py laufen lassen.")
        return 1

    d = pd.read_csv(EINGABE, usecols=["ticker", "position", "rsi"])
    d = d.dropna(subset=["rsi"])
    d = d[d["position"] >= 1]
    if d.empty:
        print("FEHLER: keine verwertbaren Zeilen in der Eingabe.")
        return 1

    zeilen = []
    for ticker, g in d.groupby("ticker", sort=True):
        # Position 0: alle Tiefspositionen dieses Wertes gepoolt.
        zeilen.append({"ticker": ticker, "position": 0,
                       **verteilung(g["rsi"].to_numpy())})
        for pos, gp in g.groupby("position", sort=True):
            zeilen.append({"ticker": ticker, "position": int(pos),
                           **verteilung(gp["rsi"].to_numpy())})

    os.makedirs(DOCS, exist_ok=True)
    with open(AUSGABE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER)
        w.writeheader()
        w.writerows(zeilen)

    werte = d["ticker"].nunique()
    belastbar = sum(1 for z in zeilen
                    if z["position"] >= 1 and z["belastbar"] == "ja")
    gesamt = sum(1 for z in zeilen if z["position"] >= 1)
    print(f"{AUSGABE}: {len(zeilen)} Zeilen, {werte} Werte, "
          f"{len(d)} Tiefs ausgewertet.")
    print(f"Wert+Position: {belastbar} von {gesamt} Kombinationen "
          f"mit mindestens {MIN_FAELLE} Faellen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())