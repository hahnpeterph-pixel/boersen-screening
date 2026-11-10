# Stundenwache

Stand: 2026-11-09 · 272 Werte mit Stundendaten · erstellt 2026-11-10 13:27 UTC

> **Sitzung noch nicht abgeschlossen.** 60 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 5, 6, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| C | 121.43 | 121.97 | 0.151 | 1 |

## Tief angetestet (4)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PM | 192.26 | 193.13 | 0.141 | 0 |
| PDD | 80.11 | 80.49 | 0.144 | 0 |
| COP | 133.4 | 134.5 | 0.241 | 0 |
| GS | 892.1 | 906.24 | 0.476 | 0 |

## Swing-Hoch ueberwunden (45)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.14 | 7.425 | 6 |
| APP | 264.045 | 410.0 | 6.498 | 7 |
| IBN | 1404.9 | 1589.0 | 5.538 | 7 |
| FRE.DE | 47.295 | 53.4 | 5.372 | 6 |
| HDB | 734.9 | 798.15 | 3.633 | 7 |
| NEM | 110.83 | 125.16 | 2.846 | 7 |
| TM | 3115.0 | 3424.0 | 2.583 | 7 |
| TTD | 13.68 | 14.955 | 1.813 | 7 |
| HEN3.DE | 84.46 | 87.18 | 1.632 | 6 |
| ABNB | 180.06 | 190.27 | 1.467 | 7 |
| SCHW | 89.96 | 92.72 | 1.443 | 7 |
| HSBC | 13.086 | 13.586 | 1.34 | 6 |
| BBVA | 22.84 | 23.82 | 1.326 | 6 |
| SONY | 4068.0 | 4259.0 | 1.279 | 7 |
| AIR.DE | 204.5 | 211.55 | 1.275 | 6 |
| SHL.DE | 42.06 | 43.32 | 1.202 | 6 |
| AMZN | 255.36 | 267.01 | 1.104 | 7 |
| CON.DE | 72.02 | 73.94 | 0.982 | 6 |
| HEI.DE | 179.6 | 184.25 | 0.804 | 6 |
| TMUS | 163.35 | 168.65 | 0.793 | 7 |
| SAN | 11.05 | 11.356 | 0.732 | 6 |
| PH | 930.84 | 957.06 | 0.694 | 7 |
| MRNA | 254.48 | 268.94 | 0.611 | 7 |
| DTG.DE | 42.33 | 43.02 | 0.59 | 6 |
| WDAY | 185.82 | 190.15 | 0.562 | 7 |
| MTX.DE | 357.5 | 365.3 | 0.555 | 6 |
| CEG | 268.64 | 275.96 | 0.532 | 6 |
| BHP | 59.0 | 59.87 | 0.522 | 7 |
| ING | 29.68 | 30.055 | 0.442 | 6 |
| SNY | 85.37 | 86.1 | 0.386 | 6 |
| TMO | 712.17 | 721.64 | 0.384 | 3 |
| GSK | 19.155 | 19.345 | 0.375 | 6 |
| MFG | 7824.0 | 7951.0 | 0.367 | 7 |
| BAYN.DE | 56.6 | 57.22 | 0.332 | 6 |
| HONA | 161.7 | 164.73 | 0.328 | 6 |
| SPG | 231.66 | 233.11 | 0.318 | 4 |
| CDNS | 331.67 | 336.47 | 0.297 | 7 |
| BNY | 150.28 | 151.16 | 0.266 | 7 |
| CBK.DE | 40.39 | 40.68 | 0.242 | 6 |
| DE | 687.07 | 691.28 | 0.214 | 7 |
| UL | 49.355 | 49.585 | 0.189 | 3 |
| GE | 333.75 | 335.58 | 0.146 | 3 |
| SMFG | 3237.0 | 3248.0 | 0.09 | 6 |
| SNPS | 465.86 | 466.88 | 0.05 | 6 |
| JNJ | 281.92 | 282.1 | 0.023 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.