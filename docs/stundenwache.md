# Stundenwache

Stand: 2026-11-02 · 272 Werte mit Stundendaten · erstellt 2026-11-03 12:48 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| ISRG | 437.51 | 436.88 | -0.046 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (7)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKR | 52.97 | 53.06 | 0.043 | 0 |
| INTC | 59.4 | 59.95 | 0.079 | 0 |
| CVS | 87.88 | 88.5 | 0.291 | 0 |
| MUFG | 3330.0 | 3375.0 | 0.453 | 0 |
| JNJ | 267.44 | 270.56 | 0.457 | 0 |
| DB1.DE | 311.8 | 314.7 | 0.457 | 0 |
| AMT | 184.53 | 188.36 | 0.623 | 0 |

## Swing-Hoch ueberwunden (77)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| REGN | 825.52 | 961.43 | 4.619 | 7 |
| BAYN.DE | 45.83 | 52.64 | 4.363 | 5 |
| IDXX | 571.75 | 671.84 | 4.295 | 7 |
| QIA.DE | 42.345 | 45.085 | 4.154 | 5 |
| MCD | 247.29 | 265.64 | 3.579 | 7 |
| IBM | 224.51 | 252.56 | 3.575 | 7 |
| HD | 314.66 | 341.24 | 3.273 | 7 |
| AZN | 128.06 | 138.42 | 3.174 | 5 |
| GEHC | 72.3 | 79.56 | 3.15 | 7 |
| RTX | 187.41 | 202.83 | 2.838 | 7 |
| CPRT | 29.43 | 31.94 | 2.701 | 7 |
| UPS | 103.08 | 109.72 | 2.604 | 7 |
| UNP | 291.93 | 307.07 | 2.466 | 7 |
| LOW | 204.52 | 218.14 | 2.461 | 7 |
| SPG | 213.63 | 221.78 | 2.082 | 7 |
| CSX | 49.22 | 51.64 | 2.065 | 7 |
| DBK.DE | 28.815 | 30.63 | 2.051 | 5 |
| MA | 633.29 | 658.25 | 1.97 | 7 |
| ROP | 450.76 | 479.5 | 1.959 | 7 |
| KDP | 35.4 | 36.95 | 1.943 | 7 |
| FRE.DE | 47.295 | 48.915 | 1.938 | 5 |
| ADS.DE | 161.15 | 169.4 | 1.915 | 5 |
| WMT | 122.4 | 127.7 | 1.911 | 7 |
| HNR1.DE | 283.2 | 291.4 | 1.794 | 5 |
| DXCM | 79.86 | 84.79 | 1.718 | 7 |
| SHL.DE | 42.06 | 43.41 | 1.714 | 5 |
| MAR | 398.42 | 416.41 | 1.7 | 7 |
| SBUX | 100.33 | 104.43 | 1.692 | 7 |
| WDAY | 185.82 | 198.17 | 1.662 | 7 |
| LULU | 100.67 | 107.77 | 1.625 | 7 |
| HEI.DE | 150.0 | 156.25 | 1.601 | 5 |
| ABT | 105.88 | 110.28 | 1.428 | 7 |
| GM | 85.79 | 89.945 | 1.393 | 7 |
| V | 414.6 | 425.51 | 1.386 | 7 |
| NEE | 82.81 | 85.035 | 1.329 | 7 |
| FDX | 307.94 | 318.35 | 1.323 | 7 |
| DUK | 125.87 | 128.38 | 1.122 | 7 |
| MDT | 96.89 | 99.3 | 1.074 | 7 |
| VRTX | 537.81 | 556.05 | 1.073 | 7 |
| HEN3.DE | 79.44 | 80.88 | 1.042 | 5 |
| COST | 1021.45 | 1040.64 | 1.021 | 7 |
| UBS | 38.96 | 39.77 | 0.985 | 5 |
| BRK-B | 549.0 | 556.715 | 0.98 | 7 |
| BIIB | 240.99 | 248.96 | 0.977 | 7 |
| LIN | 512.49 | 519.76 | 0.897 | 7 |
| MDLZ | 65.22 | 66.395 | 0.78 | 7 |
| CMCSA | 23.29 | 23.88 | 0.772 | 7 |
| PDD | 80.17 | 81.69 | 0.694 | 7 |
| IBN | 1404.9 | 1424.5 | 0.693 | 6 |
| MMM | 175.56 | 178.4 | 0.641 | 7 |
| CHTR | 112.71 | 115.53 | 0.633 | 7 |
| BAS.DE | 52.86 | 53.43 | 0.621 | 5 |
| SHW | 346.19 | 352.41 | 0.607 | 7 |
| CB | 364.86 | 369.0 | 0.605 | 7 |
| PYPL | 57.95 | 58.8 | 0.592 | 7 |
| NKE | 38.5 | 39.125 | 0.59 | 7 |
| ALV.DE | 437.5 | 441.1 | 0.565 | 5 |
| NVO | 264.75 | 267.65 | 0.544 | 5 |
| PAH3.DE | 25.6 | 25.9 | 0.476 | 5 |
| PEP | 139.0 | 140.47 | 0.459 | 6 |
| MNST | 47.54 | 48.025 | 0.438 | 7 |
| PFE | 30.44 | 30.705 | 0.421 | 6 |
| DE | 660.39 | 667.62 | 0.412 | 6 |
| CCEP | 114.55 | 115.59 | 0.404 | 6 |
| SO | 94.04 | 94.625 | 0.339 | 5 |
| KO | 95.37 | 95.85 | 0.259 | 5 |
| WFC | 85.49 | 85.905 | 0.217 | 2 |
| AXP | 326.49 | 328.03 | 0.209 | 7 |
| ADSK | 256.17 | 257.87 | 0.201 | 6 |
| NXPI | 255.31 | 257.31 | 0.171 | 7 |
| GE | 314.0 | 315.79 | 0.165 | 6 |
| PLD | 129.24 | 129.68 | 0.162 | 7 |
| ACN | 259.39 | 260.96 | 0.14 | 7 |
| COF | 210.04 | 210.74 | 0.13 | 7 |
| TMUS | 159.41 | 160.15 | 0.121 | 1 |
| SPGI | 474.61 | 475.18 | 0.049 | 6 |
| SPOT | 593.8 | 593.87 | 0.003 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.