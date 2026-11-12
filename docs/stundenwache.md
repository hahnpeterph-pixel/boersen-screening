# Stundenwache

Stand: 2026-11-11 · 272 Werte mit Stundendaten · erstellt 2026-11-12 01:27 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (4)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BNR.DE | 60.9 | 59.28 | -1.361 | 9 |
| NEM | 118.93 | 118.495 | -0.082 | 3 |
| BMW.DE | 58.12 | 58.04 | -0.047 | 9 |
| P911.DE | 46.06 | 46.05 | -0.008 | 5 |

## Tief zurueckerobert (6)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SYK | 317.87 | 318.83 | 0.076 | 2 |
| PAH3.DE | 25.17 | 25.27 | 0.142 | 1 |
| NEE | 85.64 | 85.995 | 0.182 | 1 |
| MDT | 100.8 | 101.63 | 0.313 | 1 |
| SAP.DE | 208.6 | 210.65 | 0.33 | 1 |
| SHL.DE | 42.75 | 43.38 | 0.585 | 1 |

## Tief angetestet (3)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| EOAN.DE | 18.785 | 18.895 | 0.296 | 0 |
| CM | 115.55 | 116.54 | 0.391 | 0 |
| VOW3.DE | 68.48 | 69.4 | 0.401 | 0 |

## Swing-Hoch ueberwunden (56)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.3575 | 7.973 | 9 |
| IBN | 1404.9 | 1571.6 | 5.015 | 7 |
| FRE.DE | 47.295 | 52.84 | 4.822 | 9 |
| HDB | 734.9 | 806.6 | 4.118 | 7 |
| TTD | 13.68 | 15.99 | 2.745 | 7 |
| TM | 3115.0 | 3425.0 | 2.596 | 2 |
| HEN3.DE | 84.46 | 87.42 | 1.765 | 9 |
| SCHW | 89.96 | 92.79 | 1.502 | 7 |
| TMUS | 163.35 | 172.21 | 1.36 | 7 |
| TTWO | 218.78 | 230.98 | 1.314 | 7 |
| CHTR | 127.16 | 136.34 | 1.307 | 7 |
| SONY | 4068.0 | 4264.0 | 1.303 | 2 |
| HSBC | 13.086 | 13.528 | 1.185 | 9 |
| PH | 930.84 | 972.18 | 1.081 | 7 |
| BBVA | 22.84 | 23.63 | 1.069 | 9 |
| AIR.DE | 204.5 | 210.4 | 1.06 | 9 |
| CON.DE | 72.02 | 74.08 | 1.053 | 9 |
| MFG | 7824.0 | 8159.0 | 0.996 | 2 |
| AMD | 514.61 | 552.96 | 0.896 | 7 |
| HONA | 161.7 | 169.47 | 0.837 | 7 |
| BNY | 150.28 | 152.69 | 0.745 | 7 |
| GE | 333.75 | 342.68 | 0.734 | 7 |
| WDAY | 185.82 | 191.17 | 0.714 | 7 |
| ANET | 188.53 | 196.74 | 0.691 | 7 |
| SPG | 231.66 | 234.75 | 0.662 | 7 |
| SAN | 11.05 | 11.306 | 0.612 | 9 |
| DELL | 354.5 | 373.75 | 0.579 | 7 |
| ING | 29.68 | 30.16 | 0.565 | 9 |
| AVGO | 335.74 | 345.45 | 0.544 | 7 |
| SNY | 85.37 | 86.4 | 0.544 | 9 |
| VRSK | 201.65 | 205.98 | 0.514 | 7 |
| BHP | 59.0 | 59.77 | 0.483 | 3 |
| CEG | 268.64 | 274.759 | 0.47 | 7 |
| FAST | 54.96 | 55.49 | 0.407 | 7 |
| MS | 188.3 | 190.61 | 0.382 | 7 |
| SMFG | 3237.0 | 3281.0 | 0.374 | 2 |
| RWE.DE | 58.92 | 59.44 | 0.354 | 6 |
| GS | 916.95 | 927.34 | 0.353 | 7 |
| KDP | 37.89 | 38.28 | 0.333 | 5 |
| EQIX | 1055.62 | 1068.47 | 0.317 | 7 |
| TMO | 712.17 | 719.01 | 0.307 | 6 |
| COST | 1081.55 | 1087.52 | 0.275 | 2 |
| XEL | 80.67 | 81.11 | 0.273 | 2 |
| SNOW | 296.84 | 301.27 | 0.269 | 7 |
| QCOM | 174.0 | 176.55 | 0.256 | 7 |
| UPS | 111.83 | 112.44 | 0.2 | 7 |
| BRK-B | 586.3 | 588.28 | 0.174 | 2 |
| AEP | 128.72 | 129.21 | 0.17 | 3 |
| BKR | 49.02 | 49.4 | 0.158 | 7 |
| HEI.DE | 179.6 | 180.35 | 0.13 | 9 |
| KO | 97.39 | 97.545 | 0.08 | 2 |
| ENR.DE | 131.78 | 132.42 | 0.08 | 2 |
| T | 22.21 | 22.26 | 0.076 | 1 |
| CAT | 599.78 | 601.94 | 0.069 | 6 |
| CDW | 172.47 | 173.09 | 0.068 | 7 |
| AAPL | 355.38 | 355.79 | 0.043 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.