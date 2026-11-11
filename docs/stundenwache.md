# Stundenwache

Stand: 2026-11-10 · 272 Werte mit Stundendaten · erstellt 2026-11-11 01:58 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (4)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| C | 121.43 | 122.275 | 0.236 | 0 |
| ADSK | 257.87 | 260.16 | 0.238 | 0 |
| ORLY | 88.5 | 89.38 | 0.351 | 0 |
| MSFT | 526.37 | 533.42 | 0.408 | 0 |

## Swing-Hoch ueberwunden (38)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.2 | 7.556 | 9 |
| IBN | 1404.9 | 1589.0 | 5.538 | 7 |
| FRE.DE | 47.295 | 53.31 | 5.23 | 9 |
| HDB | 734.9 | 798.15 | 3.633 | 7 |
| TM | 3115.0 | 3390.0 | 2.338 | 2 |
| TTD | 13.68 | 15.425 | 2.212 | 7 |
| SCHW | 89.96 | 93.03 | 1.63 | 7 |
| HEN3.DE | 84.46 | 86.76 | 1.371 | 9 |
| BBVA | 22.84 | 23.75 | 1.231 | 9 |
| SONY | 4068.0 | 4245.0 | 1.187 | 2 |
| CHTR | 127.16 | 134.04 | 0.987 | 5 |
| HSBC | 13.086 | 13.446 | 0.965 | 9 |
| PH | 930.84 | 965.93 | 0.918 | 7 |
| TMUS | 163.35 | 169.01 | 0.861 | 7 |
| AIR.DE | 204.5 | 209.25 | 0.853 | 9 |
| MFG | 7824.0 | 8112.0 | 0.827 | 2 |
| TTWO | 218.78 | 224.66 | 0.669 | 7 |
| CON.DE | 72.02 | 73.26 | 0.634 | 9 |
| SPG | 231.66 | 234.55 | 0.619 | 6 |
| SAN | 11.05 | 11.288 | 0.569 | 9 |
| HONA | 161.7 | 166.375 | 0.503 | 7 |
| DTG.DE | 42.33 | 42.89 | 0.475 | 9 |
| SMFG | 3237.0 | 3292.0 | 0.453 | 2 |
| HEI.DE | 179.6 | 181.9 | 0.398 | 9 |
| WDAY | 185.82 | 188.85 | 0.394 | 7 |
| GE | 333.75 | 338.0 | 0.349 | 5 |
| MTX.DE | 357.5 | 362.2 | 0.335 | 9 |
| SNY | 85.37 | 85.96 | 0.312 | 9 |
| VRSK | 201.65 | 204.01 | 0.269 | 5 |
| ING | 29.68 | 29.905 | 0.265 | 9 |
| BNY | 150.28 | 151.14 | 0.262 | 7 |
| BAYN.DE | 56.6 | 57.04 | 0.235 | 9 |
| TMO | 712.17 | 716.255 | 0.183 | 6 |
| GSK | 19.155 | 19.24 | 0.166 | 9 |
| UL | 49.355 | 49.48 | 0.102 | 5 |
| SPCX | 142.74 | 143.15 | 0.049 | 2 |
| AMD | 514.61 | 515.42 | 0.019 | 4 |
| CDNS | 331.67 | 331.7 | 0.002 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.