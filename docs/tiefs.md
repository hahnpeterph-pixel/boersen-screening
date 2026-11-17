# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-17 14:18 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 7,2 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 0,1 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 109,21 (06.11.) | 2,6 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 51,7 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 43,9 | nein | unauffaellig | + |
| Micron (MU) | 38,0 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 46,4 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 46,4 | nein | unauffaellig | + |
| Oracle (ORCL) | 42,6 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: Marke erreicht — CHART PRUEFEN. Kurs 156,14, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 350,25, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Oracle**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,25 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 213,47 steht nur -1,37 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,26 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,83 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 719,02 steht nur -2,10 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,13 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Oracle**: Der Kurs 119,09 steht nur 0,67 x ATR ueber dem KO 112,72. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 156,14 | 209,00 | -25,3 % | 155,01 | 11,33 | 22,7 | 38,3 (20 Faelle, 6,1 % der Serien) | 132,35 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 350,25 | 465,00 | -24,7 % | 346,01 | 28,10 | 38,8 | 63,0 (343 Faelle, 100,0 % der Serien) | 289,81 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,25 x ATR | 0,12 | **62,36 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,26 x ATR | 0,13 | **63,07 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,83 x ATR | 0,41 | **91,34 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 7,20 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,13 x ATR | 0,06 | **56,32 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,60 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 213,47 | 11,17 | 200,82 | 16,9x | 161,52 | 4,1x |
| Meta Platforms (META) | 626,41 | 21,69 | 576,77 | 12,6x | 493,90 | 4,7x |
| Micron (MU) | 719,02 | 66,99 | 582,41 | 5,3x | 516,03 | 3,5x |
| Microsoft (MSFT) | 517,99 | 17,89 | 478,03 | 13,0x | 441,36 | 6,8x |
| Microsoft II (MSFT) | 517,99 | 17,89 | 478,03 | 13,0x | 441,36 | 6,8x |
| Oracle (ORCL) | 119,09 | 9,51 | 99,22 | 6,0x | 90,18 | 4,1x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 12.11.2026 | 223,16 | 3,3 Mio. | 1,01x | -2,5 % |
| Take-Two (TTWO) | 09.11.2026 | 206,36 | 6,1 Mio. | 2,21x (Kapitulation) | -10,9 % |
| Take-Two (TTWO) | 30.10.2026 | 183,86 | 3,6 Mio. | 1,58x (Kapitulation) | -24,5 % |
| Meta Platforms (META) | 16.11.2026 | 620,14 | 11,5 Mio. | 0,49x (duenn) | 16,3 % |
| Meta Platforms (META) | 12.11.2026 | 618,92 | 10,3 Mio. | 0,42x (duenn) | 16,2 % |
| Meta Platforms (META) | 05.11.2026 | 583,80 | 28,7 Mio. | 1,18x | 11,1 % |
| Micron (MU) | 16.11.2026 | 716,38 | 26,7 Mio. | 0,87x | -20,0 % |
| Micron (MU) | 05.11.2026 | 650,00 | 77,9 Mio. | 2,89x (Kapitulation) | -32,3 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Microsoft (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 32,2 % |
| Microsoft (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 33,6 % |
| Microsoft (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 31,0 % |
| Microsoft II (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 7,6 % |
| Microsoft II (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 9,5 % |
| Microsoft II (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 6,0 % |
| Oracle (ORCL) | 16.11.2026 | 118,25 | 20,1 Mio. | 0,48x (duenn) | 4,7 % |
| Oracle (ORCL) | 06.11.2026 | 109,21 | 47,6 Mio. | 1,12x | -3,2 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,7 Mio. | 1,85x (Kapitulation) | 4,8 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 213,47 | 11,17 | 51,7 | 231,58 | 2026-08-20 | 1,01 |
| META | 626,41 | 21,69 | 43,9 | 524,52 | 2026-07-30 | 0,49 |
| MU | 719,02 | 66,99 | 38,0 | 915,18 | 2026-08-19 | 0,87 |
| MSFT | 517,99 | 17,89 | 46,4 | 477,15 | 2026-08-18 | 1,00 |
| ORCL | 119,09 | 9,51 | 42,6 | 137,44 | 2026-08-19 | 0,48 |
| NVDA | 156,14 | 11,33 | 22,7 | 155,01 | 2026-11-16 | - |
| AMAT | 350,25 | 28,10 | 38,8 | 346,01 | 2026-11-16 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
