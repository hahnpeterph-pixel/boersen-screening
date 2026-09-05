# Stundenwache

Stand: 2026-09-04 · 158 Werte mit Stundendaten · erstellt 2026-09-05 08:56 UTC

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
| RHM.DE | 1055.4 | 1033.0 | -0.628 | 8 |
| SRT3.DE | 241.4 | 238.4 | -0.387 | 5 |
| FRE.DE | 44.0 | 43.685 | -0.376 | 9 |
| MRK.DE | 136.9 | 136.1 | -0.327 | 9 |
| SY1.DE | 90.56 | 90.42 | -0.08 | 3 |

## Tief zurueckerobert (3)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| BEI.DE | 76.38 | 76.4 | 0.013 | 8 |
| QIA.DE | 37.18 | 37.38 | 0.157 | 1 |
| BNR.DE | 60.66 | 61.3 | 0.454 | 1 |

## Tief angetestet (10)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MCD | 255.49 | 255.7 | 0.049 | 0 |
| DIS | 105.17 | 105.29 | 0.053 | 0 |
| ROP | 405.57 | 407.22 | 0.163 | 0 |
| XEL | 75.45 | 75.73 | 0.207 | 0 |
| TMUS | 180.65 | 181.53 | 0.215 | 0 |
| UNH | 395.2 | 397.2 | 0.263 | 0 |
| CHTR | 149.47 | 151.98 | 0.323 | 0 |
| CSGP | 30.32 | 30.91 | 0.448 | 0 |
| CTAS | 198.01 | 200.44 | 0.731 | 0 |
| SNPS | 380.33 | 393.78 | 0.773 | 0 |

## Swing-Hoch ueberwunden (27)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 145.54 | 3.51 | 7 |
| HNR1.DE | 252.4 | 260.8 | 2.661 | 9 |
| VOW3.DE | 78.36 | 81.42 | 1.482 | 9 |
| CDW | 142.97 | 152.42 | 1.431 | 7 |
| CEG | 285.26 | 298.95 | 1.425 | 7 |
| CBK.DE | 41.05 | 42.05 | 1.273 | 9 |
| META | 593.34 | 616.75 | 1.252 | 7 |
| MUV2.DE | 520.4 | 528.6 | 1.16 | 9 |
| WDAY | 185.82 | 195.65 | 1.125 | 7 |
| MU | 969.44 | 1014.95 | 0.975 | 7 |
| AMD | 462.21 | 477.45 | 0.825 | 7 |
| DBK.DE | 35.03 | 35.62 | 0.8 | 9 |
| BAS.DE | 52.76 | 53.5 | 0.795 | 9 |
| ORCL | 153.99 | 158.765 | 0.768 | 7 |
| PAH3.DE | 28.76 | 29.12 | 0.559 | 9 |
| INTC | 93.7 | 95.81 | 0.496 | 7 |
| TTD | 14.17 | 14.44 | 0.472 | 7 |
| SPGI | 439.02 | 443.465 | 0.374 | 7 |
| AEP | 123.85 | 124.495 | 0.309 | 7 |
| BKR | 63.02 | 63.49 | 0.308 | 3 |
| WMT | 106.6 | 107.14 | 0.191 | 7 |
| ADI | 360.77 | 362.33 | 0.142 | 6 |
| NXPI | 227.24 | 227.85 | 0.109 | 6 |
| BMW.DE | 62.72 | 62.84 | 0.082 | 7 |
| TXN | 258.04 | 258.45 | 0.052 | 5 |
| JPM | 358.35 | 358.61 | 0.045 | 2 |
| KDP | 32.55 | 32.58 | 0.044 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.