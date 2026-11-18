# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-18 01:32 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 183,86 (30.10.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 537,27 (19.08.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 650,00 (05.11.) | 0,8 x ATR | erfuellt | zu knapp | !! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 478,53 (21.08.) | 6,9 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 478,53 (21.08.) | 0,1 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 109,21 (06.11.) | 2,9 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 45,5 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 42,1 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Micron (MU) | 37,5 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 41,9 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft II (MSFT) | 41,9 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Oracle (ORCL) | 40,0 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: Marke erreicht — CHART PRUEFEN. Kurs 155,46, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 349,22, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Meta Platforms**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft II**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Oracle**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,23 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 203,96 steht nur -2,07 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,26 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,83 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 712,42 steht nur -2,20 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,12 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Oracle**: Der Kurs 115,05 steht nur 0,27 x ATR ueber dem KO 112,72. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 155,46 | 209,00 | -25,6 % | 150,33 | 11,44 | 22,5 | 38,3 (20 Faelle, 6,1 % der Serien) | 127,44 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 349,22 | 465,00 | -24,9 % | 338,00 | 27,51 | 38,6 | 63,0 (343 Faelle, 100,0 % der Serien) | 282,97 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,23 x ATR | 0,11 | **61,47 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,26 x ATR | 0,13 | **63,13 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,83 x ATR | 0,41 | **91,40 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 6,86 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,12 x ATR | 0,06 | **56,01 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,86 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 203,96 | 12,03 | 177,61 | 7,7x | 159,81 | 4,6x |
| Meta Platforms (META) | 618,91 | 21,58 | 570,34 | 12,7x | 494,10 | 5,0x |
| Micron (MU) | 712,42 | 66,89 | 533,10 | 4,0x | 516,22 | 3,6x |
| Microsoft (MSFT) | 506,30 | 18,80 | 458,92 | 10,7x | 440,94 | 7,7x |
| Microsoft II (MSFT) | 506,30 | 18,80 | 458,92 | 10,7x | 440,94 | 7,7x |
| Oracle (ORCL) | 115,05 | 8,64 | 95,76 | 6,0x | 91,93 | 5,0x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 17.11.2026 | 201,66 | 6,0 Mio. | 1,70x (Kapitulation) | -13,5 % |
| Take-Two (TTWO) | 12.11.2026 | 223,16 | 3,3 Mio. | 1,01x | -2,5 % |
| Take-Two (TTWO) | 09.11.2026 | 206,36 | 6,1 Mio. | 2,21x (Kapitulation) | -10,9 % |
| Meta Platforms (META) | 17.11.2026 | 613,51 | 18,3 Mio. | 0,78x (duenn) | 15,4 % |
| Meta Platforms (META) | 12.11.2026 | 618,92 | 10,3 Mio. | 0,42x (duenn) | 16,2 % |
| Meta Platforms (META) | 05.11.2026 | 583,80 | 28,7 Mio. | 1,18x | 11,1 % |
| Micron (MU) | 17.11.2026 | 666,88 | 62,3 Mio. | 2,03x (Kapitulation) | -28,9 % |
| Micron (MU) | 05.11.2026 | 650,00 | 77,9 Mio. | 2,89x (Kapitulation) | -32,3 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Microsoft (MSFT) | 17.11.2026 | 496,51 | 67,6 Mio. | 2,52x (Kapitulation) | 29,9 % |
| Microsoft (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 32,2 % |
| Microsoft (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 33,6 % |
| Microsoft II (MSFT) | 17.11.2026 | 496,51 | 67,6 Mio. | 2,52x (Kapitulation) | 4,4 % |
| Microsoft II (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 7,6 % |
| Microsoft II (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 9,5 % |
| Oracle (ORCL) | 17.11.2026 | 113,04 | 32,4 Mio. | 0,78x (duenn) | 0,3 % |
| Oracle (ORCL) | 06.11.2026 | 109,21 | 47,6 Mio. | 1,12x | -3,2 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,7 Mio. | 1,85x (Kapitulation) | 4,8 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 203,96 | 12,03 | 45,5 | 231,58 | 2026-08-20 | 1,70 |
| META | 618,91 | 21,58 | 42,1 | 524,52 | 2026-07-30 | 0,78 |
| MU | 712,42 | 66,89 | 37,5 | 915,18 | 2026-08-19 | 2,03 |
| MSFT | 506,30 | 18,80 | 41,9 | 477,15 | 2026-08-18 | 2,52 |
| ORCL | 115,05 | 8,64 | 40,0 | 137,44 | 2026-08-19 | 0,78 |
| NVDA | 155,46 | 11,44 | 22,5 | 150,33 | 2026-11-17 | - |
| AMAT | 349,22 | 27,51 | 38,6 | 338,00 | 2026-11-17 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
