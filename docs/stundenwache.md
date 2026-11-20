# Stundenwache

Stand: 2026-11-19 · 272 Werte mit Stundendaten · erstellt 2026-11-20 03:12 UTC

> **Sitzung noch nicht abgeschlossen.** 10 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 3, 4, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (4)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GOOGL | 278.46 | 272.5 | -0.559 | 2 |
| MRVL | 140.9 | 138.36 | -0.162 | 2 |
| TXN | 287.86 | 285.75 | -0.135 | 2 |
| MTX.DE | 346.8 | 345.9 | -0.075 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (26)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TSLA | 374.13 | 374.43 | 0.016 | 0 |
| NEM | 99.87 | 99.98 | 0.021 | 0 |
| SCCO | 141.29 | 141.49 | 0.024 | 0 |
| AMAT | 338.0 | 338.85 | 0.032 | 0 |
| COF | 181.42 | 181.71 | 0.042 | 0 |
| CTSH | 56.2 | 56.31 | 0.048 | 0 |
| PH | 902.23 | 906.03 | 0.114 | 0 |
| GS | 843.89 | 847.52 | 0.12 | 0 |
| UNP | 289.67 | 290.59 | 0.129 | 0 |
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
| PG | 166.89 | 167.93 | 0.312 | 0 |
| GILD | 164.8 | 166.53 | 0.358 | 0 |
| EXC | 45.09 | 45.42 | 0.385 | 0 |
| BAC | 48.05 | 48.56 | 0.422 | 0 |
| SO | 92.43 | 93.3 | 0.433 | 0 |
| TRV | 385.68 | 390.81 | 0.564 | 0 |
| PGR | 224.17 | 229.99 | 1.071 | 0 |

## Swing-Hoch ueberwunden (11)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.22 | 14.907 | 9 |
| IBN | 1404.9 | 1608.9 | 5.922 | 7 |
| PDD | 79.88 | 86.0 | 1.974 | 7 |
| TM | 3115.0 | 3342.0 | 1.841 | 3 |
| SONY | 4068.0 | 4338.0 | 1.815 | 3 |
| PANW | 332.0 | 361.73 | 1.473 | 7 |
| ZS | 197.43 | 205.48 | 0.639 | 7 |
| CRWD | 236.17 | 243.38 | 0.476 | 7 |
| SRT3.DE | 296.4 | 300.0 | 0.458 | 9 |
| TJX | 138.17 | 139.46 | 0.262 | 7 |
| HDB | 821.0 | 821.8 | 0.044 | 1 |

## Reihen unstimmig - kein Urteil (1)

Stundenkurs und Tagesreihe stehen auf verschiedenen Skalen - typisch rund um Splits, wenn die beiden Yahoo-Endpunkte die Historie unterschiedlich zurueckrechnen. Die Marken aus der Tagesreihe sind hier nicht mit dem laufenden Kurs vergleichbar, deshalb steht kein Urteil. Von Hand im Chart nachsehen.

| Wert | Tief-Marke | Hoch-Marke | Stundenkurs | Abweichung |
|---|---|---|---|---|
| SNDK | 93.6738 | 126.3812 | 754.99 | 700% |

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.