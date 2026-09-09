# Stundenwache

Stand: 2026-09-08 · 158 Werte mit Stundendaten · erstellt 2026-09-09 00:14 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (50)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AMGN | 435.0 | 393.23 | -4.497 | 7 |
| HNR1.DE | 260.4 | 248.0 | -4.0 | 9 |
| BKNG | 192.19 | 180.31 | -1.953 | 7 |
| PAYX | 121.65 | 116.92 | -1.71 | 7 |
| ADP | 276.45 | 268.32 | -1.48 | 6 |
| MUV2.DE | 511.4 | 501.8 | -1.369 | 9 |
| ABNB | 181.16 | 174.534 | -1.364 | 7 |
| DASH | 211.18 | 200.38 | -1.358 | 7 |
| DXCM | 87.65 | 84.52 | -1.336 | 7 |
| BIIB | 219.82 | 212.41 | -1.313 | 7 |
| VRTX | 544.48 | 528.88 | -1.252 | 7 |
| VRSK | 182.5 | 175.5 | -1.199 | 7 |
| CTSH | 62.29 | 59.93 | -1.145 | 7 |
| ISRG | 363.23 | 350.17 | -1.134 | 7 |
| GEHC | 68.485 | 66.78 | -1.092 | 7 |
| LIN | 476.48 | 468.23 | -1.087 | 7 |
| TEAM | 186.54 | 176.42 | -1.057 | 7 |
| ROP | 405.57 | 395.58 | -0.985 | 7 |
| SBUX | 104.36 | 102.005 | -0.948 | 7 |
| V | 373.64 | 368.83 | -0.765 | 7 |
| REGN | 825.83 | 810.32 | -0.763 | 7 |
| CRM | 257.82 | 249.22 | -0.75 | 7 |
| JNJ | 273.16 | 269.15 | -0.719 | 7 |
| INTU | 330.12 | 318.83 | -0.714 | 7 |
| PDD | 81.27 | 79.76 | -0.663 | 7 |
| ADBE | 263.93 | 257.25 | -0.637 | 7 |
| MELI | 1966.0 | 1925.5699 | -0.625 | 7 |
| NFLX | 78.23 | 76.78 | -0.623 | 7 |
| MSFT | 499.36 | 494.02 | -0.529 | 7 |
| GILD | 148.41 | 146.6 | -0.49 | 7 |
| CHTR | 149.47 | 145.745 | -0.48 | 7 |
| MNST | 43.65 | 43.15 | -0.468 | 7 |
| ORLY | 86.65 | 85.88 | -0.417 | 7 |
| MDB | 365.9 | 356.0 | -0.411 | 7 |
| ADSK | 216.2 | 212.21 | -0.36 | 7 |
| MAR | 331.14 | 328.82 | -0.353 | 7 |
| ZS | 165.06 | 161.94 | -0.33 | 7 |
| AZN | 161.13 | 160.03 | -0.309 | 6 |
| CDNS | 287.9 | 284.27 | -0.308 | 3 |
| QIA.DE | 36.845 | 36.485 | -0.276 | 9 |
| WBD | 28.21 | 28.13 | -0.247 | 5 |
| COST | 914.54 | 910.13 | -0.245 | 7 |
| SHW | 327.78 | 326.19 | -0.22 | 6 |
| AAPL | 317.86 | 316.35 | -0.203 | 7 |
| HD | 315.21 | 313.72 | -0.203 | 3 |
| IDXX | 522.05 | 520.21 | -0.123 | 2 |
| ON | 71.41 | 71.1 | -0.112 | 1 |
| MRK.DE | 135.1 | 134.9 | -0.078 | 4 |
| CMCSA | 26.38 | 26.34 | -0.067 | 7 |
| DIS | 105.17 | 105.085 | -0.037 | 7 |

## Tief zurueckerobert (15)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CSGP | 30.32 | 30.32 | 0.0 | 4 |
| IBM | 231.68 | 232.125 | 0.081 | 2 |
| SAP.DE | 180.72 | 181.44 | 0.129 | 1 |
| SRT3.DE | 237.2 | 238.4 | 0.153 | 4 |
| ALV.DE | 444.1 | 444.9 | 0.154 | 6 |
| DDOG | 208.22 | 210.19 | 0.167 | 3 |
| ADS.DE | 146.85 | 147.5 | 0.177 | 2 |
| GOOGL | 337.09 | 338.43 | 0.203 | 1 |
| TTWO | 211.33 | 213.21 | 0.218 | 1 |
| KHC | 24.74 | 24.89 | 0.231 | 2 |
| TMUS | 180.65 | 181.66 | 0.247 | 3 |
| VNA.DE | 18.66 | 18.77 | 0.307 | 1 |
| RHM.DE | 1032.0 | 1051.8 | 0.547 | 3 |
| MDLZ | 60.91 | 61.63 | 0.597 | 1 |
| UNH | 395.2 | 400.87 | 0.745 | 2 |

## Tief angetestet (16)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AXP | 325.68 | 326.11 | 0.076 | 0 |
| MCD | 255.49 | 255.82 | 0.077 | 0 |
| NKE | 37.97 | 38.1036 | 0.126 | 0 |
| SY1.DE | 90.0 | 90.32 | 0.187 | 0 |
| HEI.DE | 160.45 | 161.5 | 0.236 | 0 |
| KO | 87.85 | 88.41 | 0.389 | 0 |
| TRV | 363.21 | 365.7 | 0.4 | 0 |
| VZ | 50.08 | 50.4 | 0.42 | 0 |
| PEP | 137.43 | 138.44 | 0.445 | 0 |
| DB1.DE | 277.8 | 280.1 | 0.483 | 0 |
| EXC | 43.51 | 43.955 | 0.533 | 0 |
| MMM | 165.8 | 167.53 | 0.553 | 0 |
| SHL.DE | 38.52 | 38.95 | 0.652 | 0 |
| BEI.DE | 75.34 | 76.82 | 0.977 | 0 |
| BNR.DE | 60.4 | 61.88 | 1.052 | 0 |
| BAS.DE | 52.69 | 53.68 | 1.056 | 0 |

## Swing-Hoch ueberwunden (22)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 140.34 | 3.282 | 7 |
| INTC | 93.7 | 104.4401 | 2.527 | 7 |
| AMD | 462.21 | 505.53 | 2.344 | 7 |
| CBK.DE | 41.05 | 42.77 | 2.051 | 9 |
| VOW3.DE | 78.36 | 83.1 | 1.895 | 9 |
| CEG | 285.26 | 298.96 | 1.426 | 7 |
| ORCL | 153.99 | 162.52 | 1.372 | 7 |
| META | 593.34 | 613.31 | 1.068 | 7 |
| DBK.DE | 35.03 | 35.73 | 0.953 | 8 |
| PAH3.DE | 28.76 | 29.36 | 0.814 | 9 |
| BMW.DE | 62.72 | 63.9 | 0.781 | 9 |
| AEP | 123.85 | 125.4 | 0.743 | 7 |
| QCOM | 170.6 | 174.09 | 0.681 | 7 |
| MU | 969.44 | 999.94 | 0.653 | 7 |
| BKR | 63.02 | 63.91 | 0.583 | 7 |
| KLAC | 186.78 | 189.04 | 0.295 | 7 |
| ADI | 360.77 | 363.3 | 0.23 | 7 |
| CDW | 142.97 | 144.45 | 0.224 | 7 |
| MBG.DE | 47.75 | 47.915 | 0.171 | 9 |
| XEL | 76.63 | 76.831 | 0.149 | 4 |
| TXN | 258.04 | 258.905 | 0.109 | 3 |
| WDAY | 185.82 | 186.2 | 0.044 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.