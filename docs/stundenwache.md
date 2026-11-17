# Stundenwache

Stand: 2026-11-16 · 272 Werte mit Stundendaten · erstellt 2026-11-17 04:32 UTC

> **Sitzung noch nicht abgeschlossen.** 14 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 3, 4, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| TTWO | 223.16 | 213.48 | -0.867 | 7 |
| C | 121.43 | 121.33 | -0.028 | 4 |
| GS | 892.1 | 891.61 | -0.016 | 5 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (16)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CDW | 165.33 | 165.83 | 0.055 | 0 |
| TJX | 130.67 | 131.1 | 0.108 | 0 |
| HONA | 162.34 | 163.41 | 0.122 | 0 |
| PH | 930.37 | 935.17 | 0.14 | 0 |
| BMO | 169.31 | 169.82 | 0.144 | 0 |
| VZ | 46.21 | 46.359 | 0.145 | 0 |
| CSCO | 93.9 | 94.56 | 0.159 | 0 |
| STX | 491.04 | 500.145 | 0.168 | 0 |
| VRTX | 534.12 | 537.81 | 0.207 | 0 |
| MPC | 398.1 | 402.21 | 0.208 | 0 |
| AXP | 316.96 | 319.01 | 0.255 | 0 |
| PCAR | 104.81 | 105.57 | 0.26 | 0 |
| MS | 183.91 | 185.59 | 0.292 | 0 |
| WFC | 84.05 | 84.855 | 0.388 | 0 |
| BAC | 49.63 | 50.1099 | 0.392 | 0 |
| SPG | 230.72 | 232.85 | 0.469 | 0 |

## Swing-Hoch ueberwunden (33)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.35 | 15.188 | 9 |
| IBN | 1404.9 | 1599.2 | 5.75 | 1 |
| TM | 3115.0 | 3400.0 | 2.304 | 5 |
| CHTR | 127.16 | 138.99 | 1.634 | 7 |
| SNY | 85.37 | 88.41 | 1.604 | 9 |
| COST | 1081.55 | 1114.42 | 1.544 | 7 |
| VRSK | 201.65 | 212.76 | 1.469 | 7 |
| SONY | 4068.0 | 4267.0 | 1.304 | 5 |
| KO | 97.39 | 99.605 | 1.205 | 7 |
| WDAY | 185.82 | 194.105 | 1.116 | 7 |
| ALV.DE | 466.4 | 475.4 | 1.02 | 9 |
| MUV2.DE | 579.8 | 592.0 | 0.976 | 9 |
| PG | 169.79 | 173.15 | 0.975 | 7 |
| UL | 49.355 | 50.48 | 0.941 | 9 |
| NVO | 278.0 | 285.25 | 0.898 | 8 |
| DTE.DE | 26.49 | 27.03 | 0.885 | 9 |
| CL | 99.01 | 100.99 | 0.835 | 7 |
| UNH | 406.72 | 412.1 | 0.49 | 7 |
| BNY | 150.28 | 151.69 | 0.434 | 7 |
| CCEP | 117.96 | 119.21 | 0.432 | 7 |
| NVS | 134.84 | 135.94 | 0.41 | 9 |
| CMCSA | 25.3 | 25.605 | 0.401 | 7 |
| XEL | 80.67 | 81.21 | 0.338 | 7 |
| T | 22.21 | 22.37 | 0.321 | 7 |
| ING | 29.68 | 29.91 | 0.321 | 9 |
| ADP | 310.98 | 313.15 | 0.289 | 6 |
| PEP | 145.55 | 146.475 | 0.269 | 7 |
| DUK | 129.97 | 130.58 | 0.26 | 7 |
| ODFL | 172.8 | 174.31 | 0.215 | 7 |
| DB1.DE | 329.1 | 330.2 | 0.17 | 9 |
| APP | 413.6 | 415.05 | 0.054 | 4 |
| UPS | 111.83 | 111.87 | 0.015 | 1 |
| MA | 661.84 | 661.93 | 0.005 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.