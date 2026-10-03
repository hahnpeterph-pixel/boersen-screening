# Stimmung und Tiefs – Auswertung

Stand: 03.10.2026 07:10 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

93474 Tiefs, 233 Werte, Zeitraum 01/2011 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 37697 | 40 % | 46 % | 57 % | 2,33 ATR |
| normal | 33705 | 44 % | 51 % | 62 % | 1,96 ATR |
| unruhig | 22072 | 54 % | 60 % | 72 % | 1,28 ATR |

**Je Wert (unruhig gegen ruhig), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,1 Pp | 17 | 211 |
| 1,50 ATR | +12,5 Pp | 18 | 213 |
| 2,00 ATR | +13,5 Pp | 11 | 218 |
| 2,50 ATR | +13,5 Pp | 14 | 215 |
| 3,00 ATR | +14,7 Pp | 10 | 220 |
| 4,00 ATR | +14,8 Pp | 9 | 220 |
| 5,00 ATR | +14,0 Pp | 10 | 219 |
| 7,00 ATR | +10,6 Pp | 9 | 219 |
| 10,00 ATR | +6,2 Pp | 5 | 211 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,00 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 62 % (45) → 34 % (47)
- LMT: 59 % (169) → 47 % (106)
- SPOT: 52 % (71) → 42 % (79)
- ADBE: 52 % (181) → 42 % (85)
- NOW: 60 % (171) → 52 % (91)
- GE: 33 % (149) → 66 % (107)
- UPS: 31 % (151) → 65 % (113)
- GFS: 11 % (36) → 52 % (33)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

14734 Tiefs, 39 Werte, Zeitraum 01/2011 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 4918 | 39 % | 44 % | 56 % | 2,47 ATR |
| normal | 5563 | 41 % | 47 % | 58 % | 2,26 ATR |
| unruhig | 4253 | 50 % | 58 % | 69 % | 1,47 ATR |

**Je Wert (unruhig gegen ruhig), 39 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,5 Pp | 5 | 34 |
| 1,50 ATR | +11,1 Pp | 6 | 33 |
| 2,00 ATR | +12,8 Pp | 5 | 33 |
| 2,50 ATR | +11,8 Pp | 4 | 33 |
| 3,00 ATR | +13,5 Pp | 5 | 33 |
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
- ALV.DE: 56 % (149) → 52 % (104)
- BNR.DE: 32 % (142) → 63 % (121)
- CON.DE: 41 % (143) → 72 % (111)
- HEN3.DE: 32 % (121) → 72 % (106)

## US-Werte gegen Fear & Greed

93018 Tiefs, 233 Werte, Zeitraum 01/2011 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 41416 | 48 % | 54 % | 65 % | 1,66 ATR |
| neutral | 13518 | 43 % | 49 % | 60 % | 2,10 ATR |
| Gier | 38084 | 42 % | 48 % | 60 % | 2,14 ATR |

**Je Wert (Angst gegen Gier), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +5,1 Pp | 41 | 183 |
| 1,50 ATR | +5,8 Pp | 46 | 180 |
| 2,00 ATR | +5,5 Pp | 40 | 183 |
| 2,50 ATR | +5,5 Pp | 46 | 176 |
| 3,00 ATR | +5,4 Pp | 45 | 174 |
| 4,00 ATR | +4,3 Pp | 51 | 174 |
| 5,00 ATR | +3,2 Pp | 53 | 161 |
| 7,00 ATR | +2,0 Pp | 69 | 147 |
| 10,00 ATR | +1,4 Pp | 62 | 135 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: -0,44 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- ARM: 70 % (20) → 42 % (33)
- APP: 70 % (57) → 43 % (76)
- CRWD: 69 % (68) → 50 % (68)
- CEG: 67 % (45) → 49 % (55)
- CMCSA: 57 % (167) → 46 % (184)
- PSX: 40 % (164) → 62 % (152)
- UPS: 34 % (160) → 58 % (189)
- GFS: 23 % (44) → 52 % (54)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
