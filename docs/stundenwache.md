# Stundenwache

Stand: 2026-09-28 · 273 Werte mit Stundendaten · erstellt 2026-09-28 23:52 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 182.26 | 183.84 | 0.289 | 2 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SPOT | 497.03 | 497.27 | 0.013 | 0 |
| BA | 184.24 | 184.36 | 0.018 | 0 |
| MCK | 855.65 | 856.11 | 0.023 | 0 |
| TD | 119.515 | 119.58 | 0.033 | 0 |
| SPGI | 395.125 | 395.92 | 0.09 | 0 |
| MS | 192.985 | 193.65 | 0.127 | 0 |
| IBN | 27.2 | 27.3 | 0.209 | 0 |
| ACN | 172.32 | 174.47 | 0.309 | 0 |
| SPG | 203.49 | 204.56 | 0.367 | 0 |
| ZAL.DE | 21.64 | 21.86 | 0.377 | 0 |
| SONY | 23.17 | 23.335 | 0.379 | 0 |
| BHP | 82.935 | 84.58 | 0.706 | 0 |
| NOW | 126.76 | 131.44 | 0.844 | 0 |
| CRWD | 246.51 | 259.24 | 1.008 | 0 |
| ZS | 187.6705 | 199.37 | 1.057 | 0 |

## Swing-Hoch ueberwunden (43)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.88 | 5.178 | 7 |
| NVS | 142.18 | 146.91 | 2.078 | 7 |
| EMR | 152.28 | 159.41 | 1.979 | 7 |
| MRK.DE | 133.45 | 138.55 | 1.927 | 9 |
| ILMN | 250.06 | 271.83 | 1.753 | 7 |
| LLY | 1138.79 | 1185.97 | 1.673 | 7 |
| BEI.DE | 75.74 | 78.42 | 1.606 | 9 |
| DB1.DE | 280.1 | 287.9 | 1.466 | 9 |
| PH | 939.6 | 969.55 | 1.46 | 7 |
| SHOP | 134.74 | 144.04 | 1.299 | 7 |
| TXN | 267.97 | 278.51 | 1.29 | 7 |
| DHR | 220.67 | 227.48 | 1.254 | 7 |
| MMM | 165.37 | 169.48 | 1.187 | 7 |
| BIIB | 222.25 | 228.71 | 1.183 | 7 |
| ROST | 231.85 | 237.15 | 1.052 | 7 |
| MTX.DE | 358.8 | 368.1 | 0.981 | 9 |
| TMO | 663.57 | 678.3 | 0.955 | 6 |
| ISRG | 404.44 | 414.91 | 0.923 | 7 |
| KLAC | 182.41 | 189.37 | 0.921 | 7 |
| LIN | 466.24 | 472.12 | 0.854 | 7 |
| SY1.DE | 91.74 | 93.34 | 0.817 | 9 |
| MCHP | 76.55 | 77.95 | 0.518 | 6 |
| MAR | 354.63 | 358.42 | 0.511 | 7 |
| ADI | 390.55 | 395.68 | 0.446 | 6 |
| SHW | 329.48 | 332.8 | 0.432 | 5 |
| CTAS | 198.81 | 200.53 | 0.422 | 7 |
| IDXX | 524.12 | 528.85 | 0.406 | 5 |
| BMY | 63.4 | 63.88 | 0.399 | 3 |
| WDAY | 185.82 | 188.5 | 0.397 | 7 |
| ON | 74.48 | 75.66 | 0.319 | 7 |
| BAYN.DE | 50.32 | 50.68 | 0.288 | 9 |
| AMGN | 415.76 | 418.34 | 0.281 | 5 |
| DIS | 105.1 | 105.71 | 0.278 | 5 |
| ASML | 1524.8 | 1537.6 | 0.271 | 4 |
| VRTX | 525.29 | 527.64 | 0.214 | 7 |
| CBK.DE | 42.34 | 42.53 | 0.196 | 8 |
| FRE.DE | 46.53 | 46.645 | 0.124 | 9 |
| HNR1.DE | 258.2 | 258.6 | 0.095 | 9 |
| COST | 921.99 | 922.9315 | 0.066 | 5 |
| QIA.DE | 39.505 | 39.565 | 0.063 | 3 |
| APH | 84.48 | 84.605 | 0.044 | 2 |
| CCEP | 102.81 | 102.88 | 0.032 | 2 |
| MSFT | 509.44 | 509.47 | 0.003 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.