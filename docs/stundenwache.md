# Stundenwache

Stand: 2026-11-05 · 272 Werte mit Stundendaten · erstellt 2026-11-06 02:26 UTC

> **Sitzung noch nicht abgeschlossen.** 11 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 4, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (8)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AXON | 409.4 | 383.47 | -1.299 | 5 |
| BNS | 93.28 | 91.76 | -0.865 | 3 |
| GS | 892.1 | 868.25 | -0.845 | 7 |
| C | 121.43 | 118.47 | -0.845 | 7 |
| LLY | 1382.02 | 1367.6899 | -0.28 | 2 |
| TD | 123.75 | 123.12 | -0.271 | 1 |
| MS | 183.91 | 182.44 | -0.241 | 6 |
| DHR | 227.2 | 226.46 | -0.098 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (19)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AMGN | 460.15 | 460.42 | 0.021 | 0 |
| TXN | 277.87 | 278.14 | 0.021 | 0 |
| CM | 115.58 | 115.64 | 0.023 | 0 |
| CNQ | 48.85 | 48.9 | 0.031 | 0 |
| FANG | 179.35 | 179.63 | 0.04 | 0 |
| BKR | 46.09 | 46.2 | 0.047 | 0 |
| ON | 62.76 | 62.97 | 0.05 | 0 |
| FTNT | 121.86 | 122.5 | 0.065 | 0 |
| ENB | 48.04 | 48.09 | 0.072 | 0 |
| ODFL | 169.89 | 170.52 | 0.088 | 0 |
| KLAC | 128.17 | 129.63 | 0.161 | 0 |
| TEAM | 180.813 | 182.46 | 0.168 | 0 |
| MSFT | 532.68 | 535.66 | 0.193 | 0 |
| COF | 202.06 | 203.92 | 0.289 | 0 |
| NKE | 39.08 | 39.56 | 0.415 | 0 |
| INTU | 348.22 | 354.97 | 0.473 | 0 |
| UNP | 294.48 | 297.94 | 0.483 | 0 |
| MSTR | 123.9 | 129.5 | 0.573 | 0 |
| VRSK | 194.12 | 211.71 | 2.135 | 0 |

## Swing-Hoch ueberwunden (97)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| BAYN.DE | 45.83 | 56.28 | 6.003 | 9 |
| APP | 264.045 | 356.36 | 5.036 | 7 |
| QIA.DE | 42.345 | 45.26 | 5.035 | 9 |
| MCD | 247.29 | 278.09 | 4.991 | 7 |
| HEI.DE | 150.0 | 175.45 | 4.716 | 9 |
| HNR1.DE | 283.2 | 305.6 | 4.32 | 9 |
| FRE.DE | 47.295 | 51.77 | 4.3 | 9 |
| AZN | 128.06 | 141.08 | 3.905 | 9 |
| ADS.DE | 161.15 | 179.55 | 3.783 | 9 |
| ALV.DE | 437.5 | 465.3 | 3.637 | 9 |
| LOW | 204.52 | 227.24 | 3.52 | 7 |
| DBK.DE | 28.815 | 32.505 | 3.318 | 9 |
| SHL.DE | 42.06 | 45.16 | 3.194 | 9 |
| HEN3.DE | 79.44 | 83.9 | 3.131 | 9 |
| IBN | 1404.9 | 1500.0 | 3.128 | 7 |
| BAS.DE | 52.86 | 56.11 | 3.125 | 9 |
| MDT | 96.89 | 104.88 | 3.12 | 7 |
| SPG | 213.63 | 226.52 | 3.08 | 7 |
| CPRT | 29.43 | 32.49 | 3.013 | 7 |
| NEE | 82.81 | 88.26 | 2.764 | 7 |
| MUV2.DE | 569.2 | 596.0 | 2.684 | 9 |
| ROP | 450.76 | 491.74 | 2.568 | 7 |
| CHTR | 112.71 | 125.85 | 2.536 | 7 |
| BRK-B | 549.0 | 572.04 | 2.429 | 7 |
| TM | 3115.0 | 3361.0 | 2.394 | 3 |
| COST | 1021.45 | 1066.09 | 2.235 | 7 |
| ABT | 105.88 | 113.56 | 2.172 | 7 |
| SBUX | 100.33 | 106.12 | 2.06 | 7 |
| CMCSA | 23.29 | 24.96 | 2.051 | 7 |
| SNY | 81.19 | 84.69 | 1.916 | 9 |
| NEM | 110.83 | 119.74 | 1.907 | 7 |
| MCK | 1016.92 | 1072.0 | 1.896 | 7 |
| DUK | 125.87 | 130.26 | 1.876 | 7 |
| WDAY | 185.82 | 200.21 | 1.875 | 7 |
| MAR | 398.42 | 417.47 | 1.78 | 7 |
| WMT | 122.4 | 127.69 | 1.776 | 7 |
| SYK | 312.8 | 335.02 | 1.729 | 7 |
| BMW.DE | 58.52 | 61.18 | 1.641 | 9 |
| DIS | 113.38 | 117.22 | 1.639 | 7 |
| HDB | 734.9 | 760.0 | 1.525 | 7 |
| MA | 633.29 | 655.44 | 1.457 | 7 |
| DXCM | 79.86 | 84.49 | 1.437 | 7 |
| PAH3.DE | 25.6 | 26.54 | 1.387 | 9 |
| SCHW | 89.96 | 92.575 | 1.311 | 7 |
| ZAL.DE | 27.19 | 28.63 | 1.299 | 9 |
| DHL.DE | 58.92 | 60.44 | 1.274 | 9 |
| MMM | 180.11 | 187.67 | 1.27 | 7 |
| VRSK | 201.65 | 211.71 | 1.221 | 7 |
| CON.DE | 68.2 | 70.32 | 1.156 | 9 |
| BABA | 101.6 | 105.7 | 1.017 | 1 |
| FDX | 307.94 | 316.89 | 1.016 | 7 |
| CB | 364.86 | 371.63 | 0.98 | 7 |
| SONY | 4068.0 | 4191.0 | 0.947 | 3 |
| SY1.DE | 95.12 | 97.72 | 0.911 | 9 |
| HD | 341.54 | 349.89 | 0.867 | 7 |
| SAN | 10.434 | 10.784 | 0.857 | 9 |
| V | 414.6 | 422.34 | 0.836 | 7 |
| MBG.DE | 41.795 | 42.805 | 0.825 | 9 |
| DB1.DE | 321.5 | 327.2 | 0.822 | 9 |
| DTG.DE | 41.03 | 41.76 | 0.814 | 9 |
| SPOT | 593.8 | 614.44 | 0.806 | 7 |
| UL | 49.355 | 50.29 | 0.751 | 9 |
| BTI | 46.5 | 47.17 | 0.741 | 8 |
| UBS | 38.96 | 39.73 | 0.731 | 9 |
| WELL | 240.94 | 245.38 | 0.668 | 7 |
| VZ | 45.29 | 46.155 | 0.664 | 7 |
| ADSK | 263.16 | 269.3 | 0.663 | 7 |
| EOAN.DE | 19.12 | 19.37 | 0.649 | 8 |
| PEP | 140.66 | 142.8 | 0.64 | 7 |
| AMT | 190.0 | 193.99 | 0.634 | 7 |
| BKNG | 164.73 | 168.82 | 0.618 | 7 |
| ADP | 300.54 | 305.23 | 0.566 | 6 |
| ISRG | 458.88 | 468.57 | 0.561 | 7 |
| VNA.DE | 16.89 | 17.15 | 0.506 | 9 |
| AMZN | 255.36 | 260.51 | 0.498 | 7 |
| CL | 97.5 | 98.645 | 0.462 | 7 |
| CCEP | 116.01 | 117.32 | 0.449 | 7 |
| VOW3.DE | 71.08 | 71.96 | 0.413 | 9 |
| SAP.DE | 214.4 | 216.75 | 0.377 | 9 |
| BEI.DE | 85.04 | 85.82 | 0.364 | 6 |
| BIIB | 240.99 | 244.11 | 0.355 | 7 |
| PDD | 83.15 | 84.0 | 0.351 | 6 |
| T | 21.59 | 21.82 | 0.311 | 7 |
| UPS | 110.16 | 111.025 | 0.308 | 7 |
| BNR.DE | 63.64 | 63.98 | 0.283 | 9 |
| SHW | 346.19 | 348.93 | 0.222 | 7 |
| MDLZ | 66.49 | 66.845 | 0.218 | 7 |
| TMUS | 159.41 | 160.77 | 0.218 | 7 |
| RIO | 62.3 | 62.61 | 0.187 | 8 |
| TTWO | 212.16 | 213.35 | 0.182 | 3 |
| DTE.DE | 26.17 | 26.26 | 0.142 | 4 |
| ACN | 263.66 | 265.24 | 0.134 | 7 |
| KHC | 25.23 | 25.325 | 0.128 | 4 |
| P911.DE | 47.08 | 47.18 | 0.079 | 7 |
| CTSH | 66.33 | 66.55 | 0.074 | 7 |
| PG | 166.85 | 167.08 | 0.064 | 6 |
| PAYX | 119.47 | 119.53 | 0.016 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.