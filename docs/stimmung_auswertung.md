# Stimmung und Tiefs – Auswertung

Stand: 26.09.2026 07:21 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

43448 Tiefs, 233 Werte, Zeitraum 10/2019 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 10442 | 38 % | 44 % | 53 % | 2,62 ATR |
| normal | 17294 | 41 % | 47 % | 59 % | 2,25 ATR |
| unruhig | 15712 | 50 % | 57 % | 69 % | 1,48 ATR |

**Je Wert (unruhig gegen ruhig), 231 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +9,5 Pp | 47 | 180 |
| 1,50 ATR | +10,9 Pp | 39 | 187 |
| 2,00 ATR | +12,9 Pp | 34 | 196 |
| 2,50 ATR | +14,1 Pp | 31 | 197 |
| 3,00 ATR | +14,2 Pp | 25 | 199 |
| 4,00 ATR | +15,4 Pp | 20 | 211 |
| 5,00 ATR | +15,6 Pp | 11 | 215 |
| 7,00 ATR | +15,1 Pp | 12 | 215 |
| 10,00 ATR | +10,6 Pp | 8 | 213 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,12 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 62 % (45) → 34 % (47)
- AMGN: 72 % (46) → 52 % (64)
- LMT: 53 % (43) → 33 % (75)
- SPOT: 61 % (51) → 44 % (73)
- STX: 71 % (49) → 55 % (71)
- TXN: 33 % (48) → 79 % (68)
- TD: 15 % (41) → 61 % (77)
- IDXX: 17 % (35) → 64 % (80)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

6639 Tiefs, 39 Werte, Zeitraum 10/2019 bis 06/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 2377 | 34 % | 39 % | 50 % | 2,97 ATR |
| normal | 2395 | 41 % | 47 % | 59 % | 2,25 ATR |
| unruhig | 1867 | 45 % | 52 % | 63 % | 1,84 ATR |

**Je Wert (unruhig gegen ruhig), 39 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +13,7 Pp | 9 | 29 |
| 1,50 ATR | +13,7 Pp | 11 | 28 |
| 2,00 ATR | +16,1 Pp | 10 | 28 |
| 2,50 ATR | +15,7 Pp | 12 | 27 |
| 3,00 ATR | +14,7 Pp | 12 | 27 |
| 4,00 ATR | +11,9 Pp | 12 | 27 |
| 5,00 ATR | +10,5 Pp | 12 | 26 |
| 7,00 ATR | +8,1 Pp | 6 | 32 |
| 10,00 ATR | +4,3 Pp | 1 | 36 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,39 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- ENR.DE: 63 % (51) → 38 % (42)
- ALV.DE: 50 % (66) → 35 % (43)
- FRE.DE: 45 % (49) → 30 % (50)
- BEI.DE: 46 % (57) → 33 % (45)
- HNR1.DE: 47 % (73) → 38 % (37)
- CON.DE: 21 % (62) → 67 % (48)
- MTX.DE: 35 % (52) → 82 % (44)
- HEN3.DE: 22 % (49) → 70 % (40)

## US-Werte gegen Fear & Greed

42992 Tiefs, 233 Werte, Zeitraum 10/2019 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 18912 | 48 % | 54 % | 65 % | 1,68 ATR |
| neutral | 6558 | 39 % | 44 % | 55 % | 2,51 ATR |
| Gier | 17522 | 40 % | 46 % | 58 % | 2,27 ATR |

**Je Wert (Angst gegen Gier), 231 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +7,2 Pp | 57 | 171 |
| 1,50 ATR | +7,7 Pp | 60 | 163 |
| 2,00 ATR | +7,8 Pp | 55 | 173 |
| 2,50 ATR | +7,4 Pp | 62 | 165 |
| 3,00 ATR | +7,8 Pp | 54 | 173 |
| 4,00 ATR | +7,1 Pp | 46 | 177 |
| 5,00 ATR | +7,1 Pp | 43 | 182 |
| 7,00 ATR | +6,0 Pp | 37 | 181 |
| 10,00 ATR | +4,9 Pp | 25 | 188 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: -0,64 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- APP: 70 % (57) → 43 % (76)
- ARM: 70 % (20) → 44 % (32)
- CRWD: 71 % (66) → 53 % (64)
- TSM: 67 % (101) → 50 % (103)
- CEG: 67 % (45) → 49 % (55)
- AEP: 34 % (80) → 67 % (66)
- VRSK: 33 % (67) → 67 % (86)
- AMT: 12 % (76) → 58 % (81)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
