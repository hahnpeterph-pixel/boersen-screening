# Stundenwache

Stand: 2026-10-05 · 273 Werte mit Stundendaten · erstellt 2026-10-06 00:47 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (5)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BAYN.DE | 44.55 | 43.89 | -0.467 | 3 |
| WELL | 225.36 | 224.24 | -0.241 | 4 |
| GE | 308.19 | 306.27 | -0.226 | 6 |
| PFE | 27.44 | 27.41 | -0.064 | 5 |
| PAH3.DE | 24.5 | 24.48 | -0.022 | 4 |

## Tief zurueckerobert (3)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| T | 24.21 | 24.24 | 0.055 | 5 |
| SHL.DE | 37.28 | 37.4 | 0.151 | 1 |
| VOW3.DE | 67.38 | 68.48 | 0.44 | 1 |

## Tief angetestet (25)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| LOW | 179.21 | 179.465 | 0.058 | 0 |
| JNJ | 252.51 | 252.9 | 0.083 | 0 |
| INTC | 115.31 | 116.28 | 0.147 | 0 |
| RTX | 183.83 | 184.37 | 0.152 | 0 |
| AXON | 408.24 | 411.83 | 0.171 | 0 |
| MBG.DE | 39.725 | 40.17 | 0.392 | 0 |
| ADBE | 235.525 | 238.81 | 0.415 | 0 |
| CMCSA | 21.3112 | 21.57 | 0.416 | 0 |
| SRT3.DE | 247.0 | 251.1 | 0.469 | 0 |
| NVO | 243.15 | 246.8 | 0.503 | 0 |
| DTG.DE | 40.41 | 40.9 | 0.522 | 0 |
| ENB | 45.7 | 46.045 | 0.528 | 0 |
| NEM | 113.86 | 115.835 | 0.534 | 0 |
| CCEP | 100.3 | 101.47 | 0.578 | 0 |
| GD | 328.0 | 331.8 | 0.609 | 0 |
| HONA | 152.26 | 155.71 | 0.648 | 0 |
| UPS | 91.63 | 93.13 | 0.697 | 0 |
| SPOT | 470.51 | 483.01 | 0.749 | 0 |
| MCD | 229.61 | 233.08 | 0.75 | 0 |
| PM | 185.88 | 189.58 | 0.883 | 0 |
| CVX | 202.7 | 206.52 | 0.916 | 0 |
| MDLZ | 57.35 | 58.485 | 1.008 | 0 |
| KLAC | 199.6057 | 206.85 | 1.049 | 0 |
| MO | 66.43 | 67.88 | 1.167 | 0 |
| TMO | 648.29 | 673.57 | 1.561 | 0 |

## Swing-Hoch ueberwunden (38)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.97 | 6.918 | 7 |
| TSM | 2405.0 | 2570.0 | 4.4 | 5 |
| SHOP | 134.74 | 160.1 | 3.895 | 7 |
| PBR | 54.61 | 60.52 | 3.405 | 7 |
| ON | 74.48 | 85.96 | 3.154 | 7 |
| SNPS | 445.92 | 488.57 | 2.202 | 7 |
| SPCX | 158.13 | 171.1 | 2.092 | 7 |
| MELI | 1739.88 | 1861.5 | 2.048 | 7 |
| MPC | 398.33 | 433.43 | 2.027 | 7 |
| CDNS | 330.81 | 353.62 | 1.902 | 7 |
| TXN | 284.39 | 295.07 | 1.379 | 7 |
| MSFT | 509.44 | 525.49 | 1.319 | 7 |
| VLO | 395.85 | 419.51 | 1.312 | 7 |
| IFX.DE | 60.48 | 63.57 | 1.247 | 9 |
| NVDA | 233.21 | 239.11 | 1.097 | 7 |
| PSX | 259.11 | 269.74 | 1.094 | 7 |
| APH | 84.48 | 87.29 | 1.073 | 7 |
| ILMN | 280.17 | 293.94 | 1.002 | 6 |
| CRWD | 263.87 | 272.76 | 0.83 | 7 |
| SYK | 280.17 | 285.34 | 0.823 | 7 |
| ASML | 1630.2 | 1657.6 | 0.619 | 9 |
| EMR | 160.29 | 162.37 | 0.547 | 7 |
| GEV | 973.41 | 990.42 | 0.525 | 7 |
| CSCO | 111.5 | 112.82 | 0.505 | 7 |
| FTNT | 181.37 | 184.2 | 0.473 | 7 |
| WDAY | 185.82 | 188.99 | 0.441 | 7 |
| MCK | 907.07 | 916.21 | 0.393 | 6 |
| LIN | 480.56 | 482.97 | 0.293 | 7 |
| ORCL | 140.88 | 142.54 | 0.263 | 7 |
| QIA.DE | 39.765 | 40.025 | 0.224 | 9 |
| RHM.DE | 974.8 | 981.2 | 0.221 | 2 |
| SONY | 3745.0 | 3762.0 | 0.206 | 1 |
| MRNA | 201.0 | 203.21 | 0.151 | 4 |
| NET | 357.64 | 359.63 | 0.123 | 7 |
| AMZN | 250.88 | 251.51 | 0.12 | 7 |
| XEL | 71.37 | 71.51 | 0.114 | 7 |
| AVGO | 361.86 | 362.875 | 0.102 | 5 |
| CNQ | 48.28 | 48.32 | 0.033 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.