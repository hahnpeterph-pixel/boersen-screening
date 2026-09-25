# Stundenwache

Stand: 2026-09-24 · 267 Werte mit Stundendaten · erstellt 2026-09-25 00:36 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MDT | 88.47 | 88.46 | -0.005 | 1 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MA | 561.9 | 565.91 | 0.452 | 2 |

## Tief angetestet (73)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GD | 336.23 | 336.23 | 0.0 | 0 |
| PLD | 133.65 | 133.66 | 0.005 | 0 |
| DUK | 113.17 | 113.19 | 0.013 | 0 |
| ADS.DE | 142.15 | 142.2 | 0.014 | 0 |
| ABT | 101.03 | 101.07 | 0.018 | 0 |
| CL | 85.295 | 85.33 | 0.022 | 0 |
| INTU | 276.78 | 277.13 | 0.027 | 0 |
| SNY | 40.905 | 40.925 | 0.029 | 0 |
| PBR | 20.83 | 20.85 | 0.034 | 0 |
| FDX | 279.34 | 279.59 | 0.036 | 0 |
| VNA.DE | 17.08 | 17.095 | 0.039 | 0 |
| ENB | 47.32 | 47.355 | 0.044 | 0 |
| MNST | 42.605 | 42.65 | 0.052 | 0 |
| IFX.DE | 55.98 | 56.12 | 0.053 | 0 |
| EXC | 40.155 | 40.195 | 0.056 | 0 |
| TM | 186.385 | 186.6 | 0.062 | 0 |
| ACN | 176.87 | 177.43 | 0.075 | 0 |
| SO | 82.835 | 82.93 | 0.076 | 0 |
| GSK | 49.565 | 49.645 | 0.079 | 0 |
| TTWO | 202.37 | 202.98 | 0.089 | 0 |
| DBK.DE | 30.98 | 31.065 | 0.093 | 0 |
| BNR.DE | 58.78 | 58.92 | 0.106 | 0 |
| MCK | 866.665 | 869.14 | 0.114 | 0 |
| CTSH | 56.92 | 57.19 | 0.12 | 0 |
| IBM | 226.04 | 227.02 | 0.128 | 0 |
| CDW | 138.54 | 139.36 | 0.142 | 0 |
| ARM | 303.65 | 306.43 | 0.146 | 0 |
| HD | 291.09 | 292.13 | 0.156 | 0 |
| CMCSA | 22.015 | 22.14 | 0.16 | 0 |
| BABA | 110.14 | 110.62 | 0.167 | 0 |
| CBK.DE | 41.01 | 41.17 | 0.171 | 0 |
| MBG.DE | 41.14 | 41.365 | 0.181 | 0 |
| UPS | 91.63 | 92.04 | 0.182 | 0 |
| AMT | 166.54 | 167.3 | 0.191 | 0 |
| GM | 80.045 | 80.62 | 0.208 | 0 |
| ADBE | 236.84 | 238.95 | 0.211 | 0 |
| AAPL | 334.3 | 335.87 | 0.221 | 0 |
| TTD | 12.49 | 12.63 | 0.233 | 0 |
| DXCM | 86.895 | 87.48 | 0.246 | 0 |
| SONY | 22.855 | 22.985 | 0.27 | 0 |
| BHP | 84.365 | 85.095 | 0.283 | 0 |
| SPGI | 400.61 | 403.43 | 0.29 | 0 |
| NEM | 120.02 | 121.285 | 0.299 | 0 |
| MELI | 1736.85 | 1754.35 | 0.305 | 0 |
| GS | 914.68 | 923.0 | 0.307 | 0 |
| ABBV | 263.09 | 264.87 | 0.338 | 0 |
| REGN | 789.41 | 796.01 | 0.356 | 0 |
| ASML | 1489.6 | 1507.4 | 0.379 | 0 |
| ISRG | 395.18 | 399.47 | 0.384 | 0 |
| BA | 194.4 | 196.7 | 0.399 | 0 |
| SMFG | 25.3 | 25.52 | 0.409 | 0 |
| JPM | 335.28 | 338.36 | 0.418 | 0 |
| ADP | 261.305 | 263.68 | 0.425 | 0 |
| SNOW | 328.21 | 334.1 | 0.433 | 0 |
| SAN | 14.155 | 14.29 | 0.448 | 0 |
| ADI | 377.4 | 382.56 | 0.472 | 0 |
| CM | 110.42 | 111.4 | 0.48 | 0 |
| AZN | 162.92 | 164.61 | 0.483 | 0 |
| NVO | 37.92 | 38.6199 | 0.549 | 0 |
| EOAN.DE | 17.025 | 17.2 | 0.555 | 0 |
| WFC | 80.945 | 82.19 | 0.561 | 0 |
| BNS | 91.42 | 92.24 | 0.564 | 0 |
| SCHW | 98.065 | 99.49 | 0.578 | 0 |
| MCHP | 73.13 | 74.69 | 0.632 | 0 |
| AMZN | 245.605 | 249.35 | 0.684 | 0 |
| ORCL | 133.48 | 139.525 | 0.773 | 0 |
| GEHC | 65.2 | 66.4 | 0.782 | 0 |
| ETN | 427.96 | 439.81 | 0.784 | 0 |
| BLK | 1053.49 | 1073.1899 | 0.811 | 0 |
| ANET | 198.7573 | 205.6 | 0.911 | 0 |
| TSM | 440.69 | 451.05 | 0.97 | 0 |
| UBS | 47.1801 | 48.47 | 1.106 | 0 |
| CTAS | 191.09 | 197.62 | 1.588 | 0 |

## Swing-Hoch ueberwunden (41)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 194.84 | 10.823 | 7 |
| WBD | 28.45 | 30.83 | 4.856 | 7 |
| AMD | 526.79 | 629.02 | 3.806 | 7 |
| META | 685.31 | 777.44 | 3.263 | 7 |
| INTC | 104.9 | 127.36 | 3.244 | 7 |
| SRT3.DE | 240.2 | 263.0 | 3.084 | 9 |
| DDOG | 227.58 | 256.92 | 2.854 | 7 |
| CDNS | 293.4 | 322.49 | 2.813 | 7 |
| PLTR | 177.88 | 192.61 | 2.413 | 7 |
| NET | 319.43 | 358.92 | 2.159 | 7 |
| ILMN | 250.06 | 273.87 | 1.967 | 7 |
| ZS | 196.575 | 214.64 | 1.782 | 7 |
| PH | 939.6 | 975.1 | 1.75 | 7 |
| LLY | 1138.79 | 1183.09 | 1.546 | 7 |
| PFE | 27.81 | 28.43 | 1.379 | 7 |
| SHOP | 134.74 | 145.16 | 1.378 | 7 |
| TJX | 127.8 | 131.6 | 1.368 | 7 |
| BEI.DE | 75.74 | 77.8 | 1.297 | 9 |
| MAR | 342.31 | 351.46 | 1.26 | 7 |
| TMO | 663.57 | 681.53 | 1.172 | 6 |
| EMR | 152.28 | 156.15 | 1.109 | 7 |
| FAST | 49.78 | 50.74 | 0.975 | 7 |
| CRWD | 250.32 | 259.62 | 0.771 | 7 |
| ROST | 231.85 | 235.4 | 0.737 | 7 |
| BIIB | 222.25 | 226.43 | 0.721 | 7 |
| SY1.DE | 91.74 | 93.12 | 0.702 | 9 |
| WDAY | 185.82 | 190.965 | 0.69 | 7 |
| MMM | 165.37 | 167.53 | 0.636 | 7 |
| DB1.DE | 280.1 | 283.3 | 0.585 | 9 |
| MTX.DE | 358.8 | 364.5 | 0.573 | 9 |
| DHR | 220.67 | 223.77 | 0.557 | 7 |
| KLAC | 182.41 | 186.9 | 0.552 | 7 |
| MRK.DE | 133.45 | 134.7 | 0.506 | 4 |
| FTNT | 176.1 | 178.7 | 0.393 | 7 |
| PANW | 383.12 | 389.83 | 0.393 | 7 |
| NVS | 142.18 | 143.55 | 0.351 | 7 |
| ZAL.DE | 21.95 | 22.16 | 0.343 | 9 |
| SNPS | 419.84 | 424.87 | 0.342 | 7 |
| TXN | 267.97 | 270.59 | 0.326 | 7 |
| HON | 210.59 | 211.8 | 0.288 | 6 |
| LIN | 466.24 | 468.02 | 0.248 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.