# Stundenwache

Stand: 2026-11-25 · 233 Werte mit Stundendaten · erstellt 2026-11-27 06:42 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| COF | 177.86 | 182.62 | 0.835 | 1 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TMUS | 165.73 | 166.2 | 0.096 | 0 |
| SNDK | 67.02 | 73.51 | 0.518 | 0 |
| DHR | 223.25 | 227.35 | 0.706 | 0 |
| MDT | 94.13 | 96.06 | 0.739 | 0 |
| SKHY | 1027000.0 | 1103000.0 | 0.84 | 0 |
| MRVL | 117.8 | 130.9 | 0.858 | 0 |
| ETN | 301.43 | 317.52 | 0.895 | 0 |
| FDX | 301.17 | 308.75 | 0.908 | 0 |
| C | 109.99 | 113.36 | 0.983 | 0 |
| KLAC | 122.39 | 134.08 | 0.992 | 0 |
| ON | 57.49 | 62.475 | 1.047 | 0 |
| INTC | 49.16 | 54.4408 | 1.093 | 0 |
| BLK | 1103.49 | 1141.64 | 1.121 | 0 |
| NFLX | 57.03 | 59.42 | 1.229 | 0 |
| DE | 605.34 | 641.14 | 1.468 | 0 |

## Swing-Hoch ueberwunden (50)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| SNY | 89.0 | 99.15 | 3.979 | 9 |
| TM | 3115.0 | 3385.0 | 3.27 | 7 |
| PDD | 79.88 | 87.42 | 2.433 | 7 |
| HDB | 821.0 | 862.45 | 1.903 | 3 |
| TJX | 138.17 | 146.11 | 1.843 | 7 |
| CSGP | 31.64 | 34.02 | 1.789 | 7 |
| DIS | 120.44 | 125.62 | 1.507 | 7 |
| UL | 49.355 | 50.62 | 1.38 | 9 |
| ORLY | 93.93 | 96.685 | 1.378 | 7 |
| VRTX | 542.76 | 563.95 | 1.345 | 7 |
| ADP | 308.66 | 316.75 | 1.238 | 7 |
| HD | 349.73 | 361.27 | 1.221 | 7 |
| GILD | 171.7 | 176.75 | 1.16 | 7 |
| SYK | 321.83 | 332.89 | 1.125 | 7 |
| PAYX | 115.3 | 118.5 | 1.068 | 7 |
| LOW | 228.7 | 235.66 | 0.982 | 7 |
| AXON | 320.17 | 343.25 | 0.905 | 6 |
| KHC | 25.835 | 26.5 | 0.885 | 7 |
| CPRT | 32.38 | 33.175 | 0.819 | 6 |
| MCD | 278.29 | 283.5 | 0.802 | 7 |
| BHP | 53.96 | 55.06 | 0.65 | 7 |
| TRV | 402.12 | 406.95 | 0.564 | 7 |
| CHTR | 142.6 | 147.23 | 0.553 | 5 |
| PG | 171.61 | 173.24 | 0.517 | 7 |
| WMT | 130.52 | 131.9 | 0.49 | 7 |
| T | 22.75 | 22.965 | 0.447 | 7 |
| SHEL | 35.88 | 36.175 | 0.424 | 8 |
| CDW | 172.23 | 175.01 | 0.341 | 4 |
| CMCSA | 25.49 | 25.71 | 0.327 | 7 |
| PGR | 237.07 | 238.74 | 0.32 | 7 |
| REGN | 972.24 | 981.82 | 0.316 | 6 |
| DUK | 131.27 | 131.96 | 0.315 | 7 |
| MDLZ | 67.39 | 67.8 | 0.304 | 7 |
| SO | 94.49 | 95.005 | 0.295 | 7 |
| DXCM | 84.02 | 84.81 | 0.277 | 6 |
| JNJ | 272.5 | 273.94 | 0.222 | 7 |
| BABA | 86.75 | 87.65 | 0.216 | 2 |
| CVX | 210.13 | 211.005 | 0.194 | 6 |
| VZ | 47.11 | 47.295 | 0.193 | 7 |
| CB | 379.21 | 380.5 | 0.19 | 7 |
| PEP | 143.28 | 143.92 | 0.186 | 7 |
| MUFG | 3178.0 | 3194.0 | 0.141 | 6 |
| NEE | 85.26 | 85.45 | 0.129 | 6 |
| TTWO | 225.69 | 227.27 | 0.104 | 3 |
| EXC | 46.44 | 46.51 | 0.093 | 7 |
| HON | 224.66 | 225.1 | 0.063 | 4 |
| SHW | 361.0 | 361.15 | 0.016 | 4 |
| CL | 99.63 | 99.66 | 0.014 | 5 |
| MO | 76.23 | 76.25 | 0.012 | 7 |
| FANG | 180.12 | 180.15 | 0.006 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.