# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-09-11 10:21 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

## Kaufregel

Die Knock-out-Schwelle soll **unter** einem markanten Tief liegen, mit mindestens **2,0 x ATR(14)** Abstand. Die ATR ist die mittlere Tagesschwankung des Basiswerts - ein fester Prozentsatz taugt nicht, weil er bei ruhigen und bei volatilen Werten voellig Unterschiedliches bedeutet.

Massgeblich ist das **juengste** Tief. Das tiefste Tief des Fensters steht nur zur Einordnung mit dabei und geht nicht in das Urteil ein.

_Ist in `watchlist.json` ein `chart_tief` gesetzt, gilt dieses statt des automatisch gefundenen - im Report mit 'Chart' markiert. Der Chart schlaegt das Skript._

_Als juengstes Tief zaehlt auch das Tief des zuletzt abgeschlossenen Tages, sofern es unter den Vortagen liegt - im Report mit 'unbest.' markiert, weil die Bestaetigung durch Folgetage noch aussteht._

**Regel 1 (harte Sperre):** Der KO muss mindestens 1,00 unter dem Tief liegen - in der Waehrung des Basiswerts. Verhindert nur, dass der KO auf dem Tief klebt; als alleiniges Mass taugt sie nicht.

**Regel 2+3 (Positionsgroesse):** 50 EUR bei gerade noch erfuelltem Puffer, 150 EUR ab 2,0 x ATR, dazwischen linear. Bezugstief ist das **juengstes** Tief.

### Bestehende Positionen

| Wert | KO | juengstes Tief | tiefstes Tief | Abstand | Regel 1 | Urteil | |
|---|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 208,52 (09.09.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,2 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 12,7 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,6 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 37,4 | nein | unauffaellig | + |
| Meta Platforms (META) | 66,4 | nein | beobachten | ! |
| Micron (MU) | 53,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 55,0 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 55,0 | nein | unauffaellig | + |
| Oracle (ORCL) | 53,5 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 454,01, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Oracle**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,34 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 216,96 steht nur -1,44 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,27 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,22 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 218,36 | 209,00 | 4,5 % | 217,20 | 7,72 | 49,8 | k.A. (noch nie) | 201,76 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 454,01 | 465,00 | -2,4 % | 450,56 | 16,03 | 40,8 | 36,2 (8 Faelle, 5,7 % der Serien) | 418,51 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,34 x ATR | 0,17 | **66,77 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,27 x ATR | 0,14 | **63,72 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,24 x ATR | 0,62 | **112,21 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 12,70 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,22 x ATR | 0,11 | **61,13 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,64 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 216,96 | 8,23 | 192,06 | 8,7x | 192,06 | 8,7x |
| Meta Platforms (META) | 644,38 | 20,67 | 514,77 | 5,0x | 483,16 | 4,0x |
| Micron (MU) | 977,41 | 44,51 | 884,47 | 10,5x | 648,85 | 3,0x |
| Microsoft (MSFT) | 492,44 | 10,15 | 465,70 | 18,4x | 328,90 | 3,0x |
| Microsoft II (MSFT) | 492,44 | 10,15 | 465,70 | 18,4x | 328,90 | 3,0x |
| Oracle (ORCL) | 152,94 | 6,79 | 138,95 | 10,9x | 100,93 | 2,9x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 09.09.2026 | 208,52 | 2,2 Mio. | 0,85x | -9,7 % |
| Take-Two (TTWO) | 01.09.2026 | 214,14 | 2,8 Mio. | 1,03x | -6,9 % |
| Take-Two (TTWO) | 27.08.2026 | 225,10 | 4,2 Mio. | 1,85x (Kapitulation) | -1,7 % |
| Meta Platforms (META) | 01.09.2026 | 556,10 | 15,8 Mio. | 1,03x | 6,7 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 1,1 % |
| Micron (MU) | 10.09.2026 | 973,50 | 26,1 Mio. | 0,95x | 11,7 % |
| Micron (MU) | 03.09.2026 | 918,88 | 24,2 Mio. | 0,86x | 6,4 % |
| Micron (MU) | 24.08.2026 | 887,61 | 30,0 Mio. | 0,77x (duenn) | 3,1 % |
| Microsoft (MSFT) | 10.09.2026 | 486,00 | 16,0 Mio. | 0,73x (duenn) | 28,3 % |
| Microsoft (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 29,5 % |
| Microsoft (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 27,2 % |
| Microsoft II (MSFT) | 10.09.2026 | 486,00 | 16,0 Mio. | 0,73x (duenn) | 2,3 % |
| Microsoft II (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 3,8 % |
| Microsoft II (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 0,8 % |
| Oracle (ORCL) | 10.09.2026 | 152,52 | 55,6 Mio. | 2,38x (Kapitulation) | 26,1 % |
| Oracle (ORCL) | 02.09.2026 | 139,72 | 21,9 Mio. | 0,97x | 19,3 % |
| Oracle (ORCL) | 24.08.2026 | 141,25 | 14,2 Mio. | 0,49x (duenn) | 20,2 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 216,96 | 8,23 | 37,4 | 231,58 | 2026-08-20 | 0,85 |
| META | 644,38 | 20,67 | 66,4 | 524,52 | 2026-07-30 | 1,03 |
| MU | 977,41 | 44,51 | 53,3 | 915,18 | 2026-08-19 | 0,95 |
| MSFT | 492,44 | 10,15 | 55,0 | 477,15 | 2026-08-18 | 0,73 |
| ORCL | 152,94 | 6,79 | 53,5 | 137,44 | 2026-08-19 | 2,38 |
| NVDA | 218,36 | 7,72 | 49,8 | 217,20 | 2026-09-10 | - |
| AMAT | 454,01 | 16,03 | 40,8 | 450,56 | 2026-09-10 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
