# Stundenwache

Stand: 2026-09-23 · 267 Werte mit Stundendaten · erstellt 2026-09-23 22:12 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MA | 561.9 | 559.95 | -0.219 | 6 |
| PAH3.DE | 26.26 | 26.26 | -0.0 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (30)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TD | 119.4 | 119.43 | 0.015 | 0 |
| HD | 296.68 | 296.86 | 0.028 | 0 |
| SONY | 23.185 | 23.2 | 0.031 | 0 |
| HSBC | 100.17 | 100.26 | 0.049 | 0 |
| COF | 195.84 | 196.11 | 0.057 | 0 |
| BABA | 110.591 | 110.79 | 0.068 | 0 |
| AMT | 170.485 | 170.79 | 0.075 | 0 |
| MFG | 10.735 | 10.755 | 0.083 | 0 |
| GLW | 153.6261 | 154.44 | 0.094 | 0 |
| SPG | 203.84 | 204.18 | 0.107 | 0 |
| MUFG | 22.765 | 22.82 | 0.114 | 0 |
| TTD | 12.58 | 12.67 | 0.142 | 0 |
| BLK | 1056.3199 | 1061.26 | 0.2 | 0 |
| BHP | 84.38 | 84.99 | 0.229 | 0 |
| AEP | 117.95 | 118.41 | 0.239 | 0 |
| DBK.DE | 31.515 | 31.775 | 0.291 | 0 |
| AMZN | 247.76 | 249.35 | 0.292 | 0 |
| CSGP | 27.89 | 28.25 | 0.302 | 0 |
| ADBE | 237.51 | 240.68 | 0.304 | 0 |
| SKHY | 186.11 | 189.32 | 0.317 | 0 |
| FANG | 183.51 | 185.61 | 0.323 | 0 |
| VZ | 46.165 | 46.52 | 0.325 | 0 |
| SNY | 41.405 | 41.65 | 0.348 | 0 |
| SPGI | 401.36 | 406.68 | 0.512 | 0 |
| MPC | 378.8 | 388.14 | 0.573 | 0 |
| DTE.DE | 26.51 | 26.88 | 0.584 | 0 |
| T | 24.9428 | 25.32 | 0.586 | 0 |
| DASH | 184.86 | 189.28 | 0.594 | 0 |
| PSX | 250.26 | 256.47 | 0.677 | 0 |
| MCD | 234.04 | 238.34 | 0.894 | 0 |

## Swing-Hoch ueberwunden (56)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 182.0 | 10.193 | 7 |
| WBD | 28.45 | 30.75 | 4.684 | 7 |
| ARM | 253.155 | 332.56 | 4.344 | 7 |
| AMD | 526.79 | 614.92 | 3.391 | 7 |
| MU | 944.94 | 1071.4301 | 2.717 | 7 |
| INTC | 104.9 | 122.6 | 2.645 | 7 |
| DDOG | 227.58 | 251.58 | 2.324 | 7 |
| META | 685.31 | 744.02 | 2.134 | 7 |
| PLTR | 177.88 | 191.77 | 2.039 | 7 |
| NET | 319.43 | 352.46 | 1.845 | 7 |
| SRT3.DE | 240.2 | 252.7 | 1.777 | 9 |
| ZS | 196.575 | 214.61 | 1.77 | 7 |
| DHL.DE | 55.7 | 57.5 | 1.667 | 9 |
| CDNS | 293.4 | 309.09 | 1.613 | 7 |
| PH | 939.6 | 971.23 | 1.497 | 7 |
| MMM | 165.37 | 170.28 | 1.433 | 7 |
| TJX | 127.8 | 131.655 | 1.391 | 7 |
| ISRG | 382.41 | 398.32 | 1.384 | 7 |
| DE | 689.37 | 709.68 | 1.322 | 7 |
| MAR | 342.31 | 351.61 | 1.257 | 7 |
| FAST | 49.78 | 51.01 | 1.215 | 7 |
| QCOM | 185.46 | 197.25 | 1.213 | 7 |
| IFX.DE | 55.6 | 58.59 | 1.135 | 9 |
| TSM | 435.37 | 446.68 | 1.077 | 7 |
| SHOP | 134.74 | 142.33 | 1.015 | 7 |
| MRVL | 247.89 | 260.9 | 0.99 | 7 |
| CRWD | 250.32 | 262.5 | 0.973 | 7 |
| BIIB | 222.25 | 227.59 | 0.921 | 7 |
| WDAY | 185.82 | 192.33 | 0.834 | 7 |
| ETN | 427.14 | 439.07 | 0.79 | 7 |
| PFE | 27.81 | 28.165 | 0.777 | 7 |
| KLAC | 182.41 | 187.77 | 0.656 | 7 |
| EMR | 152.28 | 154.51 | 0.644 | 7 |
| PANW | 383.12 | 393.3 | 0.588 | 6 |
| TXN | 267.97 | 272.55 | 0.566 | 7 |
| ZAL.DE | 21.95 | 22.29 | 0.533 | 8 |
| AMAT | 464.57 | 474.52 | 0.527 | 6 |
| LLY | 1138.79 | 1152.7 | 0.501 | 7 |
| ILMN | 250.06 | 255.47 | 0.494 | 7 |
| LIN | 466.24 | 469.87 | 0.476 | 7 |
| HON | 210.59 | 212.57 | 0.471 | 7 |
| TSLA | 374.12 | 380.24 | 0.47 | 7 |
| ROST | 231.85 | 234.04 | 0.456 | 7 |
| WMT | 109.74 | 110.53 | 0.43 | 7 |
| FTNT | 176.1 | 178.76 | 0.404 | 6 |
| DB1.DE | 280.1 | 282.3 | 0.404 | 8 |
| SY1.DE | 91.74 | 92.42 | 0.349 | 9 |
| MTX.DE | 358.8 | 361.3 | 0.256 | 9 |
| BEI.DE | 75.74 | 76.06 | 0.22 | 9 |
| DHR | 220.67 | 221.7 | 0.187 | 6 |
| ABBV | 264.25 | 265.13 | 0.161 | 6 |
| NVS | 142.18 | 142.74 | 0.141 | 7 |
| IDXX | 520.41 | 522.16 | 0.14 | 1 |
| TEAM | 194.01 | 195.1 | 0.119 | 6 |
| SNDK | 1807.38 | 1815.9301 | 0.08 | 7 |
| LULU | 102.18 | 102.32 | 0.027 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.