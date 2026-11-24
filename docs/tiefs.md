# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-24 04:16 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 556,10 (01.09.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 585,25 (20.11.) | 0,7 x ATR | erfuellt | zu knapp | !! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 481,03 (20.11.) | 6,7 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 481,03 (20.11.) | 0,1 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 100,25 (20.11.) | 2,8 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 49,1 | nein | unauffaellig | + |
| Meta Platforms (META) | 41,7 | nein | unauffaellig | + |
| Micron (MU) | 42,5 | nein | unauffaellig | + |
| Microsoft (MSFT) | 39,1 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 39,1 | nein | unauffaellig | + |
| Oracle (ORCL) | 43,4 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch + Marke erreicht — CHART PRUEFEN. Kurs 165,05, Marke 209,00.
- **Applied Materials**: hoeheres Hoch + Marke erreicht — CHART PRUEFEN. Kurs 346,87, Marke 465,00.

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,19 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 209,36 steht nur -1,31 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,22 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,74 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 707,70 steht nur -2,04 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,12 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Der Kurs 492,50 steht nur 0,91 x ATR ueber dem KO 474,89. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Oracle**: Der Kurs 113,68 steht nur 0,11 x ATR ueber dem KO 112,72. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 165,05 | 209,00 | -21,0 % | 124,50 | 15,62 | 42,9 | 37,2 (8 Faelle, 2,5 % der Serien) | 93,26 | **150,00 EUR** | hoeheres Hoch + Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 346,87 | 465,00 | -25,4 % | 300,62 | 30,01 | 43,1 | 52,3 (129 Faelle, 37,6 % der Serien) | 240,60 | **150,00 EUR** | hoeheres Hoch + Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,19 x ATR | 0,09 | **59,27 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,22 x ATR | 0,11 | **61,20 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,74 x ATR | 0,37 | **87,10 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 6,69 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,12 x ATR | 0,06 | **55,87 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,85 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 209,36 | 14,88 | 170,24 | 5,4x | 154,09 | 3,8x |
| Meta Platforms (META) | 597,60 | 25,31 | 508,07 | 6,7x | 505,49 | 6,5x |
| Micron (MU) | 707,70 | 74,64 | 435,96 | 2,6x | 435,96 | 2,6x |
| Microsoft (MSFT) | 492,50 | 19,27 | 442,50 | 9,8x | 442,50 | 9,8x |
| Microsoft II (MSFT) | 492,50 | 19,27 | 442,50 | 9,8x | 442,50 | 9,8x |
| Oracle (ORCL) | 113,68 | 8,68 | 82,90 | 3,7x | 82,90 | 3,7x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 20.11.2026 | 200,01 | 10,6 Mio. | 2,35x (Kapitulation) | -14,4 % |
| Take-Two (TTWO) | 17.11.2026 | 201,66 | 6,3 Mio. | 1,79x (Kapitulation) | -13,5 % |
| Take-Two (TTWO) | 12.11.2026 | 223,16 | 3,3 Mio. | 1,01x | -2,5 % |
| Meta Platforms (META) | 20.11.2026 | 558,68 | 25,7 Mio. | 1,22x (erhoeht) | 7,1 % |
| Meta Platforms (META) | 12.11.2026 | 618,92 | 10,3 Mio. | 0,42x (duenn) | 16,2 % |
| Meta Platforms (META) | 05.11.2026 | 583,80 | 28,7 Mio. | 1,18x | 11,1 % |
| Micron (MU) | 20.11.2026 | 585,25 | 59,4 Mio. | 1,86x (Kapitulation) | -46,9 % |
| Micron (MU) | 17.11.2026 | 666,88 | 33,5 Mio. | 1,09x | -28,9 % |
| Micron (MU) | 05.11.2026 | 650,00 | 77,9 Mio. | 2,89x (Kapitulation) | -32,3 % |
| Microsoft (MSFT) | 20.11.2026 | 481,03 | 47,2 Mio. | 1,67x (Kapitulation) | 27,6 % |
| Microsoft (MSFT) | 17.11.2026 | 496,51 | 28,0 Mio. | 1,04x | 29,9 % |
| Microsoft (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 32,2 % |
| Microsoft II (MSFT) | 20.11.2026 | 481,03 | 47,2 Mio. | 1,67x (Kapitulation) | 1,3 % |
| Microsoft II (MSFT) | 17.11.2026 | 496,51 | 28,0 Mio. | 1,04x | 4,4 % |
| Microsoft II (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 7,6 % |
| Oracle (ORCL) | 20.11.2026 | 100,25 | 47,8 Mio. | 1,17x | -12,4 % |
| Oracle (ORCL) | 06.11.2026 | 109,21 | 47,6 Mio. | 1,12x | -3,2 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,7 Mio. | 1,85x (Kapitulation) | 4,8 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 209,36 | 14,88 | 49,1 | 231,58 | 2026-08-20 | 2,35 |
| META | 597,60 | 25,31 | 41,7 | 524,52 | 2026-07-30 | 1,22 |
| MU | 707,70 | 74,64 | 42,5 | 915,18 | 2026-08-19 | 1,86 |
| MSFT | 492,50 | 19,27 | 39,1 | 477,15 | 2026-08-18 | 1,67 |
| ORCL | 113,68 | 8,68 | 43,4 | 137,44 | 2026-08-19 | 1,17 |
| NVDA | 165,05 | 15,62 | 42,9 | 124,50 | 2026-11-20 | - |
| AMAT | 346,87 | 30,01 | 43,1 | 300,62 | 2026-11-20 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
