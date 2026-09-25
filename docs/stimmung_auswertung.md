# Stimmung und Tiefs – Auswertung

Stand: 25.09.2026 20:29 UTC. Grundlage: puffer_je_tief.csv.gz, nur Tiefs mit mindestens 63 beobachteten Tagen. Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.

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

## Deutsche Werte gegen VDAX-NEW

Keine Stimmungsdaten.

## US-Werte gegen Fear & Greed

Keine Stimmungsdaten.

Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv (fuer die Kaufvorlage: "Bei heutiger Lage hielt Tief N dieses Werts x %").
