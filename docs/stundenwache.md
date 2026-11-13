# Stundenwache

Stand: 2026-11-12 · 272 Werte mit Stundendaten · erstellt 2026-11-13 00:02 UTC

> **Sitzung noch nicht abgeschlossen.** 6 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| PFE | 28.95 | 28.83 | -0.147 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ACN | 249.85 | 250.05 | 0.019 | 0 |
| DHR | 231.84 | 232.17 | 0.051 | 0 |
| BNS | 92.43 | 92.685 | 0.145 | 0 |
| AMAT | 376.25 | 381.28 | 0.191 | 0 |
| RY | 201.98 | 202.74 | 0.214 | 0 |
| SNOW | 288.82 | 298.75 | 0.618 | 0 |
| MRK.DE | 145.5 | 148.25 | 0.794 | 0 |
| DELL | 336.085 | 371.35 | 0.972 | 0 |

## Swing-Hoch ueberwunden (42)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.295 | 14.542 | 9 |
| IBN | 1404.9 | 1590.0 | 5.343 | 7 |
| FRE.DE | 47.295 | 53.55 | 5.05 | 9 |
| TM | 3115.0 | 3415.0 | 2.513 | 7 |
| TTD | 13.68 | 15.46 | 2.073 | 7 |
| HEN3.DE | 84.46 | 87.38 | 1.702 | 9 |
| SNY | 85.37 | 88.36 | 1.593 | 9 |
| AMD | 514.61 | 585.5801 | 1.591 | 7 |
| AVGO | 335.74 | 364.38 | 1.5 | 7 |
| ANET | 188.53 | 206.76 | 1.457 | 7 |
| SONY | 4068.0 | 4275.0 | 1.376 | 7 |
| TMUS | 163.35 | 171.06 | 1.296 | 7 |
| CON.DE | 72.02 | 74.5 | 1.257 | 9 |
| CEG | 268.64 | 282.33 | 1.023 | 7 |
| MFG | 7824.0 | 8160.0 | 0.984 | 7 |
| SCHW | 89.96 | 91.72 | 0.89 | 7 |
| BNY | 150.28 | 152.79 | 0.79 | 7 |
| CHTR | 127.16 | 132.67 | 0.762 | 7 |
| ALV.DE | 466.4 | 472.8 | 0.723 | 9 |
| AIR.DE | 204.5 | 208.3 | 0.677 | 9 |
| WDAY | 185.82 | 190.57 | 0.637 | 7 |
| MUV2.DE | 579.8 | 587.6 | 0.637 | 9 |
| VRSK | 201.65 | 206.32 | 0.594 | 7 |
| XEL | 80.67 | 81.505 | 0.534 | 7 |
| SMFG | 3237.0 | 3298.0 | 0.512 | 7 |
| HONA | 161.7 | 166.17 | 0.511 | 7 |
| ING | 29.68 | 30.065 | 0.508 | 9 |
| COST | 1081.55 | 1092.37 | 0.504 | 7 |
| FAST | 54.96 | 55.55 | 0.459 | 7 |
| SPG | 231.66 | 233.63 | 0.45 | 7 |
| BRK-B | 586.3 | 589.92 | 0.316 | 7 |
| QCOM | 174.0 | 177.16 | 0.311 | 7 |
| RWE.DE | 58.92 | 59.32 | 0.293 | 7 |
| SIE.DE | 280.4 | 282.5 | 0.244 | 9 |
| GOOGL | 296.33 | 298.75 | 0.212 | 6 |
| CAT | 599.78 | 605.4 | 0.179 | 6 |
| ENR.DE | 131.78 | 133.2 | 0.179 | 8 |
| BHP | 59.0 | 59.25 | 0.159 | 1 |
| MS | 188.3 | 189.19 | 0.152 | 7 |
| AEP | 128.72 | 128.9 | 0.063 | 7 |
| JNJ | 283.25 | 283.57 | 0.044 | 6 |
| KO | 97.39 | 97.42 | 0.016 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.