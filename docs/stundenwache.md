# Stundenwache

Stand: 2026-09-04 · 158 Werte mit Stundendaten · erstellt 2026-09-08 00:28 UTC

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (7)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| HNR1.DE | 260.4 | 253.8 | -2.129 | 9 |
| SRT3.DE | 237.2 | 233.0 | -0.534 | 9 |
| QIA.DE | 36.845 | 36.35 | -0.379 | 9 |
| SY1.DE | 90.0 | 89.5 | -0.292 | 5 |
| RHM.DE | 1032.0 | 1021.6 | -0.287 | 7 |
| MRK.DE | 135.1 | 134.5 | -0.234 | 9 |
| DTE.DE | 28.21 | 28.19 | -0.037 | 7 |

## Tief zurueckerobert (3)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SHL.DE | 38.52 | 38.72 | 0.303 | 2 |
| FRE.DE | 43.21 | 43.485 | 0.33 | 7 |
| BNR.DE | 60.4 | 60.88 | 0.341 | 1 |

## Tief angetestet (12)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCD | 255.49 | 255.7 | 0.049 | 0 |
| DIS | 105.17 | 105.29 | 0.053 | 0 |
| ROP | 405.57 | 407.22 | 0.163 | 0 |
| XEL | 75.45 | 75.73 | 0.207 | 0 |
| TMUS | 180.65 | 181.53 | 0.215 | 0 |
| UNH | 395.2 | 397.2 | 0.263 | 0 |
| SAP.DE | 180.72 | 182.22 | 0.268 | 0 |
| BAYN.DE | 48.42 | 48.71 | 0.279 | 0 |
| CHTR | 149.47 | 151.98 | 0.323 | 0 |
| CSGP | 30.32 | 30.91 | 0.448 | 0 |
| CTAS | 198.01 | 200.44 | 0.731 | 0 |
| SNPS | 380.33 | 393.78 | 0.773 | 0 |

## Swing-Hoch ueberwunden (26)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 145.54 | 3.51 | 7 |
| CBK.DE | 41.05 | 42.92 | 2.23 | 9 |
| CDW | 142.97 | 152.42 | 1.431 | 7 |
| CEG | 285.26 | 298.95 | 1.425 | 7 |
| META | 593.34 | 616.75 | 1.252 | 7 |
| WDAY | 185.82 | 195.65 | 1.125 | 7 |
| MU | 969.44 | 1014.95 | 0.975 | 7 |
| IFX.DE | 58.42 | 60.5 | 0.959 | 9 |
| VOW3.DE | 78.36 | 80.68 | 0.927 | 9 |
| AMD | 462.21 | 477.45 | 0.825 | 7 |
| ORCL | 153.99 | 158.765 | 0.768 | 7 |
| DBK.DE | 35.03 | 35.5 | 0.64 | 9 |
| INTC | 93.7 | 95.81 | 0.496 | 7 |
| TTD | 14.17 | 14.44 | 0.472 | 7 |
| MBG.DE | 47.75 | 48.14 | 0.405 | 7 |
| SPGI | 439.02 | 443.465 | 0.374 | 7 |
| AEP | 123.85 | 124.495 | 0.309 | 7 |
| BKR | 63.02 | 63.49 | 0.308 | 3 |
| CON.DE | 72.24 | 72.58 | 0.208 | 4 |
| WMT | 106.6 | 107.14 | 0.191 | 7 |
| ADI | 360.77 | 362.33 | 0.142 | 6 |
| NXPI | 227.24 | 227.85 | 0.109 | 6 |
| PAH3.DE | 28.76 | 28.82 | 0.081 | 7 |
| TXN | 258.04 | 258.45 | 0.052 | 5 |
| JPM | 358.35 | 358.61 | 0.045 | 2 |
| KDP | 32.55 | 32.58 | 0.044 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.