# Stundenwache

Stand: 2026-11-06 · 272 Werte mit Stundendaten · erstellt 2026-11-06 23:44 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| GS | 892.1 | 865.54 | -0.926 | 7 |
| C | 121.43 | 119.06 | -0.67 | 7 |
| MS | 183.91 | 181.44 | -0.404 | 5 |
| COF | 202.06 | 201.87 | -0.029 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (18)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKNG | 160.59 | 160.64 | 0.007 | 0 |
| CNQ | 48.425 | 48.53 | 0.065 | 0 |
| UNP | 289.56 | 290.13 | 0.075 | 0 |
| RY | 200.805 | 201.13 | 0.091 | 0 |
| NOW | 100.5501 | 101.95 | 0.179 | 0 |
| LMT | 562.12 | 567.11 | 0.211 | 0 |
| MMM | 183.595 | 185.17 | 0.26 | 0 |
| BNS | 91.14 | 91.72 | 0.319 | 0 |
| SMFG | 2954.5 | 2992.5 | 0.326 | 0 |
| CM | 114.31 | 115.19 | 0.334 | 0 |
| ACN | 255.61 | 260.51 | 0.418 | 0 |
| DUK | 126.74 | 127.79 | 0.438 | 0 |
| BMY | 61.33 | 62.13 | 0.447 | 0 |
| IBM | 240.426 | 244.95 | 0.556 | 0 |
| GD | 349.01 | 354.12 | 0.569 | 0 |
| MA | 639.04 | 652.64 | 0.85 | 0 |
| V | 413.0 | 422.73 | 1.009 | 0 |
| MCD | 269.125 | 276.42 | 1.109 | 0 |

## Swing-Hoch ueberwunden (17)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| APP | 264.045 | 391.25 | 5.985 | 7 |
| QIA.DE | 42.345 | 45.2 | 5.181 | 9 |
| IBN | 1404.9 | 1571.2 | 4.866 | 7 |
| FRE.DE | 47.295 | 52.23 | 4.452 | 9 |
| HDB | 734.9 | 788.25 | 2.947 | 7 |
| SHL.DE | 42.06 | 44.57 | 2.482 | 9 |
| TM | 3115.0 | 3340.0 | 2.077 | 7 |
| NEM | 110.83 | 120.9 | 2.058 | 7 |
| ABNB | 180.06 | 190.02 | 1.495 | 7 |
| WDAY | 185.82 | 192.91 | 0.899 | 7 |
| BABA | 101.6 | 104.9 | 0.813 | 7 |
| SCHW | 89.96 | 91.49 | 0.797 | 7 |
| UBS | 38.96 | 39.61 | 0.609 | 9 |
| AMZN | 255.36 | 259.35 | 0.409 | 7 |
| TTWO | 212.16 | 214.78 | 0.378 | 7 |
| VRSK | 201.65 | 204.62 | 0.343 | 7 |
| SONY | 4068.0 | 4107.0 | 0.289 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.