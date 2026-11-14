# Stundenwache

Stand: 2026-11-13 · 272 Werte mit Stundendaten · erstellt 2026-11-14 00:19 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (10)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SPG | 232.91 | 233.01 | 0.023 | 0 |
| GM | 85.91 | 86.02 | 0.035 | 0 |
| SCCO | 162.64 | 164.05 | 0.172 | 0 |
| CM | 115.14 | 115.76 | 0.255 | 0 |
| DE | 667.65 | 673.36 | 0.284 | 0 |
| TD | 123.16 | 123.83 | 0.313 | 0 |
| GD | 360.27 | 363.43 | 0.332 | 0 |
| RY | 201.14 | 202.36 | 0.343 | 0 |
| TMO | 689.79 | 699.72 | 0.462 | 0 |
| LLY | 1419.8101 | 1444.615 | 0.486 | 0 |

## Swing-Hoch ueberwunden (34)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.295 | 15.101 | 9 |
| IBN | 1404.9 | 1583.6 | 5.182 | 7 |
| TM | 3115.0 | 3429.0 | 2.582 | 7 |
| TTD | 13.68 | 15.69 | 2.311 | 7 |
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
| JNJ | 283.25 | 286.055 | 0.401 | 7 |
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
| PG | 169.79 | 169.86 | 0.022 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.