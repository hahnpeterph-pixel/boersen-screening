# Stundenwache

Stand: 2026-09-10 · 158 Werte mit Stundendaten · erstellt 2026-09-10 21:31 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| SPGI | 410.29 | 410.49 | 0.017 | 0 |
| ORCL | 152.61 | 153.05 | 0.065 | 0 |
| MCD | 252.55 | 253.025 | 0.124 | 0 |
| LIN | 460.2 | 461.49 | 0.173 | 0 |
| LULU | 95.67 | 96.89 | 0.201 | 0 |
| PAYX | 114.51 | 115.2 | 0.254 | 0 |
| CRWD | 205.4 | 208.77 | 0.256 | 0 |
| CON.DE | 69.24 | 70.46 | 0.699 | 0 |
| DB1.DE | 272.1 | 279.8 | 1.395 | 0 |

## Swing-Hoch ueberwunden (5)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 136.62 | 5.52 | 7 |
| META | 593.34 | 644.37 | 2.469 | 7 |
| DDOG | 221.0 | 221.71 | 0.06 | 7 |
| FANG | 205.0 | 205.32 | 0.059 | 3 |
| BMW.DE | 62.72 | 62.74 | 0.013 | 8 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.