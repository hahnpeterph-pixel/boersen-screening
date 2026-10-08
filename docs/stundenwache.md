# Stundenwache

Stand: 2026-10-07 · 272 Werte mit Stundendaten · erstellt 2026-10-08 01:57 UTC

> **Sitzung noch nicht abgeschlossen.** 10 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MBG.DE | 39.41 | 39.875 | 0.389 | 1 |

## Tief angetestet (18)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MUFG | 3519.0 | 3519.0 | 0.0 | 0 |
| MFG | 8380.0 | 8384.0 | 0.015 | 0 |
| MDT | 85.43 | 85.51 | 0.04 | 0 |
| CM | 108.24 | 108.33 | 0.042 | 0 |
| AXON | 405.3 | 406.0 | 0.046 | 0 |
| RY | 191.09 | 191.25 | 0.052 | 0 |
| PH | 951.62 | 952.74 | 0.056 | 0 |
| SPG | 197.32 | 197.54 | 0.085 | 0 |
| TD | 113.67 | 113.87 | 0.097 | 0 |
| SY1.DE | 90.92 | 91.22 | 0.166 | 0 |
| GD | 325.01 | 326.54 | 0.259 | 0 |
| TSLA | 374.43 | 377.62 | 0.288 | 0 |
| WDC | 397.02 | 405.4 | 0.301 | 0 |
| MNST | 42.56 | 42.865 | 0.306 | 0 |
| ABNB | 158.656 | 160.61 | 0.368 | 0 |
| SCHW | 94.7 | 95.58 | 0.393 | 0 |
| LULU | 90.56 | 91.88 | 0.404 | 0 |
| TRV | 357.61 | 360.5 | 0.46 | 0 |

## Swing-Hoch ueberwunden (35)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| SHOP | 134.74 | 165.95 | 4.24 | 7 |
| SNPS | 445.92 | 502.51 | 2.821 | 7 |
| MPC | 398.33 | 442.35 | 2.683 | 7 |
| MELI | 1739.88 | 1872.8199 | 2.274 | 7 |
| CSCO | 111.5 | 117.38 | 2.233 | 7 |
| ADSK | 222.0 | 235.06 | 1.779 | 7 |
| AMZN | 250.88 | 259.88 | 1.701 | 7 |
| VLO | 395.85 | 424.01 | 1.687 | 7 |
| TJX | 134.67 | 138.8 | 1.407 | 7 |
| AVGO | 361.86 | 376.275 | 1.39 | 7 |
| PSX | 259.11 | 271.39 | 1.367 | 7 |
| FTNT | 181.37 | 189.28 | 1.354 | 7 |
| WMT | 105.14 | 108.12 | 1.349 | 7 |
| SO | 83.98 | 85.44 | 1.155 | 7 |
| ZS | 203.44 | 213.68 | 1.093 | 7 |
| XEL | 71.37 | 72.4 | 0.835 | 7 |
| BNR.DE | 60.28 | 61.34 | 0.829 | 9 |
| COST | 931.09 | 942.01 | 0.703 | 7 |
| ANET | 212.0 | 215.82 | 0.635 | 6 |
| SHL.DE | 38.13 | 38.54 | 0.484 | 8 |
| ABBV | 268.93 | 271.31 | 0.438 | 7 |
| EXC | 41.21 | 41.48 | 0.408 | 7 |
| LIN | 480.56 | 483.94 | 0.401 | 7 |
| GOOGL | 347.03 | 350.37 | 0.373 | 3 |
| MRVL | 280.0 | 284.73 | 0.364 | 7 |
| BAS.DE | 50.93 | 51.25 | 0.294 | 9 |
| DUK | 115.17 | 115.49 | 0.222 | 7 |
| CVS | 87.51 | 87.94 | 0.207 | 7 |
| HNR1.DE | 260.8 | 261.6 | 0.175 | 3 |
| MUV2.DE | 516.2 | 517.6 | 0.159 | 1 |
| AEP | 121.8 | 122.08 | 0.145 | 7 |
| MCK | 907.07 | 909.79 | 0.115 | 7 |
| AAPL | 336.21 | 336.62 | 0.066 | 3 |
| PAYX | 101.33 | 101.52 | 0.063 | 6 |
| AMD | 645.46 | 645.83 | 0.016 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.