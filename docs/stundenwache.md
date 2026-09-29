# Stundenwache

Stand: 2026-09-28 · 273 Werte mit Stundendaten · erstellt 2026-09-29 11:20 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (1)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SPCX | 145.88 | 145.491 | -0.062 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (19)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TD | 119.51 | 119.58 | 0.036 | 0 |
| BA | 184.01 | 184.36 | 0.054 | 0 |
| BAC | 55.37 | 55.455 | 0.061 | 0 |
| CPRT | 27.11 | 27.21 | 0.101 | 0 |
| HDB | 22.33 | 22.415 | 0.142 | 0 |
| KHC | 23.452 | 23.56 | 0.186 | 0 |
| INTC | 114.71 | 116.13 | 0.209 | 0 |
| VZ | 46.43 | 46.69 | 0.235 | 0 |
| MUV2.DE | 506.2 | 508.4 | 0.267 | 0 |
| AMZN | 244.73 | 246.26 | 0.283 | 0 |
| AXP | 304.19 | 306.28 | 0.336 | 0 |
| SPG | 203.49 | 204.56 | 0.367 | 0 |
| SONY | 23.17 | 23.335 | 0.379 | 0 |
| HON | 209.73 | 211.52 | 0.424 | 0 |
| ROP | 348.77 | 354.03 | 0.566 | 0 |
| ADSK | 202.09 | 207.19 | 0.713 | 0 |
| CRWD | 246.51 | 259.24 | 1.008 | 0 |
| ZS | 187.671 | 199.37 | 1.057 | 0 |
| PANW | 367.27 | 392.06 | 1.35 | 0 |

## Swing-Hoch ueberwunden (39)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.88 | 5.178 | 7 |
| MRK.DE | 133.45 | 139.6 | 2.471 | 5 |
| NVS | 142.18 | 146.91 | 2.078 | 7 |
| EMR | 152.28 | 159.41 | 1.979 | 7 |
| MTX.DE | 358.8 | 375.3 | 1.784 | 5 |
| ILMN | 250.06 | 271.83 | 1.746 | 7 |
| LLY | 1138.79 | 1185.97 | 1.673 | 7 |
| BEI.DE | 75.74 | 78.12 | 1.477 | 5 |
| PH | 939.6 | 969.55 | 1.46 | 7 |
| ASML | 1524.8 | 1594.4 | 1.453 | 5 |
| SHOP | 134.74 | 144.04 | 1.299 | 7 |
| DB1.DE | 280.1 | 286.5 | 1.295 | 5 |
| TXN | 267.97 | 278.51 | 1.29 | 7 |
| DHR | 220.67 | 227.48 | 1.254 | 7 |
| MMM | 165.37 | 169.48 | 1.187 | 7 |
| BIIB | 222.25 | 228.71 | 1.183 | 7 |
| SY1.DE | 91.74 | 93.88 | 1.137 | 5 |
| ROST | 231.85 | 237.15 | 1.052 | 7 |
| TMO | 663.57 | 678.2 | 0.947 | 7 |
| ISRG | 404.44 | 414.91 | 0.923 | 7 |
| KLAC | 182.41 | 189.37 | 0.921 | 7 |
| LIN | 466.24 | 472.12 | 0.854 | 7 |
| MCHP | 76.55 | 77.95 | 0.518 | 6 |
| MAR | 354.63 | 358.42 | 0.511 | 7 |
| CBK.DE | 42.34 | 42.81 | 0.495 | 5 |
| ADI | 390.55 | 395.68 | 0.446 | 6 |
| SHW | 329.48 | 332.8 | 0.432 | 5 |
| CTAS | 198.81 | 200.53 | 0.422 | 7 |
| IDXX | 524.12 | 528.85 | 0.405 | 5 |
| WDAY | 185.82 | 188.5 | 0.397 | 7 |
| BMY | 63.4 | 63.88 | 0.396 | 3 |
| ON | 74.48 | 75.66 | 0.319 | 7 |
| AMGN | 415.76 | 418.34 | 0.281 | 5 |
| DIS | 105.1 | 105.71 | 0.277 | 5 |
| VRTX | 525.29 | 527.64 | 0.214 | 7 |
| COST | 921.99 | 922.9315 | 0.066 | 5 |
| APH | 84.48 | 84.605 | 0.044 | 2 |
| CCEP | 102.81 | 102.88 | 0.032 | 2 |
| MSFT | 509.44 | 509.47 | 0.003 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.