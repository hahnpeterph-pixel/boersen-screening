# Stundenwache

Stand: 2026-09-18 · 158 Werte mit Stundendaten · erstellt 2026-09-18 21:35 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (14)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DIS | 102.37 | 102.645 | 0.12 | 0 |
| MCD | 247.65 | 248.37 | 0.194 | 0 |
| HD | 298.3 | 299.95 | 0.275 | 0 |
| TRV | 372.835 | 374.64 | 0.276 | 0 |
| HNR1.DE | 251.4 | 252.8 | 0.349 | 0 |
| PG | 145.51 | 146.33 | 0.351 | 0 |
| MUV2.DE | 502.8 | 506.3 | 0.387 | 0 |
| ROP | 368.69 | 372.66 | 0.403 | 0 |
| KHC | 24.15 | 24.4377 | 0.437 | 0 |
| ADP | 268.99 | 271.47 | 0.474 | 0 |
| HON | 204.26 | 206.39 | 0.476 | 0 |
| BA | 195.47 | 198.21 | 0.512 | 0 |
| VOW3.DE | 74.96 | 76.52 | 0.519 | 0 |
| LIN | 454.19 | 460.12 | 0.827 | 0 |

## Swing-Hoch ueberwunden (20)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 154.01 | 8.598 | 7 |
| ILMN | 221.76 | 239.56 | 1.769 | 7 |
| MU | 944.94 | 1015.375 | 1.639 | 7 |
| ARM | 253.155 | 275.75 | 1.549 | 7 |
| AMD | 526.79 | 559.8 | 1.478 | 7 |
| CRWD | 218.31 | 237.62 | 1.472 | 7 |
| QIA.DE | 37.24 | 38.52 | 1.275 | 9 |
| GILD | 146.75 | 150.04 | 0.982 | 7 |
| WDAY | 185.82 | 193.86 | 0.982 | 7 |
| SRT3.DE | 240.2 | 247.3 | 0.936 | 9 |
| ISRG | 382.41 | 393.21 | 0.888 | 7 |
| FRE.DE | 45.2 | 45.985 | 0.745 | 9 |
| INTC | 104.9 | 108.62 | 0.665 | 7 |
| AAPL | 330.81 | 335.59 | 0.621 | 7 |
| AZN | 164.55 | 166.29 | 0.511 | 7 |
| DDOG | 227.58 | 229.85 | 0.214 | 7 |
| MMM | 165.37 | 165.91 | 0.158 | 3 |
| DHL.DE | 55.7 | 55.78 | 0.087 | 7 |
| ZS | 196.575 | 197.29 | 0.071 | 6 |
| NVDA | 222.0 | 222.09 | 0.015 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.