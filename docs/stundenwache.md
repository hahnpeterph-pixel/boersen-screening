# Stundenwache

Stand: 2026-11-12 · 272 Werte mit Stundendaten · erstellt 2026-11-13 12:58 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (7)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| NEE | 85.18 | 85.315 | 0.076 | 0 |
| KDP | 35.31 | 35.415 | 0.08 | 0 |
| NKE | 37.62 | 37.7627 | 0.111 | 0 |
| TMO | 696.01 | 699.67 | 0.17 | 0 |
| LRCX | 227.64 | 233.79 | 0.367 | 0 |
| STX | 516.78 | 545.42 | 0.523 | 0 |
| GEV | 783.624 | 818.44 | 0.558 | 0 |

## Swing-Hoch ueberwunden (35)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.265 | 15.141 | 5 |
| IBN | 1404.9 | 1583.6 | 5.181 | 7 |
| TM | 3115.0 | 3429.0 | 2.582 | 7 |
| TTD | 13.68 | 15.46 | 2.072 | 7 |
| SONY | 4068.0 | 4355.0 | 1.921 | 7 |
| AMD | 514.61 | 585.5801 | 1.591 | 7 |
| AVGO | 335.74 | 364.38 | 1.5 | 7 |
| ANET | 188.53 | 206.76 | 1.457 | 7 |
| SNY | 85.37 | 87.82 | 1.336 | 5 |
| TMUS | 163.35 | 171.06 | 1.295 | 7 |
| CEG | 268.64 | 282.33 | 1.023 | 7 |
| MUV2.DE | 579.8 | 590.8 | 0.897 | 5 |
| SCHW | 89.96 | 91.72 | 0.89 | 7 |
| ALV.DE | 466.4 | 474.2 | 0.876 | 5 |
| BNY | 150.28 | 152.79 | 0.79 | 7 |
| CHTR | 127.16 | 132.67 | 0.762 | 7 |
| WDAY | 185.82 | 190.57 | 0.637 | 7 |
| VRSK | 201.65 | 206.32 | 0.594 | 7 |
| RWE.DE | 58.92 | 59.66 | 0.555 | 5 |
| XEL | 80.67 | 81.505 | 0.534 | 7 |
| HONA | 161.7 | 166.17 | 0.511 | 7 |
| COST | 1081.55 | 1092.3199 | 0.501 | 7 |
| FAST | 54.96 | 55.55 | 0.459 | 7 |
| SPG | 231.66 | 233.63 | 0.45 | 7 |
| ING | 29.68 | 29.955 | 0.378 | 5 |
| BRK-B | 586.3 | 589.92 | 0.316 | 7 |
| QCOM | 174.0 | 177.16 | 0.311 | 7 |
| GOOGL | 296.33 | 298.75 | 0.212 | 6 |
| CAT | 599.78 | 605.4 | 0.179 | 6 |
| MS | 188.3 | 189.19 | 0.152 | 7 |
| UL | 49.355 | 49.5 | 0.125 | 5 |
| AEP | 128.72 | 128.9 | 0.063 | 7 |
| JNJ | 283.25 | 283.57 | 0.044 | 6 |
| ENR.DE | 131.78 | 132.0 | 0.028 | 5 |
| KO | 97.39 | 97.42 | 0.016 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.