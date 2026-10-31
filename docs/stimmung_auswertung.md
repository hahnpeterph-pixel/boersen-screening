# Stimmung und Tiefs – Auswertung

Stand: 31.10.2026 05:51 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

91265 Tiefs, 233 Werte, Zeitraum 01/2011 bis 08/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 36695 | 42 % | 47 % | 58 % | 2,23 ATR |
| normal | 33145 | 45 % | 52 % | 63 % | 1,88 ATR |
| unruhig | 21425 | 54 % | 61 % | 73 % | 1,23 ATR |

**Je Wert (unruhig gegen ruhig), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,2 Pp | 19 | 207 |
| 1,50 ATR | +12,3 Pp | 22 | 209 |
| 2,00 ATR | +13,2 Pp | 15 | 213 |
| 2,50 ATR | +13,5 Pp | 19 | 208 |
| 3,00 ATR | +14,1 Pp | 12 | 217 |
| 4,00 ATR | +14,8 Pp | 12 | 217 |
| 5,00 ATR | +13,2 Pp | 12 | 216 |
| 7,00 ATR | +10,3 Pp | 11 | 217 |
| 10,00 ATR | +5,8 Pp | 7 | 207 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,00 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 58 % (48) → 34 % (47)
- LMT: 59 % (170) → 47 % (106)
- SPOT: 53 % (72) → 42 % (79)
- ADBE: 53 % (184) → 42 % (85)
- NOW: 60 % (173) → 52 % (91)
- GE: 33 % (149) → 66 % (107)
- UPS: 31 % (152) → 65 % (113)
- GFS: 11 % (36) → 52 % (33)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

14827 Tiefs, 39 Werte, Zeitraum 01/2011 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 4919 | 39 % | 44 % | 56 % | 2,47 ATR |
| normal | 5655 | 41 % | 47 % | 58 % | 2,24 ATR |
| unruhig | 4253 | 50 % | 58 % | 68 % | 1,47 ATR |

**Je Wert (unruhig gegen ruhig), 39 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,5 Pp | 5 | 34 |
| 1,50 ATR | +11,1 Pp | 6 | 33 |
| 2,00 ATR | +12,8 Pp | 5 | 33 |
| 2,50 ATR | +11,8 Pp | 4 | 33 |
| 3,00 ATR | +13,0 Pp | 5 | 33 |
| 4,00 ATR | +10,7 Pp | 6 | 33 |
| 5,00 ATR | +8,5 Pp | 7 | 30 |
| 7,00 ATR | +6,3 Pp | 3 | 33 |
| 10,00 ATR | +4,3 Pp | 5 | 32 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,09 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- ENR.DE: 63 % (51) → 38 % (42)
- CBK.DE: 52 % (128) → 45 % (118)
- DBK.DE: 54 % (143) → 49 % (142)
- BEI.DE: 51 % (134) → 47 % (105)
- ALV.DE: 55 % (149) → 52 % (104)
- BNR.DE: 32 % (142) → 63 % (121)
- CON.DE: 41 % (143) → 72 % (111)
- HEN3.DE: 32 % (121) → 72 % (106)

## US-Werte gegen Fear & Greed

90829 Tiefs, 233 Werte, Zeitraum 01/2011 bis 08/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 40775 | 49 % | 55 % | 66 % | 1,60 ATR |
| neutral | 13218 | 43 % | 50 % | 61 % | 2,03 ATR |
| Gier | 36836 | 43 % | 49 % | 61 % | 2,06 ATR |

**Je Wert (Angst gegen Gier), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +4,9 Pp | 39 | 183 |
| 1,50 ATR | +5,8 Pp | 43 | 179 |
| 2,00 ATR | +5,9 Pp | 41 | 186 |
| 2,50 ATR | +5,6 Pp | 43 | 177 |
| 3,00 ATR | +5,4 Pp | 44 | 179 |
| 4,00 ATR | +4,4 Pp | 50 | 174 |
| 5,00 ATR | +3,4 Pp | 53 | 165 |
| 7,00 ATR | +2,0 Pp | 69 | 150 |
| 10,00 ATR | +1,3 Pp | 66 | 133 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: -0,43 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- APP: 70 % (57) → 40 % (82)
- ARM: 70 % (20) → 44 % (36)
- CRWD: 69 % (68) → 52 % (71)
- CEG: 67 % (45) → 51 % (57)
- CMCSA: 57 % (167) → 46 % (189)
- PSX: 40 % (164) → 63 % (154)
- UPS: 34 % (160) → 58 % (190)
- GFS: 23 % (44) → 51 % (57)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
