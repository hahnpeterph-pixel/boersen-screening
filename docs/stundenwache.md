# Stundenwache

Stand: 2026-09-02 · 158 Werte mit Stundendaten · erstellt 2026-09-03 09:34 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| AIR.DE | 193.4 | 193.34 | -0.016 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ADBE | 279.43 | 279.79 | 0.035 | 0 |
| VZ | 50.15 | 50.22 | 0.087 | 0 |
| AMAT | 433.57 | 438.57 | 0.223 | 0 |
| FAST | 47.65 | 47.96 | 0.31 | 0 |
| XEL | 75.06 | 75.49 | 0.331 | 0 |
| CSCO | 108.4 | 109.44 | 0.348 | 0 |
| PEP | 139.33 | 140.55 | 0.537 | 0 |
| DASH | 222.11 | 226.23 | 0.551 | 0 |
| HEN3.DE | 74.68 | 75.36 | 0.657 | 0 |

## Swing-Hoch ueberwunden (22)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 150.81 | 3.934 | 7 |
| CRM | 213.17 | 257.22 | 3.906 | 7 |
| HNR1.DE | 252.4 | 261.2 | 2.865 | 3 |
| WDAY | 185.82 | 200.82 | 1.326 | 7 |
| BKR | 63.02 | 64.621 | 0.967 | 7 |
| CDW | 142.97 | 148.67 | 0.907 | 7 |
| BAS.DE | 52.76 | 53.55 | 0.856 | 3 |
| MUV2.DE | 520.4 | 526.0 | 0.829 | 3 |
| TTD | 14.17 | 14.54 | 0.68 | 6 |
| REGN | 839.94 | 852.23 | 0.609 | 5 |
| CEG | 285.26 | 290.1 | 0.536 | 3 |
| AAPL | 322.37 | 324.99 | 0.389 | 7 |
| KHC | 26.01 | 26.265 | 0.382 | 6 |
| CHTR | 156.14 | 159.05 | 0.369 | 5 |
| PG | 146.8 | 147.645 | 0.369 | 6 |
| TMUS | 185.84 | 187.31 | 0.357 | 7 |
| JNJ | 273.98 | 275.31 | 0.244 | 7 |
| NFLX | 82.35 | 82.72 | 0.171 | 5 |
| NXPI | 227.24 | 227.88 | 0.114 | 7 |
| DBK.DE | 35.03 | 35.1 | 0.098 | 2 |
| VRTX | 555.69 | 556.9 | 0.091 | 2 |
| CBK.DE | 41.05 | 41.06 | 0.014 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.