# Stundenwache

Stand: 2026-10-29 · 272 Werte mit Stundendaten · erstellt 2026-10-30 11:18 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 4, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CSCO | 108.28 | 108.61 | 0.107 | 0 |
| INTC | 90.84 | 92.08 | 0.244 | 0 |
| CTSH | 61.55 | 62.56 | 0.346 | 0 |
| ORLY | 86.7 | 88.08 | 0.635 | 0 |
| MPC | 419.28 | 432.7 | 0.715 | 0 |
| INTU | 319.02 | 331.23 | 0.901 | 0 |
| AXON | 413.18 | 438.17 | 1.383 | 0 |
| DE | 625.97 | 660.0 | 1.947 | 0 |

## Swing-Hoch ueberwunden (98)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| COP | 130.97 | 150.01 | 5.434 | 7 |
| XOM | 164.37 | 183.18 | 4.677 | 7 |
| IBM | 224.51 | 258.25 | 4.356 | 7 |
| LMT | 559.48 | 643.68 | 4.244 | 7 |
| BTI | 42.42 | 46.12 | 4.119 | 4 |
| SNY | 73.04 | 79.84 | 4.068 | 4 |
| SRT3.DE | 257.7 | 294.2 | 3.964 | 4 |
| QIA.DE | 42.345 | 45.07 | 3.521 | 4 |
| AEP | 121.8 | 129.33 | 2.946 | 7 |
| BAYN.DE | 45.83 | 49.82 | 2.825 | 4 |
| EXC | 43.58 | 45.94 | 2.726 | 7 |
| CSX | 49.22 | 52.24 | 2.669 | 7 |
| MRK.DE | 142.6 | 151.25 | 2.547 | 4 |
| AZN | 128.06 | 136.3717 | 2.468 | 4 |
| TXN | 289.31 | 312.92 | 2.401 | 7 |
| SBUX | 100.33 | 105.62 | 2.384 | 7 |
| P911.DE | 43.59 | 46.59 | 2.365 | 4 |
| TTE | 81.63 | 85.59 | 2.321 | 4 |
| RTX | 187.41 | 199.42 | 2.244 | 7 |
| LULU | 100.67 | 109.83 | 2.202 | 7 |
| ADS.DE | 161.15 | 169.7 | 2.198 | 4 |
| CM | 113.93 | 118.82 | 2.174 | 7 |
| MCD | 247.29 | 257.39 | 2.166 | 7 |
| GD | 357.46 | 371.01 | 2.128 | 7 |
| HD | 314.66 | 328.98 | 1.907 | 7 |
| GEHC | 72.3 | 76.435 | 1.863 | 7 |
| BMO | 170.68 | 175.97 | 1.849 | 7 |
| DBK.DE | 28.815 | 30.39 | 1.779 | 4 |
| XEL | 76.54 | 79.07 | 1.731 | 7 |
| AMGN | 441.76 | 460.89 | 1.721 | 7 |
| ADI | 408.4 | 433.01 | 1.7 | 7 |
| UPS | 103.08 | 107.31 | 1.671 | 7 |
| NVS | 129.34 | 133.88 | 1.652 | 4 |
| SNPS | 459.88 | 490.28 | 1.651 | 7 |
| UNP | 291.93 | 301.94 | 1.643 | 7 |
| ENB | 48.14 | 49.25 | 1.489 | 7 |
| SHL.DE | 42.06 | 43.13 | 1.489 | 4 |
| ORCL | 128.33 | 139.59 | 1.472 | 7 |
| GILD | 159.69 | 165.63 | 1.389 | 7 |
| EMR | 165.01 | 170.75 | 1.315 | 7 |
| WDAY | 185.82 | 195.46 | 1.307 | 7 |
| HNR1.DE | 283.2 | 289.2 | 1.265 | 4 |
| RY | 202.42 | 205.99 | 1.256 | 7 |
| LLY | 1321.21 | 1373.0 | 1.178 | 7 |
| MCHP | 77.74 | 81.13 | 1.096 | 7 |
| BIIB | 240.99 | 249.81 | 1.079 | 7 |
| TSLA | 388.86 | 403.29 | 1.064 | 7 |
| EOAN.DE | 18.67 | 19.035 | 1.012 | 4 |
| BNS | 94.04 | 95.395 | 1.007 | 7 |
| NXPI | 255.31 | 265.7 | 0.996 | 6 |
| EQIX | 1008.29 | 1036.87 | 0.883 | 7 |
| SHEL | 39.8 | 40.4861 | 0.878 | 4 |
| CDNS | 331.5 | 342.76 | 0.847 | 7 |
| GS | 906.48 | 927.515 | 0.842 | 7 |
| PM | 204.0 | 208.55 | 0.82 | 7 |
| BNY | 146.86 | 149.36 | 0.788 | 7 |
| HEN3.DE | 79.44 | 80.56 | 0.769 | 4 |
| QCOM | 180.78 | 185.34 | 0.758 | 6 |
| TMO | 694.33 | 709.29 | 0.744 | 7 |
| TD | 126.05 | 127.22 | 0.6 | 7 |
| BLK | 1159.99 | 1176.3101 | 0.595 | 7 |
| WDC | 381.88 | 395.52 | 0.594 | 7 |
| MUV2.DE | 561.0 | 566.0 | 0.565 | 4 |
| SPG | 213.63 | 215.74 | 0.56 | 7 |
| LOW | 204.52 | 207.28 | 0.543 | 3 |
| FRE.DE | 47.295 | 47.72 | 0.532 | 4 |
| C | 124.01 | 125.75 | 0.525 | 7 |
| MS | 187.16 | 190.0 | 0.524 | 7 |
| BAS.DE | 52.86 | 53.37 | 0.516 | 4 |
| HEI.DE | 150.0 | 151.75 | 0.485 | 4 |
| MMM | 175.56 | 177.375 | 0.442 | 6 |
| WFC | 83.99 | 84.805 | 0.426 | 7 |
| MO | 76.09 | 76.74 | 0.393 | 2 |
| AXON | 431.13 | 438.17 | 0.39 | 5 |
| JNJ | 272.36 | 275.2 | 0.384 | 7 |
| AMAT | 414.0 | 421.7 | 0.373 | 7 |
| APH | 80.87 | 82.09 | 0.37 | 7 |
| AMD | 556.79 | 566.46 | 0.34 | 7 |
| IDXX | 571.75 | 575.98 | 0.323 | 5 |
| ALV.DE | 437.5 | 439.3 | 0.283 | 4 |
| UBS | 38.96 | 39.18 | 0.259 | 4 |
| ILMN | 286.4 | 289.84 | 0.256 | 6 |
| MA | 633.29 | 635.705 | 0.207 | 7 |
| SYK | 309.68 | 311.41 | 0.202 | 6 |
| ABBV | 289.59 | 290.89 | 0.194 | 4 |
| CPRT | 29.43 | 29.57 | 0.165 | 7 |
| VRTX | 537.81 | 540.21 | 0.151 | 6 |
| MAR | 398.42 | 399.67 | 0.145 | 7 |
| DHL.DE | 58.92 | 59.06 | 0.137 | 2 |
| USB | 60.49 | 60.645 | 0.135 | 4 |
| VOW3.DE | 70.2 | 70.4 | 0.105 | 4 |
| NVO | 264.75 | 265.2 | 0.087 | 3 |
| MDT | 96.89 | 97.1 | 0.086 | 3 |
| GLW | 128.58 | 128.9 | 0.044 | 7 |
| DB1.DE | 317.2 | 317.4 | 0.032 | 3 |
| DXCM | 79.86 | 79.93 | 0.027 | 1 |
| PAH3.DE | 25.6 | 25.61 | 0.015 | 3 |
| DUK | 125.87 | 125.89 | 0.009 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.