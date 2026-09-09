# Stundenwache

Stand: 2026-09-08 · 158 Werte mit Stundendaten · erstellt 2026-09-09 04:56 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (4)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| HNR1.DE | 260.4 | 248.0 | -4.0 | 9 |
| MUV2.DE | 511.4 | 501.8 | -1.369 | 9 |
| QIA.DE | 36.845 | 36.485 | -0.276 | 9 |
| MRK.DE | 135.1 | 134.9 | -0.078 | 4 |

## Tief zurueckerobert (6)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 180.72 | 181.44 | 0.129 | 1 |
| SRT3.DE | 237.2 | 238.4 | 0.153 | 4 |
| ALV.DE | 444.1 | 444.9 | 0.154 | 6 |
| ADS.DE | 146.85 | 147.5 | 0.177 | 2 |
| VNA.DE | 18.66 | 18.77 | 0.307 | 1 |
| RHM.DE | 1032.0 | 1051.8 | 0.547 | 3 |

## Tief angetestet (24)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PCAR | 122.4 | 122.47 | 0.027 | 0 |
| PYPL | 53.03 | 53.19 | 0.075 | 0 |
| MAR | 328.24 | 328.82 | 0.086 | 0 |
| ILMN | 210.15 | 211.11 | 0.091 | 0 |
| PAYX | 116.48 | 116.92 | 0.154 | 0 |
| SY1.DE | 90.0 | 90.32 | 0.187 | 0 |
| V | 367.44 | 368.83 | 0.222 | 0 |
| COST | 906.1 | 910.13 | 0.232 | 0 |
| HEI.DE | 160.45 | 161.5 | 0.236 | 0 |
| ABNB | 173.033 | 174.534 | 0.296 | 0 |
| KDP | 32.35 | 32.55 | 0.3 | 0 |
| CSCO | 108.48 | 109.13 | 0.334 | 0 |
| ADSK | 208.09 | 212.21 | 0.374 | 0 |
| DB1.DE | 277.8 | 280.1 | 0.483 | 0 |
| CSGP | 29.66 | 30.32 | 0.494 | 0 |
| TRV | 362.57 | 365.7 | 0.5 | 0 |
| DDOG | 203.24 | 210.19 | 0.592 | 0 |
| SHL.DE | 38.52 | 38.95 | 0.652 | 0 |
| VZ | 49.77 | 50.4 | 0.832 | 0 |
| MDLZ | 60.47 | 61.63 | 0.946 | 0 |
| BEI.DE | 75.34 | 76.82 | 0.977 | 0 |
| BNR.DE | 60.4 | 61.88 | 1.052 | 0 |
| BAS.DE | 52.69 | 53.68 | 1.056 | 0 |
| UNH | 390.44 | 400.87 | 1.273 | 0 |

## Swing-Hoch ueberwunden (21)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 140.34 | 3.227 | 7 |
| INTC | 93.7 | 104.4401 | 2.443 | 7 |
| AMD | 462.21 | 505.53 | 2.311 | 7 |
| CBK.DE | 41.05 | 42.77 | 2.051 | 9 |
| VOW3.DE | 78.36 | 83.1 | 1.895 | 9 |
| CEG | 285.26 | 298.96 | 1.488 | 7 |
| ORCL | 153.99 | 162.52 | 1.262 | 7 |
| META | 593.34 | 613.31 | 1.114 | 7 |
| DBK.DE | 35.03 | 35.73 | 0.953 | 8 |
| PAH3.DE | 28.76 | 29.36 | 0.814 | 9 |
| BMW.DE | 62.72 | 63.9 | 0.781 | 9 |
| AEP | 123.85 | 125.4 | 0.75 | 7 |
| MU | 969.44 | 999.94 | 0.698 | 7 |
| QCOM | 170.6 | 174.09 | 0.603 | 7 |
| BKR | 63.02 | 63.91 | 0.572 | 7 |
| KLAC | 186.78 | 189.04 | 0.321 | 7 |
| ADI | 360.77 | 363.3 | 0.253 | 7 |
| MBG.DE | 47.75 | 47.915 | 0.171 | 9 |
| XEL | 76.63 | 76.831 | 0.15 | 4 |
| TXN | 258.04 | 258.905 | 0.119 | 3 |
| WDAY | 185.82 | 186.2 | 0.042 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.