# Stundenwache

Stand: 2026-09-11 · 158 Werte mit Stundendaten · erstellt 2026-09-12 06:01 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (6)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| HEN3.DE | 73.44 | 72.44 | -0.91 | 3 |
| BAS.DE | 52.26 | 51.81 | -0.425 | 9 |
| BAYN.DE | 48.32 | 47.93 | -0.392 | 2 |
| SHL.DE | 38.29 | 38.17 | -0.183 | 1 |
| SY1.DE | 87.7 | 87.46 | -0.144 | 2 |
| RHM.DE | 992.7 | 988.2 | -0.12 | 2 |

## Tief zurueckerobert (6)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ZAL.DE | 22.24 | 22.24 | 0.0 | 7 |
| HEI.DE | 154.6 | 155.0 | 0.081 | 4 |
| CRWD | 205.4 | 206.67 | 0.095 | 1 |
| MBG.DE | 46.53 | 46.665 | 0.133 | 1 |
| SAP.DE | 176.2 | 177.82 | 0.283 | 6 |
| SRT3.DE | 230.9 | 233.7 | 0.413 | 1 |

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCD | 252.15 | 252.52 | 0.098 | 0 |
| BNR.DE | 60.38 | 60.62 | 0.173 | 0 |
| AEP | 122.92 | 123.34 | 0.227 | 0 |
| SPGI | 407.44 | 410.69 | 0.268 | 0 |
| PDD | 77.25 | 77.81 | 0.27 | 0 |
| ADP | 265.0 | 267.945 | 0.594 | 0 |
| KHC | 24.15 | 24.61 | 0.703 | 0 |
| ILMN | 200.01 | 206.47 | 0.746 | 0 |

## Swing-Hoch ueberwunden (12)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 143.94 | 6.535 | 7 |
| META | 593.34 | 648.23 | 2.574 | 7 |
| ADI | 366.97 | 378.98 | 1.218 | 7 |
| NXPI | 231.3 | 236.68 | 0.844 | 7 |
| CSCO | 110.43 | 112.12 | 0.811 | 7 |
| TXN | 262.74 | 268.7 | 0.803 | 7 |
| IBM | 238.29 | 243.235 | 0.779 | 6 |
| ON | 75.33 | 76.15 | 0.307 | 1 |
| AAPL | 330.81 | 332.23 | 0.181 | 7 |
| BMW.DE | 62.72 | 62.86 | 0.088 | 2 |
| CTAS | 201.38 | 201.61 | 0.071 | 7 |
| FRE.DE | 45.2 | 45.265 | 0.069 | 8 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.