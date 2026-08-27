# Stundenwache

Stand: 2026-08-27 · 158 Werte mit Stundendaten · erstellt 2026-08-27 20:56 UTC

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
| DIS | 106.75 | 106.81 | 0.026 | 0 |
| HD | 327.89 | 328.59 | 0.084 | 0 |
| BKNG | 201.76 | 202.5 | 0.121 | 0 |
| NKE | 38.1738 | 38.43 | 0.228 | 0 |
| GS | 1035.215 | 1040.9399 | 0.252 | 0 |
| BAYN.DE | 48.28 | 48.54 | 0.266 | 0 |
| JNJ | 263.84 | 265.77 | 0.369 | 0 |
| ADP | 279.31 | 284.68 | 0.901 | 0 |

## Swing-Hoch ueberwunden (30)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| SNPS | 401.98 | 464.97 | 4.411 | 7 |
| MRNA | 65.525 | 142.75 | 3.999 | 7 |
| CRM | 213.17 | 251.96 | 3.724 | 7 |
| CRWD | 195.4 | 227.95 | 2.851 | 7 |
| CDNS | 319.78 | 347.62 | 2.803 | 7 |
| ILMN | 203.75 | 227.73 | 2.701 | 7 |
| HEI.DE | 161.75 | 168.85 | 1.863 | 9 |
| DB1.DE | 280.7 | 288.7 | 1.652 | 9 |
| MSFT | 489.3 | 504.88 | 1.585 | 7 |
| PYPL | 59.44 | 61.45 | 1.458 | 7 |
| CDW | 142.97 | 148.97 | 1.016 | 7 |
| ADSK | 260.74 | 270.6 | 1.004 | 7 |
| ADBE | 279.0 | 289.14 | 0.948 | 7 |
| FTNT | 167.19 | 172.79 | 0.912 | 6 |
| HNR1.DE | 252.4 | 255.8 | 0.908 | 9 |
| TEAM | 177.88 | 185.63 | 0.882 | 7 |
| PLTR | 179.87 | 185.9 | 0.837 | 7 |
| WDAY | 185.82 | 193.75 | 0.723 | 7 |
| ORCL | 148.35 | 151.9399 | 0.565 | 5 |
| DBK.DE | 34.1 | 34.46 | 0.547 | 9 |
| WBD | 28.68 | 28.855 | 0.426 | 7 |
| INTC | 90.18 | 92.07 | 0.399 | 6 |
| ROP | 418.75 | 422.66 | 0.383 | 7 |
| SAP.DE | 188.4 | 190.58 | 0.383 | 2 |
| BMW.DE | 59.6 | 59.88 | 0.227 | 2 |
| CTSH | 63.3 | 63.77 | 0.216 | 7 |
| MCHP | 75.32 | 75.5 | 0.065 | 1 |
| NVDA | 227.92 | 228.05 | 0.02 | 3 |
| IFX.DE | 56.92 | 56.95 | 0.013 | 8 |
| IBM | 238.72 | 238.74 | 0.003 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.