# Stundenwache

Stand: 2026-10-19 · 272 Werte mit Stundendaten · erstellt 2026-10-19 22:55 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| RWE.DE | 57.16 | 57.22 | 0.048 | 1 |

## Tief angetestet (26)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AMGN | 424.75 | 424.86 | 0.01 | 0 |
| MMM | 161.96 | 162.0 | 0.012 | 0 |
| MS | 178.41 | 178.47 | 0.013 | 0 |
| C | 121.62 | 121.72 | 0.029 | 0 |
| MDT | 92.67 | 92.79 | 0.049 | 0 |
| JPM | 333.23 | 333.57 | 0.054 | 0 |
| SCHW | 89.405 | 89.58 | 0.081 | 0 |
| GEV | 903.94 | 908.42 | 0.099 | 0 |
| GLW | 131.63 | 132.83 | 0.145 | 0 |
| UBS | 38.78 | 38.92 | 0.16 | 0 |
| EXC | 42.28 | 42.41 | 0.167 | 0 |
| DBK.DE | 28.385 | 28.52 | 0.168 | 0 |
| DHR | 223.27 | 224.4 | 0.17 | 0 |
| PLD | 123.434 | 124.08 | 0.218 | 0 |
| UNP | 286.06 | 287.02 | 0.225 | 0 |
| ADP | 285.28 | 286.61 | 0.24 | 0 |
| ADI | 390.825 | 394.26 | 0.276 | 0 |
| BIIB | 231.0392 | 233.54 | 0.385 | 0 |
| JNJ | 251.52 | 253.99 | 0.394 | 0 |
| SPOT | 511.2 | 518.56 | 0.435 | 0 |
| SPGI | 423.03 | 427.82 | 0.581 | 0 |
| HD | 306.056 | 309.99 | 0.591 | 0 |
| CRM | 236.9 | 242.46 | 0.646 | 0 |
| MCD | 240.01 | 242.63 | 0.659 | 0 |
| ADBE | 241.51 | 247.06 | 0.67 | 0 |
| MFG | 7831.0 | 8075.0 | 0.911 | 0 |

## Swing-Hoch ueberwunden (57)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WMT | 105.14 | 118.71 | 5.701 | 7 |
| PBR | 54.61 | 64.67 | 5.014 | 7 |
| COP | 130.97 | 145.25 | 4.711 | 7 |
| BRK-B | 507.24 | 532.44 | 4.438 | 7 |
| CCEP | 103.27 | 111.86 | 4.33 | 7 |
| KO | 87.29 | 93.43 | 4.087 | 7 |
| XOM | 164.37 | 178.29 | 4.055 | 7 |
| COST | 931.09 | 995.65 | 4.042 | 7 |
| CVX | 207.41 | 224.43 | 3.848 | 7 |
| CL | 87.22 | 93.4 | 3.744 | 7 |
| SO | 83.98 | 89.27 | 3.569 | 7 |
| VRSK | 171.31 | 189.16 | 3.446 | 7 |
| SHEL | 36.815 | 39.31 | 3.305 | 9 |
| MUV2.DE | 516.2 | 543.4 | 3.168 | 9 |
| MNST | 43.64 | 46.805 | 3.098 | 7 |
| MO | 69.6 | 74.065 | 2.97 | 7 |
| TRV | 362.75 | 385.43 | 2.964 | 7 |
| LMT | 515.77 | 548.45 | 2.93 | 7 |
| TJX | 139.62 | 147.36 | 2.876 | 7 |
| CB | 339.66 | 356.34 | 2.736 | 7 |
| KDP | 32.14 | 34.45 | 2.7 | 7 |
| TM | 2944.5 | 3098.0 | 2.686 | 7 |
| ABNB | 164.91 | 175.5 | 2.356 | 7 |
| DUK | 115.17 | 119.27 | 2.298 | 7 |
| BTI | 42.42 | 44.41 | 2.215 | 9 |
| PEP | 127.21 | 133.6 | 2.19 | 7 |
| ROST | 227.6 | 238.67 | 2.047 | 7 |
| DB1.DE | 296.8 | 307.6 | 1.964 | 9 |
| IBM | 224.51 | 236.44 | 1.922 | 7 |
| SONY | 3797.0 | 3951.0 | 1.876 | 7 |
| EQNR | 419.3 | 435.0 | 1.682 | 8 |
| NVS | 120.02 | 124.04 | 1.638 | 9 |
| ZAL.DE | 24.73 | 25.83 | 1.562 | 9 |
| IDXX | 536.84 | 555.65 | 1.48 | 7 |
| LIN | 492.1 | 503.54 | 1.381 | 7 |
| WDAY | 185.82 | 195.15 | 1.354 | 7 |
| SYK | 287.45 | 298.06 | 1.322 | 7 |
| RTX | 187.41 | 192.2 | 1.309 | 7 |
| AEP | 121.8 | 124.72 | 1.279 | 7 |
| CNQ | 52.57 | 54.12 | 1.228 | 7 |
| BLK | 1092.92 | 1124.53 | 1.195 | 7 |
| PM | 195.22 | 201.0 | 1.128 | 7 |
| GSK | 17.91 | 18.545 | 1.005 | 9 |
| MDLZ | 62.19 | 63.33 | 0.943 | 7 |
| LLY | 1206.63 | 1240.5601 | 0.919 | 7 |
| ACN | 227.63 | 236.91 | 0.855 | 7 |
| ODFL | 182.91 | 186.77 | 0.843 | 7 |
| CTSH | 64.74 | 66.76 | 0.748 | 7 |
| IBN | 1360.8 | 1381.0 | 0.747 | 7 |
| FANG | 200.65 | 203.03 | 0.523 | 7 |
| SBUX | 96.73 | 97.86 | 0.461 | 7 |
| HNR1.DE | 270.8 | 273.0 | 0.461 | 9 |
| CDW | 150.34 | 152.68 | 0.456 | 7 |
| SRT3.DE | 257.7 | 260.7 | 0.342 | 9 |
| MRK.DE | 142.6 | 143.7 | 0.328 | 8 |
| ISRG | 430.0 | 433.2 | 0.293 | 7 |
| BMW.DE | 56.42 | 56.8 | 0.263 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.