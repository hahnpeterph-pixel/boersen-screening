# Stundenwache

Stand: 2026-10-16 · 272 Werte mit Stundendaten · erstellt 2026-10-16 22:02 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| AXON | 395.75 | 390.31 | -0.326 | 3 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (4)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| KLAC | 165.28 | 165.75 | 0.058 | 0 |
| MRVL | 226.62 | 227.76 | 0.069 | 0 |
| PLD | 124.9 | 125.71 | 0.273 | 0 |
| SNPS | 448.19 | 454.79 | 0.304 | 0 |

## Swing-Hoch ueberwunden (122)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| PBR | 54.61 | 66.17 | 5.849 | 7 |
| WMT | 105.14 | 118.81 | 5.394 | 7 |
| COP | 130.97 | 146.505 | 5.09 | 7 |
| SO | 83.98 | 91.15 | 4.831 | 7 |
| CCEP | 103.27 | 112.44 | 4.559 | 7 |
| KO | 87.29 | 93.86 | 4.527 | 7 |
| BRK-B | 507.24 | 532.12 | 4.421 | 7 |
| MA | 571.35 | 617.38 | 4.283 | 7 |
| CL | 87.22 | 94.075 | 4.209 | 7 |
| XOM | 164.37 | 178.98 | 4.154 | 7 |
| SHL.DE | 38.13 | 41.49 | 4.101 | 9 |
| MCK | 907.07 | 1005.38 | 4.041 | 7 |
| BNR.DE | 60.28 | 64.96 | 4.02 | 9 |
| XEL | 71.37 | 76.305 | 3.923 | 7 |
| CVX | 207.41 | 224.98 | 3.901 | 7 |
| PG | 149.2 | 159.33 | 3.842 | 7 |
| VRSK | 171.31 | 190.89 | 3.841 | 7 |
| ADP | 266.46 | 287.12 | 3.717 | 6 |
| MO | 69.6 | 75.105 | 3.711 | 7 |
| SY1.DE | 92.68 | 99.32 | 3.707 | 9 |
| COST | 931.09 | 989.11 | 3.618 | 7 |
| DUK | 115.17 | 121.46 | 3.594 | 7 |
| V | 377.17 | 402.58 | 3.551 | 7 |
| MAR | 362.46 | 388.03 | 3.462 | 7 |
| TRV | 362.75 | 389.15 | 3.462 | 7 |
| SHEL | 36.815 | 39.38 | 3.39 | 9 |
| MUV2.DE | 516.2 | 545.6 | 3.39 | 9 |
| LMT | 515.77 | 551.86 | 3.366 | 7 |
| CTAS | 201.45 | 213.71 | 3.364 | 7 |
| CB | 339.66 | 359.76 | 3.309 | 7 |
| ADS.DE | 148.4 | 158.6 | 3.084 | 9 |
| RHM.DE | 987.1 | 1095.4 | 3.082 | 9 |
| KDP | 32.14 | 34.635 | 2.894 | 7 |
| TJX | 139.62 | 147.33 | 2.701 | 7 |
| PAYX | 105.66 | 111.65 | 2.678 | 7 |
| TM | 2944.5 | 3093.0 | 2.637 | 7 |
| MDT | 88.5 | 94.77 | 2.482 | 7 |
| PFE | 28.17 | 29.57 | 2.435 | 7 |
| AEP | 121.8 | 127.12 | 2.389 | 7 |
| DB1.DE | 296.8 | 309.3 | 2.374 | 9 |
| BTI | 42.42 | 44.63 | 2.307 | 9 |
| EXC | 41.8 | 43.5 | 2.295 | 7 |
| MNST | 43.64 | 45.73 | 2.224 | 7 |
| MCD | 234.3 | 242.92 | 2.156 | 7 |
| CSGP | 30.16 | 32.3 | 2.126 | 7 |
| SONY | 3797.0 | 3971.0 | 2.093 | 7 |
| SAP.DE | 187.8 | 199.02 | 2.031 | 9 |
| ROP | 365.24 | 382.615 | 2.009 | 7 |
| HD | 296.6 | 309.66 | 1.984 | 7 |
| KHC | 22.59 | 23.695 | 1.937 | 7 |
| PM | 195.22 | 204.97 | 1.937 | 7 |
| ABNB | 164.91 | 173.69 | 1.912 | 7 |
| NVS | 120.02 | 124.64 | 1.856 | 9 |
| IDXX | 536.84 | 560.5 | 1.817 | 7 |
| RTX | 187.41 | 193.92 | 1.803 | 7 |
| AIR.DE | 192.0 | 199.3 | 1.733 | 9 |
| EOAN.DE | 17.22 | 17.815 | 1.732 | 9 |
| ROST | 227.6 | 236.88 | 1.73 | 7 |
| GEHC | 66.55 | 69.57 | 1.718 | 7 |
| HONA | 160.0 | 168.14 | 1.673 | 7 |
| ABT | 100.95 | 104.89 | 1.656 | 7 |
| ALV.DE | 423.7 | 433.7 | 1.655 | 9 |
| SPGI | 416.02 | 429.74 | 1.653 | 7 |
| BLK | 1092.92 | 1133.86 | 1.572 | 7 |
| LOW | 190.0 | 197.345 | 1.533 | 7 |
| ABBV | 274.94 | 285.38 | 1.514 | 7 |
| ENB | 46.94 | 48.1 | 1.513 | 7 |
| PEP | 127.21 | 131.5 | 1.505 | 7 |
| SHW | 322.85 | 334.98 | 1.497 | 7 |
| DHL.DE | 56.84 | 58.32 | 1.495 | 9 |
| EQNR | 419.3 | 433.5 | 1.45 | 8 |
| CSX | 47.73 | 48.69 | 1.393 | 7 |
| MDLZ | 62.19 | 63.91 | 1.365 | 7 |
| LLY | 1206.63 | 1257.3199 | 1.362 | 7 |
| IBN | 1360.8 | 1397.0 | 1.362 | 7 |
| IBM | 224.51 | 232.13 | 1.319 | 7 |
| NEE | 78.16 | 79.795 | 1.188 | 7 |
| CVS | 89.93 | 92.36 | 1.1 | 7 |
| TD | 118.09 | 120.41 | 1.085 | 7 |
| ODFL | 182.91 | 187.77 | 1.066 | 7 |
| NKE | 35.85 | 37.13 | 1.042 | 7 |
| BAS.DE | 52.26 | 53.27 | 1.009 | 9 |
| CNQ | 52.57 | 53.83 | 0.999 | 7 |
| GSK | 17.91 | 18.57 | 0.994 | 9 |
| SYK | 287.45 | 294.67 | 0.944 | 7 |
| INTU | 314.95 | 325.24 | 0.893 | 7 |
| ORLY | 87.77 | 89.27 | 0.872 | 7 |
| ZAL.DE | 24.73 | 25.27 | 0.798 | 9 |
| LIN | 492.1 | 498.5 | 0.779 | 7 |
| RY | 195.54 | 197.815 | 0.775 | 7 |
| AZN | 121.8 | 124.3 | 0.772 | 9 |
| WDAY | 185.82 | 190.765 | 0.734 | 7 |
| FANG | 200.65 | 203.95 | 0.731 | 4 |
| USB | 57.92 | 58.72 | 0.703 | 7 |
| HNR1.DE | 270.8 | 274.0 | 0.669 | 9 |
| DTE.DE | 25.54 | 25.95 | 0.595 | 9 |
| SPG | 203.57 | 205.45 | 0.572 | 7 |
| CTSH | 64.74 | 66.03 | 0.487 | 7 |
| MRK.DE | 142.6 | 144.2 | 0.483 | 9 |
| BMO | 165.67 | 167.025 | 0.476 | 7 |
| MRK | 144.15 | 145.96 | 0.466 | 7 |
| PCAR | 109.82 | 110.82 | 0.428 | 7 |
| BMW.DE | 56.42 | 57.0 | 0.35 | 8 |
| UL | 49.355 | 49.66 | 0.34 | 3 |
| GE | 311.73 | 313.96 | 0.331 | 7 |
| SBUX | 96.73 | 97.52 | 0.324 | 7 |
| BKNG | 161.96 | 163.43 | 0.307 | 7 |
| CM | 111.89 | 112.47 | 0.289 | 7 |
| CMCSA | 21.76 | 21.9 | 0.275 | 7 |
| PYPL | 56.4 | 56.7 | 0.263 | 7 |
| DTG.DE | 41.51 | 41.72 | 0.247 | 9 |
| DHR | 227.61 | 229.03 | 0.221 | 7 |
| DIS | 110.16 | 110.57 | 0.201 | 7 |
| ACN | 227.63 | 229.6 | 0.188 | 1 |
| SRT3.DE | 257.7 | 259.2 | 0.168 | 9 |
| ADSK | 238.59 | 239.93 | 0.159 | 5 |
| MMM | 164.3 | 164.71 | 0.118 | 4 |
| AMT | 184.75 | 185.21 | 0.096 | 4 |
| LULU | 96.88 | 97.08 | 0.063 | 6 |
| CPRT | 27.85 | 27.88 | 0.039 | 3 |
| CDW | 150.34 | 150.48 | 0.027 | 6 |
| ADBE | 245.16 | 245.2 | 0.005 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.