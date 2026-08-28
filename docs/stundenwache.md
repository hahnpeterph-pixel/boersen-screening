# Stundenwache

Stand: 2026-08-27 · 158 Werte mit Stundendaten · erstellt 2026-08-28 07:40 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| PEP | 139.68 | 139.71 | 0.014 | 0 |
| CMCSA | 26.37 | 26.395 | 0.042 | 0 |
| KO | 88.96 | 89.05 | 0.065 | 0 |
| BKNG | 201.76 | 202.5 | 0.121 | 0 |
| DTE.DE | 28.28 | 28.37 | 0.188 | 0 |
| SHW | 343.04 | 345.09 | 0.272 | 0 |
| JPM | 352.23 | 354.05 | 0.354 | 0 |
| TRV | 366.14 | 369.32 | 0.471 | 0 |
| BKR | 60.87 | 62.1 | 0.783 | 0 |
| ADP | 279.31 | 284.68 | 0.901 | 0 |

## Swing-Hoch ueberwunden (35)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| SNPS | 401.98 | 464.97 | 4.411 | 7 |
| MRNA | 65.525 | 142.75 | 3.999 | 7 |
| CRM | 213.17 | 251.96 | 3.724 | 7 |
| CRWD | 195.4 | 227.95 | 2.851 | 7 |
| CDNS | 319.78 | 347.62 | 2.8 | 7 |
| ILMN | 203.75 | 227.73 | 2.701 | 7 |
| HEI.DE | 161.75 | 169.65 | 2.137 | 1 |
| DB1.DE | 280.7 | 290.2 | 1.962 | 1 |
| MSFT | 489.3 | 504.88 | 1.585 | 7 |
| PYPL | 59.44 | 61.45 | 1.458 | 7 |
| HNR1.DE | 252.4 | 257.2 | 1.282 | 1 |
| BMW.DE | 59.6 | 61.1 | 1.145 | 1 |
| CDW | 142.97 | 148.97 | 1.016 | 7 |
| ADSK | 260.74 | 270.6 | 1.004 | 7 |
| ADBE | 279.0 | 289.14 | 0.948 | 7 |
| FTNT | 167.19 | 172.79 | 0.912 | 6 |
| TEAM | 177.88 | 185.63 | 0.881 | 7 |
| PLTR | 179.87 | 185.9 | 0.837 | 7 |
| MBG.DE | 45.62 | 46.24 | 0.788 | 1 |
| SIE.DE | 286.55 | 290.15 | 0.774 | 1 |
| DBK.DE | 34.1 | 34.595 | 0.772 | 1 |
| WDAY | 185.82 | 193.75 | 0.721 | 7 |
| ORCL | 148.35 | 151.9399 | 0.565 | 5 |
| WBD | 28.68 | 28.855 | 0.426 | 7 |
| INTC | 90.18 | 92.07 | 0.399 | 6 |
| ROP | 418.75 | 422.66 | 0.383 | 7 |
| RWE.DE | 58.48 | 58.84 | 0.261 | 1 |
| IFX.DE | 56.92 | 57.42 | 0.228 | 1 |
| CTSH | 63.3 | 63.77 | 0.216 | 7 |
| SAP.DE | 188.4 | 189.48 | 0.192 | 1 |
| P911.DE | 45.37 | 45.57 | 0.182 | 1 |
| MCHP | 75.32 | 75.5 | 0.065 | 1 |
| PAH3.DE | 28.2 | 28.23 | 0.053 | 1 |
| NVDA | 227.92 | 228.05 | 0.02 | 3 |
| IBM | 238.72 | 238.74 | 0.003 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.