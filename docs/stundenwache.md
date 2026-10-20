# Stundenwache

Stand: 2026-10-19 · 272 Werte mit Stundendaten · erstellt 2026-10-20 10:02 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 4, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| CBK.DE | 36.33 | 36.27 | -0.064 | 1 |
| BBVA | 22.46 | 22.44 | -0.033 | 1 |
| VNA.DE | 16.045 | 16.04 | -0.012 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (29)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CSX | 47.88 | 47.88 | 0.0 | 0 |
| HONA | 162.43 | 162.49 | 0.012 | 0 |
| RIO | 65.23 | 65.27 | 0.016 | 0 |
| USB | 57.82 | 57.85 | 0.027 | 0 |
| DE | 626.44 | 627.02 | 0.028 | 0 |
| WFC | 81.71 | 81.8 | 0.044 | 0 |
| MDT | 92.67 | 92.79 | 0.049 | 0 |
| ING | 29.015 | 29.05 | 0.05 | 0 |
| EXC | 42.28 | 42.41 | 0.167 | 0 |
| DHR | 223.26 | 224.4 | 0.171 | 0 |
| SIE.DE | 255.2 | 256.45 | 0.183 | 0 |
| ENB | 46.98 | 47.135 | 0.193 | 0 |
| IFX.DE | 50.51 | 51.08 | 0.195 | 0 |
| BMY | 58.44 | 58.85 | 0.218 | 0 |
| DELL | 448.55 | 455.23 | 0.221 | 0 |
| RY | 195.7 | 196.36 | 0.221 | 0 |
| XEL | 74.84 | 75.13 | 0.236 | 0 |
| SAN | 11.58 | 11.672 | 0.28 | 0 |
| BAYN.DE | 43.18 | 43.58 | 0.31 | 0 |
| BIIB | 231.04 | 233.54 | 0.385 | 0 |
| CSGP | 31.39 | 31.805 | 0.405 | 0 |
| AAPL | 340.12 | 342.97 | 0.444 | 0 |
| ADSK | 236.54 | 240.7 | 0.507 | 0 |
| SCCO | 197.5 | 201.82 | 0.614 | 0 |
| CRM | 236.9 | 242.46 | 0.646 | 0 |
| SPGI | 422.43 | 427.82 | 0.65 | 0 |
| MCD | 240.01 | 242.63 | 0.659 | 0 |
| ADBE | 241.51 | 247.06 | 0.67 | 0 |
| MCK | 977.89 | 1010.27 | 1.273 | 0 |

## Swing-Hoch ueberwunden (57)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WMT | 105.14 | 118.71 | 5.7 | 7 |
| PBR | 54.61 | 64.67 | 5.014 | 7 |
| COP | 130.97 | 145.25 | 4.71 | 7 |
| BRK-B | 507.24 | 532.44 | 4.437 | 7 |
| CCEP | 103.27 | 111.86 | 4.331 | 7 |
| KO | 87.29 | 93.43 | 4.087 | 7 |
| XOM | 164.37 | 178.29 | 4.055 | 7 |
| COST | 931.09 | 995.65 | 4.042 | 7 |
| CVX | 207.41 | 224.43 | 3.848 | 7 |
| CL | 87.22 | 93.4 | 3.744 | 7 |
| SHEL | 36.815 | 39.475 | 3.576 | 3 |
| SO | 83.98 | 89.27 | 3.569 | 7 |
| VRSK | 171.31 | 189.16 | 3.446 | 7 |
| MNST | 43.64 | 46.8 | 3.092 | 7 |
| MO | 69.6 | 74.065 | 2.971 | 7 |
| TRV | 362.75 | 385.53 | 2.967 | 7 |
| TM | 2944.5 | 3099.0 | 2.957 | 7 |
| LMT | 515.77 | 548.45 | 2.93 | 7 |
| TJX | 139.62 | 147.355 | 2.874 | 7 |
| CB | 339.66 | 356.34 | 2.736 | 7 |
| KDP | 32.14 | 34.45 | 2.7 | 7 |
| ABNB | 164.91 | 175.5 | 2.356 | 7 |
| DUK | 115.17 | 119.27 | 2.298 | 7 |
| PEP | 127.21 | 133.574 | 2.177 | 7 |
| NVS | 120.02 | 125.04 | 2.135 | 3 |
| ROST | 227.6 | 238.67 | 2.047 | 7 |
| SONY | 3797.0 | 3959.0 | 2.03 | 7 |
| BTI | 42.42 | 44.1655 | 2.021 | 3 |
| IBM | 224.51 | 236.44 | 1.922 | 7 |
| EQNR | 419.3 | 436.6 | 1.895 | 3 |
| DB1.DE | 296.8 | 307.0 | 1.879 | 3 |
| IDXX | 536.84 | 555.65 | 1.48 | 7 |
| LIN | 492.1 | 503.54 | 1.38 | 7 |
| WDAY | 185.82 | 195.15 | 1.354 | 7 |
| SYK | 287.45 | 298.06 | 1.322 | 7 |
| RTX | 187.41 | 192.2 | 1.309 | 7 |
| AEP | 121.8 | 124.72 | 1.279 | 7 |
| CNQ | 52.57 | 54.12 | 1.227 | 7 |
| BLK | 1092.92 | 1124.53 | 1.194 | 7 |
| GSK | 17.91 | 18.6092 | 1.149 | 3 |
| PM | 195.22 | 201.0 | 1.127 | 7 |
| MDLZ | 62.19 | 63.33 | 0.943 | 7 |
| LLY | 1206.63 | 1240.5601 | 0.919 | 7 |
| ACN | 227.63 | 236.9 | 0.852 | 7 |
| ODFL | 182.91 | 186.77 | 0.843 | 7 |
| ZAL.DE | 24.73 | 25.26 | 0.784 | 3 |
| CTSH | 64.74 | 66.76 | 0.748 | 7 |
| IBN | 1360.8 | 1381.0 | 0.745 | 7 |
| SRT3.DE | 257.7 | 262.8 | 0.591 | 3 |
| MRK.DE | 142.6 | 144.45 | 0.567 | 3 |
| HNR1.DE | 270.8 | 273.4 | 0.563 | 3 |
| FANG | 200.65 | 203.03 | 0.523 | 7 |
| SBUX | 96.73 | 97.86 | 0.461 | 7 |
| CDW | 150.34 | 152.69 | 0.458 | 7 |
| ISRG | 430.0 | 433.2 | 0.293 | 7 |
| BMW.DE | 56.42 | 56.68 | 0.19 | 3 |
| BP | 6.167 | 6.177 | 0.073 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.