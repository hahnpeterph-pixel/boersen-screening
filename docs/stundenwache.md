# Stundenwache

Stand: 2026-08-31 · 158 Werte mit Stundendaten · erstellt 2026-09-01 07:17 UTC

> **Sitzung noch nicht abgeschlossen.** 39 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 1, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| RHM.DE | 1087.6 | 1086.6 | -0.024 | 1 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCHP | 72.91 | 73.44 | 0.208 | 1 |

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BKNG | 198.85 | 199.07 | 0.037 | 0 |
| SBUX | 106.01 | 106.24 | 0.09 | 0 |
| CSX | 50.36 | 50.51 | 0.173 | 0 |
| MDLZ | 61.83 | 62.06 | 0.204 | 0 |
| HON | 212.22 | 213.52 | 0.244 | 0 |
| ARM | 238.095 | 241.92 | 0.254 | 0 |
| ABNB | 181.84 | 183.24 | 0.263 | 0 |
| KDP | 31.6 | 31.87 | 0.326 | 0 |
| TTWO | 216.76 | 219.7 | 0.336 | 0 |
| GOOGL | 337.16 | 339.28 | 0.344 | 0 |
| ODFL | 196.41 | 199.95 | 0.64 | 0 |
| VRTX | 532.23 | 545.39 | 0.969 | 0 |

## Swing-Hoch ueberwunden (32)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| CRM | 213.17 | 257.62 | 3.985 | 7 |
| MRNA | 65.525 | 140.41 | 3.678 | 7 |
| CRWD | 195.4 | 231.04 | 2.856 | 7 |
| SNPS | 401.98 | 439.73 | 2.399 | 7 |
| MBG.DE | 45.62 | 47.375 | 2.066 | 1 |
| HNR1.DE | 252.4 | 259.6 | 1.953 | 1 |
| CDNS | 319.78 | 338.84 | 1.905 | 7 |
| MSFT | 489.3 | 507.32 | 1.836 | 7 |
| BMW.DE | 59.6 | 61.96 | 1.823 | 1 |
| TEAM | 177.88 | 194.15 | 1.802 | 7 |
| CDW | 142.97 | 151.61 | 1.423 | 7 |
| ADBE | 279.0 | 292.75 | 1.313 | 7 |
| VOW3.DE | 75.96 | 77.98 | 1.189 | 1 |
| WDAY | 185.82 | 197.45 | 1.054 | 7 |
| RWE.DE | 58.48 | 59.88 | 1.024 | 1 |
| QCOM | 166.5 | 170.48 | 0.824 | 7 |
| BAS.DE | 52.76 | 53.51 | 0.788 | 1 |
| BNR.DE | 62.12 | 63.22 | 0.78 | 1 |
| PAH3.DE | 28.2 | 28.61 | 0.767 | 1 |
| FTNT | 167.19 | 170.94 | 0.614 | 7 |
| ROP | 418.75 | 424.67 | 0.594 | 7 |
| CTSH | 63.3 | 64.57 | 0.593 | 7 |
| DBK.DE | 34.1 | 34.475 | 0.563 | 1 |
| TTD | 13.42 | 13.725 | 0.54 | 7 |
| BKR | 63.02 | 63.56 | 0.358 | 5 |
| MUV2.DE | 520.4 | 522.4 | 0.282 | 1 |
| HEN3.DE | 76.54 | 76.74 | 0.184 | 1 |
| SY1.DE | 93.96 | 94.24 | 0.167 | 1 |
| ADP | 285.59 | 286.23 | 0.112 | 7 |
| TSLA | 366.5 | 367.92 | 0.105 | 3 |
| PAYX | 127.09 | 127.34 | 0.082 | 2 |
| P911.DE | 45.37 | 45.44 | 0.063 | 1 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.