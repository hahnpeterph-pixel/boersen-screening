# Stundenwache

Stand: 2026-09-08 · 158 Werte mit Stundendaten · erstellt 2026-09-08 21:45 UTC

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

## Tief angetestet (13)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| JPM | 353.24 | 353.55 | 0.053 | 0 |
| PYPL | 53.03 | 53.19 | 0.075 | 0 |
| ILMN | 210.15 | 211.11 | 0.091 | 0 |
| HNR1.DE | 247.4 | 248.0 | 0.157 | 0 |
| V | 367.44 | 368.83 | 0.222 | 0 |
| COST | 906.1 | 910.13 | 0.232 | 0 |
| MCD | 254.33 | 255.82 | 0.359 | 0 |
| TRV | 362.57 | 365.7 | 0.5 | 0 |
| KO | 87.68 | 88.41 | 0.536 | 0 |
| EXC | 43.5 | 43.955 | 0.56 | 0 |
| PG | 144.305 | 145.6 | 0.575 | 0 |
| DDOG | 203.24 | 210.19 | 0.592 | 0 |
| UNH | 390.555 | 400.87 | 1.261 | 0 |

## Swing-Hoch ueberwunden (19)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 140.34 | 3.227 | 7 |
| INTC | 93.7 | 104.4401 | 2.443 | 7 |
| AMD | 462.21 | 505.53 | 2.311 | 7 |
| CBK.DE | 41.05 | 42.77 | 1.995 | 9 |
| CEG | 285.26 | 298.96 | 1.488 | 7 |
| ORCL | 153.99 | 162.52 | 1.262 | 7 |
| META | 593.34 | 613.31 | 1.114 | 7 |
| DBK.DE | 35.03 | 35.73 | 0.909 | 8 |
| AEP | 123.85 | 125.4 | 0.75 | 7 |
| BMW.DE | 62.72 | 63.9 | 0.739 | 9 |
| MU | 969.44 | 999.94 | 0.698 | 7 |
| QCOM | 170.6 | 174.09 | 0.603 | 7 |
| BKR | 63.02 | 63.91 | 0.572 | 7 |
| KLAC | 186.78 | 189.04 | 0.321 | 7 |
| ADI | 360.77 | 363.3 | 0.253 | 7 |
| MBG.DE | 47.75 | 47.915 | 0.165 | 9 |
| XEL | 76.63 | 76.831 | 0.15 | 4 |
| TXN | 258.04 | 258.905 | 0.119 | 3 |
| WDAY | 185.82 | 186.2 | 0.042 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.