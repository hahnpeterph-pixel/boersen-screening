# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-10 04:06 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 183,86 (30.10.) | 0,4 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 537,27 (19.08.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 650,00 (05.11.) | 0,9 x ATR | erfuellt | zu knapp | !! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 7,8 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 0,1 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 109,21 (06.11.) | 2,8 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 52,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 46,5 | nein | unauffaellig | + |
| Micron (MU) | 36,4 | nein | unauffaellig | + |
| Microsoft (MSFT) | 57,5 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 57,5 | nein | unauffaellig | + |
| Oracle (ORCL) | 41,9 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: Marke erreicht — CHART PRUEFEN. Kurs 178,67, Marke 209,00.
- **Applied Materials**: hoeheres Hoch + Marke erreicht — CHART PRUEFEN. Kurs 370,55, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,37 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 207,40 steht nur -2,85 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,23 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,92 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 733,15 steht nur -2,11 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,14 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Oracle**: Der Kurs 119,79 steht nur 0,80 x ATR ueber dem KO 112,72. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 178,67 | 209,00 | -14,5 % | 170,24 | 8,79 | 27,4 | 51,1 (111 Faelle, 33,9 % der Serien) | 152,67 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 370,55 | 465,00 | -20,3 % | 316,95 | 25,17 | 41,4 | 63,0 (343 Faelle, 100,0 % der Serien) | 266,62 | **150,00 EUR** | hoeheres Hoch + Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,37 x ATR | 0,18 | **68,37 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,23 x ATR | 0,11 | **61,46 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,92 x ATR | 0,46 | **96,06 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 7,79 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,14 x ATR | 0,07 | **56,83 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,81 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 207,40 | 7,51 | 191,34 | 12,9x | 168,84 | 5,4x |
| Meta Platforms (META) | 641,37 | 24,74 | 534,33 | 6,0x | 487,80 | 4,2x |
| Micron (MU) | 733,15 | 60,12 | 529,76 | 3,6x | 529,76 | 3,6x |
| Microsoft (MSFT) | 545,18 | 16,54 | 491,39 | 10,1x | 444,07 | 5,4x |
| Microsoft II (MSFT) | 545,18 | 16,54 | 491,39 | 10,1x | 444,07 | 5,4x |
| Oracle (ORCL) | 119,79 | 8,78 | 91,64 | 4,3x | 91,64 | 4,3x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 09.11.2026 | 206,36 | 6,0 Mio. | 2,19x (Kapitulation) | -10,9 % |
| Take-Two (TTWO) | 30.10.2026 | 183,86 | 3,6 Mio. | 1,58x (Kapitulation) | -24,5 % |
| Take-Two (TTWO) | 13.10.2026 | 196,30 | 5,2 Mio. | 2,11x (Kapitulation) | -16,6 % |
| Meta Platforms (META) | 05.11.2026 | 583,80 | 28,7 Mio. | 1,18x | 11,1 % |
| Meta Platforms (META) | 02.11.2026 | 606,41 | 19,5 Mio. | 0,84x | 14,4 % |
| Meta Platforms (META) | 28.10.2026 | 609,00 | 35,1 Mio. | 1,69x (Kapitulation) | 14,8 % |
| Micron (MU) | 05.11.2026 | 650,00 | 77,9 Mio. | 2,89x (Kapitulation) | -32,3 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Micron (MU) | 01.10.2026 | 1.022,90 | 45,7 Mio. | 1,83x (Kapitulation) | 15,9 % |
| Microsoft (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 33,6 % |
| Microsoft (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 31,0 % |
| Microsoft (MSFT) | 23.10.2026 | 515,70 | 13,7 Mio. | 0,64x (duenn) | 32,5 % |
| Microsoft II (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 9,5 % |
| Microsoft II (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 6,0 % |
| Microsoft II (MSFT) | 23.10.2026 | 515,70 | 13,7 Mio. | 0,64x (duenn) | 7,9 % |
| Oracle (ORCL) | 06.11.2026 | 109,21 | 47,6 Mio. | 1,12x | -3,2 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,7 Mio. | 1,85x (Kapitulation) | 4,8 % |
| Oracle (ORCL) | 26.10.2026 | 123,75 | 23,0 Mio. | 0,78x (duenn) | 8,9 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 207,40 | 7,51 | 52,3 | 231,58 | 2026-08-20 | 2,19 |
| META | 641,37 | 24,74 | 46,5 | 524,52 | 2026-07-30 | 1,18 |
| MU | 733,15 | 60,12 | 36,4 | 915,18 | 2026-08-19 | 2,89 |
| MSFT | 545,18 | 16,54 | 57,5 | 477,15 | 2026-08-18 | 1,07 |
| ORCL | 119,79 | 8,78 | 41,9 | 137,44 | 2026-08-19 | 1,12 |
| NVDA | 178,67 | 8,79 | 27,4 | 170,24 | 2026-11-09 | - |
| AMAT | 370,55 | 25,17 | 41,4 | 316,95 | 2026-11-05 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
