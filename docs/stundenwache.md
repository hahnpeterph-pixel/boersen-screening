# Stundenwache

Stand: 2026-11-09 · 272 Werte mit Stundendaten · erstellt 2026-11-10 04:08 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 4, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Swing-Hoch ueberwunden (37)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| APP | 264.045 | 410.0 | 6.498 | 7 |
| QIA.DE | 42.345 | 45.12 | 6.416 | 9 |
| IBN | 1404.9 | 1589.0 | 5.538 | 7 |
| FRE.DE | 47.295 | 52.71 | 4.762 | 9 |
| HDB | 734.9 | 798.15 | 3.633 | 7 |
| NEM | 110.83 | 125.16 | 2.846 | 7 |
| TM | 3115.0 | 3418.0 | 2.542 | 4 |
| TTD | 13.68 | 14.96 | 1.82 | 7 |
| ABNB | 180.06 | 190.27 | 1.467 | 7 |
| SCHW | 89.96 | 92.72 | 1.443 | 7 |
| SONY | 4068.0 | 4233.0 | 1.105 | 4 |
| AMZN | 255.36 | 267.01 | 1.104 | 7 |
| SHL.DE | 42.06 | 43.22 | 1.065 | 9 |
| TMUS | 163.35 | 168.65 | 0.793 | 7 |
| HSBC | 13.086 | 13.3653 | 0.75 | 9 |
| PH | 930.84 | 957.06 | 0.694 | 7 |
| BBVA | 22.84 | 23.33 | 0.667 | 9 |
| MRNA | 254.48 | 268.94 | 0.611 | 7 |
| BHP | 59.0 | 60.0 | 0.6 | 5 |
| WDAY | 185.82 | 190.15 | 0.562 | 7 |
| CEG | 268.64 | 276.03 | 0.537 | 6 |
| TMO | 712.17 | 720.73 | 0.347 | 2 |
| CON.DE | 72.02 | 72.68 | 0.344 | 3 |
| HONA | 161.7 | 164.73 | 0.328 | 6 |
| SPG | 231.66 | 233.11 | 0.318 | 4 |
| SNY | 85.37 | 85.94 | 0.3 | 7 |
| CDNS | 331.67 | 336.46 | 0.296 | 7 |
| BNY | 150.28 | 151.16 | 0.266 | 7 |
| MFG | 7824.0 | 7900.0 | 0.22 | 4 |
| DE | 687.07 | 691.28 | 0.214 | 7 |
| AIR.DE | 204.5 | 205.65 | 0.204 | 2 |
| GE | 333.75 | 335.58 | 0.146 | 3 |
| RIO | 64.08 | 64.19 | 0.067 | 5 |
| SNPS | 465.86 | 466.88 | 0.05 | 6 |
| SAN | 11.05 | 11.066 | 0.038 | 2 |
| HEI.DE | 179.6 | 179.75 | 0.026 | 1 |
| JNJ | 281.92 | 282.1 | 0.023 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.