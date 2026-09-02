# Stundenwache

Stand: 2026-09-01 · 158 Werte mit Stundendaten · erstellt 2026-09-02 00:14 UTC

> **Sitzung noch nicht abgeschlossen.** 1 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (16)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ODFL | 196.41 | 187.01 | -1.53 | 7 |
| SIE.DE | 284.5 | 278.6 | -1.279 | 9 |
| BEI.DE | 79.12 | 77.86 | -0.851 | 7 |
| ADS.DE | 151.4 | 148.2 | -0.798 | 8 |
| MTX.DE | 350.4 | 343.7 | -0.794 | 9 |
| RHM.DE | 1110.8 | 1079.6 | -0.79 | 9 |
| DHL.DE | 56.14 | 55.54 | -0.778 | 8 |
| FRE.DE | 45.245 | 44.795 | -0.58 | 5 |
| DB1.DE | 287.0 | 284.6 | -0.511 | 9 |
| AIR.DE | 197.22 | 195.82 | -0.376 | 9 |
| ASML | 1446.4 | 1430.6 | -0.351 | 3 |
| HEI.DE | 164.65 | 163.7 | -0.241 | 7 |
| ENR.DE | 142.14 | 141.08 | -0.189 | 8 |
| IFX.DE | 55.91 | 55.52 | -0.184 | 4 |
| VNA.DE | 19.155 | 19.095 | -0.168 | 8 |
| SRT3.DE | 246.9 | 246.9 | -0.0 | 2 |

## Tief zurueckerobert (2)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| CBK.DE | 39.76 | 39.8 | 0.06 | 4 |
| SHL.DE | 39.13 | 39.18 | 0.084 | 1 |

## Tief angetestet (11)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DIS | 106.15 | 106.23 | 0.034 | 0 |
| BKNG | 195.4 | 195.68 | 0.046 | 0 |
| DASH | 225.26 | 225.7 | 0.059 | 0 |
| MCD | 260.75 | 261.24 | 0.096 | 0 |
| TRV | 363.215 | 363.98 | 0.118 | 0 |
| CRWD | 212.65 | 215.07 | 0.182 | 0 |
| MMM | 169.64 | 170.27 | 0.19 | 0 |
| GS | 997.0 | 1002.49 | 0.227 | 0 |
| IBM | 229.91 | 231.62 | 0.279 | 0 |
| AMD | 452.3 | 459.75 | 0.389 | 0 |
| MELI | 1906.0699 | 1963.49 | 0.832 | 0 |

## Swing-Hoch ueberwunden (20)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 154.28 | 4.189 | 7 |
| CRM | 213.17 | 258.18 | 3.974 | 7 |
| HNR1.DE | 252.4 | 259.2 | 1.874 | 9 |
| MBG.DE | 45.62 | 46.935 | 1.582 | 9 |
| CDW | 142.97 | 150.39 | 1.19 | 7 |
| WDAY | 185.82 | 198.37 | 1.111 | 7 |
| BMW.DE | 59.6 | 60.96 | 1.039 | 9 |
| ADBE | 279.0 | 286.08 | 0.682 | 7 |
| MUV2.DE | 520.4 | 524.6 | 0.592 | 8 |
| DBK.DE | 34.1 | 34.425 | 0.488 | 5 |
| AAPL | 322.37 | 325.14 | 0.416 | 7 |
| BKR | 63.02 | 63.64 | 0.404 | 7 |
| BAS.DE | 52.76 | 53.0 | 0.253 | 7 |
| VOW3.DE | 75.96 | 76.3 | 0.199 | 6 |
| BNR.DE | 62.12 | 62.3 | 0.131 | 9 |
| SPGI | 439.02 | 440.28 | 0.114 | 3 |
| GILD | 149.62 | 149.9 | 0.076 | 1 |
| CON.DE | 71.06 | 71.14 | 0.055 | 3 |
| CTSH | 63.3 | 63.38 | 0.037 | 6 |
| PAH3.DE | 28.2 | 28.21 | 0.018 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.