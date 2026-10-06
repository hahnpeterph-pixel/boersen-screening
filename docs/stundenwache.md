# Stundenwache

Stand: 2026-10-05 · 273 Werte mit Stundendaten · erstellt 2026-10-06 11:56 UTC

> **Sitzung noch nicht abgeschlossen.** 61 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| BP | 5.527 | 5.5262 | -0.006 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (17)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| JNJ | 252.51 | 252.9 | 0.083 | 0 |
| RY | 194.27 | 194.71 | 0.144 | 0 |
| INTC | 115.31 | 116.28 | 0.147 | 0 |
| NXPI | 239.26 | 241.97 | 0.377 | 0 |
| T | 24.01 | 24.24 | 0.441 | 0 |
| TRV | 357.61 | 360.82 | 0.5 | 0 |
| SPG | 199.74 | 201.39 | 0.612 | 0 |
| PEP | 124.22 | 125.65 | 0.633 | 0 |
| CCEP | 100.06 | 101.47 | 0.703 | 0 |
| UPS | 91.56 | 93.13 | 0.707 | 0 |
| BEI.DE | 75.16 | 76.32 | 0.719 | 0 |
| MCD | 229.61 | 233.08 | 0.75 | 0 |
| ADI | 409.65 | 419.1 | 0.859 | 0 |
| EXC | 40.24 | 40.82 | 0.896 | 0 |
| MDLZ | 57.35 | 58.485 | 1.008 | 0 |
| KLAC | 199.61 | 206.85 | 1.048 | 0 |
| PM | 184.11 | 189.58 | 1.266 | 0 |

## Swing-Hoch ueberwunden (43)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.97 | 6.918 | 7 |
| TSM | 2405.0 | 2580.0 | 4.712 | 5 |
| SHOP | 134.74 | 160.1 | 3.604 | 7 |
| PBR | 54.61 | 60.52 | 3.405 | 7 |
| ON | 74.48 | 85.96 | 3.154 | 7 |
| SNPS | 445.92 | 488.57 | 2.202 | 7 |
| MELI | 1739.88 | 1861.5 | 2.048 | 7 |
| MPC | 398.33 | 433.43 | 2.029 | 7 |
| SPCX | 158.13 | 171.1 | 1.912 | 7 |
| CDNS | 330.81 | 353.62 | 1.902 | 7 |
| QIA.DE | 39.765 | 41.875 | 1.685 | 5 |
| TXN | 284.39 | 295.07 | 1.379 | 7 |
| MSFT | 509.44 | 525.49 | 1.319 | 7 |
| VLO | 395.85 | 419.51 | 1.309 | 7 |
| APH | 84.48 | 87.29 | 1.102 | 7 |
| NVDA | 233.21 | 239.11 | 1.097 | 7 |
| PSX | 259.11 | 269.74 | 1.095 | 7 |
| ILMN | 280.17 | 293.94 | 1.002 | 6 |
| ASML | 1630.2 | 1668.8 | 0.906 | 5 |
| CRWD | 263.87 | 272.76 | 0.83 | 7 |
| SYK | 280.17 | 285.34 | 0.771 | 7 |
| MRK.DE | 139.95 | 141.75 | 0.595 | 5 |
| EMR | 160.29 | 162.37 | 0.547 | 7 |
| GEV | 973.41 | 990.42 | 0.521 | 7 |
| CSCO | 111.5 | 112.82 | 0.505 | 7 |
| FTNT | 181.37 | 184.2 | 0.473 | 7 |
| WDAY | 185.82 | 188.99 | 0.441 | 7 |
| MCK | 907.07 | 916.21 | 0.4 | 6 |
| DB1.DE | 291.3 | 292.8 | 0.344 | 5 |
| LIN | 480.56 | 482.97 | 0.293 | 7 |
| SONY | 3745.0 | 3769.0 | 0.29 | 7 |
| ORCL | 140.88 | 142.54 | 0.263 | 7 |
| BABA | 107.4 | 108.2 | 0.231 | 7 |
| BHP | 62.69 | 62.86 | 0.164 | 3 |
| MRNA | 201.0 | 203.21 | 0.151 | 4 |
| NET | 357.64 | 359.63 | 0.121 | 7 |
| AMZN | 250.88 | 251.51 | 0.12 | 7 |
| XEL | 71.37 | 71.51 | 0.114 | 7 |
| AVGO | 361.86 | 362.875 | 0.102 | 5 |
| BAS.DE | 50.93 | 51.0 | 0.066 | 1 |
| SAP.DE | 187.8 | 187.98 | 0.035 | 5 |
| CNQ | 48.28 | 48.32 | 0.034 | 5 |
| SRT3.DE | 268.7 | 269.0 | 0.033 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.