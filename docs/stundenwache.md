# Stundenwache

Stand: 2026-10-01 · 273 Werte mit Stundendaten · erstellt 2026-10-01 23:05 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (2)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| REGN | 741.83 | 734.37 | -0.342 | 7 |
| SPGI | 388.57 | 388.12 | -0.052 | 2 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BABA | 107.4 | 107.45 | 0.018 | 3 |
| SAP.DE | 182.26 | 187.24 | 0.921 | 1 |

## Tief angetestet (38)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GOOGL | 338.02 | 338.26 | 0.025 | 0 |
| NVS | 140.9 | 141.04 | 0.06 | 0 |
| JNJ | 258.3351 | 258.74 | 0.081 | 0 |
| DHR | 211.195 | 211.74 | 0.09 | 0 |
| AIR.DE | 185.84 | 186.28 | 0.101 | 0 |
| NEM | 114.19 | 114.67 | 0.124 | 0 |
| SHL.DE | 37.28 | 37.39 | 0.134 | 0 |
| RTX | 184.3459 | 185.03 | 0.186 | 0 |
| MMM | 162.33 | 163.055 | 0.201 | 0 |
| PG | 143.41 | 143.99 | 0.245 | 0 |
| PM | 186.92 | 188.17 | 0.293 | 0 |
| TM | 182.385 | 183.3463 | 0.317 | 0 |
| LLY | 1139.9 | 1150.05 | 0.318 | 0 |
| KO | 85.725 | 86.12 | 0.328 | 0 |
| SCCO | 196.9863 | 199.28 | 0.331 | 0 |
| BBVA | 26.64 | 26.87 | 0.341 | 0 |
| UL | 59.22 | 59.58 | 0.355 | 0 |
| PBR | 20.76 | 21.0 | 0.43 | 0 |
| MCD | 229.61 | 231.84 | 0.448 | 0 |
| ING | 33.8902 | 34.22 | 0.461 | 0 |
| FDX | 284.0 | 287.07 | 0.463 | 0 |
| AXON | 411.8 | 422.22 | 0.489 | 0 |
| ANET | 200.7938 | 204.47 | 0.525 | 0 |
| SCHW | 96.87 | 98.405 | 0.644 | 0 |
| DELL | 520.2 | 541.7 | 0.765 | 0 |
| SMFG | 24.78 | 25.275 | 0.767 | 0 |
| HD | 277.2 | 282.495 | 0.803 | 0 |
| XOM | 160.84 | 163.87 | 0.807 | 0 |
| ENB | 45.725 | 46.27 | 0.82 | 0 |
| BNY | 140.915 | 143.91 | 0.901 | 0 |
| MUV2.DE | 492.2 | 499.8 | 0.917 | 0 |
| WDC | 440.05 | 462.56 | 0.956 | 0 |
| MS | 182.49 | 188.04 | 1.093 | 0 |
| CM | 107.665 | 109.94 | 1.099 | 0 |
| EMR | 154.15 | 158.56 | 1.175 | 0 |
| NEE | 74.78 | 76.35 | 1.183 | 0 |
| FAST | 49.1091 | 50.225 | 1.189 | 0 |
| RY | 191.41 | 195.33 | 1.232 | 0 |

## Swing-Hoch ueberwunden (22)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.94 | 6.281 | 7 |
| KLAC | 182.41 | 200.33 | 2.501 | 7 |
| SNPS | 445.92 | 490.53 | 2.358 | 7 |
| AMAT | 487.68 | 529.07 | 2.144 | 7 |
| SHOP | 134.74 | 149.05 | 2.134 | 7 |
| ACN | 193.75 | 212.54 | 1.892 | 7 |
| CDNS | 330.81 | 350.71 | 1.724 | 7 |
| LRCX | 317.13 | 339.85 | 1.643 | 7 |
| ON | 74.48 | 80.04 | 1.55 | 7 |
| MPC | 398.33 | 420.22 | 1.255 | 7 |
| VLO | 395.85 | 408.43 | 0.688 | 7 |
| PSX | 259.11 | 264.19 | 0.523 | 7 |
| HDB | 22.67 | 22.945 | 0.501 | 7 |
| APH | 84.48 | 85.73 | 0.439 | 6 |
| GEV | 973.41 | 987.45 | 0.395 | 5 |
| MSFT | 509.44 | 513.105 | 0.3 | 7 |
| CRWD | 263.87 | 266.165 | 0.177 | 7 |
| STX | 925.44 | 931.69 | 0.135 | 3 |
| WDAY | 185.82 | 186.69 | 0.117 | 6 |
| SKHY | 192.83 | 193.47 | 0.074 | 2 |
| MRVL | 267.48 | 268.01 | 0.042 | 2 |
| HON | 213.64 | 213.8 | 0.037 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.