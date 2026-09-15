# Stundenwache

Stand: 2026-09-14 · 158 Werte mit Stundendaten · erstellt 2026-09-15 09:54 UTC

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

## Tief angetestet (6)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKR | 56.25 | 56.78 | 0.264 | 0 |
| MRVL | 213.63 | 219.09 | 0.4 | 0 |
| SBUX | 98.2 | 99.08 | 0.401 | 0 |
| JPM | 347.55 | 350.13 | 0.449 | 0 |
| MU | 902.6 | 924.29 | 0.497 | 0 |
| FAST | 48.63 | 49.46 | 0.784 | 0 |

## Swing-Hoch ueberwunden (16)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 146.77 | 7.073 | 7 |
| META | 593.34 | 665.71 | 3.333 | 7 |
| ZS | 169.1 | 191.6 | 2.056 | 7 |
| IBM | 238.29 | 249.09 | 1.648 | 7 |
| ADP | 268.73 | 276.64 | 1.503 | 7 |
| CRWD | 218.31 | 235.44 | 1.127 | 7 |
| WDAY | 185.82 | 194.14 | 0.949 | 7 |
| GOOGL | 344.68 | 349.485 | 0.642 | 6 |
| VZ | 50.93 | 51.295 | 0.433 | 7 |
| AAPL | 330.81 | 333.05 | 0.285 | 7 |
| TTWO | 220.71 | 222.94 | 0.275 | 3 |
| TRV | 376.57 | 378.15 | 0.253 | 5 |
| DDOG | 227.58 | 230.04 | 0.205 | 6 |
| FRE.DE | 45.2 | 45.4 | 0.204 | 2 |
| MAR | 339.3 | 340.54 | 0.171 | 1 |
| KO | 89.23 | 89.365 | 0.105 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.