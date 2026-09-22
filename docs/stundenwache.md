# Stundenwache

Stand: 2026-09-21 · 267 Werte mit Stundendaten · erstellt 2026-09-22 09:46 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| BTI | 55.53 | 55.755 | 0.227 | 1 |

## Tief angetestet (16)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ENB | 48.2 | 48.2 | 0.0 | 0 |
| MDLZ | 60.1 | 60.16 | 0.048 | 0 |
| MO | 68.45 | 68.54 | 0.064 | 0 |
| KDP | 30.56 | 30.61 | 0.079 | 0 |
| TRV | 370.68 | 371.28 | 0.09 | 0 |
| TTD | 13.82 | 13.88 | 0.094 | 0 |
| PGR | 211.84 | 212.21 | 0.095 | 0 |
| CPRT | 28.71 | 28.91 | 0.168 | 0 |
| CNQ | 48.06 | 48.3 | 0.171 | 0 |
| MUV2.DE | 501.8 | 504.0 | 0.243 | 0 |
| MBG.DE | 42.895 | 43.19 | 0.244 | 0 |
| PM | 185.84 | 187.51 | 0.368 | 0 |
| SBUX | 93.63 | 94.89 | 0.547 | 0 |
| SPOT | 503.44 | 517.09 | 0.709 | 0 |
| COST | 888.04 | 898.45 | 0.806 | 0 |
| FAST | 48.53 | 49.64 | 1.084 | 0 |

## Swing-Hoch ueberwunden (57)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 172.93 | 9.604 | 7 |
| WBD | 28.45 | 30.79 | 4.427 | 7 |
| ARM | 253.155 | 323.1 | 3.962 | 7 |
| AMD | 526.79 | 615.36 | 3.47 | 7 |
| INTC | 104.9 | 121.78 | 2.58 | 7 |
| DHL.DE | 55.7 | 58.26 | 2.513 | 3 |
| MU | 944.94 | 1043.3149 | 2.217 | 7 |
| META | 685.31 | 741.13 | 2.042 | 7 |
| BABA | 111.25 | 115.76 | 1.861 | 7 |
| QIA.DE | 37.24 | 39.005 | 1.854 | 3 |
| NET | 319.43 | 351.7564 | 1.711 | 7 |
| ILMN | 221.76 | 238.68 | 1.632 | 7 |
| SRT3.DE | 240.2 | 251.2 | 1.619 | 3 |
| ISRG | 382.41 | 401.71 | 1.58 | 7 |
| DDOG | 227.58 | 245.12 | 1.539 | 7 |
| VLO | 375.11 | 393.4 | 1.229 | 7 |
| IFX.DE | 55.6 | 58.68 | 1.223 | 3 |
| TJX | 127.8 | 130.96 | 1.161 | 7 |
| AAPL | 330.81 | 338.89 | 1.068 | 7 |
| AZN | 164.55 | 168.09 | 1.016 | 7 |
| ZS | 196.575 | 207.15 | 1.005 | 7 |
| TSM | 435.37 | 445.15 | 0.992 | 7 |
| LLY | 1138.79 | 1164.6801 | 0.991 | 7 |
| EQIX | 1033.99 | 1057.25 | 0.908 | 7 |
| QCOM | 185.46 | 194.26 | 0.906 | 7 |
| BNS | 94.02 | 95.34 | 0.882 | 7 |
| NVDA | 222.0 | 227.25 | 0.865 | 7 |
| PH | 939.6 | 958.37 | 0.839 | 7 |
| MRK | 147.09 | 149.52 | 0.806 | 7 |
| WDAY | 185.82 | 191.91 | 0.766 | 7 |
| MRVL | 247.89 | 257.33 | 0.73 | 7 |
| PLTR | 177.88 | 183.08 | 0.714 | 7 |
| ANET | 200.25 | 205.5 | 0.661 | 7 |
| GOOGL | 349.91 | 355.22 | 0.656 | 7 |
| ETN | 427.14 | 435.42 | 0.533 | 7 |
| SHOP | 134.74 | 137.9 | 0.502 | 3 |
| ADS.DE | 145.25 | 146.45 | 0.35 | 2 |
| TXN | 267.97 | 270.8 | 0.33 | 6 |
| BMO | 176.15 | 177.14 | 0.329 | 7 |
| DB1.DE | 280.1 | 281.9 | 0.327 | 3 |
| MPC | 398.52 | 402.17 | 0.243 | 7 |
| ADI | 380.36 | 382.98 | 0.236 | 4 |
| HDB | 23.55 | 23.67 | 0.209 | 7 |
| TEAM | 194.01 | 195.72 | 0.196 | 7 |
| KLAC | 182.41 | 183.96 | 0.194 | 6 |
| TD | 123.72 | 124.07 | 0.174 | 5 |
| AMZN | 257.59 | 258.43 | 0.158 | 5 |
| ZAL.DE | 21.95 | 22.04 | 0.154 | 2 |
| CDNS | 293.4 | 294.91 | 0.141 | 3 |
| TSLA | 374.12 | 375.32 | 0.088 | 6 |
| ABBV | 264.25 | 264.57 | 0.058 | 7 |
| MAR | 342.31 | 342.63 | 0.044 | 2 |
| HSBC | 103.15 | 103.2 | 0.028 | 4 |
| CSCO | 111.44 | 111.4805 | 0.016 | 1 |
| MSFT | 501.47 | 501.61 | 0.014 | 1 |
| GSK | 51.08 | 51.09 | 0.009 | 4 |
| SY1.DE | 91.74 | 91.74 | 0.0 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.