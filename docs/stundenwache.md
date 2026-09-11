# Stundenwache

Stand: 2026-09-10 · 158 Werte mit Stundendaten · erstellt 2026-09-11 10:22 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 4, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (10)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| KDP | 31.44 | 31.47 | 0.046 | 0 |
| ZAL.DE | 22.14 | 22.25 | 0.16 | 0 |
| LIN | 460.2 | 461.49 | 0.173 | 0 |
| LULU | 95.67 | 96.89 | 0.201 | 0 |
| PAYX | 114.51 | 115.2 | 0.254 | 0 |
| CRWD | 205.4 | 208.77 | 0.256 | 0 |
| BNR.DE | 60.28 | 60.68 | 0.295 | 0 |
| MMM | 161.3 | 162.865 | 0.509 | 0 |
| TMUS | 174.65 | 177.08 | 0.585 | 0 |
| BIIB | 208.93 | 215.45 | 1.146 | 0 |

## Swing-Hoch ueberwunden (5)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 136.62 | 5.52 | 7 |
| META | 593.34 | 644.37 | 2.469 | 7 |
| FRE.DE | 45.2 | 45.47 | 0.284 | 3 |
| DDOG | 221.0 | 221.71 | 0.06 | 7 |
| FANG | 205.0 | 205.32 | 0.059 | 3 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.