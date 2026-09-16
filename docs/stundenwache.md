# Stundenwache

Stand: 2026-09-15 · 158 Werte mit Stundendaten · erstellt 2026-09-16 09:48 UTC

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

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TTWO | 211.54 | 211.9 | 0.042 | 0 |
| EXC | 42.14 | 42.195 | 0.071 | 0 |
| XEL | 72.29 | 72.485 | 0.147 | 0 |
| ROP | 382.18 | 383.93 | 0.172 | 0 |
| DIS | 105.92 | 106.39 | 0.213 | 0 |
| SNPS | 362.55 | 367.72 | 0.274 | 0 |
| BKR | 56.03 | 56.72 | 0.342 | 0 |
| KDP | 31.1 | 31.51 | 0.652 | 0 |

## Swing-Hoch ueberwunden (16)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 143.77 | 7.509 | 7 |
| META | 593.34 | 670.49 | 3.43 | 7 |
| ZS | 169.1 | 193.96 | 2.297 | 7 |
| CRWD | 218.31 | 242.52 | 1.595 | 7 |
| IBM | 238.29 | 248.4 | 1.531 | 7 |
| ADP | 268.73 | 276.53 | 1.464 | 7 |
| FANG | 207.57 | 211.47 | 0.709 | 7 |
| FRE.DE | 45.2 | 45.84 | 0.652 | 2 |
| VZ | 50.93 | 51.45 | 0.615 | 7 |
| WDAY | 185.82 | 190.68 | 0.559 | 7 |
| QCOM | 185.46 | 187.87 | 0.315 | 7 |
| TRV | 376.57 | 377.97 | 0.227 | 7 |
| DDOG | 227.58 | 230.12 | 0.21 | 6 |
| AAPL | 330.81 | 331.335 | 0.067 | 1 |
| ILMN | 221.76 | 222.31 | 0.062 | 5 |
| GOOGL | 344.68 | 345.03 | 0.046 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.