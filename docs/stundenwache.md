# Stundenwache

Stand: 2026-08-28 · 158 Werte mit Stundendaten · erstellt 2026-08-30 13:00 UTC

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

## Tief angetestet (14)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCHP | 72.91 | 72.94 | 0.011 | 0 |
| CAT | 799.17 | 800.12 | 0.036 | 0 |
| FAST | 49.73 | 49.785 | 0.056 | 0 |
| ROST | 228.15 | 228.54 | 0.057 | 0 |
| GS | 1031.58 | 1033.99 | 0.105 | 0 |
| ILMN | 214.61 | 215.61 | 0.107 | 0 |
| MNST | 46.38 | 46.865 | 0.114 | 0 |
| AIR.DE | 202.35 | 202.8 | 0.127 | 0 |
| ON | 72.05 | 72.6 | 0.187 | 0 |
| SHW | 343.0 | 344.88 | 0.256 | 0 |
| REGN | 789.08 | 794.06 | 0.277 | 0 |
| ASML | 1478.2 | 1492.4 | 0.29 | 0 |
| PCAR | 124.51 | 125.34 | 0.305 | 0 |
| MDLZ | 61.67 | 62.345 | 0.58 | 0 |

## Swing-Hoch ueberwunden (35)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 256.24 | 3.963 | 7 |
| MRNA | 65.525 | 137.9473 | 3.654 | 7 |
| SNPS | 401.98 | 442.83 | 2.671 | 7 |
| MSFT | 489.3 | 513.67 | 2.494 | 7 |
| BMW.DE | 59.6 | 62.62 | 2.444 | 9 |
| HEI.DE | 161.75 | 170.8 | 2.375 | 9 |
| DB1.DE | 280.7 | 291.25 | 2.178 | 9 |
| CDNS | 319.78 | 340.42 | 2.091 | 7 |
| CRWD | 195.4 | 218.4 | 1.945 | 7 |
| MBG.DE | 45.62 | 47.015 | 1.807 | 9 |
| WDAY | 185.82 | 204.46 | 1.601 | 7 |
| TEAM | 177.88 | 190.35 | 1.407 | 7 |
| HNR1.DE | 252.4 | 257.4 | 1.336 | 9 |
| DBK.DE | 34.1 | 34.925 | 1.252 | 9 |
| ADBE | 279.0 | 291.58 | 1.204 | 7 |
| PLTR | 179.87 | 186.25 | 0.929 | 7 |
| VOW3.DE | 75.96 | 77.4 | 0.867 | 7 |
| PAH3.DE | 28.2 | 28.67 | 0.841 | 5 |
| P911.DE | 45.37 | 46.21 | 0.766 | 9 |
| CDW | 142.97 | 147.7 | 0.762 | 7 |
| ROP | 418.75 | 426.22 | 0.736 | 7 |
| SIE.DE | 286.55 | 289.9 | 0.712 | 9 |
| SAP.DE | 188.4 | 191.92 | 0.618 | 9 |
| AMZN | 263.89 | 266.38 | 0.429 | 6 |
| SPGI | 439.02 | 442.89 | 0.402 | 7 |
| ORCL | 148.35 | 150.71 | 0.376 | 7 |
| RWE.DE | 58.48 | 58.96 | 0.358 | 9 |
| CTSH | 63.3 | 64.04 | 0.348 | 7 |
| ADP | 285.59 | 287.47 | 0.325 | 7 |
| SRT3.DE | 252.2 | 254.2 | 0.273 | 3 |
| TTD | 13.42 | 13.57 | 0.268 | 7 |
| WBD | 28.68 | 28.77 | 0.232 | 7 |
| IFX.DE | 56.92 | 57.1 | 0.08 | 8 |
| ALV.DE | 452.9 | 453.2 | 0.06 | 2 |
| SBUX | 107.81 | 107.82 | 0.004 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.