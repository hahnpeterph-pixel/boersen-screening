# Stundenwache

Stand: 2026-10-22 · 272 Werte mit Stundendaten · erstellt 2026-10-23 09:55 UTC

> **Sitzung noch nicht abgeschlossen.** 60 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| ASML | 1407.4 | 1406.6 | -0.015 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (7)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| KLAC | 146.55 | 147.83 | 0.15 | 0 |
| INTC | 84.65 | 85.4901 | 0.152 | 0 |
| NEM | 111.41 | 113.96 | 0.696 | 0 |
| WFC | 81.15 | 83.02 | 0.909 | 0 |
| HON | 209.66 | 218.43 | 1.788 | 0 |
| LULU | 95.75 | 104.06 | 2.3 | 0 |
| UNP | 286.05 | 298.24 | 2.359 | 0 |

## Swing-Hoch ueberwunden (110)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| BRK-B | 507.24 | 547.09 | 6.267 | 7 |
| SO | 83.98 | 93.81 | 5.929 | 7 |
| COST | 931.09 | 1018.44 | 5.522 | 7 |
| CL | 87.22 | 97.4 | 5.452 | 7 |
| TRV | 362.75 | 405.45 | 5.283 | 7 |
| KO | 87.29 | 95.34 | 5.056 | 7 |
| DUK | 115.17 | 125.41 | 4.949 | 7 |
| COP | 130.97 | 145.63 | 4.305 | 7 |
| MO | 69.6 | 76.07 | 4.147 | 7 |
| ROP | 391.01 | 436.35 | 4.142 | 7 |
| KDP | 32.14 | 35.19 | 3.994 | 7 |
| CVX | 207.41 | 226.68 | 3.965 | 7 |
| IBM | 224.51 | 252.27 | 3.946 | 7 |
| PEP | 127.21 | 138.86 | 3.8 | 7 |
| AEP | 121.8 | 130.65 | 3.76 | 7 |
| CTSH | 64.74 | 73.72 | 3.676 | 7 |
| XOM | 164.37 | 178.23 | 3.676 | 7 |
| WDAY | 185.82 | 209.9855 | 3.514 | 7 |
| SONY | 3797.0 | 4098.0 | 3.396 | 7 |
| NVS | 120.02 | 127.54 | 3.231 | 3 |
| ADP | 290.12 | 308.09 | 3.094 | 7 |
| TM | 2944.5 | 3096.0 | 2.832 | 7 |
| CDW | 150.34 | 164.64 | 2.769 | 7 |
| CSX | 49.22 | 51.685 | 2.679 | 7 |
| LLY | 1206.63 | 1306.74 | 2.527 | 7 |
| BTI | 42.42 | 44.52 | 2.496 | 3 |
| PAYX | 112.52 | 118.805 | 2.477 | 7 |
| LIN | 492.1 | 510.44 | 2.37 | 7 |
| CSGP | 32.65 | 35.45 | 2.346 | 7 |
| ZAL.DE | 24.73 | 26.42 | 2.268 | 3 |
| SPOT | 536.74 | 583.98 | 2.22 | 7 |
| QIA.DE | 42.345 | 44.995 | 2.192 | 3 |
| KHC | 23.74 | 25.075 | 2.129 | 7 |
| SPGI | 433.67 | 453.12 | 2.09 | 7 |
| LMT | 559.48 | 590.205 | 2.071 | 7 |
| PG | 159.47 | 165.602 | 1.945 | 7 |
| SRT3.DE | 257.7 | 277.2 | 1.928 | 3 |
| EOAN.DE | 17.855 | 18.525 | 1.926 | 3 |
| CTAS | 216.8 | 224.14 | 1.88 | 7 |
| MMM | 167.95 | 175.54 | 1.85 | 7 |
| HD | 314.66 | 327.695 | 1.823 | 7 |
| XEL | 76.54 | 78.97 | 1.823 | 7 |
| ACN | 243.67 | 258.77 | 1.745 | 7 |
| FDX | 294.29 | 304.01 | 1.735 | 7 |
| HNR1.DE | 270.8 | 278.8 | 1.728 | 3 |
| BIIB | 240.99 | 253.87 | 1.705 | 7 |
| TD | 121.41 | 125.085 | 1.669 | 7 |
| BLK | 1092.92 | 1137.87 | 1.645 | 7 |
| GSK | 17.91 | 18.92 | 1.645 | 3 |
| ADBE | 256.51 | 270.65 | 1.631 | 7 |
| ODFL | 182.91 | 189.95 | 1.621 | 7 |
| RTX | 187.41 | 194.78 | 1.599 | 7 |
| EXC | 43.58 | 44.84 | 1.512 | 7 |
| INTU | 336.26 | 354.96 | 1.507 | 7 |
| SPG | 206.5 | 212.05 | 1.503 | 7 |
| NOW | 148.14 | 157.0 | 1.461 | 7 |
| SAP.DE | 204.2 | 212.35 | 1.38 | 3 |
| V | 404.74 | 414.31 | 1.287 | 7 |
| VRTX | 517.68 | 535.22 | 1.282 | 7 |
| VRSK | 195.94 | 203.29 | 1.237 | 7 |
| UNP | 291.93 | 298.24 | 1.221 | 7 |
| MCD | 247.29 | 252.59 | 1.218 | 7 |
| BMW.DE | 56.42 | 58.14 | 1.146 | 3 |
| NEE | 80.27 | 81.9 | 1.024 | 7 |
| HON | 213.5 | 218.43 | 1.005 | 6 |
| JNJ | 260.77 | 267.71 | 1.003 | 7 |
| MA | 622.49 | 632.89 | 0.995 | 7 |
| PGR | 223.78 | 229.61 | 0.981 | 7 |
| CNQ | 52.57 | 53.9 | 0.958 | 7 |
| RY | 199.27 | 201.99 | 0.951 | 7 |
| LULU | 100.67 | 104.06 | 0.938 | 6 |
| TEAM | 214.77 | 223.2 | 0.938 | 7 |
| PFE | 29.88 | 30.42 | 0.928 | 7 |
| AXP | 319.85 | 325.13 | 0.912 | 7 |
| CPRT | 28.29 | 29.095 | 0.857 | 7 |
| UNH | 414.12 | 425.06 | 0.826 | 7 |
| BMO | 168.14 | 170.44 | 0.802 | 7 |
| SNY | 73.04 | 74.19 | 0.787 | 3 |
| USB | 59.17 | 60.015 | 0.738 | 7 |
| ORLY | 90.73 | 92.02 | 0.72 | 6 |
| CMCSA | 22.41 | 22.85 | 0.672 | 7 |
| BEI.DE | 82.52 | 83.42 | 0.663 | 2 |
| LOW | 201.27 | 204.39 | 0.628 | 7 |
| SBUX | 100.33 | 101.96 | 0.61 | 7 |
| SY1.DE | 100.8 | 101.7 | 0.529 | 3 |
| AMGN | 441.76 | 447.39 | 0.517 | 7 |
| CM | 113.93 | 115.0 | 0.508 | 6 |
| REGN | 809.49 | 819.54 | 0.476 | 7 |
| CB | 361.21 | 363.97 | 0.429 | 7 |
| NKE | 37.87 | 38.31 | 0.412 | 6 |
| MDLZ | 64.67 | 65.19 | 0.384 | 4 |
| ADSK | 251.74 | 254.95 | 0.38 | 5 |
| BMY | 62.25 | 63.01 | 0.37 | 7 |
| CCEP | 113.51 | 114.27 | 0.336 | 5 |
| HEI.DE | 145.65 | 146.75 | 0.325 | 3 |
| UL | 49.355 | 49.665 | 0.316 | 3 |
| MRK.DE | 142.6 | 143.65 | 0.284 | 3 |
| NVO | 260.4 | 261.95 | 0.28 | 3 |
| ISRG | 440.4 | 443.99 | 0.273 | 5 |
| SHW | 343.64 | 345.62 | 0.257 | 6 |
| SYK | 305.03 | 307.15 | 0.24 | 6 |
| DIS | 112.69 | 113.16 | 0.231 | 2 |
| GEHC | 71.02 | 71.42 | 0.214 | 5 |
| BP | 6.227 | 6.247 | 0.134 | 3 |
| ZS | 237.22 | 237.83 | 0.053 | 4 |
| MDT | 96.5 | 96.58 | 0.03 | 1 |
| MBG.DE | 41.53 | 41.56 | 0.029 | 1 |
| AAPL | 348.15 | 348.32 | 0.028 | 1 |
| IDXX | 566.55 | 566.85 | 0.022 | 2 |
| EQNR | 440.3 | 440.4 | 0.01 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.