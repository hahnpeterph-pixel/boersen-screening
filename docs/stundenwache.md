# Stundenwache

Stand: 2026-08-27 · 158 Werte mit Stundendaten · erstellt 2026-08-28 07:14 UTC

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (3)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DTE.DE | 28.9 | 28.22 | -1.392 | 9 |
| HEN3.DE | 75.58 | 75.48 | -0.086 | 9 |
| MUV2.DE | 515.0 | 514.8 | -0.022 | 5 |

## Tief zurueckerobert (4)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SHL.DE | 39.19 | 39.27 | 0.122 | 8 |
| BNR.DE | 60.12 | 60.38 | 0.165 | 3 |
| MBG.DE | 44.52 | 45.615 | 1.553 | 1 |
| VOW3.DE | 72.14 | 75.2 | 1.993 | 1 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| PEP | 139.68 | 139.71 | 0.014 | 0 |
| CMCSA | 26.37 | 26.395 | 0.042 | 0 |
| KO | 88.96 | 89.05 | 0.065 | 0 |
| BKNG | 201.76 | 202.5 | 0.121 | 0 |
| BAS.DE | 51.16 | 51.38 | 0.241 | 0 |
| SHW | 343.04 | 345.09 | 0.272 | 0 |
| JPM | 352.23 | 354.05 | 0.354 | 0 |
| TRV | 366.14 | 369.32 | 0.471 | 0 |
| ADS.DE | 150.7 | 153.15 | 0.578 | 0 |
| VNA.DE | 19.7 | 19.92 | 0.634 | 0 |
| BKR | 60.87 | 62.1 | 0.783 | 0 |
| ADP | 279.31 | 284.68 | 0.901 | 0 |
| PAH3.DE | 27.09 | 27.88 | 1.455 | 0 |
| P911.DE | 42.93 | 44.9 | 1.937 | 0 |
| BMW.DE | 57.56 | 59.88 | 2.002 | 0 |

## Swing-Hoch ueberwunden (32)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| SNPS | 401.98 | 464.97 | 4.411 | 7 |
| MRNA | 65.525 | 142.75 | 3.999 | 7 |
| CRM | 213.17 | 251.96 | 3.724 | 7 |
| CRWD | 195.4 | 227.95 | 2.851 | 7 |
| CDNS | 319.78 | 347.62 | 2.8 | 7 |
| ILMN | 203.75 | 227.73 | 2.701 | 7 |
| HEI.DE | 161.75 | 168.85 | 1.886 | 9 |
| DB1.DE | 280.7 | 288.7 | 1.6 | 9 |
| MSFT | 489.3 | 504.88 | 1.585 | 7 |
| PYPL | 59.44 | 61.45 | 1.458 | 7 |
| CDW | 142.97 | 148.97 | 1.016 | 7 |
| ADSK | 260.74 | 270.6 | 1.004 | 7 |
| SY1.DE | 90.1 | 91.66 | 0.978 | 9 |
| ADBE | 279.0 | 289.14 | 0.948 | 7 |
| FTNT | 167.19 | 172.79 | 0.912 | 6 |
| TEAM | 177.88 | 185.63 | 0.881 | 7 |
| HNR1.DE | 252.4 | 255.8 | 0.856 | 9 |
| PLTR | 179.87 | 185.9 | 0.837 | 7 |
| WDAY | 185.82 | 193.75 | 0.721 | 7 |
| ORCL | 148.35 | 151.9399 | 0.565 | 5 |
| DBK.DE | 34.1 | 34.46 | 0.538 | 9 |
| WBD | 28.68 | 28.855 | 0.426 | 7 |
| INTC | 90.18 | 92.07 | 0.399 | 6 |
| SAP.DE | 188.4 | 190.58 | 0.394 | 2 |
| ROP | 418.75 | 422.66 | 0.383 | 7 |
| BMW.DE | 59.6 | 59.88 | 0.242 | 2 |
| ALV.DE | 443.5 | 444.6 | 0.218 | 9 |
| CTSH | 63.3 | 63.77 | 0.216 | 7 |
| MCHP | 75.32 | 75.5 | 0.065 | 1 |
| NVDA | 227.92 | 228.05 | 0.02 | 3 |
| IFX.DE | 56.92 | 56.95 | 0.013 | 8 |
| IBM | 238.72 | 238.74 | 0.003 | 4 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.