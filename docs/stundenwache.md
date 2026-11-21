# Stundenwache

Stand: 2026-11-20 · 272 Werte mit Stundendaten · erstellt 2026-11-21 00:43 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| LIN | 508.0 | 502.975 | -0.506 | 3 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (26)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AXON | 291.11 | 291.43 | 0.012 | 0 |
| RY | 183.31 | 183.44 | 0.031 | 0 |
| SPOT | 576.04 | 577.03 | 0.048 | 0 |
| VLO | 333.37 | 334.18 | 0.048 | 0 |
| TD | 112.78 | 112.92 | 0.057 | 0 |
| BA | 155.57 | 155.9 | 0.065 | 0 |
| CRM | 179.92 | 180.57 | 0.072 | 0 |
| WELL | 239.95 | 240.38 | 0.087 | 0 |
| SPG | 223.94 | 224.37 | 0.092 | 0 |
| PFE | 27.355 | 27.43 | 0.097 | 0 |
| PSX | 238.36 | 239.45 | 0.105 | 0 |
| PM | 183.56 | 184.16 | 0.106 | 0 |
| SPGI | 438.38 | 439.62 | 0.111 | 0 |
| MS | 164.92 | 165.66 | 0.115 | 0 |
| NET | 271.95 | 274.72 | 0.117 | 0 |
| GD | 340.73 | 341.775 | 0.119 | 0 |
| BNY | 140.78 | 141.25 | 0.124 | 0 |
| DHR | 219.93 | 220.695 | 0.125 | 0 |
| CNQ | 44.16 | 44.35 | 0.127 | 0 |
| C | 110.165 | 110.68 | 0.132 | 0 |
| PLD | 122.185 | 122.56 | 0.141 | 0 |
| NEM | 93.91 | 94.685 | 0.142 | 0 |
| JPM | 309.19 | 310.54 | 0.15 | 0 |
| SCHW | 89.82 | 90.22 | 0.169 | 0 |
| BLK | 1095.1 | 1102.13 | 0.192 | 0 |
| GE | 307.4 | 309.72 | 0.21 | 0 |

## Swing-Hoch ueberwunden (8)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.075 | 14.45 | 9 |
| IBN | 1404.9 | 1640.0 | 6.534 | 7 |
| SONY | 4068.0 | 4317.0 | 1.651 | 7 |
| TM | 3115.0 | 3307.0 | 1.531 | 7 |
| HDB | 821.0 | 846.0 | 1.265 | 7 |
| PDD | 79.88 | 83.65 | 1.226 | 7 |
| TJX | 138.17 | 139.67 | 0.304 | 7 |
| VRSK | 201.65 | 202.23 | 0.073 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.