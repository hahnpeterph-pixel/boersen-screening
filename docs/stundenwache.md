# Stundenwache

Stand: 2026-10-02 · 273 Werte mit Stundendaten · erstellt 2026-10-02 22:54 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| REGN | 741.83 | 735.73 | -0.285 | 7 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (17)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BIIB | 219.84 | 220.01 | 0.033 | 0 |
| ACN | 198.375 | 199.03 | 0.064 | 0 |
| ZS | 195.11 | 196.56 | 0.157 | 0 |
| GE | 308.2 | 309.55 | 0.159 | 0 |
| TM | 180.94 | 181.58 | 0.211 | 0 |
| BABA | 105.15 | 105.85 | 0.258 | 0 |
| CTAS | 191.86 | 193.02 | 0.289 | 0 |
| LULU | 93.435 | 94.46 | 0.296 | 0 |
| PM | 185.975 | 187.5 | 0.365 | 0 |
| DTG.DE | 40.405 | 40.75 | 0.367 | 0 |
| VRTX | 499.95 | 504.57 | 0.403 | 0 |
| KO | 85.17 | 85.665 | 0.431 | 0 |
| SPGI | 382.24 | 386.34 | 0.502 | 0 |
| WELL | 225.36 | 227.75 | 0.513 | 0 |
| LMT | 498.5501 | 505.52 | 0.617 | 0 |
| WDC | 396.57 | 415.12 | 0.713 | 0 |
| ABT | 95.06 | 97.51 | 1.221 | 0 |

## Swing-Hoch ueberwunden (43)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.93 | 6.545 | 7 |
| KLAC | 182.41 | 206.94 | 3.593 | 7 |
| AMAT | 487.68 | 540.04 | 2.916 | 7 |
| ON | 74.48 | 84.89 | 2.807 | 7 |
| SHOP | 134.74 | 151.39 | 2.557 | 7 |
| LRCX | 317.13 | 347.45 | 2.344 | 7 |
| SNPS | 445.92 | 490.05 | 2.344 | 7 |
| CDNS | 330.81 | 351.49 | 1.754 | 7 |
| IFX.DE | 60.48 | 64.38 | 1.574 | 9 |
| MPC | 398.33 | 422.5 | 1.396 | 7 |
| TXN | 284.39 | 293.81 | 1.229 | 7 |
| TSM | 461.87 | 472.91 | 1.12 | 7 |
| ADI | 405.38 | 417.185 | 1.09 | 7 |
| APH | 84.48 | 87.0 | 0.962 | 7 |
| CAT | 827.81 | 845.53 | 0.855 | 7 |
| MSFT | 509.44 | 517.86 | 0.711 | 7 |
| VLO | 395.85 | 406.3 | 0.58 | 6 |
| PSX | 259.11 | 264.63 | 0.568 | 6 |
| CRWD | 263.87 | 270.07 | 0.557 | 7 |
| NXPI | 239.83 | 243.76 | 0.544 | 7 |
| ASML | 1630.2 | 1653.6 | 0.513 | 8 |
| PBR | 21.34 | 21.645 | 0.51 | 3 |
| GEV | 973.41 | 988.79 | 0.474 | 7 |
| MRVL | 267.48 | 272.4 | 0.418 | 7 |
| GLW | 161.39 | 164.23 | 0.394 | 7 |
| GFS | 49.425 | 50.18 | 0.382 | 7 |
| EMR | 160.29 | 161.62 | 0.35 | 7 |
| MCHP | 80.37 | 81.32 | 0.345 | 7 |
| ODFL | 178.99 | 180.53 | 0.324 | 7 |
| SKHY | 192.83 | 195.11 | 0.292 | 6 |
| QIA.DE | 39.765 | 40.095 | 0.289 | 1 |
| CSCO | 111.5 | 112.19 | 0.261 | 3 |
| ORCL | 140.88 | 142.51 | 0.257 | 5 |
| SHEL | 95.85 | 96.23 | 0.228 | 5 |
| NVDA | 233.21 | 233.99 | 0.151 | 7 |
| CNQ | 48.28 | 48.455 | 0.148 | 5 |
| SPCX | 158.13 | 158.975 | 0.136 | 3 |
| AMZN | 250.88 | 251.53 | 0.121 | 3 |
| HON | 213.64 | 214.01 | 0.088 | 6 |
| HEI.DE | 147.55 | 147.75 | 0.045 | 4 |
| WDAY | 185.82 | 186.12 | 0.043 | 7 |
| FDX | 290.16 | 290.41 | 0.038 | 1 |
| XEL | 71.37 | 71.41 | 0.031 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.