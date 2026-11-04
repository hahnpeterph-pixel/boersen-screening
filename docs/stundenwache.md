# Stundenwache

Stand: 2026-11-03 · 272 Werte mit Stundendaten · erstellt 2026-11-04 02:23 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 4, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (15)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SHOP | 153.33 | 142.66 | -1.319 | 7 |
| ZAL.DE | 26.4 | 25.42 | -1.237 | 7 |
| COP | 146.54 | 144.435 | -0.548 | 7 |
| TJX | 139.08 | 137.65 | -0.527 | 7 |
| EOAN.DE | 18.62 | 18.44 | -0.51 | 9 |
| XOM | 179.67 | 177.5 | -0.484 | 7 |
| CVX | 227.42 | 225.36 | -0.408 | 7 |
| SAP.DE | 207.95 | 206.25 | -0.301 | 9 |
| MRK.DE | 149.6 | 148.65 | -0.289 | 8 |
| PSX | 274.38 | 272.04 | -0.229 | 2 |
| PGR | 230.21 | 229.17 | -0.172 | 6 |
| ENB | 49.0 | 48.935 | -0.088 | 1 |
| TM | 3007.0 | 3005.0 | -0.032 | 1 |
| MUFG | 3309.0 | 3306.0 | -0.029 | 1 |
| MFG | 7390.0 | 7386.0 | -0.014 | 1 |

## Tief zurueckerobert (6)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MO | 76.91 | 76.92 | 0.005 | 5 |
| SCCO | 173.3525 | 173.44 | 0.01 | 5 |
| DB1.DE | 313.5 | 314.2 | 0.106 | 2 |
| ISRG | 437.51 | 440.7 | 0.232 | 1 |
| MPC | 419.28 | 427.63 | 0.449 | 1 |
| CBK.DE | 37.61 | 38.1 | 0.567 | 1 |

## Tief angetestet (13)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BABA | 97.2 | 97.45 | 0.068 | 0 |
| AXON | 413.18 | 416.51 | 0.183 | 0 |
| CNQ | 53.28 | 53.565 | 0.201 | 0 |
| RWE.DE | 56.52 | 56.86 | 0.247 | 0 |
| SRT3.DE | 289.0 | 292.2 | 0.325 | 0 |
| DHR | 227.53 | 230.1 | 0.369 | 0 |
| VLO | 380.54 | 387.65 | 0.38 | 0 |
| SNOW | 287.93 | 295.04 | 0.385 | 0 |
| PM | 205.57 | 208.02 | 0.416 | 0 |
| GD | 368.48 | 374.34 | 0.819 | 0 |
| TTD | 12.375 | 12.865 | 0.839 | 0 |
| TMO | 679.4 | 698.37 | 0.881 | 0 |
| IFX.DE | 50.18 | 52.61 | 0.89 | 0 |

## Swing-Hoch ueberwunden (61)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| REGN | 825.52 | 974.25 | 5.132 | 7 |
| BAYN.DE | 45.83 | 52.3 | 4.522 | 9 |
| IDXX | 571.75 | 672.2 | 4.119 | 7 |
| QIA.DE | 42.345 | 45.005 | 3.619 | 9 |
| GEHC | 72.3 | 80.63 | 3.613 | 7 |
| MCD | 247.29 | 263.09 | 3.058 | 7 |
| RTX | 187.41 | 203.83 | 3.022 | 7 |
| AZN | 128.06 | 137.88 | 2.981 | 9 |
| UPS | 103.08 | 109.16 | 2.384 | 7 |
| SPG | 213.63 | 222.08 | 2.159 | 7 |
| P911.DE | 43.59 | 46.1 | 1.976 | 9 |
| DBK.DE | 28.815 | 30.565 | 1.966 | 9 |
| HEI.DE | 150.0 | 157.65 | 1.918 | 9 |
| ADS.DE | 161.15 | 168.95 | 1.889 | 9 |
| UNP | 291.93 | 303.37 | 1.863 | 7 |
| FRE.DE | 47.295 | 48.895 | 1.853 | 9 |
| SBUX | 100.33 | 104.74 | 1.812 | 7 |
| CPRT | 29.43 | 31.06 | 1.714 | 7 |
| HNR1.DE | 283.2 | 291.2 | 1.662 | 9 |
| MAR | 398.42 | 416.245 | 1.658 | 7 |
| SHL.DE | 42.06 | 43.33 | 1.648 | 9 |
| LOW | 204.52 | 213.23 | 1.574 | 7 |
| WDAY | 185.82 | 197.93 | 1.557 | 7 |
| ROP | 450.76 | 473.39 | 1.502 | 7 |
| FDX | 307.94 | 318.02 | 1.281 | 7 |
| ABT | 105.88 | 109.41 | 1.164 | 7 |
| MA | 633.29 | 647.31 | 1.106 | 7 |
| DXCM | 79.86 | 82.98 | 1.101 | 7 |
| BRK-B | 549.0 | 557.135 | 1.045 | 7 |
| HEN3.DE | 79.44 | 80.94 | 1.028 | 9 |
| NVO | 264.75 | 270.15 | 1.006 | 8 |
| BIIB | 240.99 | 249.09 | 0.987 | 7 |
| NEE | 82.81 | 84.33 | 0.908 | 7 |
| WMT | 122.4 | 124.81 | 0.888 | 7 |
| MDT | 96.89 | 98.88 | 0.887 | 7 |
| GM | 85.79 | 88.33 | 0.852 | 7 |
| V | 414.6 | 420.38 | 0.737 | 7 |
| IBN | 1404.9 | 1424.5 | 0.693 | 6 |
| NXPI | 255.31 | 262.97 | 0.647 | 7 |
| GE | 314.0 | 320.66 | 0.613 | 7 |
| UBS | 38.96 | 39.45 | 0.579 | 9 |
| ALV.DE | 437.5 | 441.0 | 0.54 | 9 |
| PH | 930.84 | 945.105 | 0.514 | 7 |
| CMCSA | 23.29 | 23.685 | 0.512 | 7 |
| BAS.DE | 52.86 | 53.34 | 0.497 | 9 |
| DIS | 113.38 | 114.23 | 0.42 | 5 |
| DE | 660.39 | 665.82 | 0.309 | 7 |
| DUK | 125.87 | 126.5 | 0.282 | 7 |
| PAH3.DE | 25.6 | 25.78 | 0.272 | 9 |
| SPOT | 593.8 | 600.22 | 0.266 | 6 |
| CB | 364.86 | 366.53 | 0.244 | 7 |
| CHTR | 112.71 | 113.76 | 0.238 | 7 |
| PYPL | 57.95 | 58.195 | 0.17 | 7 |
| MUV2.DE | 569.2 | 570.4 | 0.13 | 5 |
| APH | 83.87 | 84.185 | 0.086 | 2 |
| DHL.DE | 58.92 | 59.0 | 0.077 | 7 |
| GEV | 914.88 | 918.14 | 0.061 | 6 |
| HON | 223.81 | 224.06 | 0.044 | 6 |
| WFC | 85.49 | 85.535 | 0.023 | 3 |
| WELL | 240.94 | 241.08 | 0.022 | 5 |
| SNY | 81.19 | 81.22 | 0.018 | 8 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.