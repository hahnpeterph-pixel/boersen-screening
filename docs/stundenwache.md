# Stundenwache

Stand: 2026-08-25 · 158 Werte mit Stundendaten · erstellt 2026-08-25 17:40 UTC

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter

## Tief gebrochen (3)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ODFL | 198.19 | 198.1 | -0.015 | 1 |
| CRWD | 183.76 | 183.64 | -0.013 | 1 |
| MCD | 268.91 | 268.875 | -0.007 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PANW | 339.521 | 339.55 | 0.002 | 0 |
| CTAS | 203.61 | 204.15 | 0.139 | 0 |
| PG | 144.96 | 145.3 | 0.151 | 0 |
| LULU | 117.12 | 118.4895 | 0.314 | 0 |
| DTE.DE | 28.9 | 29.11 | 0.342 | 0 |
| ADP | 279.31 | 281.655 | 0.397 | 0 |
| NKE | 39.03 | 39.685 | 0.587 | 0 |
| SAP.DE | 182.74 | 185.9 | 0.599 | 0 |
| SPGI | 423.9 | 432.175 | 0.883 | 0 |

## Swing-Hoch ueberwunden (31)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRK | 131.09 | 155.4 | 5.335 | 5 |
| MRNA | 65.525 | 159.31 | 5.152 | 5 |
| VZ | 47.45 | 50.17 | 3.424 | 5 |
| V | 365.14 | 382.475 | 2.742 | 5 |
| ILMN | 203.75 | 225.905 | 2.386 | 5 |
| AMGN | 420.26 | 444.335 | 2.358 | 5 |
| DIS | 107.11 | 111.35 | 1.887 | 5 |
| PYPL | 59.44 | 62.135 | 1.851 | 5 |
| DASH | 219.53 | 232.71 | 1.561 | 5 |
| MELI | 1874.98 | 1995.3149 | 1.525 | 5 |
| SY1.DE | 90.1 | 92.38 | 1.479 | 9 |
| DB1.DE | 280.7 | 288.0 | 1.458 | 9 |
| NFLX | 78.73 | 81.99 | 1.429 | 5 |
| ALV.DE | 443.5 | 450.6 | 1.322 | 9 |
| CTSH | 60.09 | 62.855 | 1.195 | 5 |
| CMCSA | 26.49 | 27.19 | 1.186 | 5 |
| CDNS | 319.78 | 329.49 | 1.069 | 5 |
| AZN | 165.91 | 169.09 | 1.045 | 5 |
| WDAY | 185.82 | 194.87 | 0.802 | 5 |
| VRTX | 546.17 | 554.38 | 0.493 | 5 |
| WBD | 28.68 | 28.865 | 0.407 | 5 |
| HNR1.DE | 252.4 | 253.8 | 0.337 | 7 |
| LIN | 483.49 | 486.125 | 0.331 | 5 |
| HEI.DE | 161.75 | 162.7 | 0.283 | 4 |
| SNPS | 401.98 | 404.745 | 0.257 | 4 |
| TSLA | 351.26 | 353.2925 | 0.169 | 5 |
| ABNB | 189.2 | 189.94 | 0.105 | 5 |
| MNST | 47.98 | 48.61 | 0.058 | 5 |
| MSFT | 489.3 | 489.75 | 0.048 | 4 |
| GS | 1054.63 | 1055.4351 | 0.035 | 2 |
| GOOGL | 346.73 | 346.835 | 0.017 | 2 |

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.