# Stundenwache

Stand: 2026-08-25 · 158 Werte mit Stundendaten · erstellt 2026-08-25 20:25 UTC

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
| MDLZ | 62.91 | 62.98 | 0.056 | 0 |
| ODFL | 197.86 | 198.34 | 0.077 | 0 |
| CRM | 204.78 | 205.71 | 0.121 | 0 |
| CTAS | 203.61 | 204.67 | 0.274 | 0 |
| LULU | 117.12 | 118.35 | 0.282 | 0 |
| DTE.DE | 28.9 | 29.11 | 0.342 | 0 |
| NKE | 39.03 | 39.47 | 0.395 | 0 |
| ADP | 279.31 | 282.79 | 0.587 | 0 |
| SAP.DE | 182.74 | 185.9 | 0.599 | 0 |
| SPGI | 423.9 | 432.98 | 0.968 | 0 |

## Swing-Hoch ueberwunden (31)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRK | 131.09 | 156.45 | 5.435 | 7 |
| MRNA | 65.525 | 158.87 | 5.097 | 7 |
| VZ | 47.45 | 50.22 | 3.481 | 7 |
| V | 365.14 | 384.02 | 2.96 | 7 |
| ILMN | 203.75 | 225.0 | 2.284 | 7 |
| AMGN | 420.26 | 442.19 | 2.148 | 7 |
| PYPL | 59.44 | 62.26 | 1.936 | 7 |
| DIS | 107.11 | 111.24 | 1.838 | 7 |
| DASH | 219.53 | 233.42 | 1.645 | 7 |
| MELI | 1874.98 | 1997.38 | 1.551 | 7 |
| NFLX | 78.73 | 82.255 | 1.539 | 7 |
| SY1.DE | 90.1 | 92.38 | 1.479 | 9 |
| DB1.DE | 280.7 | 288.0 | 1.458 | 9 |
| ALV.DE | 443.5 | 450.6 | 1.322 | 9 |
| CDNS | 319.78 | 331.84 | 1.295 | 7 |
| CTSH | 60.09 | 63.06 | 1.283 | 7 |
| AZN | 165.91 | 169.615 | 1.217 | 7 |
| CMCSA | 26.49 | 27.085 | 1.002 | 7 |
| WDAY | 185.82 | 194.33 | 0.753 | 7 |
| SNPS | 401.98 | 408.82 | 0.624 | 6 |
| LIN | 483.49 | 487.21 | 0.467 | 7 |
| WBD | 28.68 | 28.865 | 0.407 | 7 |
| VRTX | 546.17 | 552.88 | 0.402 | 7 |
| HNR1.DE | 252.4 | 253.8 | 0.337 | 7 |
| HEI.DE | 161.75 | 162.7 | 0.283 | 4 |
| MSFT | 489.3 | 491.55 | 0.239 | 6 |
| GS | 1054.63 | 1059.1066 | 0.192 | 4 |
| ABNB | 189.2 | 190.48 | 0.182 | 7 |
| AMD | 477.36 | 479.25 | 0.092 | 5 |
| MNST | 47.98 | 48.71 | 0.067 | 7 |
| GOOGL | 346.73 | 346.94 | 0.033 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.