# Stundenwache

Stand: 2026-10-01 · 273 Werte mit Stundendaten · erstellt 2026-10-02 11:02 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 4, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| REGN | 741.83 | 734.37 | -0.341 | 7 |
| SPGI | 388.57 | 388.12 | -0.052 | 2 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BABA | 107.4 | 107.45 | 0.018 | 3 |

## Tief angetestet (30)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GOOGL | 338.02 | 338.26 | 0.025 | 0 |
| NVO | 37.37 | 37.405 | 0.032 | 0 |
| PEP | 125.53 | 125.63 | 0.043 | 0 |
| BTI | 53.13 | 53.185 | 0.053 | 0 |
| GILD | 147.19 | 147.45 | 0.075 | 0 |
| PFE | 28.08 | 28.12 | 0.088 | 0 |
| BMW.DE | 54.28 | 54.46 | 0.094 | 0 |
| CL | 84.33 | 84.52 | 0.141 | 0 |
| WELL | 226.23 | 227.09 | 0.18 | 0 |
| RTX | 184.33 | 185.03 | 0.19 | 0 |
| MELI | 1668.4399 | 1684.6801 | 0.31 | 0 |
| HONA | 152.26 | 154.1 | 0.313 | 0 |
| WMT | 103.59 | 104.29 | 0.326 | 0 |
| SCCO | 196.9 | 199.28 | 0.343 | 0 |
| UL | 59.22 | 59.58 | 0.355 | 0 |
| MCD | 229.61 | 231.84 | 0.448 | 0 |
| V | 357.36 | 359.97 | 0.45 | 0 |
| BAYN.DE | 44.6 | 45.25 | 0.461 | 0 |
| AXON | 411.8 | 422.22 | 0.489 | 0 |
| ANET | 200.771 | 204.47 | 0.528 | 0 |
| SCHW | 96.87 | 98.405 | 0.644 | 0 |
| LOW | 179.21 | 182.37 | 0.735 | 0 |
| MUFG | 22.21 | 22.6 | 0.763 | 0 |
| SMFG | 24.78 | 25.275 | 0.767 | 0 |
| XOM | 160.81 | 163.87 | 0.815 | 0 |
| SPG | 198.41 | 200.84 | 0.885 | 0 |
| WDC | 440.05 | 462.56 | 0.956 | 0 |
| NEE | 74.78 | 76.35 | 1.182 | 0 |
| FAST | 49.11 | 50.225 | 1.188 | 0 |
| AEP | 117.34 | 119.78 | 1.308 | 0 |

## Swing-Hoch ueberwunden (24)

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
| MPC | 398.33 | 420.22 | 1.253 | 7 |
| IFX.DE | 60.48 | 62.66 | 0.926 | 4 |
| VLO | 395.85 | 408.43 | 0.687 | 7 |
| PSX | 259.11 | 264.19 | 0.523 | 7 |
| HDB | 22.67 | 22.945 | 0.501 | 7 |
| APH | 84.48 | 85.73 | 0.439 | 6 |
| STX | 925.44 | 945.57 | 0.436 | 4 |
| GEV | 973.41 | 987.45 | 0.395 | 5 |
| MSFT | 509.44 | 513.105 | 0.3 | 7 |
| ASML | 1630.2 | 1638.2 | 0.181 | 3 |
| CRWD | 263.87 | 266.165 | 0.177 | 7 |
| WDAY | 185.82 | 186.69 | 0.117 | 6 |
| SKHY | 192.83 | 193.47 | 0.074 | 2 |
| MRVL | 267.48 | 268.01 | 0.042 | 2 |
| HON | 213.64 | 213.8 | 0.037 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.