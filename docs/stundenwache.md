# Stundenwache

Stand: 2026-10-14 · 272 Werte mit Stundendaten · erstellt 2026-10-15 00:56 UTC

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
| SKHY | 1304000.0 | 1298000.0 | -0.073 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (39)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ENR.DE | 135.56 | 135.7 | 0.027 | 0 |
| DDOG | 268.37 | 269.38 | 0.081 | 0 |
| SNOW | 333.91 | 335.08 | 0.081 | 0 |
| INTC | 97.67 | 98.11 | 0.083 | 0 |
| PAH3.DE | 24.48 | 24.55 | 0.098 | 0 |
| CEG | 277.83 | 279.62 | 0.11 | 0 |
| CRWD | 248.0306 | 249.345 | 0.119 | 0 |
| HEI.DE | 140.65 | 141.25 | 0.145 | 0 |
| META | 734.2865 | 738.0 | 0.165 | 0 |
| SPCX | 151.101 | 152.23 | 0.165 | 0 |
| DELL | 502.3432 | 507.57 | 0.183 | 0 |
| DBK.DE | 29.41 | 29.61 | 0.254 | 0 |
| SPG | 197.86 | 198.7 | 0.284 | 0 |
| ANET | 193.3001 | 195.39 | 0.296 | 0 |
| CRM | 233.59 | 235.99 | 0.298 | 0 |
| CDNS | 325.85 | 329.53 | 0.319 | 0 |
| TSLA | 363.82 | 367.31 | 0.319 | 0 |
| SPGI | 405.85 | 408.6 | 0.366 | 0 |
| ADSK | 228.59 | 231.24 | 0.368 | 0 |
| PDD | 80.725 | 81.41 | 0.368 | 0 |
| SCCO | 198.12 | 200.74 | 0.401 | 0 |
| UBER | 68.625 | 69.3 | 0.415 | 0 |
| SYK | 278.58 | 281.63 | 0.422 | 0 |
| GEV | 922.24 | 941.76 | 0.49 | 0 |
| NEM | 109.84 | 111.54 | 0.518 | 0 |
| ORLY | 85.89 | 86.69 | 0.522 | 0 |
| NKE | 34.71 | 35.315 | 0.528 | 0 |
| USB | 55.7 | 56.29 | 0.581 | 0 |
| DASH | 178.995 | 183.92 | 0.63 | 0 |
| RY | 191.59 | 193.79 | 0.771 | 0 |
| CM | 108.87 | 110.44 | 0.794 | 0 |
| TD | 115.87 | 117.64 | 0.879 | 0 |
| SCHW | 95.06 | 96.77 | 0.986 | 0 |
| MUV2.DE | 522.8 | 531.4 | 1.103 | 0 |
| DTE.DE | 24.56 | 25.31 | 1.135 | 0 |
| MS | 176.44 | 181.6 | 1.142 | 0 |
| JPM | 326.4 | 335.315 | 1.5 | 0 |
| BAC | 49.26 | 51.41 | 1.735 | 0 |
| FAST | 49.54 | 52.01 | 1.948 | 0 |

## Swing-Hoch ueberwunden (90)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| PBR | 54.61 | 65.28 | 5.531 | 7 |
| MPC | 398.33 | 484.8 | 5.356 | 7 |
| WMT | 105.14 | 116.2 | 4.764 | 7 |
| PSX | 259.11 | 297.29 | 4.469 | 7 |
| SO | 83.98 | 89.38 | 4.013 | 7 |
| VLO | 395.85 | 459.89 | 3.966 | 7 |
| XOM | 164.37 | 177.06 | 3.95 | 7 |
| COP | 130.97 | 142.37 | 3.849 | 7 |
| CL | 87.22 | 92.8 | 3.803 | 7 |
| BRK-B | 507.24 | 526.79 | 3.796 | 7 |
| BNR.DE | 60.28 | 64.58 | 3.618 | 9 |
| KO | 87.29 | 91.8 | 3.563 | 7 |
| CVX | 207.41 | 222.14 | 3.52 | 7 |
| XEL | 71.37 | 75.385 | 3.31 | 7 |
| MA | 571.35 | 603.37 | 3.264 | 7 |
| BP | 5.64 | 6.134 | 3.229 | 9 |
| MCK | 907.07 | 977.28 | 3.021 | 7 |
| COST | 931.09 | 981.97 | 2.989 | 7 |
| CNQ | 48.28 | 51.835 | 2.982 | 7 |
| DUK | 115.17 | 119.66 | 2.974 | 7 |
| SHEL | 36.815 | 39.07 | 2.962 | 9 |
| PG | 149.2 | 156.525 | 2.846 | 7 |
| SY1.DE | 92.68 | 97.26 | 2.715 | 9 |
| FANG | 186.18 | 197.48 | 2.692 | 7 |
| MO | 69.6 | 73.155 | 2.684 | 7 |
| TRV | 362.75 | 377.9 | 2.54 | 7 |
| ADP | 266.46 | 279.085 | 2.418 | 6 |
| PM | 195.22 | 205.6 | 2.337 | 7 |
| MDT | 88.5 | 94.23 | 2.31 | 7 |
| AEP | 121.8 | 126.2 | 2.261 | 7 |
| CTAS | 201.45 | 208.61 | 2.222 | 7 |
| V | 377.17 | 391.51 | 2.174 | 7 |
| VRSK | 171.31 | 180.635 | 2.139 | 7 |
| SHL.DE | 38.13 | 39.94 | 2.129 | 9 |
| CCEP | 103.27 | 107.26 | 2.122 | 7 |
| CB | 339.66 | 350.17 | 1.978 | 7 |
| PFE | 28.17 | 29.225 | 1.833 | 7 |
| SAP.DE | 187.8 | 197.44 | 1.78 | 9 |
| ADS.DE | 148.4 | 154.2 | 1.735 | 9 |
| HEN3.DE | 75.6 | 77.62 | 1.582 | 9 |
| MAR | 362.46 | 371.88 | 1.423 | 7 |
| DB1.DE | 296.8 | 303.5 | 1.35 | 9 |
| PAYX | 105.66 | 108.38 | 1.324 | 7 |
| EQNR | 419.3 | 432.7 | 1.314 | 8 |
| ABBV | 274.94 | 283.525 | 1.305 | 7 |
| EXC | 41.8 | 42.62 | 1.228 | 7 |
| TM | 2944.5 | 3007.0 | 1.214 | 1 |
| GEHC | 66.55 | 68.49 | 1.201 | 7 |
| KDP | 32.14 | 33.125 | 1.122 | 7 |
| TJX | 139.62 | 142.79 | 1.119 | 7 |
| UNH | 383.48 | 395.755 | 1.098 | 7 |
| MCD | 234.3 | 238.26 | 1.07 | 7 |
| AMGN | 415.79 | 426.32 | 1.02 | 7 |
| NVS | 120.02 | 122.4 | 0.998 | 9 |
| ROP | 365.24 | 372.51 | 0.915 | 7 |
| MRK | 144.15 | 147.37 | 0.907 | 7 |
| ABT | 100.95 | 102.98 | 0.878 | 7 |
| CSX | 47.73 | 48.3 | 0.853 | 7 |
| PEP | 127.21 | 129.31 | 0.848 | 7 |
| BEI.DE | 80.08 | 81.12 | 0.68 | 9 |
| LMT | 515.77 | 522.37 | 0.673 | 6 |
| IBM | 224.51 | 227.96 | 0.634 | 7 |
| MNST | 43.64 | 44.24 | 0.631 | 6 |
| ENB | 46.94 | 47.35 | 0.597 | 7 |
| ROST | 227.6 | 230.61 | 0.596 | 6 |
| ALV.DE | 423.7 | 426.6 | 0.511 | 5 |
| WDAY | 185.82 | 188.85 | 0.499 | 5 |
| GSK | 17.91 | 18.1325 | 0.498 | 2 |
| FAST | 51.39 | 52.01 | 0.489 | 6 |
| ABNB | 164.91 | 167.06 | 0.477 | 7 |
| AZN | 121.8 | 123.2 | 0.472 | 3 |
| REGN | 768.66 | 779.26 | 0.47 | 6 |
| GILD | 152.26 | 153.555 | 0.363 | 5 |
| MDLZ | 62.19 | 62.58 | 0.342 | 6 |
| ODFL | 182.91 | 184.38 | 0.33 | 3 |
| BTI | 42.42 | 42.63 | 0.256 | 9 |
| EOAN.DE | 17.22 | 17.3 | 0.238 | 8 |
| SHW | 322.85 | 324.55 | 0.225 | 3 |
| AAPL | 341.57 | 343.04 | 0.223 | 7 |
| KHC | 22.59 | 22.7 | 0.209 | 7 |
| CVS | 89.93 | 90.44 | 0.209 | 4 |
| NEE | 78.16 | 78.4 | 0.181 | 5 |
| LLY | 1206.63 | 1210.84 | 0.123 | 7 |
| LIN | 492.1 | 493.04 | 0.117 | 2 |
| GOOGL | 347.03 | 347.87 | 0.104 | 7 |
| RHM.DE | 987.1 | 989.4 | 0.078 | 2 |
| MMM | 164.3 | 164.53 | 0.068 | 1 |
| BAS.DE | 52.26 | 52.32 | 0.054 | 8 |
| DHL.DE | 56.84 | 56.88 | 0.042 | 3 |
| BABA | 110.4 | 110.5 | 0.028 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.