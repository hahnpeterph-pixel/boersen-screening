# Stundenwache

Stand: 2026-09-16 · 158 Werte mit Stundendaten · erstellt 2026-09-16 22:00 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (4)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PCAR | 119.77 | 118.26 | -0.559 | 3 |
| ZAL.DE | 21.75 | 21.48 | -0.38 | 9 |
| CBK.DE | 41.99 | 41.63 | -0.361 | 5 |
| VOW3.DE | 79.86 | 79.2 | -0.236 | 9 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (7)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| WMT | 107.45 | 107.52 | 0.04 | 0 |
| CSGP | 30.265 | 30.36 | 0.077 | 0 |
| SPGI | 404.855 | 406.77 | 0.156 | 0 |
| ADI | 359.33 | 362.21 | 0.276 | 0 |
| FANG | 191.49 | 194.51 | 0.461 | 0 |
| CTAS | 197.59 | 199.47 | 0.555 | 0 |
| BA | 197.02 | 202.05 | 1.003 | 0 |

## Swing-Hoch ueberwunden (12)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 145.65 | 8.083 | 7 |
| META | 593.34 | 673.33 | 3.752 | 7 |
| CRWD | 218.31 | 241.41 | 1.525 | 7 |
| FRE.DE | 45.2 | 46.055 | 0.847 | 8 |
| ILMN | 221.76 | 228.96 | 0.769 | 7 |
| TRV | 376.57 | 378.95 | 0.378 | 6 |
| GILD | 146.75 | 147.72 | 0.29 | 7 |
| DDOG | 227.58 | 230.83 | 0.279 | 7 |
| DHL.DE | 55.7 | 55.92 | 0.25 | 7 |
| AAPL | 330.81 | 332.5 | 0.22 | 7 |
| WDAY | 185.82 | 187.7 | 0.22 | 7 |
| QIA.DE | 37.24 | 37.27 | 0.031 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.