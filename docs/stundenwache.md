# Stundenwache

Stand: 2026-11-20 · 272 Werte mit Stundendaten · erstellt 2026-11-21 03:15 UTC

> **Sitzung noch nicht abgeschlossen.** 3 Werte haben weniger als 7 Stundenkerzen (erfasste Stunden: 5, 6, 7, 8, 9). Bei diesen ist "Schluss" der Stand im Moment des Abrufs, nicht der Tagesschluss - die Urteile koennen sich bis Handelsende noch drehen.

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
| LIN | 508.0 | 502.975 | -0.506 | 3 |

## Tief zurueckerobert (1)

Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, den die Tageskerze verschluckt.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| RWE.DE | 55.3 | 55.58 | 0.196 | 1 |

## Tief angetestet (21)

Docht bis unter die Marke, kein Stundenschluss darunter.

| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |
|---|---|---|---|---|
| AXON | 291.11 | 291.42 | 0.012 | 0 |
| ENR.DE | 118.56 | 118.68 | 0.016 | 0 |
| SHL.DE | 42.85 | 42.87 | 0.018 | 0 |
| RHM.DE | 692.3 | 693.3 | 0.02 | 0 |
| ADS.DE | 165.65 | 165.8 | 0.03 | 0 |
| BAYN.DE | 53.76 | 53.82 | 0.035 | 0 |
| ENB | 45.65 | 45.69 | 0.047 | 0 |
| BMO | 156.16 | 156.36 | 0.053 | 0 |
| NOW | 87.34 | 87.65 | 0.066 | 0 |
| CRM | 179.92 | 180.57 | 0.072 | 0 |
| STX | 453.64 | 457.52 | 0.079 | 0 |
| VOW3.DE | 62.62 | 62.78 | 0.082 | 0 |
| DB1.DE | 314.3 | 315.2 | 0.14 | 0 |
| MBG.DE | 37.57 | 37.73 | 0.144 | 0 |
| BKR | 44.53 | 44.83 | 0.145 | 0 |
| CSCO | 89.99 | 90.685 | 0.162 | 0 |
| ASML | 1163.6 | 1176.2 | 0.176 | 0 |
| SRT3.DE | 285.8 | 287.3 | 0.185 | 0 |
| BMW.DE | 53.32 | 53.64 | 0.192 | 0 |
| ON | 59.14 | 60.84 | 0.358 | 0 |
| SAP.DE | 181.64 | 184.0 | 0.369 | 0 |

## Swing-Hoch ueberwunden (8)

| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |
|---|---|---|---|---|
| QIA.DE | 42.345 | 45.075 | 14.45 | 9 |
| IBN | 1404.9 | 1640.0 | 6.52 | 7 |
| SONY | 4068.0 | 4317.0 | 1.651 | 7 |
| TM | 3115.0 | 3307.0 | 1.531 | 7 |
| HDB | 821.0 | 846.0 | 1.264 | 7 |
| PDD | 79.88 | 83.65 | 1.226 | 7 |
| TJX | 138.17 | 139.67 | 0.304 | 7 |
| VRSK | 201.65 | 202.23 | 0.073 | 7 |

## Reihen unstimmig - kein Urteil (0)

Keine.

---

Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. Der Abstand zum eigenen Knock-out steht bewusst nicht hier - Positionsdaten bleiben ausserhalb des Repos.