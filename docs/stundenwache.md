# Stundenwache

Stand: 2026-10-30 · 272 Werte mit Stundendaten · erstellt 2026-10-31 01:37 UTC

> **Sitzung noch nicht abgeschlossen.** 2 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (3)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ISRG | 437.51 | 431.88 | -0.408 | 4 |
| IDXX | 555.21 | 551.31 | -0.25 | 2 |
| TTD | 12.375 | 12.29 | -0.149 | 4 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (14)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| RWE.DE | 57.46 | 57.58 | 0.088 | 0 |
| CBK.DE | 37.69 | 37.78 | 0.103 | 0 |
| ASML | 1405.6 | 1411.8 | 0.107 | 0 |
| AIR.DE | 191.28 | 192.26 | 0.185 | 0 |
| USB | 59.19 | 59.44 | 0.201 | 0 |
| WFC | 82.97 | 83.42 | 0.231 | 0 |
| AXP | 316.68 | 319.02 | 0.334 | 0 |
| EMR | 163.14 | 164.8 | 0.351 | 0 |
| STX | 625.3 | 644.37 | 0.373 | 0 |
| SNPS | 460.14 | 467.9 | 0.394 | 0 |
| CDNS | 322.25 | 328.03 | 0.407 | 0 |
| MU | 861.59 | 884.89 | 0.457 | 0 |
| NVDA | 200.92 | 204.81 | 0.595 | 0 |
| MCHP | 75.32 | 77.35 | 0.608 | 0 |

## Swing-Hoch ueberwunden (78)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| COP | 130.97 | 154.05 | 6.492 | 7 |
| XOM | 164.37 | 187.25 | 5.531 | 7 |
| IBM | 224.51 | 257.86 | 4.291 | 7 |
| SNY | 73.04 | 80.08 | 4.19 | 9 |
| BTI | 42.42 | 45.97 | 3.952 | 9 |
| LMT | 559.48 | 637.06 | 3.716 | 7 |
| REGN | 825.52 | 927.86 | 3.702 | 7 |
| QIA.DE | 42.345 | 45.09 | 3.539 | 9 |
| AZN | 128.06 | 139.98 | 3.295 | 9 |
| AEP | 121.8 | 130.15 | 3.186 | 7 |
| BAYN.DE | 45.83 | 50.22 | 3.078 | 9 |
| EXC | 43.58 | 46.15 | 2.835 | 7 |
| MRK.DE | 142.6 | 151.15 | 2.512 | 9 |
| CSX | 49.22 | 51.98 | 2.401 | 7 |
| P911.DE | 43.59 | 46.57 | 2.349 | 9 |
| GILD | 159.69 | 170.8 | 2.306 | 7 |
| MCD | 247.29 | 258.18 | 2.262 | 7 |
| RTX | 187.41 | 199.86 | 2.226 | 7 |
| TTE | 81.63 | 85.38 | 2.188 | 9 |
| XEL | 76.54 | 79.82 | 2.178 | 7 |
| GD | 357.46 | 372.7 | 2.131 | 7 |
| AMGN | 441.76 | 466.05 | 2.046 | 7 |
| UPS | 103.08 | 108.25 | 2.027 | 7 |
| LLY | 1321.21 | 1416.3 | 1.971 | 7 |
| GEHC | 72.3 | 76.57 | 1.96 | 7 |
| UNP | 291.93 | 303.91 | 1.946 | 7 |
| ADS.DE | 161.15 | 168.75 | 1.935 | 9 |
| HD | 314.66 | 329.25 | 1.903 | 7 |
| ENB | 48.14 | 49.45 | 1.757 | 7 |
| NVS | 129.34 | 134.12 | 1.714 | 9 |
| WDAY | 185.82 | 197.731 | 1.624 | 7 |
| BIIB | 240.99 | 253.68 | 1.601 | 7 |
| LULU | 100.67 | 107.27 | 1.512 | 7 |
| DBK.DE | 28.815 | 30.15 | 1.481 | 9 |
| HNR1.DE | 283.2 | 290.0 | 1.417 | 9 |
| SBUX | 100.33 | 103.58 | 1.365 | 7 |
| VRTX | 537.81 | 559.05 | 1.25 | 7 |
| ROP | 450.76 | 466.81 | 1.179 | 7 |
| SPG | 213.63 | 217.77 | 1.09 | 7 |
| MO | 76.09 | 78.0 | 1.062 | 7 |
| SHL.DE | 42.06 | 42.82 | 1.042 | 9 |
| LOW | 204.52 | 209.12 | 0.885 | 7 |
| DXCM | 79.86 | 82.32 | 0.875 | 7 |
| SHEL | 39.8 | 40.485 | 0.87 | 9 |
| DE | 660.39 | 675.285 | 0.854 | 7 |
| PM | 204.0 | 208.9 | 0.839 | 7 |
| CPRT | 29.43 | 30.12 | 0.817 | 7 |
| ABBV | 289.59 | 294.88 | 0.766 | 7 |
| DUK | 125.87 | 127.44 | 0.707 | 7 |
| FDX | 307.94 | 313.29 | 0.698 | 7 |
| MUV2.DE | 561.0 | 567.2 | 0.685 | 9 |
| EOAN.DE | 18.67 | 18.905 | 0.642 | 9 |
| KDP | 35.4 | 35.855 | 0.621 | 7 |
| FANG | 208.65 | 212.06 | 0.606 | 7 |
| HEN3.DE | 79.44 | 80.3 | 0.59 | 9 |
| NEE | 82.81 | 83.755 | 0.574 | 7 |
| GM | 85.79 | 87.41 | 0.549 | 7 |
| BAS.DE | 52.86 | 53.38 | 0.52 | 9 |
| DB1.DE | 317.2 | 320.4 | 0.496 | 7 |
| CNQ | 55.5 | 56.13 | 0.47 | 7 |
| FRE.DE | 47.295 | 47.675 | 0.467 | 9 |
| WMT | 122.4 | 123.52 | 0.424 | 7 |
| NXPI | 255.31 | 259.82 | 0.405 | 6 |
| MA | 633.29 | 638.01 | 0.402 | 7 |
| CVX | 234.08 | 235.59 | 0.319 | 7 |
| ALV.DE | 437.5 | 439.5 | 0.309 | 8 |
| ORCL | 128.33 | 130.69 | 0.293 | 7 |
| UBS | 38.96 | 39.21 | 0.29 | 9 |
| NVO | 264.75 | 266.1 | 0.251 | 7 |
| LIN | 512.49 | 514.48 | 0.25 | 6 |
| NKE | 38.5 | 38.69 | 0.182 | 7 |
| PGR | 230.28 | 231.27 | 0.165 | 7 |
| MAR | 398.42 | 399.66 | 0.145 | 7 |
| ABT | 105.88 | 106.25 | 0.124 | 7 |
| JNJ | 272.36 | 273.2 | 0.109 | 7 |
| PFE | 30.44 | 30.505 | 0.108 | 4 |
| PAH3.DE | 25.6 | 25.64 | 0.061 | 7 |
| BNR.DE | 63.18 | 63.22 | 0.031 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.