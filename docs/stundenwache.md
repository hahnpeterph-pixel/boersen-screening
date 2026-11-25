# Stundenwache

Stand: 2026-11-25 · 272 Werte mit Stundendaten · erstellt 2026-11-25 15:26 UTC

> **Sitzung noch nicht abgeschlossen.** 206 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 3, 5, 6, 7, 8). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (7)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BMO | 157.0 | 156.865 | -0.037 | 1 |
| CM | 103.385 | 103.32 | -0.027 | 1 |
| CBK.DE | 34.19 | 34.16 | -0.027 | 1 |
| STX | 438.75 | 437.59 | -0.024 | 1 |
| SNDK | 68.6 | 68.32 | -0.023 | 1 |
| BNS | 83.085 | 83.055 | -0.016 | 1 |
| AMAT | 293.58 | 293.255 | -0.011 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| WDC | 250.72 | 250.855 | 0.005 | 0 |
| NET | 267.0386 | 267.28 | 0.01 | 0 |
| BLK | 1107.46 | 1108.215 | 0.023 | 0 |
| ANET | 154.61 | 155.14 | 0.036 | 0 |
| SCCO | 130.305 | 130.77 | 0.056 | 0 |
| DDOG | 152.13 | 152.805 | 0.063 | 0 |
| MS | 162.61 | 163.19 | 0.096 | 0 |
| JPM | 309.538 | 310.55 | 0.133 | 0 |
| BNY | 142.27 | 142.78 | 0.147 | 0 |
| SPCX | 113.97 | 115.72 | 0.197 | 0 |
| CAT | 512.6 | 518.2942 | 0.199 | 0 |
| PSX | 230.9 | 232.61 | 0.201 | 0 |
| PH | 865.93 | 874.05 | 0.268 | 0 |
| MDT | 94.14 | 95.19 | 0.402 | 0 |
| NOW | 86.86 | 89.0351 | 0.483 | 0 |

## Swing-Hoch ueberwunden (39)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.11 | 14.284 | 8 |
| SNY | 89.0 | 98.54 | 3.693 | 8 |
| SONY | 4068.0 | 4532.0 | 2.815 | 7 |
| TM | 3115.0 | 3421.0 | 2.384 | 7 |
| PDD | 79.88 | 85.14 | 1.735 | 1 |
| TJX | 138.17 | 144.76 | 1.53 | 1 |
| UL | 49.355 | 50.62 | 1.303 | 8 |
| VNA.DE | 16.99 | 17.5 | 1.269 | 8 |
| GILD | 171.7 | 176.99 | 1.215 | 1 |
| HDB | 821.0 | 846.2 | 1.112 | 7 |
| CSGP | 31.64 | 32.89 | 0.995 | 1 |
| DTE.DE | 26.51 | 26.96 | 0.871 | 8 |
| T | 22.75 | 23.1499 | 0.855 | 1 |
| VRTX | 542.76 | 554.44 | 0.761 | 1 |
| ADP | 308.66 | 312.52 | 0.618 | 1 |
| ORLY | 93.93 | 95.115 | 0.615 | 1 |
| HD | 349.73 | 355.015 | 0.589 | 1 |
| MCD | 278.29 | 281.585 | 0.532 | 1 |
| PG | 171.61 | 173.25 | 0.531 | 1 |
| DUK | 131.27 | 132.375 | 0.508 | 1 |
| VZ | 47.11 | 47.59 | 0.507 | 1 |
| WMT | 130.52 | 131.82 | 0.466 | 1 |
| JNJ | 272.5 | 275.425 | 0.451 | 1 |
| TRV | 402.12 | 405.76 | 0.436 | 1 |
| KHC | 25.835 | 26.135 | 0.418 | 1 |
| SO | 94.49 | 95.205 | 0.415 | 1 |
| PAYX | 115.3 | 116.38 | 0.378 | 1 |
| EXC | 46.44 | 46.705 | 0.357 | 1 |
| PEP | 143.28 | 144.44 | 0.342 | 1 |
| DIS | 120.44 | 121.48 | 0.328 | 1 |
| LOW | 228.7 | 230.92 | 0.327 | 1 |
| SYK | 321.83 | 324.91 | 0.327 | 1 |
| CB | 379.21 | 381.305 | 0.316 | 1 |
| PGR | 237.07 | 238.21 | 0.222 | 1 |
| CVX | 210.13 | 210.79 | 0.148 | 1 |
| MDLZ | 67.39 | 67.555 | 0.125 | 1 |
| HEI.DE | 179.45 | 179.95 | 0.109 | 8 |
| MO | 76.23 | 76.33 | 0.062 | 1 |
| CMCSA | 25.49 | 25.5041 | 0.022 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.