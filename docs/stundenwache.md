# Stundenwache

Stand: 2026-10-06 · 273 Werte mit Stundendaten · erstellt 2026-10-07 11:42 UTC

> **Sitzung noch nicht abgeschlossen.** 60 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MBG.DE | 39.41 | 39.015 | -0.331 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ALV.DE | 415.7 | 416.1 | 0.05 | 0 |
| BA | 189.33 | 189.82 | 0.077 | 0 |
| IFX.DE | 60.74 | 60.96 | 0.082 | 0 |
| CTSH | 56.93 | 57.21 | 0.123 | 0 |
| USB | 57.05 | 57.29 | 0.245 | 0 |
| SY1.DE | 90.92 | 91.4 | 0.266 | 0 |
| CPRT | 26.64 | 26.83 | 0.276 | 0 |
| CVS | 85.53 | 86.42 | 0.451 | 0 |
| KHC | 21.76 | 22.02 | 0.478 | 0 |
| GILD | 142.6 | 144.27 | 0.482 | 0 |
| ROST | 221.77 | 224.24 | 0.498 | 0 |
| HON | 210.74 | 212.84 | 0.543 | 0 |

## Swing-Hoch ueberwunden (60)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.97 | 7.244 | 7 |
| SHOP | 134.74 | 164.5 | 4.141 | 7 |
| ON | 74.48 | 86.28 | 3.752 | 7 |
| SNPS | 445.92 | 505.37 | 2.976 | 7 |
| PBR | 54.61 | 59.46 | 2.938 | 7 |
| CDNS | 330.81 | 359.58 | 2.393 | 7 |
| CSCO | 111.5 | 117.97 | 2.338 | 7 |
| CEG | 271.0 | 300.16 | 2.266 | 7 |
| SPCX | 158.13 | 171.99 | 2.138 | 7 |
| MPC | 398.33 | 432.33 | 2.035 | 7 |
| MELI | 1739.88 | 1858.79 | 2.026 | 7 |
| TXN | 284.39 | 297.32 | 1.755 | 7 |
| GEV | 973.41 | 1029.42 | 1.687 | 7 |
| MSFT | 509.44 | 529.49 | 1.642 | 7 |
| FTNT | 181.37 | 191.29 | 1.616 | 7 |
| APH | 84.48 | 88.63 | 1.61 | 7 |
| CRWD | 263.87 | 278.93 | 1.362 | 7 |
| VLO | 395.85 | 419.34 | 1.352 | 7 |
| AVGO | 361.86 | 375.92 | 1.323 | 7 |
| ADSK | 222.0 | 231.27 | 1.303 | 7 |
| SO | 83.98 | 85.43 | 1.15 | 7 |
| PSX | 259.11 | 269.82 | 1.123 | 7 |
| LIN | 480.56 | 490.0 | 1.117 | 7 |
| NVDA | 233.21 | 239.17 | 1.11 | 7 |
| XEL | 71.37 | 72.725 | 1.088 | 7 |
| AMZN | 250.88 | 256.33 | 1.033 | 7 |
| WMT | 105.14 | 107.22 | 0.94 | 7 |
| ZS | 203.44 | 212.4 | 0.932 | 7 |
| BNR.DE | 60.28 | 61.4 | 0.884 | 5 |
| TJX | 134.67 | 137.04 | 0.784 | 7 |
| QIA.DE | 39.765 | 40.6 | 0.723 | 5 |
| EXC | 41.21 | 41.69 | 0.716 | 4 |
| MCK | 907.07 | 922.18 | 0.658 | 7 |
| ORCL | 140.88 | 144.77 | 0.64 | 7 |
| PANW | 409.5 | 419.95 | 0.623 | 7 |
| ANET | 212.0 | 215.36 | 0.535 | 6 |
| MRVL | 280.0 | 287.19 | 0.531 | 7 |
| GLW | 165.14 | 168.99 | 0.497 | 7 |
| EQIX | 1036.52 | 1047.3101 | 0.44 | 7 |
| SBUX | 95.29 | 96.11 | 0.438 | 6 |
| BAS.DE | 50.93 | 51.38 | 0.414 | 5 |
| DUK | 115.17 | 115.67 | 0.346 | 1 |
| COST | 931.09 | 935.75 | 0.307 | 4 |
| EMR | 160.29 | 161.38 | 0.289 | 7 |
| CON.DE | 70.64 | 71.14 | 0.28 | 5 |
| BP | 5.64 | 5.674 | 0.236 | 4 |
| DELL | 568.0 | 573.83 | 0.225 | 7 |
| CAT | 858.87 | 863.4 | 0.2 | 7 |
| SHL.DE | 38.13 | 38.27 | 0.166 | 4 |
| AMD | 645.46 | 649.55 | 0.162 | 7 |
| NEE | 77.7 | 77.88 | 0.137 | 1 |
| MAR | 360.6 | 361.32 | 0.106 | 5 |
| HONA | 156.92 | 157.44 | 0.105 | 6 |
| WDAY | 185.82 | 186.46 | 0.088 | 7 |
| GOOGL | 347.03 | 347.7 | 0.076 | 5 |
| PH | 983.96 | 984.95 | 0.052 | 6 |
| CVX | 207.41 | 207.6 | 0.049 | 5 |
| XOM | 164.37 | 164.46 | 0.028 | 7 |
| CL | 87.22 | 87.25 | 0.022 | 4 |
| SHEL | 36.815 | 36.82 | 0.008 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.