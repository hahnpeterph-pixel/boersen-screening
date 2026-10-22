# Stundenwache

Stand: 2026-10-21 · 272 Werte mit Stundendaten · erstellt 2026-10-22 00:45 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (1)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CCEP | 110.27 | 110.23 | -0.019 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (31)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ROST | 233.98 | 234.18 | 0.036 | 0 |
| AMT | 177.145 | 177.62 | 0.095 | 0 |
| DXCM | 79.92 | 80.25 | 0.12 | 0 |
| LRCX | 259.06 | 260.81 | 0.124 | 0 |
| GEHC | 68.71 | 68.995 | 0.163 | 0 |
| BKNG | 156.93 | 158.33 | 0.288 | 0 |
| GE | 293.525 | 295.835 | 0.288 | 0 |
| MDLZ | 62.376 | 62.745 | 0.298 | 0 |
| APP | 264.08 | 267.84 | 0.313 | 0 |
| ABBV | 282.155 | 284.72 | 0.35 | 0 |
| DTE.DE | 25.31 | 25.58 | 0.402 | 0 |
| LOW | 194.485 | 196.55 | 0.433 | 0 |
| BNR.DE | 62.16 | 62.71 | 0.438 | 0 |
| IDXX | 547.6 | 553.23 | 0.44 | 0 |
| MCK | 1005.42 | 1015.5 | 0.453 | 0 |
| WMT | 116.63 | 117.73 | 0.463 | 0 |
| SBUX | 97.92 | 99.09 | 0.468 | 0 |
| JNJ | 254.56 | 257.7 | 0.492 | 0 |
| NFLX | 64.1 | 65.0475 | 0.493 | 0 |
| SNDK | 1327.62 | 1378.3 | 0.562 | 0 |
| CB | 351.61 | 355.02 | 0.569 | 0 |
| MPC | 458.6919 | 468.27 | 0.577 | 0 |
| EQNR | 426.3 | 432.6 | 0.667 | 0 |
| MCD | 243.3292 | 246.22 | 0.717 | 0 |
| ACN | 234.01 | 240.27 | 0.755 | 0 |
| VLO | 423.685 | 436.88 | 0.77 | 0 |
| PAH3.DE | 24.82 | 25.35 | 0.784 | 0 |
| ABT | 97.67 | 100.56 | 0.976 | 0 |
| ADS.DE | 155.95 | 160.9 | 1.37 | 0 |
| BMO | 165.6 | 170.44 | 1.697 | 0 |
| DHR | 217.56 | 234.02 | 2.356 | 0 |

## Swing-Hoch ueberwunden (84)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| BRK-B | 507.24 | 540.87 | 5.696 | 7 |
| TRV | 362.75 | 398.81 | 4.647 | 7 |
| COP | 130.97 | 145.68 | 4.521 | 7 |
| COST | 931.09 | 998.18 | 4.422 | 7 |
| IBM | 224.51 | 251.48 | 4.367 | 7 |
| SO | 83.98 | 90.385 | 4.363 | 7 |
| CVX | 207.41 | 226.77 | 4.187 | 7 |
| XOM | 164.37 | 178.09 | 3.829 | 7 |
| SONY | 3797.0 | 4114.0 | 3.793 | 1 |
| CL | 87.22 | 93.405 | 3.784 | 7 |
| KO | 87.29 | 92.675 | 3.611 | 7 |
| KDP | 32.14 | 34.46 | 3.105 | 7 |
| DUK | 115.17 | 120.68 | 2.993 | 7 |
| NVS | 120.02 | 127.04 | 2.966 | 9 |
| MO | 69.6 | 73.83 | 2.901 | 7 |
| TM | 2944.5 | 3089.0 | 2.641 | 1 |
| PEP | 127.21 | 134.69 | 2.634 | 7 |
| WDAY | 185.82 | 202.9 | 2.583 | 7 |
| AEP | 121.8 | 127.37 | 2.458 | 7 |
| BLK | 1092.92 | 1149.47 | 2.051 | 7 |
| CTSH | 64.74 | 69.52 | 2.048 | 7 |
| LLY | 1206.63 | 1272.2 | 1.726 | 7 |
| CDW | 150.34 | 158.31 | 1.683 | 7 |
| BTI | 42.42 | 43.78 | 1.662 | 9 |
| BNS | 91.66 | 94.0 | 1.631 | 7 |
| MMM | 167.95 | 174.69 | 1.629 | 7 |
| TD | 121.41 | 124.685 | 1.525 | 7 |
| ZAL.DE | 24.73 | 25.79 | 1.48 | 9 |
| ODFL | 182.91 | 188.9 | 1.407 | 7 |
| HNR1.DE | 270.8 | 277.2 | 1.378 | 9 |
| GSK | 17.91 | 18.74 | 1.374 | 9 |
| CNQ | 52.57 | 54.25 | 1.262 | 7 |
| TEAM | 214.77 | 225.5315 | 1.223 | 7 |
| MAR | 394.74 | 403.93 | 1.218 | 7 |
| SPGI | 433.67 | 443.09 | 1.072 | 7 |
| EOAN.DE | 17.855 | 18.23 | 1.052 | 9 |
| LIN | 492.1 | 500.47 | 1.049 | 7 |
| NXPI | 233.67 | 242.43 | 1.01 | 7 |
| SPCX | 151.01 | 159.27 | 1.0 | 7 |
| RTX | 187.41 | 191.59 | 0.954 | 7 |
| RY | 199.27 | 201.94 | 0.939 | 7 |
| IBN | 1360.8 | 1385.0 | 0.859 | 7 |
| CTAS | 216.8 | 220.08 | 0.848 | 7 |
| SAP.DE | 204.2 | 208.55 | 0.808 | 7 |
| NOW | 148.14 | 153.12 | 0.806 | 7 |
| BMO | 168.14 | 170.44 | 0.806 | 7 |
| FAST | 51.39 | 52.49 | 0.758 | 7 |
| ADP | 290.12 | 294.13 | 0.743 | 6 |
| FDX | 294.29 | 298.21 | 0.741 | 7 |
| ROP | 391.01 | 397.3 | 0.727 | 7 |
| AXP | 319.85 | 323.69 | 0.66 | 7 |
| HEI.DE | 145.65 | 147.85 | 0.618 | 7 |
| ON | 75.07 | 76.94 | 0.52 | 7 |
| COF | 204.01 | 206.54 | 0.516 | 7 |
| VRTX | 517.68 | 524.41 | 0.512 | 5 |
| CM | 113.93 | 114.97 | 0.508 | 7 |
| MS | 184.83 | 187.11 | 0.458 | 3 |
| BMW.DE | 56.42 | 57.08 | 0.457 | 9 |
| V | 404.74 | 408.02 | 0.453 | 7 |
| BNY | 144.42 | 145.85 | 0.449 | 7 |
| QIA.DE | 42.345 | 42.9 | 0.426 | 9 |
| SNY | 73.04 | 73.7 | 0.405 | 9 |
| NVDA | 219.62 | 221.87 | 0.382 | 6 |
| SRT3.DE | 257.7 | 261.2 | 0.38 | 8 |
| ADS.DE | 159.65 | 160.9 | 0.346 | 8 |
| MRK.DE | 142.6 | 143.7 | 0.322 | 9 |
| ILMN | 278.59 | 282.87 | 0.272 | 6 |
| HON | 213.5 | 214.6 | 0.261 | 7 |
| CSGP | 32.65 | 32.905 | 0.244 | 7 |
| MUV2.DE | 549.4 | 551.4 | 0.235 | 3 |
| NVO | 260.4 | 261.7 | 0.226 | 3 |
| UNH | 414.12 | 416.97 | 0.217 | 7 |
| MRNA | 242.29 | 245.88 | 0.186 | 7 |
| XEL | 76.54 | 76.765 | 0.179 | 7 |
| ALV.DE | 435.2 | 436.3 | 0.177 | 4 |
| TMO | 694.33 | 698.145 | 0.171 | 5 |
| DHR | 233.02 | 234.02 | 0.143 | 1 |
| SY1.DE | 100.8 | 101.0 | 0.116 | 5 |
| BA | 191.9 | 192.29 | 0.098 | 3 |
| FANG | 200.65 | 200.92 | 0.054 | 6 |
| CVS | 93.35 | 93.46 | 0.049 | 7 |
| TXN | 284.47 | 284.85 | 0.039 | 6 |
| PAYX | 112.52 | 112.56 | 0.018 | 6 |
| MA | 622.49 | 622.65 | 0.015 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.