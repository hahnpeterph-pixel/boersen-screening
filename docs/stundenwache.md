# Stundenwache

Stand: 2026-09-03 · 158 Werte mit Stundendaten · erstellt 2026-09-04 04:30 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (3)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SIE.DE | 273.0 | 269.95 | -0.601 | 8 |
| BNR.DE | 61.62 | 61.42 | -0.143 | 5 |
| SY1.DE | 91.46 | 91.27 | -0.11 | 6 |

## Tief zurueckerobert (13)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ASML | 1423.4 | 1424.4 | 0.023 | 3 |
| ZAL.DE | 22.91 | 22.93 | 0.03 | 3 |
| LIN | 482.16 | 482.405 | 0.031 | 2 |
| RHM.DE | 1067.4 | 1069.4 | 0.053 | 4 |
| MRK.DE | 138.1 | 138.3 | 0.08 | 2 |
| ADS.DE | 147.6 | 148.7 | 0.275 | 2 |
| MTX.DE | 340.3 | 342.9 | 0.289 | 4 |
| HEN3.DE | 75.1 | 75.6 | 0.465 | 1 |
| DTG.DE | 45.07 | 45.58 | 0.592 | 5 |
| AIR.DE | 193.74 | 196.78 | 0.794 | 1 |
| DHL.DE | 54.52 | 55.21 | 0.855 | 2 |
| PAH3.DE | 27.28 | 27.98 | 1.167 | 4 |
| VOW3.DE | 73.52 | 76.26 | 1.464 | 3 |

## Tief angetestet (11)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DASH | 221.61 | 221.98 | 0.048 | 0 |
| SHL.DE | 38.77 | 38.89 | 0.197 | 0 |
| BEI.DE | 76.46 | 76.82 | 0.229 | 0 |
| IFX.DE | 54.53 | 55.36 | 0.392 | 0 |
| RWE.DE | 57.28 | 57.9 | 0.442 | 0 |
| VZ | 50.15 | 50.59 | 0.575 | 0 |
| NKE | 37.97 | 38.745 | 0.684 | 0 |
| ON | 71.41 | 73.68 | 0.8 | 0 |
| JNJ | 273.16 | 278.44 | 0.916 | 0 |
| ARM | 229.3 | 242.59 | 0.926 | 0 |
| BMW.DE | 59.98 | 61.78 | 1.291 | 0 |

## Swing-Hoch ueberwunden (31)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 264.43 | 4.481 | 7 |
| MRNA | 65.525 | 148.86 | 3.781 | 7 |
| HNR1.DE | 252.4 | 263.2 | 3.203 | 9 |
| WDAY | 185.82 | 206.91 | 2.458 | 7 |
| MBG.DE | 45.62 | 47.105 | 1.654 | 9 |
| CDW | 142.97 | 153.92 | 1.629 | 7 |
| TTD | 14.17 | 15.075 | 1.623 | 7 |
| MUV2.DE | 520.4 | 529.4 | 1.245 | 9 |
| BAS.DE | 52.76 | 53.73 | 1.021 | 9 |
| SPGI | 439.02 | 450.64 | 0.995 | 7 |
| META | 593.34 | 610.68 | 0.883 | 7 |
| AAPL | 322.37 | 328.21 | 0.837 | 7 |
| DBK.DE | 35.03 | 35.585 | 0.783 | 8 |
| CBK.DE | 41.05 | 41.58 | 0.735 | 4 |
| TSLA | 366.5 | 376.355 | 0.698 | 7 |
| WMT | 106.6 | 108.45 | 0.672 | 7 |
| JPM | 358.35 | 362.05 | 0.67 | 6 |
| TMUS | 185.84 | 188.06 | 0.566 | 7 |
| KDP | 32.55 | 32.89 | 0.447 | 7 |
| AEP | 123.85 | 124.7 | 0.402 | 7 |
| BKR | 63.02 | 63.63 | 0.394 | 7 |
| EXC | 44.23 | 44.54 | 0.384 | 7 |
| BIIB | 222.85 | 224.405 | 0.282 | 6 |
| MELI | 1972.59 | 1991.58 | 0.28 | 7 |
| TRV | 372.47 | 374.25 | 0.276 | 6 |
| VRTX | 555.69 | 558.1 | 0.191 | 7 |
| REGN | 839.94 | 843.46 | 0.173 | 6 |
| NFLX | 82.35 | 82.69 | 0.153 | 6 |
| PG | 146.8 | 146.9 | 0.044 | 6 |
| ALV.DE | 452.9 | 453.1 | 0.039 | 2 |
| ORCL | 153.99 | 154.05 | 0.01 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.