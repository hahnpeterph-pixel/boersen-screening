# Stundenwache

Stand: 2026-08-26 · 158 Werte mit Stundendaten · erstellt 2026-08-27 05:59 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (6)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 182.74 | 179.86 | -0.546 | 9 |
| P911.DE | 43.58 | 43.19 | -0.364 | 9 |
| SHL.DE | 39.62 | 39.48 | -0.212 | 9 |
| VOW3.DE | 72.76 | 72.5 | -0.166 | 9 |
| ADS.DE | 151.9 | 151.25 | -0.156 | 2 |
| PAH3.DE | 27.27 | 27.25 | -0.037 | 8 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| VNA.DE | 19.74 | 19.765 | 0.07 | 1 |
| MBG.DE | 44.615 | 44.73 | 0.156 | 1 |

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ABNB | 187.9 | 188.0 | 0.014 | 0 |
| LULU | 115.87 | 116.35 | 0.112 | 0 |
| GS | 1036.78 | 1040.6899 | 0.173 | 0 |
| ASML | 1481.2 | 1494.2 | 0.263 | 0 |
| BNR.DE | 60.24 | 60.88 | 0.392 | 0 |
| FANG | 196.65 | 199.83 | 0.546 | 0 |
| RHM.DE | 1110.4 | 1143.0 | 0.694 | 0 |
| ADBE | 265.04 | 273.37 | 0.822 | 0 |

## Swing-Hoch ueberwunden (30)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRK | 131.09 | 153.14 | 4.685 | 7 |
| MRNA | 65.525 | 149.65 | 4.447 | 7 |
| VZ | 47.45 | 50.19 | 3.542 | 7 |
| HEI.DE | 161.75 | 172.0 | 3.056 | 9 |
| V | 365.14 | 383.81 | 2.968 | 7 |
| ILMN | 203.75 | 224.92 | 2.369 | 7 |
| DASH | 219.53 | 236.92 | 2.138 | 7 |
| SY1.DE | 90.1 | 93.2 | 2.011 | 9 |
| PYPL | 59.44 | 61.82 | 1.705 | 7 |
| ALV.DE | 443.5 | 452.0 | 1.582 | 9 |
| CDNS | 319.78 | 334.81 | 1.564 | 7 |
| CMCSA | 26.49 | 27.21 | 1.235 | 7 |
| NFLX | 78.73 | 81.46 | 1.229 | 7 |
| DIS | 107.11 | 109.64 | 1.159 | 7 |
| CBK.DE | 40.13 | 40.92 | 1.134 | 9 |
| DB1.DE | 280.7 | 286.2 | 1.098 | 9 |
| MELI | 1874.98 | 1950.5699 | 1.05 | 7 |
| DBK.DE | 34.1 | 34.64 | 0.932 | 9 |
| LIN | 483.49 | 490.28 | 0.872 | 7 |
| HNR1.DE | 252.4 | 255.6 | 0.77 | 9 |
| MSFT | 489.3 | 496.17 | 0.753 | 7 |
| SNPS | 401.98 | 410.14 | 0.733 | 7 |
| WDAY | 185.82 | 190.66 | 0.433 | 7 |
| SIE.DE | 286.55 | 288.75 | 0.367 | 9 |
| SBUX | 107.81 | 108.48 | 0.255 | 2 |
| AMD | 477.36 | 481.01 | 0.184 | 7 |
| WBD | 28.68 | 28.725 | 0.105 | 7 |
| ORCL | 148.35 | 148.87 | 0.083 | 2 |
| VRTX | 546.17 | 547.29 | 0.068 | 7 |
| CSCO | 112.19 | 112.42 | 0.067 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.