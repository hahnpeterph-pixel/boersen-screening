# Stundenwache

Stand: 2026-09-09 · 158 Werte mit Stundendaten · erstellt 2026-09-10 09:29 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (21)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PDD | 78.57 | 78.615 | 0.02 | 0 |
| MCD | 253.35 | 253.53 | 0.045 | 0 |
| VNA.DE | 18.4 | 18.42 | 0.052 | 0 |
| ROST | 224.84 | 225.3 | 0.078 | 0 |
| KDP | 31.99 | 32.08 | 0.136 | 0 |
| SHW | 319.61 | 320.71 | 0.158 | 0 |
| FAST | 48.6 | 48.79 | 0.182 | 0 |
| MSFT | 489.8 | 491.77 | 0.199 | 0 |
| CSGP | 29.33 | 29.58 | 0.205 | 0 |
| EXC | 43.48 | 43.72 | 0.301 | 0 |
| TTWO | 208.52 | 211.091 | 0.314 | 0 |
| AMZN | 250.65 | 252.48 | 0.321 | 0 |
| AEP | 123.92 | 124.7 | 0.377 | 0 |
| CON.DE | 69.24 | 69.94 | 0.405 | 0 |
| DXCM | 82.8 | 83.91 | 0.465 | 0 |
| HNR1.DE | 246.8 | 248.6 | 0.506 | 0 |
| XEL | 75.45 | 76.17 | 0.531 | 0 |
| REGN | 796.73 | 807.66 | 0.553 | 0 |
| DB1.DE | 272.1 | 275.4 | 0.643 | 0 |
| MNST | 42.19 | 42.84 | 0.653 | 0 |
| MUV2.DE | 496.8 | 503.0 | 0.765 | 0 |

## Swing-Hoch ueberwunden (15)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 135.6 | 4.473 | 7 |
| AMD | 462.21 | 521.08 | 3.181 | 7 |
| META | 593.34 | 653.415 | 3.018 | 7 |
| INTC | 93.7 | 106.23 | 2.992 | 7 |
| MU | 969.44 | 1027.506 | 1.317 | 7 |
| QCOM | 170.6 | 176.42 | 0.991 | 7 |
| TXN | 258.04 | 261.6 | 0.512 | 7 |
| ADI | 360.77 | 365.16 | 0.46 | 7 |
| BKR | 63.02 | 63.64 | 0.374 | 7 |
| DDOG | 221.0 | 225.17 | 0.35 | 7 |
| IBM | 238.29 | 239.95 | 0.295 | 3 |
| RWE.DE | 60.3 | 60.54 | 0.172 | 3 |
| DBK.DE | 35.03 | 35.12 | 0.116 | 3 |
| BMW.DE | 62.72 | 62.84 | 0.075 | 3 |
| WDAY | 185.82 | 186.04 | 0.026 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.