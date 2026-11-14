# Stimmung und Tiefs – Auswertung

Stand: 14.11.2026 06:31 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

91510 Tiefs, 233 Werte, Zeitraum 01/2011 bis 09/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 36888 | 41 % | 47 % | 58 % | 2,24 ATR |
| normal | 33197 | 45 % | 52 % | 63 % | 1,88 ATR |
| unruhig | 21425 | 54 % | 61 % | 73 % | 1,23 ATR |

**Je Wert (unruhig gegen ruhig), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,4 Pp | 19 | 206 |
| 1,50 ATR | +12,4 Pp | 21 | 209 |
| 2,00 ATR | +13,3 Pp | 14 | 212 |
| 2,50 ATR | +13,8 Pp | 17 | 211 |
| 3,00 ATR | +14,1 Pp | 11 | 218 |
| 4,00 ATR | +14,9 Pp | 12 | 218 |
| 5,00 ATR | +13,2 Pp | 13 | 216 |
| 7,00 ATR | +10,2 Pp | 11 | 217 |
| 10,00 ATR | +5,8 Pp | 7 | 207 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,02 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 57 % (49) → 34 % (47)
- LMT: 59 % (170) → 47 % (106)
- SPOT: 53 % (72) → 42 % (79)
- ADBE: 53 % (185) → 42 % (85)
- NOW: 60 % (174) → 52 % (91)
- UPS: 31 % (153) → 65 % (113)
- GE: 32 % (151) → 66 % (107)
- GFS: 11 % (36) → 52 % (33)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

14862 Tiefs, 39 Werte, Zeitraum 01/2011 bis 08/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 4940 | 39 % | 44 % | 56 % | 2,47 ATR |
| normal | 5669 | 41 % | 47 % | 58 % | 2,24 ATR |
| unruhig | 4253 | 50 % | 58 % | 69 % | 1,47 ATR |

**Je Wert (unruhig gegen ruhig), 39 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,5 Pp | 5 | 33 |
| 1,50 ATR | +11,4 Pp | 6 | 33 |
| 2,00 ATR | +12,7 Pp | 5 | 33 |
| 2,50 ATR | +11,8 Pp | 4 | 33 |
| 3,00 ATR | +13,5 Pp | 5 | 34 |
| 4,00 ATR | +10,7 Pp | 6 | 33 |
| 5,00 ATR | +8,5 Pp | 7 | 31 |
| 7,00 ATR | +6,2 Pp | 3 | 33 |
| 10,00 ATR | +4,3 Pp | 5 | 32 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,04 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- ENR.DE: 62 % (52) → 38 % (42)
- CBK.DE: 52 % (128) → 45 % (118)
- DBK.DE: 53 % (144) → 49 % (142)
- BEI.DE: 51 % (134) → 47 % (105)
- ALV.DE: 55 % (150) → 52 % (104)
- BNR.DE: 33 % (143) → 63 % (121)
- CON.DE: 41 % (144) → 72 % (111)
- HEN3.DE: 32 % (122) → 72 % (106)

## US-Werte gegen Fear & Greed

91074 Tiefs, 233 Werte, Zeitraum 01/2011 bis 09/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 40796 | 49 % | 55 % | 66 % | 1,60 ATR |
| neutral | 13232 | 44 % | 50 % | 61 % | 2,03 ATR |
| Gier | 37046 | 43 % | 49 % | 61 % | 2,07 ATR |

**Je Wert (Angst gegen Gier), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +5,0 Pp | 39 | 183 |
| 1,50 ATR | +5,9 Pp | 43 | 176 |
| 2,00 ATR | +5,8 Pp | 40 | 186 |
| 2,50 ATR | +5,8 Pp | 42 | 178 |
| 3,00 ATR | +5,5 Pp | 45 | 180 |
| 4,00 ATR | +4,6 Pp | 47 | 176 |
| 5,00 ATR | +3,4 Pp | 53 | 165 |
| 7,00 ATR | +1,9 Pp | 71 | 149 |
| 10,00 ATR | +1,3 Pp | 68 | 133 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: -0,43 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- APP: 69 % (58) → 40 % (82)
- ARM: 67 % (21) → 44 % (36)
- CRWD: 68 % (69) → 52 % (71)
- CEG: 65 % (46) → 51 % (57)
- CMCSA: 57 % (168) → 46 % (189)
- PSX: 41 % (165) → 63 % (154)
- UPS: 34 % (161) → 58 % (191)
- GFS: 23 % (44) → 51 % (57)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
