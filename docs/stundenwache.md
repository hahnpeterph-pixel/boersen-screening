# Stundenwache

Stand: 2026-11-03 · 272 Werte mit Stundendaten · erstellt 2026-11-04 04:46 UTC

> **Sitzung noch nicht abgeschlossen.** 13 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 3, 4, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| ISRG | 437.51 | 440.7 | 0.232 | 1 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKR | 52.78 | 52.79 | 0.005 | 0 |
| PEP | 137.09 | 137.22 | 0.04 | 0 |
| CSX | 50.63 | 50.7 | 0.059 | 0 |
| XOM | 177.2 | 177.5 | 0.067 | 0 |
| MNST | 47.02 | 47.15 | 0.117 | 0 |
| ENB | 48.84 | 48.935 | 0.13 | 0 |
| TJX | 137.02 | 137.65 | 0.219 | 0 |
| UPS | 108.59 | 109.16 | 0.226 | 0 |
| KDP | 34.37 | 34.725 | 0.388 | 0 |
| C | 121.43 | 122.705 | 0.444 | 0 |
| NKE | 37.94 | 38.48 | 0.498 | 0 |
| ADP | 292.29 | 296.735 | 0.553 | 0 |
| GD | 368.36 | 374.34 | 0.795 | 0 |
| TTD | 12.375 | 12.865 | 0.839 | 0 |
| IFX.DE | 50.18 | 52.61 | 0.893 | 0 |

## Swing-Hoch ueberwunden (58)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| REGN | 825.52 | 974.25 | 5.132 | 7 |
| IDXX | 571.75 | 672.2 | 4.119 | 7 |
| QIA.DE | 42.345 | 45.005 | 4.013 | 9 |
| BAYN.DE | 45.83 | 52.3 | 3.996 | 9 |
| GEHC | 72.3 | 80.63 | 3.613 | 7 |
| MCD | 247.29 | 263.09 | 3.058 | 7 |
| RTX | 187.41 | 203.83 | 3.012 | 7 |
| AZN | 128.06 | 137.88 | 2.981 | 9 |
| SPG | 213.63 | 222.08 | 2.189 | 7 |
| DBK.DE | 28.815 | 30.565 | 1.905 | 9 |
| FRE.DE | 47.295 | 48.895 | 1.896 | 9 |
| HEI.DE | 150.0 | 157.65 | 1.85 | 9 |
| SBUX | 100.33 | 104.74 | 1.812 | 7 |
| ADS.DE | 161.15 | 168.95 | 1.811 | 9 |
| HNR1.DE | 283.2 | 291.2 | 1.739 | 9 |
| CPRT | 29.43 | 31.06 | 1.714 | 7 |
| MAR | 398.42 | 416.245 | 1.658 | 7 |
| SHL.DE | 42.06 | 43.33 | 1.606 | 9 |
| WDAY | 185.82 | 197.93 | 1.557 | 7 |
| LOW | 204.52 | 213.23 | 1.538 | 7 |
| ROP | 450.76 | 473.39 | 1.502 | 7 |
| FDX | 307.94 | 318.02 | 1.285 | 7 |
| ABT | 105.88 | 109.41 | 1.164 | 7 |
| DXCM | 79.86 | 82.98 | 1.101 | 7 |
| HEN3.DE | 79.44 | 80.94 | 1.078 | 9 |
| MA | 633.29 | 647.31 | 1.067 | 7 |
| BRK-B | 549.0 | 557.135 | 1.045 | 7 |
| NVO | 264.75 | 270.15 | 1.006 | 8 |
| BIIB | 240.99 | 249.09 | 0.987 | 7 |
| MDT | 96.89 | 98.88 | 0.909 | 7 |
| NEE | 82.81 | 84.33 | 0.909 | 7 |
| WMT | 122.4 | 124.81 | 0.888 | 7 |
| GM | 85.79 | 88.33 | 0.851 | 7 |
| IBN | 1404.9 | 1426.5 | 0.762 | 2 |
| V | 414.6 | 420.38 | 0.737 | 7 |
| NXPI | 255.31 | 262.97 | 0.647 | 7 |
| GE | 314.0 | 320.66 | 0.609 | 7 |
| UBS | 38.96 | 39.45 | 0.579 | 9 |
| ALV.DE | 437.5 | 441.0 | 0.538 | 9 |
| BAS.DE | 52.86 | 53.34 | 0.521 | 9 |
| CMCSA | 23.29 | 23.685 | 0.512 | 7 |
| PH | 930.84 | 945.105 | 0.5 | 7 |
| DIS | 113.38 | 114.23 | 0.42 | 5 |
| DE | 660.39 | 665.82 | 0.307 | 7 |
| DUK | 125.87 | 126.5 | 0.283 | 7 |
| PAH3.DE | 25.6 | 25.78 | 0.276 | 9 |
| SPOT | 593.8 | 600.22 | 0.267 | 6 |
| CB | 364.86 | 366.53 | 0.251 | 7 |
| CHTR | 112.71 | 113.76 | 0.238 | 7 |
| PYPL | 57.95 | 58.195 | 0.17 | 7 |
| MUV2.DE | 569.2 | 570.4 | 0.135 | 5 |
| APH | 83.87 | 84.185 | 0.082 | 2 |
| DHL.DE | 58.92 | 59.0 | 0.076 | 7 |
| GEV | 914.88 | 918.14 | 0.062 | 6 |
| HON | 223.81 | 224.06 | 0.044 | 6 |
| WFC | 85.49 | 85.535 | 0.025 | 3 |
| WELL | 240.94 | 241.08 | 0.022 | 5 |
| SNY | 81.19 | 81.22 | 0.018 | 8 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.