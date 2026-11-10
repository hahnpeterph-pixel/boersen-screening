# Stundenwache

Stand: 2026-11-09 · 272 Werte mit Stundendaten · erstellt 2026-11-10 02:01 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 2, 3, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| COF | 202.06 | 198.63 | -0.518 | 7 |
| SY1.DE | 95.68 | 94.6 | -0.375 | 6 |
| HNR1.DE | 291.4 | 289.8 | -0.264 | 9 |
| CNQ | 48.42 | 48.05 | -0.227 | 7 |
| MUV2.DE | 568.4 | 566.4 | -0.176 | 9 |
| AXON | 307.0 | 303.01 | -0.168 | 5 |
| PM | 193.62 | 193.13 | -0.082 | 4 |
| BNR.DE | 61.48 | 61.46 | -0.015 | 6 |

## Tief zurueckerobert (4)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CVX | 210.43 | 210.78 | 0.061 | 2 |
| BAS.DE | 53.81 | 53.94 | 0.115 | 3 |
| C | 121.43 | 121.97 | 0.151 | 1 |
| CB | 362.3 | 363.4 | 0.152 | 1 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BMW.DE | 58.88 | 58.92 | 0.023 | 0 |
| COP | 134.19 | 134.5 | 0.067 | 0 |
| BABA | 101.6 | 102.0 | 0.102 | 0 |
| MSTR | 123.9 | 125.66 | 0.181 | 0 |
| XOM | 163.51 | 164.73 | 0.235 | 0 |
| PGR | 225.78 | 227.52 | 0.338 | 0 |
| VOW3.DE | 69.42 | 70.24 | 0.371 | 0 |
| PAH3.DE | 25.92 | 26.23 | 0.452 | 0 |
| GS | 892.1 | 906.24 | 0.476 | 0 |
| MBG.DE | 41.205 | 41.885 | 0.528 | 0 |
| VLO | 342.0 | 356.86 | 0.749 | 0 |
| SPOT | 589.5 | 609.25 | 0.759 | 0 |
| PSX | 243.02 | 253.04 | 0.875 | 0 |
| ADS.DE | 173.1 | 178.0 | 0.965 | 0 |
| RHM.DE | 798.0 | 844.3 | 1.01 | 0 |

## Swing-Hoch ueberwunden (38)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| APP | 264.045 | 410.0 | 6.861 | 7 |
| IBN | 1404.9 | 1589.0 | 5.538 | 7 |
| QIA.DE | 42.345 | 45.12 | 5.036 | 9 |
| FRE.DE | 47.295 | 52.71 | 4.816 | 9 |
| HDB | 734.9 | 798.15 | 3.633 | 7 |
| NEM | 110.83 | 125.16 | 2.929 | 7 |
| TM | 3115.0 | 3436.0 | 2.693 | 2 |
| TTD | 13.68 | 14.96 | 1.82 | 7 |
| SONY | 4068.0 | 4289.0 | 1.512 | 2 |
| ABNB | 180.06 | 190.27 | 1.467 | 7 |
| SCHW | 89.96 | 92.72 | 1.438 | 7 |
| SHL.DE | 42.06 | 43.22 | 1.147 | 9 |
| AMZN | 255.36 | 267.01 | 1.104 | 7 |
| TMUS | 163.35 | 168.65 | 0.793 | 7 |
| HSBC | 13.086 | 13.3653 | 0.75 | 9 |
| PH | 930.84 | 957.06 | 0.712 | 7 |
| BHP | 59.0 | 60.17 | 0.703 | 3 |
| BBVA | 22.84 | 23.33 | 0.667 | 9 |
| MRNA | 254.48 | 268.94 | 0.611 | 7 |
| WDAY | 185.82 | 190.15 | 0.563 | 7 |
| CEG | 268.64 | 276.03 | 0.537 | 6 |
| MFG | 7824.0 | 7964.0 | 0.405 | 2 |
| CON.DE | 72.02 | 72.68 | 0.37 | 3 |
| TMO | 712.17 | 720.73 | 0.365 | 2 |
| HONA | 161.7 | 164.73 | 0.35 | 6 |
| SPG | 231.66 | 233.11 | 0.322 | 4 |
| SNY | 85.37 | 85.94 | 0.3 | 7 |
| CDNS | 331.67 | 336.46 | 0.296 | 7 |
| BNY | 150.28 | 151.16 | 0.266 | 7 |
| DE | 687.07 | 691.28 | 0.223 | 7 |
| AIR.DE | 204.5 | 205.65 | 0.215 | 2 |
| SMFG | 3237.0 | 3260.0 | 0.189 | 2 |
| GE | 333.75 | 335.58 | 0.144 | 3 |
| RIO | 64.08 | 64.19 | 0.067 | 5 |
| SNPS | 465.86 | 466.88 | 0.05 | 6 |
| SAN | 11.05 | 11.066 | 0.038 | 2 |
| HEI.DE | 179.6 | 179.75 | 0.027 | 1 |
| JNJ | 281.92 | 282.1 | 0.023 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.