# Stundenwache

Stand: 2026-08-31 · 158 Werte mit Stundendaten · erstellt 2026-09-01 08:19 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| MCHP | 72.91 | 73.44 | 0.208 | 1 |

## Tief angetestet (17)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKNG | 198.85 | 199.07 | 0.036 | 0 |
| DASH | 231.215 | 231.74 | 0.071 | 0 |
| SBUX | 106.01 | 106.24 | 0.093 | 0 |
| V | 378.8 | 379.49 | 0.116 | 0 |
| CSX | 50.36 | 50.51 | 0.175 | 0 |
| ADP | 284.93 | 286.23 | 0.23 | 0 |
| ARM | 238.095 | 241.92 | 0.258 | 0 |
| ABNB | 181.84 | 183.24 | 0.268 | 0 |
| HON | 212.22 | 213.52 | 0.289 | 0 |
| KDP | 31.6 | 31.87 | 0.326 | 0 |
| TTWO | 216.76 | 219.7 | 0.331 | 0 |
| GOOGL | 337.16 | 339.28 | 0.344 | 0 |
| PAYX | 125.56 | 127.34 | 0.589 | 0 |
| AIR.DE | 194.24 | 197.16 | 0.742 | 0 |
| ISRG | 366.73 | 376.87 | 0.968 | 0 |
| VRTX | 532.23 | 545.39 | 0.977 | 0 |
| PG | 142.71 | 145.15 | 1.175 | 0 |

## Swing-Hoch ueberwunden (28)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 257.62 | 3.985 | 7 |
| MRNA | 65.525 | 140.41 | 3.678 | 7 |
| CRWD | 195.4 | 231.04 | 2.856 | 7 |
| SNPS | 401.98 | 439.73 | 2.454 | 7 |
| CDNS | 319.78 | 338.84 | 1.968 | 7 |
| HNR1.DE | 252.4 | 259.4 | 1.899 | 2 |
| MSFT | 489.3 | 507.32 | 1.836 | 7 |
| TEAM | 177.88 | 194.15 | 1.802 | 7 |
| MBG.DE | 45.62 | 46.8 | 1.368 | 2 |
| CDW | 142.97 | 151.61 | 1.351 | 7 |
| ADBE | 279.0 | 292.75 | 1.338 | 7 |
| BMW.DE | 59.6 | 61.38 | 1.323 | 2 |
| WDAY | 185.82 | 197.45 | 0.984 | 7 |
| BNR.DE | 62.12 | 63.32 | 0.842 | 2 |
| VOW3.DE | 75.96 | 77.28 | 0.762 | 2 |
| QCOM | 166.95 | 170.48 | 0.727 | 7 |
| MRK.DE | 140.35 | 141.95 | 0.693 | 2 |
| BAS.DE | 52.76 | 53.36 | 0.62 | 2 |
| ROP | 418.75 | 424.67 | 0.588 | 7 |
| RWE.DE | 58.48 | 59.28 | 0.58 | 2 |
| FTNT | 167.19 | 170.94 | 0.57 | 7 |
| TTD | 13.42 | 13.725 | 0.54 | 7 |
| BKR | 63.02 | 63.56 | 0.36 | 5 |
| PAH3.DE | 28.2 | 28.4 | 0.36 | 2 |
| MUV2.DE | 520.4 | 522.4 | 0.28 | 2 |
| TSLA | 366.5 | 367.92 | 0.105 | 3 |
| CON.DE | 71.06 | 71.2 | 0.1 | 2 |
| SRT3.DE | 252.2 | 252.5 | 0.043 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.