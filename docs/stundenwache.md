# Stundenwache

Stand: 2026-09-02 · 158 Werte mit Stundendaten · erstellt 2026-09-03 00:16 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (33)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MDB | 430.525 | 375.29 | -2.468 | 7 |
| PLTR | 179.75 | 169.46 | -1.514 | 7 |
| ODFL | 196.41 | 187.61 | -1.432 | 7 |
| DTG.DE | 46.17 | 45.17 | -1.233 | 9 |
| DB1.DE | 283.8 | 278.4 | -1.17 | 9 |
| DDOG | 223.02 | 209.22 | -1.108 | 7 |
| SIE.DE | 277.85 | 274.2 | -0.738 | 9 |
| CRWD | 212.65 | 203.42 | -0.694 | 7 |
| HON | 208.81 | 206.125 | -0.58 | 6 |
| FAST | 48.53 | 47.96 | -0.571 | 7 |
| ADSK | 247.35 | 241.73 | -0.543 | 7 |
| DHL.DE | 55.3 | 54.86 | -0.541 | 9 |
| CDNS | 311.87 | 306.81 | -0.448 | 7 |
| CTAS | 199.66 | 198.09 | -0.431 | 6 |
| MNST | 44.89 | 44.43 | -0.409 | 7 |
| ZS | 176.39 | 172.76 | -0.387 | 7 |
| BEI.DE | 77.4 | 76.82 | -0.377 | 9 |
| ORLY | 87.55 | 86.99 | -0.291 | 7 |
| COST | 933.25 | 928.47 | -0.28 | 5 |
| SAP.DE | 183.32 | 181.72 | -0.279 | 8 |
| VNA.DE | 18.78 | 18.7 | -0.219 | 4 |
| ROP | 417.51 | 415.79 | -0.17 | 5 |
| IDXX | 541.53 | 538.99 | -0.163 | 2 |
| MMM | 169.52 | 169.03 | -0.147 | 4 |
| HEI.DE | 161.75 | 161.3 | -0.113 | 4 |
| MAR | 333.74 | 333.14 | -0.086 | 4 |
| CON.DE | 69.56 | 69.44 | -0.077 | 6 |
| PDD | 82.45 | 82.26 | -0.071 | 3 |
| CPRT | 32.22 | 32.17 | -0.042 | 2 |
| HD | 318.8 | 318.54 | -0.032 | 2 |
| FRE.DE | 44.77 | 44.76 | -0.013 | 8 |
| AMAT | 438.83 | 438.57 | -0.011 | 5 |
| INTU | 343.0 | 342.94 | -0.004 | 3 |

## Tief zurueckerobert (12)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MSFT | 496.78 | 496.81 | 0.003 | 3 |
| MCD | 260.74 | 260.825 | 0.017 | 1 |
| PANW | 328.0 | 328.47 | 0.026 | 4 |
| SNPS | 413.97 | 415.99 | 0.12 | 4 |
| TEAM | 185.45 | 186.56 | 0.12 | 1 |
| P911.DE | 43.9 | 44.05 | 0.128 | 5 |
| CSCO | 108.93 | 109.44 | 0.163 | 2 |
| SRT3.DE | 245.6 | 246.9 | 0.173 | 5 |
| BMW.DE | 60.3 | 60.66 | 0.262 | 1 |
| MRK.DE | 138.45 | 139.5 | 0.427 | 1 |
| SHL.DE | 39.07 | 39.39 | 0.548 | 6 |
| AIR.DE | 194.2 | 196.92 | 0.733 | 1 |

## Tief angetestet (20)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AZN | 161.39 | 161.58 | 0.061 | 0 |
| LRCX | 286.59 | 288.44 | 0.116 | 0 |
| PCAR | 121.81 | 122.16 | 0.128 | 0 |
| DASH | 225.26 | 226.23 | 0.13 | 0 |
| PAYX | 123.38 | 123.99 | 0.197 | 0 |
| GEHC | 70.25 | 70.55 | 0.199 | 0 |
| IBM | 229.9 | 231.71 | 0.295 | 0 |
| MTX.DE | 340.6 | 343.6 | 0.338 | 0 |
| XEL | 75.06 | 75.49 | 0.341 | 0 |
| ADP | 279.31 | 281.69 | 0.41 | 0 |
| KO | 87.81 | 88.425 | 0.427 | 0 |
| ABNB | 180.75 | 183.27 | 0.509 | 0 |
| PEP | 139.33 | 140.55 | 0.543 | 0 |
| RHM.DE | 1070.6 | 1092.0 | 0.554 | 0 |
| KLAC | 168.07 | 172.28 | 0.565 | 0 |
| ENR.DE | 139.2 | 142.24 | 0.567 | 0 |
| CAT | 774.55 | 791.7 | 0.655 | 0 |
| GOOGL | 333.05 | 337.13 | 0.657 | 0 |
| MDLZ | 61.42 | 62.45 | 0.88 | 0 |
| ORCL | 139.95 | 145.77 | 0.978 | 0 |

## Swing-Hoch ueberwunden (23)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 150.81 | 4.025 | 7 |
| CRM | 213.17 | 257.22 | 3.89 | 7 |
| HNR1.DE | 252.4 | 259.6 | 2.066 | 9 |
| WDAY | 185.82 | 200.82 | 1.328 | 7 |
| BKR | 63.02 | 64.621 | 1.043 | 7 |
| CDW | 142.97 | 148.67 | 0.915 | 7 |
| MBG.DE | 45.62 | 46.305 | 0.759 | 9 |
| TTD | 14.17 | 14.54 | 0.661 | 6 |
| BAS.DE | 52.76 | 53.39 | 0.643 | 9 |
| REGN | 839.94 | 852.23 | 0.641 | 5 |
| CEG | 285.26 | 290.1 | 0.56 | 3 |
| AAPL | 322.37 | 324.99 | 0.393 | 7 |
| CHTR | 156.14 | 159.05 | 0.388 | 5 |
| KHC | 26.01 | 26.265 | 0.384 | 6 |
| PG | 146.8 | 147.645 | 0.382 | 6 |
| TMUS | 185.84 | 187.31 | 0.376 | 7 |
| MUV2.DE | 520.4 | 523.0 | 0.356 | 9 |
| JNJ | 273.98 | 275.31 | 0.256 | 7 |
| NFLX | 82.35 | 82.72 | 0.164 | 5 |
| NXPI | 227.24 | 227.88 | 0.117 | 7 |
| VRTX | 555.69 | 556.9 | 0.091 | 2 |
| ADBE | 279.0 | 279.79 | 0.076 | 7 |
| CTSH | 63.3 | 63.39 | 0.042 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.