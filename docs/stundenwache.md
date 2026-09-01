# Stundenwache

Stand: 2026-08-31 · 158 Werte mit Stundendaten · erstellt 2026-09-01 06:53 UTC

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (5)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| VNA.DE | 19.685 | 19.27 | -1.288 | 9 |
| AIR.DE | 202.3 | 197.98 | -1.217 | 9 |
| ENR.DE | 147.94 | 142.16 | -1.062 | 9 |
| ASML | 1476.4 | 1447.0 | -0.635 | 3 |
| BEI.DE | 79.76 | 79.3 | -0.314 | 7 |

## Tief zurueckerobert (3)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| FRE.DE | 45.54 | 45.635 | 0.123 | 6 |
| MTX.DE | 351.5 | 352.6 | 0.134 | 1 |
| MCHP | 72.91 | 73.44 | 0.208 | 1 |

## Tief angetestet (15)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKNG | 198.85 | 199.07 | 0.036 | 0 |
| DASH | 231.215 | 231.74 | 0.071 | 0 |
| SBUX | 106.01 | 106.24 | 0.09 | 0 |
| CSX | 50.36 | 50.51 | 0.173 | 0 |
| MDLZ | 61.83 | 62.06 | 0.204 | 0 |
| ADP | 284.93 | 286.23 | 0.23 | 0 |
| HON | 212.22 | 213.52 | 0.244 | 0 |
| ARM | 238.095 | 241.92 | 0.254 | 0 |
| ABNB | 181.84 | 183.24 | 0.263 | 0 |
| KDP | 31.6 | 31.87 | 0.326 | 0 |
| TTWO | 216.76 | 219.7 | 0.336 | 0 |
| GOOGL | 337.16 | 339.28 | 0.344 | 0 |
| ODFL | 196.41 | 199.95 | 0.64 | 0 |
| ISRG | 366.73 | 376.87 | 0.968 | 0 |
| VRTX | 532.23 | 545.39 | 0.969 | 0 |

## Swing-Hoch ueberwunden (32)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 257.62 | 3.985 | 7 |
| MRNA | 65.525 | 140.41 | 3.678 | 7 |
| CRWD | 195.4 | 231.04 | 2.856 | 7 |
| SNPS | 401.98 | 439.73 | 2.399 | 7 |
| BMW.DE | 59.6 | 62.36 | 2.047 | 9 |
| CDNS | 319.78 | 338.84 | 1.968 | 7 |
| MSFT | 489.3 | 507.32 | 1.836 | 7 |
| TEAM | 177.88 | 194.15 | 1.802 | 7 |
| MBG.DE | 45.62 | 47.065 | 1.734 | 9 |
| DB1.DE | 280.7 | 287.9 | 1.546 | 9 |
| HNR1.DE | 252.4 | 258.0 | 1.49 | 9 |
| CDW | 142.97 | 151.61 | 1.351 | 7 |
| ADBE | 279.0 | 292.75 | 1.338 | 7 |
| VOW3.DE | 75.96 | 78.0 | 1.184 | 9 |
| WDAY | 185.82 | 197.45 | 1.054 | 7 |
| HEI.DE | 161.75 | 165.55 | 0.975 | 9 |
| QCOM | 166.5 | 170.48 | 0.824 | 7 |
| DBK.DE | 34.1 | 34.635 | 0.804 | 9 |
| PAH3.DE | 28.2 | 28.63 | 0.779 | 9 |
| BNR.DE | 62.12 | 62.96 | 0.598 | 9 |
| ROP | 418.75 | 424.67 | 0.594 | 7 |
| CTSH | 63.3 | 64.57 | 0.593 | 7 |
| FTNT | 167.19 | 170.94 | 0.57 | 7 |
| TTD | 13.42 | 13.725 | 0.54 | 7 |
| SAP.DE | 188.4 | 191.44 | 0.535 | 9 |
| CON.DE | 71.06 | 71.66 | 0.433 | 7 |
| BKR | 63.02 | 63.56 | 0.358 | 5 |
| P911.DE | 45.37 | 45.71 | 0.298 | 9 |
| BAS.DE | 52.76 | 52.95 | 0.204 | 9 |
| RWE.DE | 58.48 | 58.7 | 0.161 | 9 |
| TSLA | 366.5 | 367.92 | 0.105 | 3 |
| PAYX | 127.09 | 127.34 | 0.082 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.