# Stundenwache

Stand: 2026-09-14 · 158 Werte mit Stundendaten · erstellt 2026-09-15 05:20 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (10)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ENR.DE | 140.6 | 132.24 | -1.663 | 9 |
| ASML | 1447.4 | 1386.2 | -1.356 | 9 |
| RWE.DE | 58.88 | 57.62 | -0.909 | 9 |
| MTX.DE | 337.2 | 329.3 | -0.886 | 9 |
| DBK.DE | 34.675 | 34.115 | -0.687 | 9 |
| IFX.DE | 55.2 | 53.95 | -0.577 | 9 |
| HEI.DE | 152.5 | 149.85 | -0.527 | 9 |
| SRT3.DE | 230.3 | 227.0 | -0.507 | 2 |
| VNA.DE | 17.945 | 17.93 | -0.037 | 2 |
| MRK.DE | 130.65 | 130.6 | -0.02 | 2 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AIR.DE | 194.58 | 195.06 | 0.11 | 1 |
| CON.DE | 69.24 | 69.6 | 0.203 | 4 |

## Tief angetestet (11)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKR | 56.25 | 56.78 | 0.264 | 0 |
| P911.DE | 44.49 | 44.86 | 0.28 | 0 |
| MBG.DE | 46.33 | 46.69 | 0.347 | 0 |
| MRVL | 213.63 | 219.09 | 0.4 | 0 |
| SBUX | 98.2 | 99.08 | 0.401 | 0 |
| JPM | 347.55 | 350.13 | 0.449 | 0 |
| MU | 902.6 | 924.29 | 0.497 | 0 |
| SIE.DE | 258.1 | 261.25 | 0.514 | 0 |
| SY1.DE | 87.2 | 88.18 | 0.583 | 0 |
| HEN3.DE | 72.3 | 73.14 | 0.752 | 0 |
| FAST | 48.63 | 49.46 | 0.784 | 0 |

## Swing-Hoch ueberwunden (17)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 146.77 | 7.073 | 7 |
| META | 593.34 | 665.71 | 3.333 | 7 |
| ZS | 169.1 | 191.6 | 2.056 | 7 |
| IBM | 238.29 | 249.09 | 1.648 | 7 |
| ADP | 268.73 | 276.415 | 1.46 | 6 |
| CRWD | 218.31 | 235.44 | 1.127 | 7 |
| WDAY | 185.82 | 194.14 | 0.949 | 7 |
| GOOGL | 344.68 | 349.485 | 0.642 | 6 |
| VZ | 50.93 | 51.295 | 0.433 | 7 |
| DHL.DE | 55.7 | 55.94 | 0.286 | 4 |
| AAPL | 330.81 | 333.05 | 0.285 | 7 |
| TTWO | 220.71 | 222.94 | 0.275 | 3 |
| TRV | 376.57 | 378.15 | 0.253 | 5 |
| DDOG | 227.58 | 230.04 | 0.205 | 6 |
| FRE.DE | 45.2 | 45.395 | 0.199 | 7 |
| MAR | 339.3 | 340.54 | 0.171 | 1 |
| KO | 89.23 | 89.365 | 0.105 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.