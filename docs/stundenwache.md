# Stundenwache

Stand: 2026-09-04 · 158 Werte mit Stundendaten · erstellt 2026-09-07 08:19 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCD | 255.49 | 255.7 | 0.049 | 0 |
| DIS | 105.17 | 105.29 | 0.053 | 0 |
| SRT3.DE | 230.9 | 231.6 | 0.088 | 0 |
| ROP | 405.57 | 407.22 | 0.163 | 0 |
| XEL | 75.45 | 75.73 | 0.207 | 0 |
| TMUS | 180.65 | 181.53 | 0.215 | 0 |
| ALV.DE | 446.8 | 448.1 | 0.253 | 0 |
| UNH | 395.2 | 397.2 | 0.263 | 0 |
| CHTR | 149.47 | 151.98 | 0.323 | 0 |
| CSGP | 30.32 | 30.91 | 0.448 | 0 |
| CTAS | 198.01 | 200.44 | 0.731 | 0 |
| SNPS | 380.33 | 393.78 | 0.773 | 0 |

## Swing-Hoch ueberwunden (22)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 145.54 | 3.51 | 7 |
| CBK.DE | 41.05 | 42.48 | 1.727 | 2 |
| CDW | 142.97 | 152.42 | 1.431 | 7 |
| CEG | 285.26 | 298.95 | 1.425 | 7 |
| META | 593.34 | 616.75 | 1.252 | 7 |
| WDAY | 185.82 | 195.65 | 1.125 | 7 |
| MU | 969.44 | 1014.95 | 0.975 | 7 |
| AMD | 462.21 | 477.45 | 0.825 | 7 |
| ORCL | 153.99 | 158.765 | 0.768 | 7 |
| DBK.DE | 35.03 | 35.4 | 0.512 | 2 |
| INTC | 93.7 | 95.81 | 0.496 | 7 |
| TTD | 14.17 | 14.44 | 0.472 | 7 |
| SPGI | 439.02 | 443.465 | 0.374 | 7 |
| AEP | 123.85 | 124.495 | 0.309 | 7 |
| BKR | 63.02 | 63.49 | 0.308 | 3 |
| IFX.DE | 58.42 | 58.83 | 0.207 | 2 |
| WMT | 106.6 | 107.14 | 0.191 | 7 |
| ADI | 360.77 | 362.33 | 0.142 | 6 |
| NXPI | 227.24 | 227.85 | 0.109 | 6 |
| TXN | 258.04 | 258.45 | 0.052 | 5 |
| JPM | 358.35 | 358.61 | 0.045 | 2 |
| KDP | 32.55 | 32.58 | 0.044 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.