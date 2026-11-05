# Stundenwache

Stand: 2026-11-04 · 272 Werte mit Stundendaten · erstellt 2026-11-05 02:28 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 4, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (3)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| IFX.DE | 50.18 | 50.65 | 0.181 | 1 |
| COF | 202.06 | 206.27 | 0.708 | 1 |
| DTG.DE | 39.88 | 41.03 | 1.339 | 1 |

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ETN | 350.05 | 352.79 | 0.143 | 0 |
| DELL | 366.62 | 372.21 | 0.179 | 0 |
| ENB | 48.45 | 48.775 | 0.48 | 0 |
| MCHP | 73.55 | 75.47 | 0.526 | 0 |
| ADI | 396.76 | 406.41 | 0.546 | 0 |
| MPC | 379.1 | 392.67 | 0.629 | 0 |
| ON | 68.61 | 71.27 | 0.687 | 0 |
| VLO | 347.25 | 365.35 | 0.896 | 0 |
| NVS | 130.84 | 134.08 | 1.224 | 0 |
| DB1.DE | 309.8 | 318.1 | 1.269 | 0 |
| PLD | 126.83 | 131.38 | 1.865 | 0 |
| ZAL.DE | 25.08 | 27.48 | 2.272 | 0 |

## Swing-Hoch ueberwunden (132)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MCD | 247.29 | 280.345 | 5.557 | 7 |
| GEHC | 72.3 | 85.79 | 5.152 | 7 |
| IDXX | 571.75 | 699.21 | 4.898 | 7 |
| BAYN.DE | 45.83 | 53.94 | 4.896 | 9 |
| QIA.DE | 42.345 | 45.23 | 4.677 | 9 |
| HEI.DE | 150.0 | 171.85 | 4.305 | 9 |
| FRE.DE | 47.295 | 51.64 | 4.135 | 9 |
| LOW | 204.52 | 229.49 | 4.063 | 7 |
| SPG | 213.63 | 228.56 | 3.777 | 7 |
| AZN | 128.06 | 140.32 | 3.73 | 9 |
| SBUX | 100.33 | 109.68 | 3.701 | 7 |
| DBK.DE | 28.815 | 32.42 | 3.56 | 9 |
| BRK-B | 549.0 | 579.665 | 3.447 | 7 |
| NVO | 264.75 | 285.2 | 3.419 | 8 |
| REGN | 825.52 | 930.77 | 3.357 | 7 |
| CPRT | 29.43 | 32.61 | 3.278 | 7 |
| HNR1.DE | 283.2 | 298.6 | 3.277 | 9 |
| MDT | 96.89 | 105.03 | 3.237 | 7 |
| SHL.DE | 42.06 | 44.78 | 3.126 | 9 |
| ADS.DE | 161.15 | 175.3 | 3.067 | 9 |
| ALV.DE | 437.5 | 459.6 | 3.041 | 9 |
| NEE | 82.81 | 88.4399 | 2.964 | 7 |
| DXCM | 79.86 | 88.465 | 2.92 | 7 |
| ABT | 105.88 | 115.55 | 2.894 | 7 |
| MA | 633.29 | 672.69 | 2.846 | 7 |
| V | 414.6 | 436.66 | 2.701 | 7 |
| ROP | 450.76 | 492.21 | 2.647 | 7 |
| FDX | 307.94 | 329.5 | 2.621 | 7 |
| MAR | 398.42 | 424.76 | 2.557 | 7 |
| UBS | 38.96 | 41.25 | 2.483 | 9 |
| MMM | 180.11 | 193.99 | 2.481 | 7 |
| DIS | 113.38 | 118.95 | 2.472 | 7 |
| WMT | 122.4 | 129.23 | 2.46 | 7 |
| SYK | 312.8 | 339.78 | 2.266 | 7 |
| HEN3.DE | 79.44 | 82.48 | 2.196 | 9 |
| WDAY | 185.82 | 201.81 | 2.069 | 7 |
| GM | 85.79 | 92.41 | 2.026 | 7 |
| CMCSA | 23.29 | 24.86 | 1.966 | 7 |
| MCK | 1016.92 | 1067.03 | 1.891 | 6 |
| BAS.DE | 52.86 | 54.57 | 1.819 | 9 |
| SCHW | 89.96 | 93.37 | 1.786 | 7 |
| MUV2.DE | 569.2 | 584.8 | 1.685 | 7 |
| BIIB | 240.99 | 254.52 | 1.638 | 7 |
| NEM | 110.83 | 118.15 | 1.634 | 7 |
| DUK | 125.87 | 129.61 | 1.632 | 7 |
| CHTR | 112.71 | 120.25 | 1.597 | 7 |
| DHL.DE | 58.92 | 60.7 | 1.597 | 9 |
| BMW.DE | 58.52 | 61.08 | 1.591 | 5 |
| BLK | 1179.84 | 1224.515 | 1.548 | 7 |
| HD | 341.54 | 355.52 | 1.543 | 7 |
| UPS | 110.16 | 114.31 | 1.532 | 7 |
| SNY | 81.19 | 83.88 | 1.517 | 9 |
| ROST | 235.71 | 245.755 | 1.514 | 7 |
| SHW | 346.19 | 363.51 | 1.511 | 7 |
| CON.DE | 68.2 | 70.78 | 1.465 | 9 |
| PYPL | 57.95 | 60.16 | 1.461 | 7 |
| ISRG | 458.88 | 482.17 | 1.435 | 7 |
| CB | 364.86 | 374.18 | 1.402 | 7 |
| SPOT | 593.8 | 627.76 | 1.365 | 7 |
| COST | 1021.45 | 1046.59 | 1.355 | 7 |
| GE | 314.0 | 329.49 | 1.348 | 7 |
| TM | 3115.0 | 3210.0 | 1.237 | 3 |
| BABA | 101.6 | 106.3 | 1.217 | 1 |
| CBK.DE | 38.69 | 39.86 | 1.173 | 9 |
| AMZN | 255.36 | 266.14 | 1.154 | 7 |
| MS | 188.3 | 193.99 | 1.09 | 7 |
| WELL | 240.94 | 248.01 | 1.081 | 7 |
| PAH3.DE | 25.6 | 26.33 | 1.074 | 9 |
| DTE.DE | 26.17 | 26.81 | 1.062 | 6 |
| WFC | 85.49 | 87.435 | 1.061 | 7 |
| SONY | 4068.0 | 4192.0 | 1.025 | 3 |
| BKNG | 164.73 | 170.98 | 0.991 | 7 |
| MSFT | 541.29 | 556.03 | 0.981 | 7 |
| JPM | 345.75 | 352.19 | 0.956 | 6 |
| BNY | 150.28 | 152.69 | 0.869 | 6 |
| NKE | 39.57 | 40.485 | 0.834 | 7 |
| NXPI | 255.31 | 265.09 | 0.826 | 7 |
| AXP | 326.49 | 332.68 | 0.815 | 7 |
| AMT | 190.0 | 194.9 | 0.766 | 7 |
| HON | 223.81 | 228.42 | 0.76 | 7 |
| SAN | 10.434 | 10.726 | 0.75 | 9 |
| ADSK | 263.16 | 270.09 | 0.744 | 7 |
| VZ | 45.29 | 46.185 | 0.697 | 7 |
| IBN | 1404.9 | 1424.1 | 0.674 | 7 |
| APP | 264.045 | 271.34 | 0.569 | 7 |
| ADP | 300.54 | 305.035 | 0.556 | 5 |
| PEP | 140.66 | 142.52 | 0.556 | 7 |
| MDLZ | 66.49 | 67.365 | 0.555 | 6 |
| TRV | 404.44 | 409.31 | 0.542 | 6 |
| PFE | 30.44 | 30.79 | 0.539 | 6 |
| MBG.DE | 41.795 | 42.45 | 0.539 | 4 |
| CL | 97.5 | 98.75 | 0.524 | 7 |
| RY | 208.19 | 209.77 | 0.491 | 5 |
| GS | 916.95 | 928.2 | 0.452 | 6 |
| PLD | 130.29 | 131.38 | 0.447 | 2 |
| CDW | 165.42 | 168.82 | 0.438 | 5 |
| BEI.DE | 85.04 | 85.9 | 0.429 | 3 |
| USB | 60.49 | 61.04 | 0.426 | 6 |
| CTAS | 226.69 | 229.07 | 0.425 | 7 |
| SPGI | 477.32 | 481.68 | 0.359 | 7 |
| T | 21.59 | 21.84 | 0.341 | 7 |
| MELI | 1728.47 | 1751.15 | 0.337 | 7 |
| UL | 49.355 | 49.755 | 0.334 | 2 |
| KHC | 25.23 | 25.46 | 0.315 | 7 |
| HSBC | 13.086 | 13.196 | 0.314 | 7 |
| ZAL.DE | 27.19 | 27.48 | 0.275 | 3 |
| SY1.DE | 95.12 | 95.82 | 0.252 | 2 |
| MNST | 48.47 | 48.75 | 0.249 | 6 |
| FAST | 52.91 | 53.2 | 0.246 | 6 |
| AIR.DE | 199.08 | 200.4 | 0.239 | 4 |
| AMGN | 475.65 | 478.38 | 0.236 | 5 |
| LIN | 522.93 | 524.78 | 0.207 | 6 |
| BNS | 96.17 | 96.46 | 0.195 | 5 |
| GOOGL | 287.0 | 289.03 | 0.19 | 7 |
| VNA.DE | 16.89 | 16.985 | 0.19 | 6 |
| MRNA | 254.48 | 258.31 | 0.163 | 1 |
| PG | 166.85 | 167.34 | 0.139 | 6 |
| SIE.DE | 274.65 | 275.7 | 0.139 | 5 |
| DASH | 197.24 | 198.63 | 0.138 | 6 |
| TJX | 144.25 | 144.7 | 0.138 | 6 |
| HDB | 734.9 | 736.7 | 0.115 | 4 |
| VOW3.DE | 71.08 | 71.32 | 0.113 | 4 |
| C | 124.44 | 124.75 | 0.102 | 5 |
| TTD | 13.17 | 13.2261 | 0.099 | 7 |
| TD | 127.96 | 128.16 | 0.099 | 4 |
| BMY | 64.05 | 64.21 | 0.093 | 1 |
| SAP.DE | 214.4 | 214.9 | 0.08 | 3 |
| LULU | 111.76 | 112.09 | 0.074 | 7 |
| UNP | 307.89 | 308.36 | 0.072 | 3 |
| ACN | 263.66 | 264.44 | 0.066 | 6 |
| BMO | 177.25 | 177.435 | 0.056 | 3 |
| CM | 119.73 | 119.86 | 0.055 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.