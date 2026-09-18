# Stundenwache

Stand: 2026-09-17 · 158 Werte mit Stundendaten · erstellt 2026-09-18 06:09 UTC

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
| PCAR | 119.77 | 117.35 | -0.903 | 7 |
| CBK.DE | 41.99 | 41.77 | -0.221 | 9 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CMCSA | 22.84 | 22.92 | 0.106 | 0 |
| TXN | 257.1 | 258.11 | 0.122 | 0 |
| HEI.DE | 146.9 | 147.6 | 0.142 | 0 |
| ADSK | 216.4 | 218.66 | 0.219 | 0 |
| CSX | 47.53 | 47.895 | 0.356 | 0 |
| LIN | 455.7 | 458.435 | 0.394 | 0 |
| CTSH | 61.03 | 61.9 | 0.428 | 0 |
| MDLZ | 61.47 | 62.03 | 0.47 | 0 |
| VRTX | 510.2 | 516.35 | 0.566 | 0 |

## Swing-Hoch ueberwunden (23)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 158.01 | 8.992 | 7 |
| ILMN | 221.76 | 245.13 | 2.318 | 7 |
| CRWD | 218.31 | 245.72 | 2.028 | 7 |
| WDAY | 185.82 | 199.205 | 1.476 | 7 |
| QIA.DE | 37.24 | 38.64 | 1.443 | 9 |
| GILD | 146.75 | 150.87 | 1.206 | 7 |
| P911.DE | 45.97 | 47.23 | 0.912 | 8 |
| AMD | 526.79 | 544.78 | 0.819 | 7 |
| AAPL | 330.81 | 337.08 | 0.801 | 7 |
| ARM | 253.155 | 264.89 | 0.795 | 7 |
| DDOG | 227.58 | 235.97 | 0.782 | 7 |
| MU | 944.94 | 977.52 | 0.76 | 7 |
| DHL.DE | 55.7 | 56.33 | 0.716 | 9 |
| FRE.DE | 45.2 | 45.91 | 0.703 | 9 |
| INTC | 104.9 | 108.75 | 0.683 | 7 |
| TRV | 376.57 | 379.5 | 0.459 | 7 |
| AZN | 164.55 | 166.125 | 0.453 | 7 |
| QCOM | 185.46 | 188.71 | 0.402 | 7 |
| PAH3.DE | 29.78 | 29.97 | 0.233 | 3 |
| ISRG | 382.41 | 383.57 | 0.1 | 4 |
| ZS | 196.575 | 197.35 | 0.078 | 3 |
| SAP.DE | 187.26 | 187.58 | 0.053 | 4 |
| MRK | 147.09 | 147.17 | 0.027 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.