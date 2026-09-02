# Stundenwache

Stand: 2026-09-02 · 158 Werte mit Stundendaten · erstellt 2026-09-02 21:40 UTC

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

## Tief angetestet (8)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AMAT | 433.57 | 438.57 | 0.223 | 0 |
| XEL | 75.06 | 75.49 | 0.331 | 0 |
| CSCO | 108.3993 | 109.44 | 0.348 | 0 |
| PEP | 139.33 | 140.55 | 0.546 | 0 |
| DASH | 222.11 | 226.23 | 0.558 | 0 |
| RWE.DE | 57.28 | 58.08 | 0.57 | 0 |
| SRT3.DE | 241.4 | 246.9 | 0.706 | 0 |
| AIR.DE | 193.74 | 196.92 | 0.83 | 0 |

## Swing-Hoch ueberwunden (21)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 150.81 | 3.934 | 7 |
| CRM | 213.17 | 257.22 | 3.907 | 7 |
| HNR1.DE | 252.4 | 259.6 | 2.136 | 9 |
| WDAY | 185.82 | 200.82 | 1.326 | 7 |
| BKR | 63.02 | 64.621 | 1.017 | 7 |
| CDW | 142.97 | 148.67 | 0.897 | 7 |
| MBG.DE | 45.62 | 46.305 | 0.763 | 9 |
| TTD | 14.17 | 14.54 | 0.68 | 6 |
| BAS.DE | 52.76 | 53.39 | 0.663 | 9 |
| REGN | 839.94 | 852.23 | 0.622 | 5 |
| CEG | 285.26 | 290.1 | 0.54 | 3 |
| KHC | 26.01 | 26.265 | 0.414 | 6 |
| AAPL | 322.37 | 324.99 | 0.389 | 7 |
| CHTR | 156.14 | 159.05 | 0.376 | 5 |
| PG | 146.8 | 147.645 | 0.374 | 6 |
| MUV2.DE | 520.4 | 523.0 | 0.36 | 9 |
| TMUS | 185.84 | 187.31 | 0.357 | 7 |
| JNJ | 273.98 | 275.31 | 0.244 | 7 |
| NFLX | 82.35 | 82.72 | 0.171 | 5 |
| NXPI | 227.24 | 227.88 | 0.114 | 7 |
| VRTX | 555.69 | 556.9 | 0.091 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.