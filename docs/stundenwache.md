# Stundenwache

Stand: 2026-11-05 · 272 Werte mit Stundendaten · erstellt 2026-11-06 12:52 UTC

> **Sitzung noch nicht abgeschlossen.** 59 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (9)

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
| BP | 5.516 | 5.512 | -0.021 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (20)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SHEL | 36.805 | 36.81 | 0.005 | 0 |
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

## Swing-Hoch ueberwunden (65)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.23 | 5.321 | 5 |
| APP | 264.045 | 356.36 | 5.036 | 7 |
| MCD | 247.29 | 278.09 | 4.991 | 7 |
| IBN | 1404.9 | 1571.2 | 4.866 | 7 |
| LOW | 204.52 | 227.24 | 3.52 | 7 |
| MDT | 96.89 | 104.88 | 3.12 | 7 |
| SPG | 213.63 | 226.52 | 3.08 | 7 |
| CPRT | 29.43 | 32.49 | 3.013 | 7 |
| HDB | 734.9 | 788.25 | 2.94 | 7 |
| NEE | 82.81 | 88.26 | 2.764 | 7 |
| ROP | 450.76 | 491.74 | 2.568 | 7 |
| CHTR | 112.71 | 125.85 | 2.536 | 7 |
| BRK-B | 549.0 | 572.04 | 2.429 | 7 |
| COST | 1021.45 | 1066.09 | 2.235 | 7 |
| ABT | 105.88 | 113.56 | 2.172 | 7 |
| TM | 3115.0 | 3340.0 | 2.077 | 7 |
| SBUX | 100.33 | 106.12 | 2.06 | 7 |
| CMCSA | 23.29 | 24.96 | 2.051 | 7 |
| NEM | 110.83 | 119.74 | 1.907 | 7 |
| MCK | 1016.92 | 1072.0 | 1.896 | 7 |
| DUK | 125.87 | 130.26 | 1.876 | 7 |
| WDAY | 185.82 | 200.21 | 1.875 | 7 |
| MAR | 398.42 | 417.47 | 1.78 | 7 |
| WMT | 122.4 | 127.69 | 1.776 | 7 |
| SYK | 312.8 | 335.02 | 1.729 | 7 |
| SHL.DE | 42.06 | 43.72 | 1.641 | 5 |
| DIS | 113.38 | 117.22 | 1.639 | 7 |
| MA | 633.29 | 655.44 | 1.457 | 7 |
| DXCM | 79.86 | 84.49 | 1.437 | 7 |
| SCHW | 89.96 | 92.575 | 1.311 | 7 |
| MMM | 180.11 | 187.67 | 1.27 | 7 |
| VRSK | 201.65 | 211.71 | 1.221 | 7 |
| FDX | 307.94 | 316.89 | 1.016 | 7 |
| CB | 364.86 | 371.63 | 0.98 | 7 |
| HD | 341.54 | 349.89 | 0.867 | 7 |
| V | 414.6 | 422.34 | 0.836 | 7 |
| BABA | 101.6 | 104.9 | 0.813 | 7 |
| ADP | 300.54 | 307.23 | 0.807 | 7 |
| SPOT | 593.8 | 614.44 | 0.806 | 7 |
| WELL | 240.94 | 245.38 | 0.668 | 7 |
| VZ | 45.29 | 46.155 | 0.664 | 7 |
| ADSK | 263.16 | 269.3 | 0.663 | 7 |
| PEP | 140.66 | 142.8 | 0.64 | 7 |
| AMT | 190.0 | 193.99 | 0.634 | 7 |
| BKNG | 164.73 | 168.82 | 0.618 | 7 |
| ISRG | 458.88 | 468.57 | 0.561 | 7 |
| UBS | 38.96 | 39.52 | 0.525 | 5 |
| AMZN | 255.36 | 260.51 | 0.498 | 7 |
| CL | 97.5 | 98.645 | 0.462 | 7 |
| CCEP | 116.01 | 117.32 | 0.449 | 7 |
| BIIB | 240.99 | 244.11 | 0.355 | 7 |
| PDD | 83.15 | 84.0 | 0.351 | 6 |
| T | 21.59 | 21.82 | 0.311 | 7 |
| UPS | 110.16 | 111.025 | 0.308 | 7 |
| SONY | 4068.0 | 4107.0 | 0.289 | 7 |
| SHW | 346.19 | 348.93 | 0.222 | 7 |
| MDLZ | 66.49 | 66.845 | 0.218 | 7 |
| TMUS | 159.41 | 160.77 | 0.218 | 7 |
| TTWO | 212.16 | 213.35 | 0.182 | 3 |
| ACN | 263.66 | 265.24 | 0.134 | 7 |
| KHC | 25.23 | 25.325 | 0.128 | 4 |
| DB1.DE | 321.5 | 322.1 | 0.086 | 3 |
| CTSH | 66.33 | 66.55 | 0.074 | 7 |
| PG | 166.85 | 167.08 | 0.064 | 6 |
| PAYX | 119.47 | 119.53 | 0.016 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.