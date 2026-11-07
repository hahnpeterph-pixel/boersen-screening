# Stundenwache

Stand: 2026-11-06 · 272 Werte mit Stundendaten · erstellt 2026-11-07 01:56 UTC

> **Sitzung noch nicht abgeschlossen.** 5 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus `tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.

Lesart der Urteile:

- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen
- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber geschlossen. Auf der Tageskerze nicht erkennbar.
- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter
- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten

## Tief gebrochen (4)

Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| GS | 892.1 | 865.54 | -0.926 | 7 |
| C | 121.43 | 119.06 | -0.67 | 7 |
| MS | 183.91 | 181.44 | -0.404 | 5 |
| COF | 202.06 | 201.87 | -0.029 | 2 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (33)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| RY | 200.8 | 201.13 | 0.092 | 0 |
| NOW | 100.5501 | 101.95 | 0.179 | 0 |
| HNR1.DE | 291.4 | 292.6 | 0.198 | 0 |
| BNR.DE | 61.48 | 61.74 | 0.201 | 0 |
| SAP.DE | 208.9 | 210.4 | 0.232 | 0 |
| MPC | 367.72 | 372.73 | 0.233 | 0 |
| AVGO | 289.77 | 293.32 | 0.235 | 0 |
| VOW3.DE | 69.42 | 70.04 | 0.281 | 0 |
| GEHC | 81.4926 | 82.38 | 0.306 | 0 |
| DHL.DE | 57.1 | 57.5 | 0.306 | 0 |
| EXC | 45.3 | 45.605 | 0.317 | 0 |
| SMFG | 2954.5 | 2992.5 | 0.326 | 0 |
| CTSH | 63.69 | 64.725 | 0.341 | 0 |
| CMCSA | 24.09 | 24.395 | 0.384 | 0 |
| PAYX | 115.27 | 117.02 | 0.449 | 0 |
| MTX.DE | 336.8 | 343.2 | 0.452 | 0 |
| BEI.DE | 83.88 | 84.88 | 0.455 | 0 |
| SHW | 338.2 | 344.07 | 0.461 | 0 |
| CDW | 152.4 | 156.99 | 0.541 | 0 |
| P911.DE | 46.19 | 46.91 | 0.562 | 0 |
| TRV | 389.64 | 395.25 | 0.619 | 0 |
| HONA | 147.4 | 152.93 | 0.638 | 0 |
| NEE | 85.64 | 86.95 | 0.647 | 0 |
| LULU | 107.55 | 110.75 | 0.676 | 0 |
| ENB | 46.38 | 46.89 | 0.693 | 0 |
| EOAN.DE | 18.785 | 19.085 | 0.769 | 0 |
| HEN3.DE | 82.06 | 83.26 | 0.821 | 0 |
| SBUX | 102.69 | 105.39 | 0.91 | 0 |
| TMUS | 155.58 | 161.95 | 0.975 | 0 |
| PYPL | 57.57 | 59.23 | 1.014 | 0 |
| HON | 211.94 | 220.15 | 1.129 | 0 |
| JNJ | 265.55 | 276.26 | 1.363 | 0 |
| DTG.DE | 38.42 | 40.36 | 1.811 | 0 |

## Swing-Hoch ueberwunden (17)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| APP | 264.045 | 391.25 | 5.985 | 7 |
| QIA.DE | 42.345 | 45.2 | 5.181 | 9 |
| IBN | 1404.9 | 1571.2 | 4.866 | 7 |
| FRE.DE | 47.295 | 52.23 | 4.452 | 9 |
| HDB | 734.9 | 788.25 | 2.947 | 7 |
| SHL.DE | 42.06 | 44.57 | 2.482 | 9 |
| TM | 3115.0 | 3340.0 | 2.077 | 7 |
| NEM | 110.83 | 120.9 | 2.058 | 7 |
| ABNB | 180.06 | 190.02 | 1.495 | 7 |
| WDAY | 185.82 | 192.91 | 0.899 | 7 |
| BABA | 101.6 | 104.9 | 0.813 | 7 |
| SCHW | 89.96 | 91.49 | 0.797 | 7 |
| UBS | 38.96 | 39.61 | 0.609 | 9 |
| AMZN | 255.36 | 259.35 | 0.409 | 7 |
| TTWO | 212.16 | 214.78 | 0.378 | 7 |
| VRSK | 201.65 | 204.62 | 0.343 | 7 |
| SONY | 4068.0 | 4107.0 | 0.289 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.