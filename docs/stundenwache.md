# Stundenwache

Stand: 2026-11-23 · 272 Werte mit Stundendaten · erstellt 2026-11-24 04:18 UTC

> **Sitzung noch nicht abgeschlossen.** 12 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 4, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (0)

Keine.

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MNST | 42.24 | 42.43 | 0.13 | 0 |
| COF | 177.86 | 180.09 | 0.323 | 0 |
| PAYX | 111.29 | 112.55 | 0.418 | 0 |
| ADP | 298.62 | 302.3025 | 0.571 | 0 |
| CCEP | 114.01 | 115.56 | 0.583 | 0 |
| CMCSA | 24.29 | 24.73 | 0.622 | 0 |
| SPOT | 573.129 | 585.99 | 0.633 | 0 |
| LIN | 508.0 | 516.92 | 0.861 | 0 |
| WMT | 125.84 | 129.57 | 1.158 | 0 |

## Swing-Hoch ueberwunden (9)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.195 | 14.522 | 9 |
| PDD | 79.88 | 87.189 | 2.306 | 7 |
| TM | 3115.0 | 3327.0 | 1.682 | 5 |
| SONY | 4068.0 | 4326.0 | 1.637 | 5 |
| ZS | 218.105 | 229.3 | 0.72 | 7 |
| NVDA | 159.7 | 165.185 | 0.351 | 7 |
| TJX | 138.17 | 139.28 | 0.227 | 7 |
| VNA.DE | 16.99 | 17.05 | 0.133 | 7 |
| INTC | 59.44 | 59.67 | 0.049 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.