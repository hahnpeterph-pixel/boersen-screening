# Stimmung und Tiefs – Auswertung

Stand: 28.11.2026 07:56 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

91756 Tiefs, 233 Werte, Zeitraum 01/2011 bis 09/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 37087 | 41 % | 47 % | 58 % | 2,25 ATR |
| normal | 33244 | 45 % | 52 % | 63 % | 1,89 ATR |
| unruhig | 21425 | 54 % | 61 % | 73 % | 1,23 ATR |

**Je Wert (unruhig gegen ruhig), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +11,6 Pp | 20 | 208 |
| 1,50 ATR | +12,4 Pp | 21 | 209 |
| 2,00 ATR | +13,9 Pp | 14 | 213 |
| 2,50 ATR | +14,1 Pp | 14 | 213 |
| 3,00 ATR | +14,4 Pp | 10 | 218 |
| 4,00 ATR | +15,0 Pp | 12 | 217 |
| 5,00 ATR | +13,3 Pp | 12 | 216 |
| 7,00 ATR | +10,1 Pp | 11 | 217 |
| 10,00 ATR | +5,8 Pp | 7 | 207 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,02 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 56 % (50) → 34 % (47)
- LMT: 59 % (171) → 47 % (106)
- ADBE: 52 % (187) → 42 % (85)
- SPOT: 51 % (74) → 42 % (79)
- NOW: 60 % (176) → 52 % (91)
- UPS: 31 % (153) → 65 % (113)
- GE: 32 % (152) → 66 % (107)
- GFS: 11 % (37) → 52 % (33)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

0 Tiefs, 0 Werte, Zeitraum – bis –.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 0 | – % | – % | – % | – ATR |
| normal | 0 | – % | – % | – % | – ATR |
| unruhig | 0 | – % | – % | – % | – ATR |

**Je Wert (unruhig gegen ruhig), 0 Werte vergleichbar:**

Zu wenige Faelle je Wert fuer einen Vergleich.

## US-Werte gegen Fear & Greed

91320 Tiefs, 233 Werte, Zeitraum 01/2011 bis 09/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 40798 | 49 % | 55 % | 66 % | 1,60 ATR |
| neutral | 13380 | 43 % | 49 % | 60 % | 2,06 ATR |
| Gier | 37142 | 43 % | 49 % | 61 % | 2,07 ATR |

**Je Wert (Angst gegen Gier), 232 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +5,2 Pp | 37 | 184 |
| 1,50 ATR | +5,9 Pp | 44 | 177 |
| 2,00 ATR | +5,9 Pp | 42 | 185 |
| 2,50 ATR | +5,8 Pp | 43 | 181 |
| 3,00 ATR | +5,7 Pp | 44 | 180 |
| 4,00 ATR | +4,6 Pp | 45 | 177 |
| 5,00 ATR | +3,6 Pp | 54 | 165 |
| 7,00 ATR | +1,9 Pp | 70 | 147 |
| 10,00 ATR | +1,3 Pp | 68 | 132 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: -0,43 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- APP: 69 % (58) → 40 % (82)
- ARM: 67 % (21) → 44 % (36)
- CRWD: 68 % (69) → 52 % (71)
- CEG: 65 % (46) → 51 % (57)
- CMCSA: 56 % (170) → 46 % (189)
- COST: 44 % (176) → 67 % (181)
- UPS: 34 % (161) → 58 % (191)
- GFS: 23 % (44) → 51 % (57)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
