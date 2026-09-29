# Stundenwache

Stand: 2026-09-29 · 273 Werte mit Stundendaten · erstellt 2026-09-29 22:56 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MA | 561.9 | 563.66 | 0.207 | 1 |

## Tief angetestet (36)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TTE | 87.6 | 87.65 | 0.032 | 0 |
| NVDA | 227.025 | 227.3 | 0.051 | 0 |
| LULU | 96.62 | 96.85 | 0.064 | 0 |
| MUV2.DE | 506.2 | 506.8 | 0.073 | 0 |
| BABA | 107.41 | 107.76 | 0.13 | 0 |
| ABBV | 262.59 | 263.27 | 0.133 | 0 |
| BNY | 146.29 | 146.97 | 0.212 | 0 |
| AXP | 303.995 | 305.51 | 0.249 | 0 |
| RY | 198.985 | 199.74 | 0.252 | 0 |
| BMO | 168.825 | 169.6 | 0.269 | 0 |
| CVS | 86.375 | 87.1 | 0.332 | 0 |
| SAN | 14.07 | 14.18 | 0.364 | 0 |
| TM | 185.49 | 186.73 | 0.384 | 0 |
| TD | 118.28 | 119.01 | 0.384 | 0 |
| HEI.DE | 142.55 | 144.15 | 0.388 | 0 |
| PSX | 248.51 | 252.22 | 0.403 | 0 |
| MUFG | 22.9301 | 23.14 | 0.428 | 0 |
| PH | 961.63 | 970.61 | 0.431 | 0 |
| BNS | 91.84 | 92.48 | 0.451 | 0 |
| GS | 903.85 | 916.47 | 0.466 | 0 |
| CM | 110.76 | 111.74 | 0.466 | 0 |
| SMFG | 25.745 | 26.03 | 0.47 | 0 |
| SPGI | 388.57 | 392.57 | 0.474 | 0 |
| VLO | 379.57 | 387.89 | 0.476 | 0 |
| SPG | 203.02 | 204.31 | 0.498 | 0 |
| SPCX | 145.88 | 149.2 | 0.549 | 0 |
| MFG | 10.835 | 10.995 | 0.595 | 0 |
| ADP | 258.3 | 261.76 | 0.683 | 0 |
| MPC | 380.02 | 392.13 | 0.724 | 0 |
| ACN | 172.13 | 177.27 | 0.736 | 0 |
| CB | 328.15 | 332.11 | 0.875 | 0 |
| PLD | 130.76 | 132.59 | 0.885 | 0 |
| PEP | 126.42 | 128.69 | 1.039 | 0 |
| PFE | 28.26 | 28.725 | 1.043 | 0 |
| DUK | 112.52 | 114.2 | 1.104 | 0 |
| EXC | 39.73 | 40.64 | 1.357 | 0 |

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.85 | 5.25 | 7 |
| SHOP | 134.74 | 148.3 | 2.0 | 7 |
| KLAC | 182.41 | 196.5 | 1.902 | 7 |
| ILMN | 250.06 | 272.0 | 1.726 | 7 |
| TXN | 267.97 | 281.82 | 1.7 | 7 |
| LLY | 1138.79 | 1186.24 | 1.663 | 7 |
| MRK.DE | 133.45 | 137.65 | 1.64 | 9 |
| ASML | 1524.8 | 1605.8 | 1.623 | 9 |
| MTX.DE | 358.8 | 371.5 | 1.367 | 9 |
| EMR | 152.28 | 157.28 | 1.348 | 7 |
| AMAT | 487.68 | 512.15 | 1.272 | 7 |
| DB1.DE | 280.1 | 285.9 | 1.173 | 9 |
| BEI.DE | 75.74 | 77.62 | 1.163 | 9 |
| TMO | 663.57 | 679.82 | 1.061 | 6 |
| LIN | 466.24 | 473.42 | 1.031 | 7 |
| DHR | 220.67 | 226.18 | 1.014 | 7 |
| MAR | 354.63 | 361.73 | 0.98 | 7 |
| MMM | 165.37 | 168.52 | 0.905 | 7 |
| SY1.DE | 91.74 | 93.38 | 0.866 | 9 |
| AMGN | 415.76 | 423.74 | 0.844 | 7 |
| MCHP | 76.55 | 78.78 | 0.811 | 7 |
| IDXX | 524.12 | 533.55 | 0.791 | 7 |
| ISRG | 404.44 | 412.25 | 0.69 | 7 |
| ADI | 390.55 | 398.27 | 0.661 | 7 |
| ROST | 231.85 | 234.41 | 0.515 | 7 |
| WDAY | 185.82 | 189.18 | 0.495 | 6 |
| LRCX | 317.13 | 324.04 | 0.484 | 7 |
| TSM | 452.88 | 457.05 | 0.404 | 7 |
| ON | 74.48 | 75.93 | 0.389 | 7 |
| TJX | 132.75 | 133.85 | 0.37 | 3 |
| DIS | 105.1 | 105.47 | 0.174 | 6 |
| SHW | 329.48 | 330.53 | 0.135 | 4 |
| GLW | 157.72 | 158.72 | 0.124 | 5 |
| MRNA | 202.67 | 203.38 | 0.056 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.