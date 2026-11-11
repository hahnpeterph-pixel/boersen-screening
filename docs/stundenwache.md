# Stundenwache

Stand: 2026-11-10 · 272 Werte mit Stundendaten · erstellt 2026-11-11 12:38 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.185 | 14.276 | 5 |
| FRE.DE | 47.295 | 53.0 | 4.796 | 5 |
| IBN | 1404.9 | 1571.6 | 4.767 | 7 |
| HDB | 734.9 | 806.6 | 4.076 | 7 |
| TM | 3115.0 | 3415.0 | 2.548 | 7 |
| TTD | 13.68 | 15.425 | 2.212 | 7 |
| SCHW | 89.96 | 93.03 | 1.63 | 7 |
| HEN3.DE | 84.46 | 86.82 | 1.435 | 5 |
| CON.DE | 72.02 | 74.14 | 1.104 | 5 |
| MFG | 7824.0 | 8175.0 | 1.0 | 7 |
| CHTR | 127.16 | 134.04 | 0.987 | 5 |
| PH | 930.84 | 965.93 | 0.918 | 7 |
| SONY | 4068.0 | 4205.0 | 0.901 | 7 |
| TMUS | 163.35 | 169.01 | 0.861 | 7 |
| AIR.DE | 204.5 | 209.05 | 0.836 | 5 |
| BHP | 59.0 | 60.39 | 0.824 | 7 |
| TTWO | 218.78 | 224.66 | 0.669 | 7 |
| SPG | 231.66 | 234.55 | 0.619 | 6 |
| RWE.DE | 58.92 | 59.68 | 0.508 | 2 |
| HONA | 161.7 | 166.375 | 0.503 | 7 |
| SAN | 11.05 | 11.244 | 0.486 | 5 |
| SMFG | 3237.0 | 3296.0 | 0.486 | 7 |
| WDAY | 185.82 | 188.85 | 0.391 | 7 |
| GE | 333.75 | 338.0 | 0.349 | 5 |
| TMO | 712.17 | 718.51 | 0.285 | 7 |
| VRSK | 201.65 | 204.01 | 0.269 | 5 |
| DTG.DE | 42.33 | 42.65 | 0.265 | 5 |
| BNY | 150.28 | 151.14 | 0.262 | 7 |
| ING | 29.68 | 29.88 | 0.249 | 5 |
| SNY | 85.37 | 85.74 | 0.208 | 5 |
| SPCX | 142.74 | 143.15 | 0.049 | 2 |
| AMD | 514.61 | 515.49 | 0.021 | 4 |
| ENR.DE | 131.78 | 131.92 | 0.018 | 1 |
| CDNS | 331.67 | 331.7 | 0.002 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.