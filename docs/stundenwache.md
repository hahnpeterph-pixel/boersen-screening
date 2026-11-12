# Stundenwache

Stand: 2026-11-11 · 272 Werte mit Stundendaten · erstellt 2026-11-12 03:00 UTC

> **Sitzung noch nicht abgeschlossen.** 9 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 3, 4, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (1)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BABA | 96.05 | 96.0 | -0.013 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (5)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| NEE | 85.57 | 85.995 | 0.246 | 0 |
| CL | 96.82 | 98.03 | 0.491 | 0 |
| CPRT | 31.68 | 32.18 | 0.536 | 0 |
| AMGN | 459.14 | 468.25 | 0.703 | 0 |
| HD | 344.31 | 351.38 | 0.708 | 0 |

## Swing-Hoch ueberwunden (53)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.3575 | 14.798 | 9 |
| IBN | 1404.9 | 1571.6 | 4.767 | 7 |
| FRE.DE | 47.295 | 52.84 | 4.611 | 9 |
| HDB | 734.9 | 806.6 | 4.076 | 7 |
| TTD | 13.68 | 15.99 | 2.745 | 7 |
| TM | 3115.0 | 3398.0 | 2.37 | 3 |
| HEN3.DE | 84.46 | 87.42 | 1.777 | 9 |
| SCHW | 89.96 | 92.79 | 1.478 | 7 |
| TMUS | 163.35 | 172.21 | 1.36 | 7 |
| TTWO | 218.78 | 230.98 | 1.314 | 7 |
| CHTR | 127.16 | 136.34 | 1.307 | 7 |
| PH | 930.84 | 972.18 | 1.228 | 7 |
| MFG | 7824.0 | 8227.0 | 1.198 | 3 |
| SONY | 4068.0 | 4246.0 | 1.183 | 3 |
| AIR.DE | 204.5 | 210.4 | 1.082 | 9 |
| CON.DE | 72.02 | 74.08 | 1.067 | 9 |
| AMD | 514.61 | 552.96 | 0.896 | 7 |
| HONA | 161.7 | 169.47 | 0.836 | 7 |
| GE | 333.75 | 342.68 | 0.753 | 7 |
| BNY | 150.28 | 152.69 | 0.745 | 7 |
| SPG | 231.66 | 234.75 | 0.716 | 7 |
| WDAY | 185.82 | 191.17 | 0.714 | 7 |
| ANET | 188.53 | 196.74 | 0.691 | 7 |
| SAN | 11.05 | 11.306 | 0.64 | 9 |
| ING | 29.68 | 30.16 | 0.597 | 9 |
| SMFG | 3237.0 | 3307.0 | 0.595 | 3 |
| BHP | 59.0 | 59.92 | 0.577 | 4 |
| SNY | 85.37 | 86.4 | 0.57 | 9 |
| DELL | 354.5 | 373.75 | 0.566 | 7 |
| AVGO | 335.74 | 345.45 | 0.544 | 7 |
| VRSK | 201.65 | 205.98 | 0.513 | 7 |
| CEG | 268.64 | 274.759 | 0.47 | 7 |
| FAST | 54.96 | 55.49 | 0.407 | 7 |
| MS | 188.3 | 190.61 | 0.386 | 7 |
| GS | 916.95 | 927.34 | 0.353 | 7 |
| RWE.DE | 58.92 | 59.44 | 0.348 | 6 |
| EQIX | 1055.62 | 1068.47 | 0.338 | 7 |
| KDP | 37.89 | 38.28 | 0.333 | 5 |
| COST | 1081.55 | 1087.52 | 0.275 | 2 |
| XEL | 80.67 | 81.11 | 0.273 | 2 |
| SNOW | 296.84 | 301.27 | 0.272 | 7 |
| TMO | 712.17 | 717.71 | 0.264 | 7 |
| QCOM | 174.0 | 176.55 | 0.256 | 7 |
| UPS | 111.83 | 112.44 | 0.206 | 7 |
| BRK-B | 586.3 | 588.28 | 0.174 | 2 |
| AEP | 128.72 | 129.21 | 0.17 | 3 |
| BKR | 49.02 | 49.4 | 0.158 | 7 |
| T | 22.21 | 22.26 | 0.082 | 1 |
| KO | 97.39 | 97.545 | 0.08 | 2 |
| ENR.DE | 131.78 | 132.42 | 0.08 | 2 |
| CAT | 599.78 | 601.94 | 0.069 | 6 |
| CDW | 172.47 | 173.09 | 0.068 | 7 |
| AAPL | 355.38 | 355.79 | 0.043 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.