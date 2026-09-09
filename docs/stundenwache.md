# Stundenwache

Stand: 2026-09-09 · 158 Werte mit Stundendaten · erstellt 2026-09-09 21:36 UTC

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

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SPGI | 418.26 | 418.36 | 0.008 | 0 |
| MCD | 253.3458 | 253.53 | 0.046 | 0 |
| ROST | 224.84 | 225.3 | 0.078 | 0 |
| MBG.DE | 46.53 | 46.66 | 0.123 | 0 |
| MSFT | 489.8 | 491.77 | 0.199 | 0 |
| ORCL | 160.375 | 161.69 | 0.203 | 0 |
| TTWO | 208.5183 | 211.091 | 0.315 | 0 |
| KLAC | 180.74 | 182.92 | 0.318 | 0 |
| AMZN | 250.65 | 252.48 | 0.321 | 0 |
| AEP | 123.92 | 124.7 | 0.377 | 0 |
| XEL | 75.45 | 76.17 | 0.531 | 0 |
| MUV2.DE | 490.8 | 496.3 | 0.65 | 0 |

## Swing-Hoch ueberwunden (12)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 135.6 | 4.473 | 7 |
| AMD | 462.21 | 521.08 | 3.181 | 7 |
| META | 593.34 | 653.415 | 3.018 | 7 |
| INTC | 93.7 | 106.23 | 2.999 | 7 |
| MU | 969.44 | 1027.506 | 1.317 | 7 |
| QCOM | 170.6 | 176.42 | 0.991 | 7 |
| TXN | 258.04 | 261.6 | 0.513 | 7 |
| ADI | 360.77 | 365.16 | 0.46 | 7 |
| BKR | 63.02 | 63.64 | 0.374 | 7 |
| DDOG | 221.0 | 225.17 | 0.35 | 7 |
| IBM | 238.29 | 239.95 | 0.295 | 3 |
| WDAY | 185.82 | 186.04 | 0.026 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.