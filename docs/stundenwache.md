# Stundenwache

Stand: 2026-11-03 · 272 Werte mit Stundendaten · erstellt 2026-11-04 12:54 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (17)

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
| ADP | 292.29 | 295.96 | 0.457 | 0 |
| RHM.DE | 970.2 | 988.5 | 0.484 | 0 |
| NKE | 37.94 | 38.48 | 0.498 | 0 |
| BHP | 54.68 | 55.56 | 0.638 | 0 |
| GD | 368.36 | 374.34 | 0.795 | 0 |
| TTD | 12.375 | 12.865 | 0.839 | 0 |
| NVS | 130.84 | 133.28 | 0.942 | 0 |

## Swing-Hoch ueberwunden (66)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| REGN | 825.52 | 974.25 | 5.132 | 7 |
| BAYN.DE | 45.83 | 53.7 | 4.835 | 5 |
| QIA.DE | 42.345 | 45.09 | 4.461 | 5 |
| HEI.DE | 150.0 | 170.45 | 4.155 | 5 |
| IDXX | 571.75 | 672.2 | 4.119 | 7 |
| GEHC | 72.3 | 80.63 | 3.613 | 7 |
| DBK.DE | 28.815 | 32.18 | 3.39 | 5 |
| AZN | 128.06 | 138.6697 | 3.361 | 5 |
| NVO | 264.75 | 284.7 | 3.335 | 5 |
| MCD | 247.29 | 263.09 | 3.058 | 7 |
| RTX | 187.41 | 203.83 | 3.012 | 7 |
| ADS.DE | 161.15 | 174.0 | 2.89 | 5 |
| SHL.DE | 42.06 | 44.24 | 2.645 | 5 |
| HNR1.DE | 283.2 | 294.8 | 2.636 | 5 |
| FRE.DE | 47.295 | 49.505 | 2.504 | 5 |
| UBS | 38.96 | 40.97 | 2.214 | 5 |
| SPG | 213.63 | 222.08 | 2.189 | 7 |
| ALV.DE | 437.5 | 452.1 | 2.186 | 5 |
| HEN3.DE | 79.44 | 81.96 | 1.879 | 5 |
| SBUX | 100.33 | 104.74 | 1.812 | 7 |
| CPRT | 29.43 | 31.06 | 1.714 | 7 |
| MAR | 398.42 | 416.245 | 1.658 | 7 |
| WDAY | 185.82 | 197.93 | 1.557 | 7 |
| LOW | 204.52 | 213.23 | 1.538 | 7 |
| ROP | 450.76 | 473.39 | 1.502 | 7 |
| CBK.DE | 38.69 | 40.12 | 1.459 | 5 |
| BAS.DE | 52.86 | 54.18 | 1.452 | 5 |
| FDX | 307.94 | 318.02 | 1.285 | 7 |
| ABT | 105.88 | 109.41 | 1.164 | 7 |
| CON.DE | 68.2 | 70.14 | 1.107 | 5 |
| DXCM | 79.86 | 82.98 | 1.101 | 7 |
| MA | 633.29 | 647.31 | 1.067 | 7 |
| BRK-B | 549.0 | 557.135 | 1.045 | 7 |
| DHL.DE | 58.92 | 59.98 | 1.007 | 5 |
| BIIB | 240.99 | 249.09 | 0.987 | 7 |
| SNY | 81.19 | 82.86 | 0.984 | 5 |
| MDT | 96.89 | 98.88 | 0.909 | 7 |
| NEE | 82.81 | 84.33 | 0.909 | 7 |
| WMT | 122.4 | 124.81 | 0.888 | 7 |
| MUV2.DE | 569.2 | 576.6 | 0.86 | 3 |
| SAN | 10.434 | 10.762 | 0.854 | 5 |
| GM | 85.79 | 88.33 | 0.851 | 7 |
| PAH3.DE | 25.6 | 26.11 | 0.762 | 5 |
| V | 414.6 | 420.38 | 0.737 | 7 |
| IBN | 1404.9 | 1424.1 | 0.673 | 7 |
| NXPI | 255.31 | 262.97 | 0.647 | 7 |
| GE | 314.0 | 320.66 | 0.609 | 7 |
| CMCSA | 23.29 | 23.685 | 0.512 | 7 |
| DTE.DE | 26.17 | 26.46 | 0.506 | 2 |
| PH | 930.84 | 945.105 | 0.5 | 7 |
| DIS | 113.38 | 114.24 | 0.425 | 5 |
| DE | 660.39 | 665.82 | 0.307 | 7 |
| DUK | 125.87 | 126.5 | 0.283 | 7 |
| SPOT | 593.8 | 600.22 | 0.267 | 6 |
| CB | 364.86 | 366.53 | 0.251 | 7 |
| CHTR | 112.71 | 113.76 | 0.238 | 7 |
| HSBC | 13.086 | 13.154 | 0.197 | 3 |
| PYPL | 57.95 | 58.195 | 0.17 | 7 |
| HDB | 734.9 | 736.7 | 0.114 | 4 |
| VNA.DE | 16.89 | 16.94 | 0.102 | 2 |
| BMW.DE | 58.52 | 58.66 | 0.095 | 1 |
| APH | 83.87 | 84.185 | 0.082 | 2 |
| GEV | 914.88 | 918.14 | 0.062 | 6 |
| HON | 223.81 | 224.06 | 0.044 | 6 |
| WFC | 85.49 | 85.535 | 0.025 | 3 |
| WELL | 240.94 | 241.08 | 0.022 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.