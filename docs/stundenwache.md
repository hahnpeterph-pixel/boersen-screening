# Stundenwache

Stand: 2026-09-29 · 273 Werte mit Stundendaten · erstellt 2026-09-30 11:04 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 4, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (2)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ALV.DE | 418.3 | 418.3 | -0.0 | 1 |
| HNR1.DE | 254.4 | 254.4 | -0.0 | 1 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 182.26 | 183.2 | 0.18 | 1 |
| MA | 561.9 | 563.66 | 0.206 | 1 |

## Tief angetestet (33)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TTE | 87.6 | 87.65 | 0.032 | 0 |
| NVDA | 227.03 | 227.3 | 0.05 | 0 |
| LULU | 96.62 | 96.85 | 0.064 | 0 |
| T | 24.46 | 24.5 | 0.065 | 0 |
| ABBV | 262.59 | 263.27 | 0.133 | 0 |
| WFC | 80.12 | 80.5 | 0.179 | 0 |
| ROP | 347.45 | 349.6 | 0.235 | 0 |
| RY | 198.99 | 199.74 | 0.251 | 0 |
| USB | 57.81 | 58.15 | 0.273 | 0 |
| GM | 79.58 | 80.475 | 0.327 | 0 |
| EQNR | 40.96 | 41.355 | 0.337 | 0 |
| SAN | 14.07 | 14.18 | 0.363 | 0 |
| TM | 185.49 | 186.73 | 0.384 | 0 |
| JNJ | 265.59 | 267.58 | 0.397 | 0 |
| PSX | 248.51 | 252.22 | 0.403 | 0 |
| REGN | 741.83 | 750.52 | 0.453 | 0 |
| GS | 903.85 | 916.47 | 0.466 | 0 |
| CM | 110.76 | 111.74 | 0.466 | 0 |
| SPGI | 388.57 | 392.57 | 0.474 | 0 |
| VLO | 379.57 | 387.89 | 0.476 | 0 |
| MDLZ | 58.79 | 59.33 | 0.494 | 0 |
| SPG | 203.01 | 204.31 | 0.502 | 0 |
| SPCX | 145.88 | 149.2 | 0.549 | 0 |
| MFG | 10.82 | 10.995 | 0.648 | 0 |
| HONA | 151.39 | 155.46 | 0.664 | 0 |
| VRTX | 519.25 | 526.7 | 0.673 | 0 |
| GILD | 148.79 | 151.32 | 0.732 | 0 |
| MCK | 847.29 | 865.32 | 0.878 | 0 |
| MRK | 146.09 | 149.32 | 0.964 | 0 |
| PEP | 126.42 | 128.69 | 1.039 | 0 |
| PFE | 28.26 | 28.725 | 1.043 | 0 |
| DUK | 112.52 | 114.2 | 1.104 | 0 |
| EXC | 39.73 | 40.64 | 1.357 | 0 |

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.85 | 5.25 | 7 |
| SHOP | 134.74 | 148.3 | 2.0 | 7 |
| MTX.DE | 358.8 | 376.5 | 1.922 | 4 |
| KLAC | 182.41 | 196.5 | 1.902 | 7 |
| DB1.DE | 280.1 | 288.6 | 1.809 | 4 |
| ASML | 1524.8 | 1610.4 | 1.772 | 4 |
| ILMN | 250.06 | 272.0 | 1.726 | 7 |
| TXN | 267.97 | 281.82 | 1.7 | 7 |
| LLY | 1138.79 | 1186.24 | 1.663 | 7 |
| MRK.DE | 133.45 | 137.7 | 1.648 | 4 |
| BEI.DE | 75.74 | 78.2 | 1.57 | 4 |
| EMR | 152.28 | 157.28 | 1.348 | 7 |
| AMAT | 487.68 | 512.15 | 1.272 | 7 |
| TMO | 663.57 | 679.61 | 1.047 | 7 |
| LIN | 466.24 | 473.42 | 1.031 | 7 |
| DHR | 220.67 | 226.18 | 1.014 | 7 |
| MAR | 354.63 | 361.73 | 0.98 | 7 |
| MMM | 165.37 | 168.52 | 0.906 | 7 |
| AMGN | 415.76 | 423.74 | 0.842 | 7 |
| SY1.DE | 91.74 | 93.28 | 0.822 | 4 |
| MCHP | 76.55 | 78.78 | 0.811 | 7 |
| IDXX | 524.12 | 533.55 | 0.791 | 7 |
| ISRG | 404.44 | 412.25 | 0.69 | 7 |
| ADI | 390.55 | 398.27 | 0.661 | 7 |
| ROST | 231.85 | 234.41 | 0.515 | 7 |
| WDAY | 185.82 | 189.18 | 0.495 | 6 |
| LRCX | 317.13 | 324.04 | 0.484 | 7 |
| TSM | 452.88 | 457.05 | 0.404 | 7 |
| ON | 74.48 | 75.93 | 0.388 | 7 |
| TJX | 132.75 | 133.85 | 0.37 | 3 |
| DIS | 105.1 | 105.47 | 0.174 | 6 |
| SHW | 329.48 | 330.53 | 0.135 | 4 |
| GLW | 157.72 | 158.72 | 0.124 | 5 |
| MRNA | 202.67 | 203.38 | 0.056 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.