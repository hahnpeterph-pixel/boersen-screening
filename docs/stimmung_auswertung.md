# Stimmung und Tiefs – Auswertung

Stand: 25.09.2026 20:39 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), nur Werte mit je mindestens 10 Faellen in beiden Lagen. Die Gesamtzeile ist nur zur Orientierung.

## US-Werte gegen VIX

43363 Tiefs, 233 Werte, Zeitraum 10/2019 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 10438 | 38 % | 44 % | 53 % | 2,62 ATR |
| normal | 17213 | 41 % | 47 % | 58 % | 2,25 ATR |
| unruhig | 15712 | 50 % | 57 % | 69 % | 1,48 ATR |

**Je Wert (unruhig gegen ruhig), 231 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +9,8 Pp | 46 | 179 |
| 1,50 ATR | +11,2 Pp | 38 | 190 |
| 2,00 ATR | +12,9 Pp | 35 | 195 |
| 2,50 ATR | +14,3 Pp | 31 | 196 |
| 3,00 ATR | +14,5 Pp | 25 | 198 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,12 ATR.

Staerkste Unterschiede bei 2 ATR (haelt ruhig → unruhig):

- APP: 62 % (45) → 34 % (47)
- AMGN: 72 % (46) → 52 % (64)
- LMT: 53 % (43) → 33 % (75)
- SPOT: 62 % (52) → 44 % (73)
- STX: 71 % (49) → 55 % (71)
- TD: 15 % (41) → 61 % (77)
- IDXX: 17 % (35) → 64 % (80)
- TXN: 33 % (49) → 79 % (68)

## Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)

6643 Tiefs, 39 Werte, Zeitraum 10/2019 bis 06/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| ruhig | 2371 | 34 % | 39 % | 50 % | 2,97 ATR |
| normal | 2405 | 41 % | 47 % | 59 % | 2,23 ATR |
| unruhig | 1867 | 45 % | 52 % | 63 % | 1,84 ATR |

**Je Wert (unruhig gegen ruhig), 39 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +13,7 Pp | 9 | 29 |
| 1,50 ATR | +13,7 Pp | 11 | 28 |
| 2,00 ATR | +16,3 Pp | 10 | 28 |
| 2,50 ATR | +15,6 Pp | 12 | 27 |
| 3,00 ATR | +14,9 Pp | 12 | 27 |

Benoetigter Puffer (unruhig minus ruhig), Median ueber die Werte: -1,35 ATR.

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

4747 Tiefs, 232 Werte, Zeitraum 09/2025 bis 07/2026.

| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |
|---|---|---|---|---|---|
| Angst | 2748 | 45 % | 54 % | 66 % | 1,77 ATR |
| neutral | 761 | 37 % | 43 % | 52 % | 2,71 ATR |
| Gier | 1238 | 46 % | 52 % | 64 % | 1,88 ATR |

**Je Wert (Angst gegen Gier), 2 Werte vergleichbar:**

| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |
|---|---|---|---|
| 1,00 ATR | +3,9 Pp | 1 | 1 |
| 1,50 ATR | -1,8 Pp | 1 | 1 |
| 2,00 ATR | -3,0 Pp | 1 | 1 |
| 2,50 ATR | +1,2 Pp | 1 | 1 |
| 3,00 ATR | -2,4 Pp | 1 | 1 |

Benoetigter Puffer (Angst minus Gier), Median ueber die Werte: +0,19 ATR.

Staerkste Unterschiede bei 2 ATR (haelt Gier → Angst):

- PG: 73 % (11) → 20 % (15)
- NEM: 0 % (11) → 47 % (15)
- PG: 73 % (11) → 20 % (15)
- NEM: 0 % (11) → 47 % (15)

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
