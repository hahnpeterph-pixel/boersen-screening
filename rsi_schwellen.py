"""rsi_schwellen.py - Wertspezifische Kauf-RSI-Schwellen je Tiefsposition.

Entscheidung 79: RSI-Schwellen sind wertspezifisch, keine festen Zahlen.
Die Grenze "RSI unter 50" stammt aus dem Durchschnitt ueber alle Werte
und beschreibt keinen einzigen davon richtig. Synopsys dreht historisch
an Tief 1 bei RSI 62,7 nach oben, an Tief 4 bei 37,2 - dieselbe Zahl auf
beide anzuwenden filtert einmal zu streng und einmal zu lasch.

Gemessen wird der RSI an den TIEFS dieses Wertes nach der Umkehr-Regel
(tiefs_regel.py), getrennt nach der Position des Tiefs in der laufenden
Abwaertsserie. Ausgewiesen wird p75, nicht der Median: die Schwelle soll
die Grenze des ueblichen Bereichs markieren, nicht seine Mitte.

KEINE Mindestfallzahl, KEINE Zusammenfassung duenner Zellen, KEINE
Pauschale (02.09.2026). Eine Tiefsposition mit vier Faellen bekommt ihre
Schwelle aus diesen vier Faellen. Dass es nur vier sind, ist das Ergebnis
und kein Mangel - der Wert erreicht diese Position eben selten. Genau das
steht als anteil_serien in der Datei: der Anteil der Abwaertsserien
dieses Wertes, die ueberhaupt so weit kamen. Ein Ersatz durch einen
gepoolten oder pauschalen Wert wuerde diese Information zerstoeren und
durch eine Zahl ersetzen, die fuer diesen Wert an dieser Position nie
gemessen wurde.

Kein Pooling ueber Werte (Entscheidung 77), kein Pooling ueber
Tiefspositionen.

Eingabe:  docs/puffer_je_tief.csv.gz   (eine Zeile je Tief, aus historie.py)
Ausgabe:  docs/rsi_schwellen.csv       (eine Zeile je Wert und Tiefsposition)

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

FELDER = ["ticker", "position", "faelle", "serien", "anteil_serien",
          "rsi_min", "rsi_p25", "rsi_median", "rsi_p75", "rsi_max"]


def verteilung(werte: np.ndarray) -> dict:
    """Volle Verteilung statt eines einzelnen Kennwerts - der p75 allein
    verschweigt, wie breit die Streuung an dieser Position ist."""
    return {
        "faelle": int(werte.size),
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
        # Jede Abwaertsserie hat genau ein Tief 1 - die Zahl der Tiefs an
        # Position 1 ist damit die Zahl der Serien dieses Wertes und der
        # richtige Nenner fuer die Seltenheit der spaeteren Positionen.
        serien = int((g["position"] == 1).sum())
        for pos, gp in g.groupby("position", sort=True):
            v = verteilung(gp["rsi"].to_numpy())
            zeilen.append({
                "ticker": ticker,
                "position": int(pos),
                "serien": serien,
                "anteil_serien": (round(v["faelle"] / serien * 100, 1)
                                  if serien else ""),
                **v,
            })

    os.makedirs(DOCS, exist_ok=True)
    with open(AUSGABE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER)
        w.writeheader()
        w.writerows(zeilen)

    tiefste = max(z["position"] for z in zeilen)
    print(f"{AUSGABE}: {len(zeilen)} Zeilen, {d['ticker'].nunique()} Werte, "
          f"{len(d)} Tiefs ausgewertet, tiefste Position {tiefste}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
