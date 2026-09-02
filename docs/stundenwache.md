# Stundenwache

Stand: 2026-09-01 · 158 Werte mit Stundendaten · erstellt 2026-09-02 09:24 UTC

> **Sitzung noch nicht abgeschlossen.** 40 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 3, 7). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (2)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| ODFL | 196.41 | 187.01 | -1.53 | 7 |
| PAH3.DE | 27.48 | 27.46 | -0.034 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (17)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| DHL.DE | 54.78 | 54.8 | 0.025 | 0 |
| ADSK | 247.35 | 247.69 | 0.033 | 0 |
| DASH | 225.26 | 225.7 | 0.059 | 0 |
| AXP | 323.92 | 324.27 | 0.06 | 0 |
| DTG.DE | 45.83 | 45.88 | 0.062 | 0 |
| MNST | 44.89 | 44.99 | 0.089 | 0 |
| ROP | 417.51 | 418.43 | 0.091 | 0 |
| CRWD | 212.65 | 215.07 | 0.182 | 0 |
| FAST | 48.53 | 48.75 | 0.22 | 0 |
| PCAR | 121.81 | 122.51 | 0.256 | 0 |
| IBM | 229.9 | 231.62 | 0.28 | 0 |
| AZN | 161.39 | 162.42 | 0.333 | 0 |
| TXN | 250.43 | 253.42 | 0.359 | 0 |
| AMD | 452.3 | 459.75 | 0.389 | 0 |
| ROST | 224.5 | 229.14 | 0.666 | 0 |
| MELI | 1906.0699 | 1963.49 | 0.832 | 0 |
| CSX | 47.83 | 48.71 | 0.883 | 0 |

## Swing-Hoch ueberwunden (14)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| MRNA | 65.525 | 154.28 | 4.189 | 7 |
| CRM | 213.17 | 258.18 | 3.974 | 7 |
| HNR1.DE | 252.4 | 260.6 | 2.464 | 3 |
| CDW | 142.97 | 150.39 | 1.19 | 7 |
| WDAY | 185.82 | 198.37 | 1.111 | 7 |
| MBG.DE | 45.62 | 46.355 | 0.832 | 3 |
| MUV2.DE | 520.4 | 525.4 | 0.719 | 3 |
| ADBE | 279.0 | 286.08 | 0.682 | 7 |
| AAPL | 322.37 | 325.14 | 0.416 | 7 |
| BKR | 63.02 | 63.64 | 0.404 | 7 |
| BAS.DE | 52.76 | 53.0 | 0.253 | 3 |
| SPGI | 439.02 | 440.28 | 0.114 | 3 |
| GILD | 149.62 | 149.9 | 0.076 | 1 |
| CTSH | 63.3 | 63.38 | 0.037 | 6 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.