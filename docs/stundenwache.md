# Stundenwache

Stand: 2026-09-15 · 158 Werte mit Stundendaten · erstellt 2026-09-16 04:26 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (2)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DBK.DE | 33.795 | 33.42 | -0.455 | 9 |
| ZAL.DE | 22.0 | 21.76 | -0.339 | 2 |

## Tief zurueckerobert (9)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DTG.DE | 43.49 | 43.5 | 0.011 | 3 |
| ASML | 1369.6 | 1373.6 | 0.079 | 1 |
| VNA.DE | 17.875 | 18.005 | 0.322 | 6 |
| MBG.DE | 46.31 | 46.725 | 0.39 | 3 |
| BNR.DE | 60.28 | 60.82 | 0.406 | 5 |
| CON.DE | 68.74 | 69.6 | 0.47 | 1 |
| MRK.DE | 129.7 | 131.1 | 0.521 | 2 |
| HEN3.DE | 72.22 | 72.86 | 0.554 | 1 |
| RWE.DE | 57.08 | 58.26 | 0.775 | 1 |

## Tief angetestet (11)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TTWO | 211.54 | 211.9 | 0.042 | 0 |
| EXC | 42.14 | 42.195 | 0.071 | 0 |
| XEL | 72.29 | 72.485 | 0.147 | 0 |
| SIE.DE | 257.85 | 258.925 | 0.17 | 0 |
| ROP | 382.18 | 383.93 | 0.172 | 0 |
| DIS | 105.92 | 106.39 | 0.213 | 0 |
| ENR.DE | 131.52 | 132.98 | 0.27 | 0 |
| SNPS | 362.55 | 367.72 | 0.274 | 0 |
| BKR | 56.03 | 56.72 | 0.342 | 0 |
| IFX.DE | 53.4 | 54.47 | 0.447 | 0 |
| KDP | 31.1 | 31.51 | 0.652 | 0 |

## Swing-Hoch ueberwunden (17)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 143.77 | 7.509 | 7 |
| META | 593.34 | 670.49 | 3.43 | 7 |
| ZS | 169.1 | 193.96 | 2.297 | 7 |
| ADP | 268.73 | 277.575 | 1.661 | 6 |
| CRWD | 218.31 | 242.52 | 1.595 | 7 |
| IBM | 238.29 | 248.4 | 1.531 | 7 |
| FANG | 207.57 | 211.47 | 0.709 | 7 |
| VZ | 50.93 | 51.45 | 0.615 | 7 |
| WDAY | 185.82 | 190.68 | 0.559 | 7 |
| QCOM | 185.46 | 187.87 | 0.315 | 7 |
| TRV | 376.57 | 377.97 | 0.227 | 7 |
| DDOG | 227.58 | 230.12 | 0.21 | 6 |
| DHL.DE | 55.7 | 55.84 | 0.165 | 3 |
| FRE.DE | 45.2 | 45.335 | 0.136 | 8 |
| AAPL | 330.81 | 331.335 | 0.067 | 1 |
| ILMN | 221.76 | 222.31 | 0.062 | 5 |
| GOOGL | 344.68 | 345.03 | 0.046 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.