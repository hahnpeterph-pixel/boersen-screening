# Stundenwache

Stand: 2026-09-22 · 267 Werte mit Stundendaten · erstellt 2026-09-22 21:57 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MA | 561.9 | 556.69 | -0.594 | 7 |
| AXP | 308.67 | 305.21 | -0.531 | 6 |
| MS | 200.26 | 200.21 | -0.009 | 3 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| COF | 200.28 | 200.79 | 0.101 | 1 |

## Tief angetestet (24)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| RHM.DE | 986.6 | 987.1 | 0.014 | 0 |
| SMFG | 26.14 | 26.15 | 0.017 | 0 |
| UNH | 372.42 | 372.95 | 0.053 | 0 |
| SPGI | 401.95 | 402.57 | 0.059 | 0 |
| CMCSA | 22.36 | 22.42 | 0.078 | 0 |
| MUV2.DE | 501.8 | 502.6 | 0.088 | 0 |
| MDT | 90.56 | 90.77 | 0.098 | 0 |
| ENB | 47.795 | 47.92 | 0.151 | 0 |
| BMY | 62.04 | 62.25 | 0.165 | 0 |
| MUFG | 23.01 | 23.1 | 0.179 | 0 |
| GD | 342.215 | 343.45 | 0.181 | 0 |
| COP | 124.4926 | 125.26 | 0.214 | 0 |
| VZ | 46.1701 | 46.445 | 0.256 | 0 |
| HDB | 23.245 | 23.42 | 0.3 | 0 |
| CM | 114.13 | 114.79 | 0.316 | 0 |
| BRK-B | 501.5 | 503.61 | 0.335 | 0 |
| HSBC | 100.92 | 101.6 | 0.365 | 0 |
| MBG.DE | 42.895 | 43.375 | 0.391 | 0 |
| EQNR | 41.3375 | 41.82 | 0.407 | 0 |
| CB | 333.14 | 335.8 | 0.51 | 0 |
| SNY | 42.03 | 42.48 | 0.656 | 0 |
| CSCO | 104.51 | 106.43 | 0.67 | 0 |
| PGR | 203.6456 | 206.92 | 0.761 | 0 |
| PBR | 20.2407 | 20.75 | 0.835 | 0 |

## Swing-Hoch ueberwunden (64)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 182.57 | 10.316 | 7 |
| WBD | 28.45 | 30.82 | 4.624 | 7 |
| ARM | 253.155 | 333.33 | 4.481 | 7 |
| AMD | 526.79 | 624.0 | 3.811 | 7 |
| MU | 944.94 | 1094.58 | 3.267 | 7 |
| INTC | 104.9 | 123.84 | 2.888 | 7 |
| DHL.DE | 55.7 | 58.64 | 2.751 | 9 |
| SRT3.DE | 240.2 | 254.4 | 2.018 | 9 |
| SHOP | 134.74 | 147.8 | 1.982 | 7 |
| BABA | 111.25 | 116.27 | 1.919 | 7 |
| META | 685.31 | 736.68 | 1.887 | 7 |
| NET | 319.43 | 352.945 | 1.85 | 7 |
| DDOG | 227.58 | 247.51 | 1.848 | 7 |
| IFX.DE | 55.6 | 59.97 | 1.682 | 9 |
| ISRG | 382.41 | 402.02 | 1.647 | 7 |
| TSM | 435.37 | 452.05 | 1.631 | 7 |
| ZS | 196.575 | 210.24 | 1.333 | 7 |
| QCOM | 185.46 | 198.27 | 1.326 | 7 |
| QIA.DE | 37.24 | 38.5 | 1.298 | 9 |
| AAPL | 330.81 | 339.73 | 1.249 | 7 |
| MRK | 147.09 | 150.91 | 1.221 | 7 |
| PH | 939.6 | 964.8 | 1.187 | 7 |
| LLY | 1138.79 | 1170.48 | 1.182 | 7 |
| NVDA | 222.0 | 228.83 | 1.155 | 7 |
| MMM | 165.37 | 169.3 | 1.133 | 7 |
| MRVL | 247.89 | 262.27 | 1.106 | 7 |
| AZN | 164.55 | 168.355 | 1.098 | 7 |
| TJX | 127.8 | 130.8 | 1.076 | 7 |
| ETN | 427.14 | 442.47 | 1.009 | 7 |
| PLTR | 177.88 | 184.98 | 1.007 | 7 |
| EQIX | 1033.99 | 1059.27 | 1.002 | 7 |
| CDNS | 293.4 | 302.81 | 0.991 | 7 |
| SY1.DE | 91.74 | 93.58 | 0.937 | 7 |
| ADI | 380.36 | 390.36 | 0.921 | 7 |
| DE | 689.37 | 703.24 | 0.882 | 7 |
| ZAL.DE | 21.95 | 22.47 | 0.826 | 8 |
| MAR | 342.31 | 348.06 | 0.8 | 7 |
| SNDK | 1807.38 | 1886.05 | 0.75 | 7 |
| KLAC | 182.41 | 188.29 | 0.727 | 7 |
| ANET | 200.25 | 205.175 | 0.637 | 7 |
| BEI.DE | 75.74 | 76.62 | 0.595 | 6 |
| EMR | 152.28 | 154.24 | 0.546 | 7 |
| BIIB | 222.25 | 225.41 | 0.526 | 6 |
| AMAT | 464.57 | 472.47 | 0.425 | 6 |
| TXN | 267.97 | 271.41 | 0.423 | 7 |
| ADS.DE | 145.25 | 146.75 | 0.42 | 8 |
| TSLA | 374.12 | 378.86 | 0.361 | 7 |
| BHP | 86.93 | 87.81 | 0.346 | 4 |
| FAST | 49.78 | 50.09 | 0.306 | 4 |
| WDAY | 185.82 | 188.19 | 0.298 | 7 |
| LULU | 102.18 | 103.72 | 0.294 | 7 |
| HON | 210.59 | 211.85 | 0.287 | 5 |
| MCHP | 75.16 | 75.815 | 0.262 | 6 |
| PFE | 27.81 | 27.93 | 0.257 | 5 |
| HEN3.DE | 74.9 | 75.2 | 0.223 | 3 |
| WMT | 109.74 | 110.12 | 0.21 | 3 |
| ABBV | 264.25 | 265.32 | 0.197 | 6 |
| ABT | 103.3 | 103.71 | 0.173 | 7 |
| ROST | 231.85 | 232.63 | 0.16 | 5 |
| GOOGL | 349.91 | 351.185 | 0.147 | 7 |
| MRK.DE | 133.45 | 133.8 | 0.135 | 2 |
| DHR | 220.67 | 221.21 | 0.094 | 5 |
| IDXX | 520.41 | 521.49 | 0.08 | 6 |
| BNS | 94.02 | 94.04 | 0.013 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.