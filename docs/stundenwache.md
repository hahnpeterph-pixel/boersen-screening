# Stundenwache

Stand: 2026-11-24 · 272 Werte mit Stundendaten · erstellt 2026-11-25 04:57 UTC

> **Sitzung noch nicht abgeschlossen.** 13 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 2, 3, 4, 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| CON.DE | 69.16 | 69.12 | -0.021 | 1 |

## Tief zurueckerobert (0)

Keine.

## Tief angetestet (9)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| TXN | 257.84 | 258.58 | 0.038 | 0 |
| IFX.DE | 43.44 | 43.56 | 0.038 | 0 |
| CBK.DE | 35.6 | 35.65 | 0.043 | 0 |
| GEV | 708.965 | 720.18 | 0.192 | 0 |
| INTC | 53.54 | 54.895 | 0.277 | 0 |
| BAS.DE | 48.585 | 49.1 | 0.4 | 0 |
| CAT | 528.61 | 540.61 | 0.407 | 0 |
| BMW.DE | 52.44 | 53.26 | 0.579 | 0 |
| AMT | 178.21 | 182.81 | 0.982 | 0 |

## Swing-Hoch ueberwunden (32)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.215 | 15.191 | 9 |
| SONY | 4068.0 | 4508.0 | 2.699 | 5 |
| PDD | 79.88 | 87.2 | 2.35 | 7 |
| TM | 3115.0 | 3416.0 | 2.345 | 5 |
| SNY | 89.0 | 93.7 | 2.028 | 9 |
| VRTX | 542.76 | 564.16 | 1.379 | 7 |
| GILD | 171.7 | 178.29 | 1.368 | 7 |
| TJX | 138.17 | 143.93 | 1.241 | 7 |
| BIIB | 261.0 | 269.27 | 1.055 | 7 |
| HDB | 821.0 | 843.95 | 1.017 | 2 |
| ZS | 218.105 | 231.74 | 0.882 | 7 |
| ORLY | 93.93 | 95.5 | 0.769 | 7 |
| CSGP | 31.64 | 32.635 | 0.731 | 6 |
| DIS | 120.44 | 122.52 | 0.623 | 7 |
| WMT | 130.52 | 132.3 | 0.596 | 7 |
| JNJ | 272.5 | 276.47 | 0.587 | 7 |
| DTE.DE | 26.51 | 26.79 | 0.498 | 3 |
| REGN | 972.24 | 987.2 | 0.47 | 7 |
| HD | 349.73 | 353.78 | 0.424 | 6 |
| P911.DE | 43.83 | 44.26 | 0.396 | 1 |
| MCD | 278.29 | 280.84 | 0.392 | 7 |
| LOW | 228.7 | 231.0 | 0.327 | 6 |
| PG | 171.61 | 172.53 | 0.278 | 7 |
| ADP | 308.66 | 310.32 | 0.258 | 5 |
| UL | 49.355 | 49.61 | 0.251 | 2 |
| T | 22.75 | 22.87 | 0.247 | 7 |
| VNA.DE | 16.99 | 17.075 | 0.217 | 9 |
| SYK | 321.83 | 324.07 | 0.216 | 6 |
| DXCM | 84.02 | 84.65 | 0.197 | 6 |
| SCHW | 93.75 | 93.915 | 0.071 | 6 |
| VZ | 47.11 | 47.16 | 0.051 | 7 |
| HON | 224.66 | 224.82 | 0.022 | 2 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.