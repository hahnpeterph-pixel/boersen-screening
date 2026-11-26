# Stundenwache

Stand: 2026-11-25 · 272 Werte mit Stundendaten · erstellt 2026-11-26 02:08 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (17)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CBK.DE | 35.55 | 34.25 | -1.114 | 9 |
| ING | 27.14 | 26.445 | -0.973 | 8 |
| BBVA | 21.82 | 21.3 | -0.924 | 8 |
| SIE.DE | 254.35 | 246.25 | -0.883 | 6 |
| IFX.DE | 43.44 | 40.725 | -0.867 | 9 |
| SAN | 10.252 | 10.05 | -0.748 | 6 |
| ENR.DE | 117.24 | 111.7 | -0.743 | 8 |
| BAYN.DE | 51.7 | 50.48 | -0.733 | 9 |
| HSBC | 12.34 | 12.174 | -0.541 | 5 |
| CON.DE | 69.16 | 68.12 | -0.539 | 4 |
| MPC | 348.27 | 346.21 | -0.123 | 6 |
| SNDK | 74.87 | 73.51 | -0.098 | 7 |
| STX | 473.96 | 469.72 | -0.08 | 6 |
| DHL.DE | 56.18 | 56.08 | -0.073 | 1 |
| ANET | 164.9 | 163.95 | -0.063 | 7 |
| SRT3.DE | 285.8 | 285.3 | -0.063 | 2 |
| RIO | 55.32 | 55.27 | -0.03 | 2 |

## Tief zurueckerobert (28)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MS | 167.4 | 167.53 | 0.019 | 4 |
| NET | 282.105 | 283.35 | 0.051 | 5 |
| ETN | 316.41 | 317.52 | 0.059 | 4 |
| PH | 895.23 | 897.74 | 0.075 | 4 |
| GFS | 36.0 | 36.21 | 0.077 | 4 |
| WDC | 269.42 | 272.23 | 0.096 | 4 |
| GEV | 708.965 | 714.75 | 0.099 | 3 |
| VLO | 321.33 | 322.99 | 0.115 | 3 |
| CM | 104.11 | 104.51 | 0.15 | 3 |
| APH | 72.37 | 73.1 | 0.152 | 5 |
| DELL | 290.5 | 297.0439 | 0.162 | 3 |
| GLW | 98.62 | 100.2 | 0.163 | 3 |
| EQIX | 967.75 | 978.4 | 0.282 | 2 |
| SHEL | 35.33 | 35.56 | 0.303 | 1 |
| MSTR | 77.32 | 80.03 | 0.313 | 4 |
| BNS | 83.56 | 84.29 | 0.357 | 2 |
| C | 111.95 | 113.36 | 0.362 | 2 |
| PSX | 232.58 | 236.06 | 0.375 | 1 |
| SPCX | 123.52 | 127.32 | 0.415 | 3 |
| GE | 312.22 | 317.11 | 0.443 | 1 |
| NEM | 98.66 | 101.45 | 0.528 | 3 |
| NOW | 89.62 | 92.16 | 0.546 | 1 |
| EMR | 153.87 | 157.17 | 0.548 | 2 |
| TD | 114.52 | 115.99 | 0.587 | 1 |
| EQNR | 377.9 | 385.7 | 0.726 | 5 |
| BMO | 157.33 | 160.13 | 0.731 | 1 |
| SCCO | 133.95 | 140.935 | 0.784 | 2 |
| COF | 177.86 | 182.62 | 0.785 | 1 |

## Tief angetestet (7)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AIR.DE | 190.0 | 190.24 | 0.043 | 0 |
| BP | 5.401 | 5.447 | 0.349 | 0 |
| MDT | 94.49 | 96.06 | 0.603 | 0 |
| FDX | 302.75 | 308.75 | 0.68 | 0 |
| SNOW | 252.755 | 267.64 | 0.894 | 0 |
| HONA | 150.1 | 157.82 | 1.133 | 0 |
| DE | 605.34 | 641.14 | 1.656 | 0 |

## Swing-Hoch ueberwunden (53)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.07 | 14.423 | 9 |
| SNY | 89.0 | 97.95 | 3.863 | 9 |
| TM | 3115.0 | 3412.0 | 3.08 | 2 |
| SONY | 4068.0 | 4496.0 | 2.897 | 2 |
| PDD | 79.88 | 87.42 | 2.433 | 7 |
| CSGP | 31.64 | 34.02 | 1.789 | 7 |
| TJX | 138.17 | 146.11 | 1.71 | 7 |
| DIS | 120.44 | 125.61 | 1.504 | 7 |
| UL | 49.355 | 50.78 | 1.405 | 9 |
| ORLY | 93.93 | 96.685 | 1.378 | 7 |
| VRTX | 542.76 | 563.95 | 1.345 | 7 |
| HD | 349.73 | 361.27 | 1.221 | 7 |
| ADP | 308.66 | 316.44 | 1.191 | 6 |
| GILD | 171.7 | 176.75 | 1.16 | 7 |
| HDB | 821.0 | 846.2 | 1.136 | 7 |
| PAYX | 115.3 | 118.5 | 1.068 | 7 |
| SYK | 321.83 | 332.89 | 1.067 | 7 |
| LOW | 228.7 | 235.66 | 0.988 | 7 |
| VNA.DE | 16.99 | 17.365 | 0.956 | 9 |
| KHC | 25.835 | 26.5 | 0.885 | 7 |
| AXON | 320.17 | 343.25 | 0.849 | 6 |
| CPRT | 32.38 | 33.175 | 0.819 | 6 |
| MCD | 278.29 | 283.5 | 0.802 | 7 |
| DTE.DE | 26.51 | 26.95 | 0.781 | 9 |
| TRV | 402.12 | 406.95 | 0.564 | 7 |
| CHTR | 142.6 | 147.23 | 0.553 | 5 |
| PG | 171.61 | 173.24 | 0.517 | 7 |
| WMT | 130.52 | 131.9 | 0.491 | 7 |
| T | 22.75 | 22.965 | 0.442 | 7 |
| CDW | 172.23 | 175.01 | 0.341 | 4 |
| CMCSA | 25.49 | 25.71 | 0.327 | 7 |
| REGN | 972.24 | 981.82 | 0.316 | 6 |
| PGR | 237.07 | 238.74 | 0.306 | 7 |
| MDLZ | 67.39 | 67.8 | 0.304 | 7 |
| DUK | 131.27 | 131.96 | 0.3 | 7 |
| DXCM | 84.02 | 84.81 | 0.277 | 6 |
| SO | 94.49 | 95.005 | 0.272 | 7 |
| HEI.DE | 179.45 | 180.65 | 0.257 | 9 |
| JNJ | 272.5 | 273.94 | 0.222 | 7 |
| VZ | 47.11 | 47.295 | 0.193 | 7 |
| PEP | 143.28 | 143.92 | 0.186 | 7 |
| CB | 379.21 | 380.5 | 0.18 | 7 |
| CVX | 210.13 | 211.005 | 0.18 | 6 |
| P911.DE | 43.83 | 43.98 | 0.138 | 7 |
| NEE | 85.26 | 85.45 | 0.122 | 6 |
| TTWO | 225.69 | 227.27 | 0.104 | 3 |
| EXC | 46.44 | 46.51 | 0.093 | 7 |
| HON | 224.66 | 225.1 | 0.063 | 4 |
| SHW | 361.0 | 361.15 | 0.016 | 4 |
| CL | 99.63 | 99.66 | 0.014 | 5 |
| MO | 76.23 | 76.25 | 0.012 | 7 |
| FANG | 180.12 | 180.15 | 0.006 | 3 |
| BHP | 53.96 | 53.97 | 0.006 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.