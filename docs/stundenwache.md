# Stundenwache

Stand: 2026-11-04 · 272 Werte mit Stundendaten · erstellt 2026-11-05 13:04 UTC

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
| COF | 202.06 | 206.27 | 0.708 | 1 |

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ETN | 350.05 | 352.79 | 0.143 | 0 |
| DELL | 366.62 | 372.21 | 0.179 | 0 |
| ENB | 48.45 | 48.775 | 0.48 | 0 |
| MCHP | 73.55 | 75.47 | 0.526 | 0 |
| ADI | 396.76 | 406.435 | 0.548 | 0 |
| MPC | 379.1 | 392.67 | 0.629 | 0 |
| ON | 68.61 | 71.27 | 0.687 | 0 |
| VLO | 347.25 | 365.35 | 0.896 | 0 |
| PLD | 126.83 | 131.38 | 1.865 | 0 |

## Swing-Hoch ueberwunden (139)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| BAYN.DE | 45.83 | 55.7 | 5.833 | 5 |
| MCD | 247.29 | 280.345 | 5.557 | 7 |
| GEHC | 72.3 | 85.79 | 5.152 | 7 |
| HEI.DE | 150.0 | 177.7 | 5.147 | 5 |
| QIA.DE | 42.345 | 45.245 | 5.034 | 5 |
| IDXX | 571.75 | 699.88 | 4.924 | 7 |
| DBK.DE | 28.815 | 33.63 | 4.561 | 5 |
| FRE.DE | 47.295 | 51.69 | 4.27 | 5 |
| HNR1.DE | 283.2 | 303.2 | 4.192 | 5 |
| ADS.DE | 161.15 | 181.05 | 4.1 | 5 |
| LOW | 204.52 | 229.49 | 4.063 | 7 |
| TM | 3115.0 | 3497.0 | 4.038 | 7 |
| AZN | 128.06 | 141.12 | 3.944 | 5 |
| ALV.DE | 437.5 | 465.9 | 3.83 | 5 |
| SPG | 213.63 | 228.56 | 3.777 | 7 |
| SBUX | 100.33 | 109.68 | 3.701 | 7 |
| BRK-B | 549.0 | 579.665 | 3.447 | 7 |
| REGN | 825.52 | 930.77 | 3.357 | 7 |
| CPRT | 29.43 | 32.62 | 3.289 | 7 |
| MDT | 96.89 | 105.03 | 3.237 | 7 |
| IBN | 1404.9 | 1500.0 | 3.125 | 7 |
| NEE | 82.81 | 88.4399 | 2.964 | 7 |
| BAS.DE | 52.86 | 55.73 | 2.933 | 5 |
| DXCM | 79.86 | 88.465 | 2.92 | 7 |
| ABT | 105.88 | 115.55 | 2.894 | 7 |
| HEN3.DE | 79.44 | 83.36 | 2.87 | 5 |
| MA | 633.29 | 672.69 | 2.846 | 7 |
| V | 414.6 | 436.66 | 2.701 | 7 |
| MUV2.DE | 569.2 | 594.6 | 2.698 | 5 |
| ROP | 450.76 | 492.21 | 2.647 | 7 |
| FDX | 307.94 | 329.5 | 2.621 | 7 |
| MAR | 398.42 | 424.76 | 2.557 | 7 |
| MMM | 180.11 | 193.99 | 2.481 | 7 |
| WMT | 122.4 | 129.23 | 2.46 | 7 |
| DIS | 113.38 | 118.92 | 2.459 | 7 |
| UBS | 38.96 | 41.14 | 2.351 | 5 |
| SYK | 312.8 | 339.78 | 2.266 | 7 |
| SHL.DE | 42.06 | 44.13 | 2.163 | 5 |
| WDAY | 185.82 | 201.81 | 2.069 | 7 |
| GM | 85.79 | 92.41 | 2.026 | 7 |
| CMCSA | 23.29 | 24.86 | 1.966 | 7 |
| SNY | 81.19 | 84.62 | 1.906 | 5 |
| MCK | 1016.92 | 1067.03 | 1.891 | 6 |
| BABA | 101.6 | 109.1 | 1.87 | 7 |
| SCHW | 89.96 | 93.37 | 1.786 | 7 |
| BIIB | 240.99 | 254.53 | 1.639 | 7 |
| NEM | 110.83 | 118.15 | 1.634 | 7 |
| DUK | 125.87 | 129.61 | 1.632 | 7 |
| CON.DE | 68.2 | 71.08 | 1.608 | 5 |
| BMW.DE | 58.52 | 61.12 | 1.604 | 5 |
| CHTR | 112.71 | 120.25 | 1.597 | 7 |
| DHL.DE | 58.92 | 60.74 | 1.575 | 5 |
| BLK | 1179.84 | 1224.515 | 1.548 | 7 |
| HD | 341.54 | 355.52 | 1.543 | 7 |
| UPS | 110.16 | 114.31 | 1.532 | 7 |
| NVO | 264.75 | 274.6 | 1.526 | 6 |
| HDB | 734.9 | 760.0 | 1.525 | 7 |
| ROST | 235.71 | 245.755 | 1.514 | 7 |
| SHW | 346.19 | 363.54 | 1.514 | 7 |
| PYPL | 57.95 | 60.16 | 1.461 | 7 |
| ISRG | 458.88 | 482.17 | 1.435 | 7 |
| ZAL.DE | 27.19 | 28.78 | 1.435 | 5 |
| CB | 364.86 | 374.18 | 1.402 | 7 |
| SAN | 10.434 | 10.988 | 1.376 | 5 |
| SPOT | 593.8 | 627.76 | 1.365 | 7 |
| COST | 1021.45 | 1046.58 | 1.354 | 7 |
| GE | 314.0 | 329.5 | 1.349 | 7 |
| SONY | 4068.0 | 4220.0 | 1.257 | 7 |
| PAH3.DE | 25.6 | 26.43 | 1.224 | 5 |
| AMZN | 255.36 | 266.14 | 1.154 | 7 |
| MS | 188.3 | 193.99 | 1.09 | 7 |
| WELL | 240.94 | 248.01 | 1.081 | 7 |
| WFC | 85.49 | 87.435 | 1.061 | 7 |
| BKNG | 164.73 | 170.98 | 0.991 | 7 |
| MSFT | 541.29 | 556.03 | 0.981 | 7 |
| JPM | 345.75 | 352.19 | 0.956 | 6 |
| BNY | 150.28 | 152.69 | 0.869 | 6 |
| DTG.DE | 41.03 | 41.78 | 0.837 | 5 |
| NKE | 39.57 | 40.485 | 0.834 | 7 |
| NXPI | 255.31 | 265.09 | 0.826 | 7 |
| MBG.DE | 41.795 | 42.795 | 0.817 | 5 |
| AXP | 326.49 | 332.68 | 0.815 | 7 |
| AMT | 190.0 | 194.9 | 0.766 | 7 |
| HON | 223.81 | 228.42 | 0.76 | 7 |
| SAP.DE | 214.4 | 219.1 | 0.754 | 5 |
| HSBC | 13.086 | 13.352 | 0.75 | 5 |
| ADSK | 263.16 | 270.09 | 0.744 | 7 |
| DB1.DE | 321.5 | 326.2 | 0.698 | 5 |
| SY1.DE | 95.12 | 97.08 | 0.698 | 5 |
| VZ | 45.29 | 46.185 | 0.697 | 7 |
| VNA.DE | 16.89 | 17.22 | 0.642 | 5 |
| VOW3.DE | 71.08 | 72.32 | 0.582 | 5 |
| APP | 264.045 | 271.3 | 0.566 | 7 |
| PEP | 140.66 | 142.52 | 0.556 | 7 |
| MDLZ | 66.49 | 67.365 | 0.555 | 6 |
| AIR.DE | 199.08 | 202.05 | 0.549 | 5 |
| TRV | 404.44 | 409.31 | 0.542 | 6 |
| PFE | 30.44 | 30.79 | 0.539 | 6 |
| CL | 97.5 | 98.75 | 0.524 | 7 |
| RY | 208.19 | 209.77 | 0.491 | 5 |
| RIO | 62.3 | 63.1 | 0.482 | 5 |
| GS | 916.95 | 928.2 | 0.452 | 6 |
| PLD | 130.29 | 131.38 | 0.447 | 2 |
| CDW | 165.42 | 168.82 | 0.438 | 5 |
| USB | 60.49 | 61.04 | 0.426 | 6 |
| CTAS | 226.69 | 229.07 | 0.425 | 7 |
| ADP | 300.54 | 303.51 | 0.368 | 7 |
| SPGI | 477.32 | 481.68 | 0.359 | 7 |
| EOAN.DE | 19.12 | 19.25 | 0.351 | 4 |
| T | 21.59 | 21.84 | 0.341 | 7 |
| BBVA | 22.84 | 23.09 | 0.339 | 5 |
| MELI | 1728.47 | 1751.15 | 0.337 | 7 |
| KHC | 25.23 | 25.46 | 0.315 | 7 |
| MNST | 48.47 | 48.75 | 0.249 | 6 |
| FAST | 52.91 | 53.2 | 0.246 | 6 |
| AMGN | 475.65 | 478.38 | 0.236 | 5 |
| UL | 49.355 | 49.62 | 0.219 | 5 |
| LIN | 522.93 | 524.78 | 0.207 | 6 |
| BNR.DE | 63.64 | 63.88 | 0.2 | 5 |
| BNS | 96.17 | 96.46 | 0.195 | 5 |
| GOOGL | 287.0 | 288.99 | 0.187 | 7 |
| MRNA | 254.48 | 258.31 | 0.163 | 1 |
| CBK.DE | 38.69 | 38.86 | 0.162 | 5 |
| TJX | 144.25 | 144.74 | 0.15 | 6 |
| PG | 166.85 | 167.36 | 0.145 | 6 |
| DASH | 197.24 | 198.63 | 0.138 | 6 |
| BTI | 46.5 | 46.6 | 0.118 | 4 |
| P911.DE | 47.08 | 47.21 | 0.103 | 3 |
| C | 124.44 | 124.75 | 0.102 | 5 |
| TD | 127.96 | 128.16 | 0.099 | 4 |
| TTD | 13.17 | 13.225 | 0.097 | 7 |
| BMY | 64.05 | 64.21 | 0.093 | 1 |
| LULU | 111.76 | 112.09 | 0.074 | 7 |
| UNP | 307.89 | 308.36 | 0.072 | 3 |
| ACN | 263.66 | 264.44 | 0.066 | 6 |
| BMO | 177.25 | 177.435 | 0.056 | 3 |
| CM | 119.73 | 119.86 | 0.055 | 3 |
| BEI.DE | 85.04 | 85.08 | 0.019 | 2 |
| ING | 29.5 | 29.505 | 0.006 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.