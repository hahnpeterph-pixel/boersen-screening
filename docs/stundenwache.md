# Stundenwache

Stand: 2026-08-26 · 158 Werte mit Stundendaten · erstellt 2026-08-26 19:33 UTC

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

## Tief angetestet (5)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| REGN | 816.63 | 817.42 | 0.041 | 0 |
| ABNB | 187.9 | 188.27 | 0.053 | 0 |
| VNA.DE | 19.71 | 19.765 | 0.159 | 0 |
| LULU | 115.87 | 116.81 | 0.22 | 0 |
| FANG | 196.65 | 199.54 | 0.496 | 0 |

## Swing-Hoch ueberwunden (31)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRK | 131.09 | 152.805 | 4.624 | 7 |
| MRNA | 65.525 | 146.1001 | 4.26 | 7 |
| VZ | 47.45 | 50.255 | 3.626 | 7 |
| V | 365.14 | 383.62 | 2.938 | 7 |
| HEI.DE | 161.75 | 172.0 | 2.723 | 9 |
| ILMN | 203.75 | 224.04 | 2.271 | 7 |
| DASH | 219.53 | 237.48 | 2.207 | 7 |
| SY1.DE | 90.1 | 93.2 | 1.943 | 9 |
| PYPL | 59.44 | 61.905 | 1.766 | 7 |
| ALV.DE | 443.5 | 452.0 | 1.681 | 9 |
| CDNS | 319.78 | 333.8001 | 1.459 | 7 |
| NFLX | 78.73 | 81.765 | 1.366 | 7 |
| MELI | 1874.98 | 1961.535 | 1.202 | 7 |
| CBK.DE | 40.13 | 40.92 | 1.177 | 9 |
| DIS | 107.11 | 109.575 | 1.132 | 7 |
| CMCSA | 26.49 | 27.135 | 1.107 | 7 |
| DB1.DE | 280.7 | 286.2 | 1.1 | 9 |
| LIN | 483.49 | 491.52 | 1.031 | 7 |
| DBK.DE | 34.1 | 34.64 | 0.807 | 9 |
| HNR1.DE | 252.4 | 255.6 | 0.806 | 9 |
| MSFT | 489.3 | 496.23 | 0.762 | 7 |
| SNPS | 401.98 | 409.9006 | 0.712 | 7 |
| SIE.DE | 286.55 | 288.75 | 0.434 | 9 |
| WDAY | 185.82 | 190.345 | 0.405 | 7 |
| AMD | 477.36 | 482.07 | 0.237 | 7 |
| CSCO | 112.19 | 112.895 | 0.206 | 3 |
| WBD | 28.68 | 28.765 | 0.2 | 7 |
| VRTX | 546.17 | 548.63 | 0.151 | 7 |
| ORCL | 148.35 | 149.0799 | 0.117 | 2 |
| SBUX | 107.81 | 107.91 | 0.039 | 2 |
| CSX | 52.0 | 52.01 | 0.012 | 5 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.