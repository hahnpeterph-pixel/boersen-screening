# Stundenwache

Stand: 2026-09-30 · 273 Werte mit Stundendaten · erstellt 2026-10-01 11:30 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (2)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ABBV | 262.59 | 261.75 | -0.168 | 1 |
| FAST | 49.53 | 49.53 | -0.0 | 1 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 182.26 | 186.46 | 0.817 | 1 |

## Tief angetestet (16)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| WMT | 103.92 | 103.925 | 0.002 | 0 |
| NVO | 37.89 | 37.905 | 0.013 | 0 |
| BAC | 54.39 | 54.41 | 0.015 | 0 |
| ROST | 233.31 | 233.4 | 0.019 | 0 |
| BRK-B | 497.95 | 498.19 | 0.04 | 0 |
| CTAS | 194.83 | 195.1 | 0.064 | 0 |
| AMT | 163.35 | 163.66 | 0.082 | 0 |
| SHW | 322.42 | 323.43 | 0.125 | 0 |
| HDB | 22.26 | 22.34 | 0.137 | 0 |
| WFC | 79.82 | 80.11 | 0.138 | 0 |
| USB | 57.56 | 57.76 | 0.162 | 0 |
| VZ | 45.73 | 45.905 | 0.168 | 0 |
| NKE | 35.16 | 35.39 | 0.254 | 0 |
| SRT3.DE | 255.4 | 257.7 | 0.276 | 0 |
| MO | 66.91 | 67.33 | 0.316 | 0 |
| MUV2.DE | 492.2 | 497.1 | 0.591 | 0 |

## Swing-Hoch ueberwunden (19)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.935 | 5.657 | 7 |
| SHOP | 134.74 | 148.43 | 2.025 | 7 |
| MTX.DE | 358.8 | 376.1 | 1.839 | 5 |
| ILMN | 250.06 | 273.7 | 1.815 | 7 |
| KLAC | 182.41 | 195.03 | 1.792 | 7 |
| AMAT | 487.68 | 511.67 | 1.293 | 7 |
| LIN | 466.24 | 474.65 | 1.204 | 7 |
| LRCX | 317.13 | 328.61 | 0.847 | 7 |
| TMO | 663.57 | 675.19 | 0.758 | 7 |
| WDAY | 185.82 | 190.45 | 0.675 | 7 |
| LLY | 1138.79 | 1159.3101 | 0.644 | 7 |
| ON | 74.48 | 76.85 | 0.639 | 7 |
| AMGN | 415.76 | 421.49 | 0.624 | 7 |
| TSM | 452.88 | 456.28 | 0.34 | 7 |
| MSFT | 509.44 | 512.96 | 0.296 | 7 |
| ISRG | 404.44 | 406.66 | 0.21 | 7 |
| MAR | 354.63 | 355.77 | 0.154 | 7 |
| CRWD | 263.87 | 264.73 | 0.067 | 7 |
| PANW | 396.3 | 397.4 | 0.058 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.