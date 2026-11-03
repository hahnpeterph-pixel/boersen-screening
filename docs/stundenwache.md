# Stundenwache

Stand: 2026-11-02 · 272 Werte mit Stundendaten · erstellt 2026-11-03 01:35 UTC

> **Sitzung noch nicht abgeschlossen.** 6 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (14)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| WDC | 361.11 | 338.61 | -0.915 | 7 |
| STX | 625.3 | 593.26 | -0.627 | 6 |
| DELL | 413.0 | 392.66 | -0.575 | 5 |
| RWE.DE | 57.46 | 56.76 | -0.513 | 8 |
| CVS | 89.55 | 88.5 | -0.477 | 7 |
| SNDK | 1115.16 | 1075.0 | -0.407 | 4 |
| TMO | 691.74 | 684.275 | -0.358 | 6 |
| RHM.DE | 1006.4 | 994.1 | -0.329 | 2 |
| NET | 271.635 | 265.25 | -0.309 | 3 |
| ANET | 166.86 | 164.13 | -0.268 | 5 |
| SNOW | 295.26 | 290.52 | -0.261 | 3 |
| EQIX | 1001.43 | 993.4 | -0.239 | 6 |
| CNQ | 53.92 | 53.65 | -0.202 | 4 |
| ISRG | 437.51 | 436.88 | -0.046 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CVX | 227.63 | 227.91 | 0.059 | 0 |
| ETN | 364.84 | 366.14 | 0.075 | 0 |
| SHOP | 154.26 | 156.36 | 0.265 | 0 |
| CBK.DE | 37.69 | 38.03 | 0.389 | 0 |
| MUFG | 3330.0 | 3375.0 | 0.453 | 0 |
| SRT3.DE | 289.6 | 296.7 | 0.75 | 0 |
| SIE.DE | 264.95 | 270.65 | 0.794 | 0 |
| CON.DE | 66.44 | 67.62 | 0.84 | 0 |

## Swing-Hoch ueberwunden (93)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| REGN | 825.52 | 961.43 | 4.619 | 7 |
| COP | 130.97 | 146.85 | 4.467 | 7 |
| IDXX | 571.75 | 671.84 | 4.295 | 7 |
| LMT | 559.48 | 643.16 | 4.008 | 7 |
| BTI | 42.42 | 45.88 | 3.798 | 9 |
| XOM | 164.37 | 179.75 | 3.718 | 7 |
| MCD | 247.29 | 265.63 | 3.578 | 7 |
| IBM | 224.51 | 252.56 | 3.575 | 7 |
| QIA.DE | 42.345 | 45.0 | 3.423 | 9 |
| HD | 314.66 | 341.24 | 3.273 | 7 |
| GEHC | 72.3 | 79.56 | 3.15 | 7 |
| AZN | 128.06 | 138.32 | 2.921 | 9 |
| ADS.DE | 161.15 | 172.25 | 2.825 | 9 |
| BAYN.DE | 45.83 | 49.83 | 2.804 | 9 |
| RTX | 187.41 | 202.83 | 2.757 | 7 |
| CPRT | 29.43 | 31.94 | 2.701 | 7 |
| LOW | 204.52 | 218.14 | 2.622 | 7 |
| UPS | 103.08 | 109.72 | 2.603 | 7 |
| UNP | 291.93 | 307.07 | 2.46 | 7 |
| P911.DE | 43.59 | 46.52 | 2.31 | 9 |
| MRK.DE | 142.6 | 150.4 | 2.292 | 9 |
| GD | 357.46 | 373.53 | 2.247 | 7 |
| SPG | 213.63 | 221.78 | 2.145 | 7 |
| MA | 633.29 | 658.25 | 2.123 | 7 |
| CSX | 49.22 | 51.64 | 2.067 | 7 |
| DBK.DE | 28.815 | 30.615 | 1.997 | 9 |
| ROP | 450.76 | 479.56 | 1.973 | 7 |
| KDP | 35.4 | 36.95 | 1.943 | 7 |
| WMT | 122.4 | 127.7 | 1.911 | 7 |
| SHL.DE | 42.06 | 43.43 | 1.879 | 9 |
| FRE.DE | 47.295 | 48.82 | 1.874 | 9 |
| LLY | 1321.21 | 1411.49 | 1.871 | 7 |
| DXCM | 79.86 | 84.79 | 1.718 | 7 |
| MAR | 398.42 | 416.41 | 1.7 | 7 |
| SBUX | 100.33 | 104.43 | 1.692 | 7 |
| HNR1.DE | 283.2 | 291.2 | 1.667 | 9 |
| WDAY | 185.82 | 198.17 | 1.664 | 7 |
| HEI.DE | 150.0 | 155.95 | 1.632 | 9 |
| LULU | 100.67 | 107.77 | 1.627 | 7 |
| ABT | 105.88 | 110.28 | 1.428 | 7 |
| GM | 85.79 | 89.945 | 1.407 | 7 |
| ENB | 48.14 | 49.185 | 1.401 | 7 |
| V | 414.6 | 425.52 | 1.388 | 7 |
| FDX | 307.94 | 318.35 | 1.358 | 7 |
| NEE | 82.81 | 85.035 | 1.351 | 7 |
| HEN3.DE | 79.44 | 81.24 | 1.235 | 9 |
| DUK | 125.87 | 128.38 | 1.13 | 7 |
| MDT | 96.89 | 99.3 | 1.078 | 7 |
| VRTX | 537.81 | 556.05 | 1.073 | 7 |
| BRK-B | 549.0 | 557.23 | 1.048 | 7 |
| COST | 1021.45 | 1040.64 | 1.021 | 7 |
| NVO | 264.75 | 270.2 | 0.991 | 7 |
| BIIB | 240.99 | 248.96 | 0.977 | 7 |
| UBS | 38.96 | 39.79 | 0.972 | 9 |
| LIN | 512.49 | 519.76 | 0.897 | 7 |
| BAS.DE | 52.86 | 53.68 | 0.819 | 9 |
| MUV2.DE | 561.0 | 568.2 | 0.795 | 9 |
| MDLZ | 65.22 | 66.395 | 0.781 | 7 |
| CMCSA | 23.29 | 23.88 | 0.772 | 7 |
| PM | 204.0 | 208.35 | 0.745 | 7 |
| PDD | 80.17 | 81.69 | 0.694 | 7 |
| CHTR | 112.71 | 115.53 | 0.634 | 7 |
| MMM | 175.56 | 178.37 | 0.634 | 7 |
| PGR | 230.28 | 234.07 | 0.632 | 7 |
| CB | 364.86 | 369.0 | 0.62 | 7 |
| SHW | 346.19 | 352.41 | 0.607 | 7 |
| MO | 76.09 | 77.18 | 0.606 | 7 |
| PYPL | 57.95 | 58.8 | 0.592 | 7 |
| NKE | 38.5 | 39.125 | 0.59 | 7 |
| PAH3.DE | 25.6 | 25.94 | 0.518 | 4 |
| PEP | 139.0 | 140.47 | 0.459 | 6 |
| PFE | 30.44 | 30.705 | 0.439 | 6 |
| MNST | 47.54 | 48.025 | 0.438 | 7 |
| ALV.DE | 437.5 | 440.3 | 0.432 | 7 |
| CCEP | 114.55 | 115.59 | 0.417 | 6 |
| DE | 660.39 | 667.62 | 0.414 | 6 |
| SO | 94.04 | 94.625 | 0.334 | 5 |
| DHL.DE | 58.92 | 59.26 | 0.331 | 7 |
| EOAN.DE | 18.67 | 18.77 | 0.273 | 9 |
| KO | 95.37 | 95.86 | 0.265 | 5 |
| BNR.DE | 63.18 | 63.5 | 0.25 | 4 |
| BMW.DE | 58.52 | 58.82 | 0.223 | 3 |
| WFC | 85.49 | 85.905 | 0.213 | 2 |
| AXP | 326.49 | 328.03 | 0.209 | 7 |
| ADSK | 256.17 | 257.87 | 0.201 | 6 |
| GE | 314.0 | 315.79 | 0.177 | 6 |
| NXPI | 255.31 | 257.3 | 0.171 | 7 |
| PLD | 129.24 | 129.68 | 0.155 | 7 |
| ACN | 259.39 | 260.96 | 0.14 | 7 |
| COF | 210.04 | 210.74 | 0.129 | 7 |
| TMUS | 159.41 | 160.15 | 0.122 | 1 |
| SPGI | 474.61 | 475.18 | 0.049 | 6 |
| SPOT | 593.8 | 593.87 | 0.003 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.