# Stundenwache

Stand: 2026-09-30 · 273 Werte mit Stundendaten · erstellt 2026-09-30 22:55 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 6, 7, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| ABBV | 262.59 | 261.75 | -0.168 | 1 |
| HEI.DE | 142.55 | 141.85 | -0.167 | 3 |
| BMO | 167.22 | 167.2 | -0.007 | 1 |
| CB | 325.25 | 325.23 | -0.004 | 1 |
| AZN | 161.47 | 161.46 | -0.003 | 1 |
| FAST | 49.53 | 49.53 | -0.0 | 1 |
| CM | 110.12 | 110.12 | -0.0 | 1 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| SAP.DE | 182.26 | 185.98 | 0.709 | 1 |

## Tief angetestet (14)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| MA | 551.44 | 551.44 | 0.0 | 0 |
| WMT | 103.92 | 103.925 | 0.002 | 0 |
| TD | 117.53 | 117.54 | 0.005 | 0 |
| LOW | 184.23 | 184.32 | 0.022 | 0 |
| BRK-B | 497.95 | 498.19 | 0.04 | 0 |
| ABT | 98.73 | 98.83 | 0.05 | 0 |
| ALV.DE | 415.8 | 416.2 | 0.051 | 0 |
| ING | 35.445 | 35.495 | 0.077 | 0 |
| FDX | 284.5201 | 285.1 | 0.085 | 0 |
| HDB | 22.26 | 22.34 | 0.137 | 0 |
| DE | 668.58 | 671.28 | 0.173 | 0 |
| UNH | 365.76 | 367.15 | 0.18 | 0 |
| MUV2.DE | 501.8 | 503.6 | 0.218 | 0 |
| CEG | 247.24 | 253.97 | 0.703 | 0 |

## Swing-Hoch ueberwunden (23)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| WBD | 28.45 | 30.935 | 5.657 | 7 |
| SHOP | 134.74 | 148.43 | 2.025 | 7 |
| MRK.DE | 133.45 | 138.2 | 1.842 | 9 |
| ILMN | 250.06 | 273.7 | 1.817 | 7 |
| KLAC | 182.41 | 195.03 | 1.792 | 7 |
| MTX.DE | 358.8 | 374.8 | 1.737 | 9 |
| ASML | 1524.8 | 1608.4 | 1.725 | 9 |
| AMAT | 487.68 | 511.67 | 1.293 | 7 |
| DB1.DE | 280.1 | 286.0 | 1.25 | 9 |
| LIN | 466.24 | 474.65 | 1.204 | 7 |
| BEI.DE | 75.74 | 77.32 | 0.996 | 9 |
| TMO | 663.57 | 677.63 | 0.917 | 6 |
| LRCX | 317.13 | 328.61 | 0.848 | 7 |
| WDAY | 185.82 | 190.45 | 0.675 | 7 |
| LLY | 1138.79 | 1159.3101 | 0.644 | 7 |
| ON | 74.48 | 76.85 | 0.639 | 7 |
| AMGN | 415.76 | 421.49 | 0.624 | 7 |
| TSM | 452.88 | 456.28 | 0.34 | 7 |
| MSFT | 509.44 | 512.96 | 0.296 | 7 |
| ISRG | 404.44 | 406.66 | 0.21 | 7 |
| MAR | 354.63 | 355.77 | 0.155 | 7 |
| CRWD | 263.87 | 264.73 | 0.067 | 7 |
| PANW | 396.3 | 397.4 | 0.058 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.