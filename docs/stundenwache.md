# Stundenwache

Stand: 2026-11-19 · 272 Werte mit Stundendaten · erstellt 2026-11-20 13:57 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| GOOGL | 278.46 | 272.5 | -0.559 | 2 |
| MRVL | 140.9 | 138.36 | -0.162 | 2 |
| TXN | 287.86 | 285.75 | -0.135 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (30)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DB1.DE | 314.6 | 314.6 | 0.0 | 0 |
| TSLA | 374.13 | 374.43 | 0.016 | 0 |
| NEM | 99.87 | 99.98 | 0.021 | 0 |
| SCCO | 141.29 | 141.49 | 0.024 | 0 |
| AMAT | 338.0 | 338.78 | 0.029 | 0 |
| PSX | 242.26 | 242.68 | 0.04 | 0 |
| COF | 181.42 | 181.71 | 0.042 | 0 |
| CTSH | 56.2 | 56.31 | 0.048 | 0 |
| APP | 377.332 | 379.1 | 0.062 | 0 |
| RHM.DE | 698.6 | 703.0 | 0.09 | 0 |
| PH | 902.23 | 906.03 | 0.114 | 0 |
| GS | 843.89 | 847.52 | 0.12 | 0 |
| UNP | 289.67 | 290.57 | 0.126 | 0 |
| BKR | 46.38 | 46.68 | 0.143 | 0 |
| SHW | 338.0 | 339.8 | 0.148 | 0 |
| V | 400.74 | 402.42 | 0.161 | 0 |
| VRTX | 517.82 | 520.51 | 0.165 | 0 |
| AMD | 480.5 | 489.165 | 0.17 | 0 |
| DE | 621.13 | 624.95 | 0.191 | 0 |
| KDP | 34.09 | 34.4 | 0.208 | 0 |
| AXP | 309.41 | 311.15 | 0.227 | 0 |
| BMY | 57.88 | 58.335 | 0.246 | 0 |
| SPGI | 439.35 | 442.67 | 0.302 | 0 |
| PG | 166.89 | 167.92 | 0.309 | 0 |
| GILD | 164.8 | 166.53 | 0.358 | 0 |
| EXC | 45.09 | 45.42 | 0.385 | 0 |
| BAC | 48.05 | 48.56 | 0.422 | 0 |
| SO | 92.43 | 93.3 | 0.433 | 0 |
| TRV | 385.68 | 390.81 | 0.564 | 0 |
| PGR | 224.17 | 229.99 | 1.071 | 0 |

## Swing-Hoch ueberwunden (10)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.145 | 15.283 | 6 |
| IBN | 1404.9 | 1640.0 | 6.52 | 7 |
| PDD | 79.88 | 86.0 | 1.973 | 7 |
| SONY | 4068.0 | 4317.0 | 1.651 | 7 |
| TM | 3115.0 | 3307.0 | 1.531 | 7 |
| PANW | 332.0 | 361.73 | 1.473 | 7 |
| HDB | 821.0 | 846.0 | 1.264 | 7 |
| ZS | 197.43 | 205.46 | 0.637 | 7 |
| CRWD | 236.17 | 243.38 | 0.476 | 7 |
| TJX | 138.17 | 139.46 | 0.262 | 7 |

## Reihen unstimmig - kein Urteil (1)

Stundenkurs und Tagesreihe stehen auf verschiedenen Skalen - typisch rund um Splits, wenn die beiden Yahoo-Endpunkte die Historie unterschiedlich zurueckrechnen. Die Marken aus der Tagesreihe sind hier nicht mit dem laufenden Kurs vergleichbar, deshalb steht kein Urteil. Von Hand im Chart nachsehen.

| Wert | Tief-Marke | Hoch-Marke | Stundenkurs | Abweichung |
|---|---|---|---|---|
| SNDK | 93.6738 | 126.3812 | 754.99 | 700% |

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.