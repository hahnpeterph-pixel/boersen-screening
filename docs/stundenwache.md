# Stundenwache

Stand: 2026-11-16 · 272 Werte mit Stundendaten · erstellt 2026-11-17 02:28 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 4, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (45)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| P911.DE | 45.4 | 43.96 | -1.253 | 9 |
| SCCO | 162.58 | 153.87 | -1.063 | 7 |
| BNS | 92.13 | 90.65 | -0.842 | 7 |
| GM | 85.91 | 83.67 | -0.705 | 7 |
| BMO | 172.08 | 169.82 | -0.654 | 7 |
| TD | 123.15 | 121.78 | -0.639 | 7 |
| MSTR | 108.25 | 103.0657 | -0.612 | 7 |
| EMR | 164.0 | 160.68 | -0.599 | 7 |
| TJX | 133.34 | 131.1 | -0.578 | 7 |
| CM | 115.13 | 113.81 | -0.542 | 6 |
| ETN | 347.58 | 336.92 | -0.516 | 7 |
| GLW | 110.56 | 106.21 | -0.508 | 7 |
| CON.DE | 73.72 | 72.8 | -0.475 | 7 |
| RY | 201.13 | 199.67 | -0.41 | 6 |
| DE | 662.35 | 654.0 | -0.408 | 4 |
| BAS.DE | 54.27 | 53.81 | -0.406 | 2 |
| NEM | 112.26 | 110.37 | -0.382 | 7 |
| SNDK | 848.498 | 808.93 | -0.347 | 7 |
| GEV | 783.624 | 763.46 | -0.322 | 7 |
| NET | 300.28 | 293.69 | -0.29 | 7 |
| PH | 944.8 | 935.17 | -0.29 | 7 |
| GFS | 40.2 | 39.43 | -0.29 | 4 |
| PAH3.DE | 24.29 | 24.09 | -0.282 | 3 |
| DELL | 330.42 | 320.54 | -0.261 | 7 |
| RTX | 196.37 | 194.925 | -0.26 | 4 |
| GE | 328.1 | 325.29 | -0.24 | 6 |
| SIE.DE | 274.6 | 272.55 | -0.235 | 8 |
| WFC | 85.28 | 84.855 | -0.213 | 5 |
| WDC | 286.54 | 281.08 | -0.192 | 7 |
| ENB | 47.46 | 47.31 | -0.19 | 4 |
| SNOW | 283.41 | 280.54 | -0.176 | 6 |
| LMT | 588.74 | 585.47 | -0.162 | 6 |
| STX | 507.09 | 500.145 | -0.128 | 6 |
| APH | 76.05 | 75.46 | -0.119 | 6 |
| BEI.DE | 83.84 | 83.6 | -0.112 | 1 |
| IFX.DE | 49.425 | 49.11 | -0.102 | 6 |
| BHP | 55.05 | 54.93 | -0.074 | 1 |
| PM | 196.42 | 196.04 | -0.073 | 4 |
| GD | 360.18 | 359.8 | -0.04 | 4 |
| NOW | 99.63 | 99.395 | -0.032 | 3 |
| C | 121.43 | 121.33 | -0.028 | 4 |
| DBK.DE | 33.0 | 32.975 | -0.022 | 2 |
| GS | 892.1 | 891.61 | -0.016 | 5 |
| VOW3.DE | 67.12 | 67.1 | -0.009 | 1 |
| SPG | 232.87 | 232.85 | -0.005 | 6 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TMO | 689.71 | 691.59 | 0.087 | 1 |
| SPCX | 136.64 | 137.365 | 0.091 | 3 |

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AIR.DE | 205.0 | 205.1 | 0.018 | 0 |
| DHR | 229.92 | 230.09 | 0.026 | 0 |
| EQIX | 1041.28 | 1043.51 | 0.057 | 0 |
| HONA | 162.78 | 163.41 | 0.073 | 0 |
| HEI.DE | 176.85 | 178.15 | 0.227 | 0 |
| MS | 183.91 | 185.59 | 0.298 | 0 |
| NEE | 84.37 | 85.36 | 0.553 | 0 |
| SHOP | 142.1 | 147.81 | 0.642 | 0 |

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.35 | 15.382 | 9 |
| IBN | 1404.9 | 1585.0 | 5.291 | 7 |
| TM | 3115.0 | 3393.0 | 2.248 | 3 |
| CHTR | 127.16 | 138.99 | 1.634 | 7 |
| SNY | 85.37 | 88.41 | 1.604 | 9 |
| COST | 1081.55 | 1114.42 | 1.544 | 7 |
| VRSK | 201.65 | 212.76 | 1.469 | 7 |
| SONY | 4068.0 | 4284.0 | 1.415 | 3 |
| KO | 97.39 | 99.605 | 1.205 | 7 |
| WDAY | 185.82 | 194.105 | 1.116 | 7 |
| ALV.DE | 466.4 | 475.4 | 1.011 | 9 |
| MUV2.DE | 579.8 | 592.0 | 0.995 | 9 |
| PG | 169.79 | 173.15 | 0.975 | 7 |
| UL | 49.355 | 50.48 | 0.941 | 9 |
| NVO | 278.0 | 285.25 | 0.898 | 8 |
| DTE.DE | 26.49 | 27.03 | 0.898 | 9 |
| CL | 99.01 | 100.99 | 0.835 | 7 |
| UNH | 406.72 | 412.1 | 0.49 | 7 |
| BNY | 150.28 | 151.69 | 0.434 | 7 |
| CCEP | 117.96 | 119.21 | 0.432 | 7 |
| NVS | 134.84 | 135.94 | 0.41 | 9 |
| CMCSA | 25.3 | 25.605 | 0.401 | 7 |
| XEL | 80.67 | 81.21 | 0.338 | 7 |
| T | 22.21 | 22.37 | 0.324 | 7 |
| ING | 29.68 | 29.91 | 0.321 | 9 |
| RWE.DE | 58.92 | 59.34 | 0.311 | 9 |
| ADP | 310.98 | 313.15 | 0.289 | 6 |
| PEP | 145.55 | 146.475 | 0.269 | 7 |
| DUK | 129.97 | 130.58 | 0.269 | 7 |
| ODFL | 172.8 | 174.31 | 0.215 | 7 |
| DB1.DE | 329.1 | 330.2 | 0.168 | 9 |
| APP | 413.6 | 415.05 | 0.055 | 4 |
| UPS | 111.83 | 111.87 | 0.013 | 1 |
| MA | 661.84 | 661.93 | 0.005 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.