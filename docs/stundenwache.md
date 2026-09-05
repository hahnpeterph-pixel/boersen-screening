# Stundenwache

Stand: 2026-09-04 · 158 Werte mit Stundendaten · erstellt 2026-09-05 00:05 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (31)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ADSK | 235.88 | 217.95 | -1.742 | 7 |
| ADBE | 279.43 | 266.5 | -1.314 | 7 |
| DASH | 221.61 | 211.75 | -1.285 | 7 |
| SNPS | 410.52 | 393.78 | -1.065 | 7 |
| CDNS | 302.36 | 292.74 | -0.87 | 7 |
| ROP | 415.01 | 407.22 | -0.807 | 7 |
| KHC | 25.3 | 24.85 | -0.683 | 7 |
| RHM.DE | 1055.4 | 1033.0 | -0.628 | 8 |
| NFLX | 79.6 | 78.24 | -0.61 | 6 |
| LIN | 482.16 | 477.49 | -0.597 | 7 |
| DXCM | 89.05 | 87.895 | -0.498 | 7 |
| INTU | 339.32 | 332.68 | -0.424 | 7 |
| PEP | 138.58 | 137.63 | -0.412 | 5 |
| PAYX | 122.8 | 121.7 | -0.397 | 4 |
| SRT3.DE | 241.4 | 238.4 | -0.387 | 5 |
| FRE.DE | 44.0 | 43.685 | -0.376 | 9 |
| DIS | 106.14 | 105.29 | -0.358 | 7 |
| MRK.DE | 136.9 | 136.1 | -0.327 | 9 |
| SBUX | 105.22 | 104.45 | -0.31 | 3 |
| VRSK | 187.44 | 185.9 | -0.267 | 7 |
| BKNG | 194.68 | 193.29 | -0.213 | 7 |
| ZS | 171.32 | 169.46 | -0.205 | 6 |
| CTSH | 62.71 | 62.315 | -0.192 | 3 |
| MNST | 43.97 | 43.81 | -0.141 | 7 |
| WBD | 28.3 | 28.26 | -0.12 | 7 |
| MDB | 371.0 | 368.74 | -0.093 | 1 |
| MCD | 256.12 | 255.7 | -0.092 | 1 |
| SY1.DE | 90.56 | 90.42 | -0.08 | 3 |
| CSGP | 30.99 | 30.91 | -0.061 | 6 |
| ADP | 278.08 | 277.95 | -0.024 | 1 |
| VZ | 50.15 | 50.135 | -0.02 | 1 |

## Tief zurueckerobert (5)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BEI.DE | 76.38 | 76.4 | 0.013 | 8 |
| ISRG | 365.42 | 366.67 | 0.108 | 2 |
| QIA.DE | 37.18 | 37.38 | 0.157 | 1 |
| AZN | 161.18 | 162.67 | 0.437 | 1 |
| BNR.DE | 60.66 | 61.3 | 0.454 | 1 |

## Tief angetestet (5)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| COST | 915.31 | 915.54 | 0.013 | 0 |
| TTWO | 213.6 | 214.76 | 0.134 | 0 |
| GEHC | 68.5 | 68.85 | 0.221 | 0 |
| MDLZ | 60.98 | 61.275 | 0.236 | 0 |
| IDXX | 527.74 | 535.205 | 0.49 | 0 |

## Swing-Hoch ueberwunden (29)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 259.3 | 4.032 | 7 |
| MRNA | 65.525 | 145.54 | 3.63 | 7 |
| HNR1.DE | 252.4 | 260.8 | 2.661 | 9 |
| VOW3.DE | 78.36 | 81.42 | 1.482 | 9 |
| CEG | 285.26 | 298.95 | 1.457 | 7 |
| CDW | 142.97 | 152.42 | 1.406 | 7 |
| CBK.DE | 41.05 | 42.05 | 1.273 | 9 |
| META | 593.34 | 616.75 | 1.191 | 7 |
| MUV2.DE | 520.4 | 528.6 | 1.16 | 9 |
| WDAY | 185.82 | 195.65 | 1.146 | 7 |
| MU | 969.44 | 1014.95 | 0.968 | 7 |
| AMD | 462.21 | 477.45 | 0.857 | 7 |
| DBK.DE | 35.03 | 35.62 | 0.8 | 9 |
| BAS.DE | 52.76 | 53.5 | 0.795 | 9 |
| ORCL | 153.99 | 158.765 | 0.774 | 7 |
| PAH3.DE | 28.76 | 29.12 | 0.559 | 9 |
| INTC | 93.7 | 95.81 | 0.497 | 7 |
| TTD | 14.17 | 14.44 | 0.484 | 7 |
| SPGI | 439.02 | 443.465 | 0.381 | 7 |
| AEP | 123.85 | 124.495 | 0.305 | 7 |
| BKR | 63.02 | 63.49 | 0.304 | 3 |
| WMT | 106.6 | 107.14 | 0.196 | 7 |
| ADI | 360.77 | 362.33 | 0.143 | 6 |
| NXPI | 227.24 | 227.85 | 0.106 | 6 |
| BMW.DE | 62.72 | 62.84 | 0.082 | 7 |
| MELI | 1972.59 | 1977.765 | 0.076 | 7 |
| TXN | 258.04 | 258.45 | 0.052 | 5 |
| JPM | 358.35 | 358.61 | 0.047 | 2 |
| KDP | 32.55 | 32.58 | 0.039 | 7 |

## Reihen unstimmig - kein Urteil (1)

Stundenkurs und Tagesreihe stehen auf verschiedenen Skalen - typisch rund um Splits, wenn die beiden Yahoo-Endpunkte die Historie unterschiedlich zurueckrechnen. Die Marken aus der Tagesreihe sind hier nicht mit dem laufenden Kurs vergleichbar, deshalb steht kein Urteil. Von Hand im Chart nachsehen.

| Wert | Tief-Marke | Hoch-Marke | Stundenkurs | Abweichung |
|---|---|---|---|---|
| LULU | 117.25 | 124.47 | 100.61 | 17% |

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.