# Stundenwache

Stand: 2026-11-17 · 272 Werte mit Stundendaten · erstellt 2026-11-18 14:09 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (6)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| NKE | 37.62 | 35.86 | -1.106 | 5 |
| GS | 892.1 | 877.42 | -0.481 | 7 |
| C | 121.43 | 119.95 | -0.4 | 7 |
| MS | 183.91 | 183.55 | -0.062 | 6 |
| SAP.DE | 197.4 | 197.24 | -0.028 | 1 |
| BMW.DE | 54.94 | 54.9 | -0.024 | 1 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| LULU | 104.03 | 104.14 | 0.025 | 1 |

## Tief angetestet (28)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MSTR | 96.35 | 96.52 | 0.019 | 0 |
| SHW | 343.34 | 343.6 | 0.022 | 0 |
| ING | 28.895 | 28.93 | 0.051 | 0 |
| ABT | 104.59 | 104.77 | 0.057 | 0 |
| IDXX | 687.72 | 689.93 | 0.067 | 0 |
| FANG | 176.43 | 177.01 | 0.085 | 0 |
| PGR | 234.2 | 234.7 | 0.099 | 0 |
| KDP | 34.62 | 34.785 | 0.111 | 0 |
| MNST | 44.26 | 44.435 | 0.125 | 0 |
| AZN | 136.7 | 137.12 | 0.127 | 0 |
| AEP | 125.58 | 125.97 | 0.134 | 0 |
| WFC | 82.42 | 82.71 | 0.137 | 0 |
| NFLX | 59.41 | 59.68 | 0.145 | 0 |
| NEE | 84.21 | 84.495 | 0.154 | 0 |
| DBK.DE | 30.23 | 30.4 | 0.154 | 0 |
| PEP | 141.46 | 142.04 | 0.158 | 0 |
| MPC | 391.37 | 395.71 | 0.214 | 0 |
| SCCO | 153.02 | 155.41 | 0.281 | 0 |
| AXON | 291.11 | 298.32 | 0.288 | 0 |
| BAC | 49.08 | 49.45 | 0.294 | 0 |
| PSX | 253.74 | 256.94 | 0.306 | 0 |
| RY | 195.32 | 196.52 | 0.321 | 0 |
| CSCO | 93.66 | 95.111 | 0.345 | 0 |
| APH | 74.63 | 76.38 | 0.371 | 0 |
| QCOM | 162.46 | 166.705 | 0.393 | 0 |
| ON | 66.12 | 67.97 | 0.395 | 0 |
| MCD | 271.64 | 275.82 | 0.554 | 0 |
| WELL | 241.52 | 245.82 | 0.847 | 0 |

## Swing-Hoch ueberwunden (12)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.2 | 14.456 | 6 |
| IBN | 1404.9 | 1601.3 | 5.721 | 7 |
| TM | 3115.0 | 3385.0 | 2.211 | 7 |
| CHTR | 127.16 | 138.51 | 1.511 | 7 |
| COST | 1081.55 | 1110.3 | 1.336 | 7 |
| SONY | 4068.0 | 4253.0 | 1.217 | 7 |
| PG | 169.79 | 171.78 | 0.575 | 7 |
| VRSK | 201.65 | 205.4 | 0.476 | 7 |
| VNA.DE | 16.99 | 17.115 | 0.281 | 6 |
| T | 22.21 | 22.315 | 0.214 | 7 |
| SRT3.DE | 296.4 | 297.0 | 0.077 | 5 |
| CMCSA | 25.3 | 25.33 | 0.039 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.