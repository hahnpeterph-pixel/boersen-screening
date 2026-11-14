# Stundenwache

Stand: 2026-11-13 · 272 Werte mit Stundendaten · erstellt 2026-11-14 02:27 UTC

> **Sitzung noch nicht abgeschlossen.** 4 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (20)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GM | 85.91 | 86.02 | 0.035 | 0 |
| TMUS | 169.55 | 169.965 | 0.07 | 0 |
| SHW | 348.92 | 349.87 | 0.074 | 0 |
| MRNA | 221.7 | 223.23 | 0.08 | 0 |
| IFX.DE | 49.425 | 49.88 | 0.148 | 0 |
| ASML | 1325.2 | 1337.6 | 0.192 | 0 |
| CDNS | 319.86 | 323.04 | 0.208 | 0 |
| ABBV | 293.56 | 295.17 | 0.217 | 0 |
| SYK | 306.55 | 309.64 | 0.235 | 0 |
| NET | 300.28 | 305.73 | 0.24 | 0 |
| ENB | 47.46 | 47.675 | 0.273 | 0 |
| MBG.DE | 40.385 | 40.745 | 0.284 | 0 |
| SNDK | 848.4983 | 884.5003 | 0.316 | 0 |
| GE | 328.1 | 331.83 | 0.318 | 0 |
| BMW.DE | 56.8 | 57.56 | 0.44 | 0 |
| DHR | 229.92 | 233.05 | 0.483 | 0 |
| ADS.DE | 174.95 | 178.25 | 0.635 | 0 |
| SHL.DE | 43.32 | 44.1 | 0.695 | 0 |
| HEN3.DE | 84.42 | 87.16 | 1.425 | 0 |
| SCHW | 89.76 | 92.99 | 1.534 | 0 |

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.295 | 15.101 | 9 |
| IBN | 1404.9 | 1583.6 | 5.182 | 7 |
| TM | 3115.0 | 3429.0 | 2.582 | 7 |
| TTD | 13.68 | 15.685 | 2.306 | 7 |
| SONY | 4068.0 | 4355.0 | 1.921 | 7 |
| CHTR | 127.16 | 138.49 | 1.574 | 7 |
| WDAY | 185.82 | 196.39 | 1.432 | 7 |
| SNY | 85.37 | 87.82 | 1.323 | 9 |
| ALV.DE | 466.4 | 477.4 | 1.236 | 9 |
| COST | 1081.55 | 1106.41 | 1.152 | 7 |
| MUV2.DE | 579.8 | 592.2 | 1.012 | 9 |
| KO | 97.39 | 99.27 | 0.997 | 7 |
| BNY | 150.28 | 153.42 | 0.984 | 7 |
| CEG | 268.64 | 280.22 | 0.852 | 7 |
| VRSK | 201.65 | 207.82 | 0.788 | 7 |
| ANET | 188.53 | 197.34 | 0.667 | 7 |
| XEL | 80.67 | 81.62 | 0.605 | 7 |
| BRK-B | 586.3 | 593.12 | 0.601 | 7 |
| ING | 29.68 | 30.095 | 0.567 | 9 |
| UL | 49.355 | 49.915 | 0.475 | 9 |
| RWE.DE | 58.92 | 59.56 | 0.475 | 9 |
| MS | 188.3 | 190.67 | 0.42 | 7 |
| JNJ | 283.25 | 286.055 | 0.393 | 7 |
| DB1.DE | 329.1 | 331.1 | 0.305 | 5 |
| CL | 99.01 | 99.68 | 0.291 | 6 |
| ODFL | 172.8 | 174.57 | 0.244 | 5 |
| CCEP | 117.96 | 118.58 | 0.214 | 7 |
| UPS | 111.83 | 112.43 | 0.201 | 5 |
| DTE.DE | 26.49 | 26.57 | 0.133 | 9 |
| AAPL | 355.38 | 356.4 | 0.108 | 7 |
| UNH | 406.72 | 407.6 | 0.081 | 2 |
| NVO | 278.0 | 278.45 | 0.059 | 1 |
| EOAN.DE | 19.46 | 19.47 | 0.026 | 4 |
| PG | 169.79 | 169.86 | 0.021 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.