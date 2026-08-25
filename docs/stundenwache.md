# Stundenwache

Stand: 2026-08-25 · 158 Werte mit Stundendaten · erstellt 2026-08-25 17:46 UTC

> **Sitzung noch nicht abgeschlossen.** 118 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| CTAS | 203.61 | 204.15 | 0.139 | 0 |
| PG | 144.96 | 145.38 | 0.187 | 0 |
| LULU | 117.12 | 118.6 | 0.34 | 0 |
| DTE.DE | 28.9 | 29.11 | 0.342 | 0 |
| ADP | 279.31 | 282.04 | 0.462 | 0 |
| NKE | 39.03 | 39.68 | 0.583 | 0 |
| SAP.DE | 182.74 | 185.9 | 0.599 | 0 |
| SPGI | 423.9 | 432.025 | 0.867 | 0 |

## Swing-Hoch ueberwunden (30)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRK | 131.09 | 155.6 | 5.356 | 5 |
| MRNA | 65.525 | 157.9444 | 5.074 | 5 |
| VZ | 47.45 | 50.19 | 3.45 | 5 |
| V | 365.14 | 382.58 | 2.759 | 5 |
| ILMN | 203.75 | 226.22 | 2.42 | 5 |
| AMGN | 420.26 | 444.845 | 2.408 | 5 |
| DIS | 107.11 | 111.44 | 1.927 | 5 |
| PYPL | 59.44 | 62.215 | 1.906 | 5 |
| MELI | 1874.98 | 1998.995 | 1.572 | 5 |
| NFLX | 78.73 | 82.23 | 1.534 | 5 |
| DASH | 219.53 | 232.455 | 1.531 | 5 |
| SY1.DE | 90.1 | 92.38 | 1.479 | 9 |
| DB1.DE | 280.7 | 288.0 | 1.458 | 9 |
| ALV.DE | 443.5 | 450.6 | 1.322 | 9 |
| CMCSA | 26.49 | 27.225 | 1.245 | 5 |
| CTSH | 60.09 | 62.92 | 1.223 | 5 |
| AZN | 165.91 | 169.345 | 1.128 | 5 |
| CDNS | 319.78 | 329.09 | 1.025 | 5 |
| WDAY | 185.82 | 195.02 | 0.815 | 5 |
| VRTX | 546.17 | 554.23 | 0.484 | 5 |
| WBD | 28.68 | 28.88 | 0.44 | 5 |
| HNR1.DE | 252.4 | 253.8 | 0.337 | 7 |
| LIN | 483.49 | 486.14 | 0.332 | 5 |
| HEI.DE | 161.75 | 162.7 | 0.283 | 4 |
| SNPS | 401.98 | 404.34 | 0.219 | 4 |
| TSLA | 351.26 | 353.21 | 0.162 | 5 |
| ABNB | 189.2 | 190.07 | 0.124 | 5 |
| MSFT | 489.3 | 490.025 | 0.078 | 4 |
| MNST | 47.98 | 48.59 | 0.056 | 5 |
| GS | 1054.63 | 1055.04 | 0.018 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.