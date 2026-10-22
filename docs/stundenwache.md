# Stundenwache

Stand: 2026-10-21 · 272 Werte mit Stundendaten · erstellt 2026-10-22 10:01 UTC

> **Sitzung noch nicht abgeschlossen.** 60 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 4, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| HSBC | 13.65 | 13.646 | -0.013 | 1 |
| UBS | 38.62 | 38.61 | -0.012 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (10)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAN | 11.56 | 11.566 | 0.018 | 0 |
| CBK.DE | 36.2 | 36.29 | 0.097 | 0 |
| MDLZ | 62.38 | 62.745 | 0.295 | 0 |
| SBUX | 97.92 | 99.09 | 0.468 | 0 |
| MCD | 243.33 | 246.22 | 0.717 | 0 |
| ACN | 234.01 | 240.27 | 0.755 | 0 |
| VLO | 423.69 | 436.88 | 0.77 | 0 |
| CMCSA | 21.58 | 22.07 | 0.817 | 0 |
| ABT | 97.67 | 100.56 | 0.976 | 0 |
| BMO | 165.6 | 170.44 | 1.697 | 0 |

## Swing-Hoch ueberwunden (79)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| BRK-B | 507.24 | 540.87 | 5.696 | 7 |
| TRV | 362.75 | 398.81 | 4.647 | 7 |
| COP | 130.97 | 145.68 | 4.52 | 7 |
| COST | 931.09 | 998.18 | 4.422 | 7 |
| IBM | 224.51 | 251.48 | 4.367 | 7 |
| SO | 83.98 | 90.385 | 4.361 | 7 |
| CVX | 207.41 | 226.77 | 4.187 | 7 |
| XOM | 164.37 | 178.09 | 3.829 | 7 |
| CL | 87.22 | 93.405 | 3.785 | 7 |
| KO | 87.29 | 92.675 | 3.611 | 7 |
| NVS | 120.02 | 127.64 | 3.378 | 3 |
| SONY | 3797.0 | 4069.0 | 3.219 | 7 |
| KDP | 32.14 | 34.46 | 3.105 | 7 |
| DUK | 115.17 | 120.68 | 2.989 | 7 |
| MO | 69.6 | 73.83 | 2.897 | 7 |
| TM | 2944.5 | 3093.0 | 2.714 | 7 |
| PEP | 127.21 | 134.69 | 2.634 | 7 |
| WDAY | 185.82 | 202.9 | 2.583 | 7 |
| AEP | 121.8 | 127.37 | 2.458 | 7 |
| BTI | 42.42 | 44.36 | 2.36 | 3 |
| QIA.DE | 42.345 | 45.165 | 2.255 | 3 |
| BLK | 1092.92 | 1149.47 | 2.05 | 7 |
| CTSH | 64.74 | 69.52 | 2.046 | 7 |
| HNR1.DE | 270.8 | 279.6 | 2.033 | 3 |
| ZAL.DE | 24.73 | 26.1 | 1.905 | 3 |
| LLY | 1206.63 | 1272.2 | 1.724 | 7 |
| CDW | 150.34 | 158.31 | 1.682 | 7 |
| BNS | 91.66 | 94.0 | 1.631 | 7 |
| MMM | 167.95 | 174.69 | 1.629 | 7 |
| TD | 121.41 | 124.685 | 1.524 | 7 |
| GSK | 17.91 | 18.81 | 1.514 | 3 |
| ODFL | 182.91 | 188.9 | 1.406 | 7 |
| CNQ | 52.57 | 54.25 | 1.262 | 7 |
| TEAM | 214.77 | 225.5315 | 1.223 | 7 |
| MAR | 394.74 | 403.93 | 1.218 | 7 |
| SRT3.DE | 257.7 | 268.7 | 1.122 | 3 |
| SPGI | 433.67 | 443.09 | 1.072 | 7 |
| LIN | 492.1 | 500.47 | 1.049 | 7 |
| NXPI | 233.67 | 242.43 | 1.01 | 7 |
| SPCX | 151.01 | 159.27 | 1.0 | 7 |
| RTX | 187.41 | 191.59 | 0.954 | 7 |
| RY | 199.27 | 201.94 | 0.939 | 7 |
| EOAN.DE | 17.855 | 18.165 | 0.926 | 3 |
| CTAS | 216.8 | 220.08 | 0.848 | 7 |
| ADP | 290.12 | 294.5 | 0.811 | 7 |
| NOW | 148.14 | 153.12 | 0.806 | 7 |
| BMO | 168.14 | 170.44 | 0.806 | 7 |
| FAST | 51.39 | 52.49 | 0.758 | 7 |
| FDX | 294.29 | 298.21 | 0.741 | 7 |
| ROP | 391.01 | 397.3 | 0.727 | 7 |
| AXP | 319.85 | 323.69 | 0.66 | 7 |
| SAP.DE | 204.2 | 207.1 | 0.526 | 3 |
| ON | 75.07 | 76.94 | 0.52 | 7 |
| COF | 204.01 | 206.54 | 0.516 | 7 |
| VRTX | 517.68 | 524.41 | 0.51 | 5 |
| CM | 113.93 | 114.97 | 0.485 | 7 |
| MUV2.DE | 549.4 | 553.0 | 0.468 | 3 |
| MS | 184.83 | 187.11 | 0.458 | 3 |
| V | 404.74 | 408.02 | 0.453 | 7 |
| BNY | 144.42 | 145.85 | 0.449 | 7 |
| SY1.DE | 100.8 | 101.55 | 0.434 | 3 |
| BMW.DE | 56.42 | 57.04 | 0.433 | 3 |
| NVO | 260.4 | 262.8 | 0.425 | 4 |
| NVDA | 219.62 | 221.87 | 0.382 | 6 |
| ILMN | 278.59 | 282.87 | 0.272 | 6 |
| HON | 213.5 | 214.6 | 0.261 | 7 |
| CSGP | 32.65 | 32.905 | 0.244 | 7 |
| UNH | 414.12 | 416.97 | 0.217 | 7 |
| MRNA | 242.29 | 245.88 | 0.186 | 7 |
| XEL | 76.54 | 76.765 | 0.179 | 7 |
| DHR | 233.02 | 234.02 | 0.143 | 1 |
| BP | 6.227 | 6.2416 | 0.103 | 2 |
| BA | 191.9 | 192.29 | 0.098 | 3 |
| FANG | 200.65 | 200.92 | 0.054 | 6 |
| CVS | 93.35 | 93.46 | 0.049 | 7 |
| TXN | 284.47 | 284.85 | 0.039 | 6 |
| SHL.DE | 41.75 | 41.77 | 0.026 | 2 |
| PAYX | 112.52 | 112.56 | 0.018 | 6 |
| MA | 622.49 | 622.65 | 0.015 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.