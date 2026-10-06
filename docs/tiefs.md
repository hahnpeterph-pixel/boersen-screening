# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-10-06 11:54 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 199,46 (28.09.) | 0,5 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,3 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 373,35 (09.07.) | 10,6 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 373,35 (09.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,9 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 38,3 | nein | unauffaellig | + |
| Meta Platforms (META) | 64,0 | nein | beobachten | ! |
| Micron (MU) | 57,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 66,2 | nein | beobachten | ! |
| Microsoft II (MSFT) | 66,2 | nein | beobachten | ! |
| Oracle (ORCL) | 48,5 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch — CHART PRUEFEN. Kurs 238,90, Marke 209,00.

## Verkaufssignal — bitte pruefen

- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,51 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 203,46 steht nur -4,72 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,20 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,19 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 238,90 | 209,00 | 14,3 % | 227,03 | 5,38 | 66,9 | 64,8 (328 Faelle, 100,0 % der Serien) | 216,28 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 542,28 | 465,00 | 16,6 % | 533,59 | 17,88 | 69,6 | k.A. (noch nie) | 497,82 | **150,00 EUR** | warten | - |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,51 x ATR | 0,26 | **75,71 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,20 x ATR | 0,10 | **59,89 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,32 x ATR | 0,66 | **116,15 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 10,59 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,19 x ATR | 0,09 | **59,29 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,92 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 203,46 | 5,37 | 189,70 | 14,8x | 188,72 | 13,8x |
| Meta Platforms (META) | 741,90 | 28,65 | 655,88 | 8,6x | 467,18 | 2,7x |
| Micron (MU) | 1.063,96 | 41,86 | 971,84 | 11,5x | 654,16 | 2,6x |
| Microsoft (MSFT) | 525,18 | 12,17 | 466,89 | 9,0x | 349,02 | 3,0x |
| Microsoft II (MSFT) | 525,18 | 12,17 | 466,89 | 9,0x | 349,02 | 3,0x |
| Oracle (ORCL) | 142,48 | 6,30 | 118,98 | 6,1x | 101,90 | 3,5x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 01.10.2026 | 200,44 | 2,7 Mio. | 1,06x | -14,2 % |
| Take-Two (TTWO) | 28.09.2026 | 199,46 | 2,1 Mio. | 0,73x (duenn) | -14,7 % |
| Take-Two (TTWO) | 21.09.2026 | 204,00 | 2,6 Mio. | 0,93x | -12,2 % |
| Meta Platforms (META) | 28.09.2026 | 713,19 | 27,9 Mio. | 1,22x (erhoeht) | 27,2 % |
| Meta Platforms (META) | 18.09.2026 | 660,80 | 27,6 Mio. | 1,53x (Kapitulation) | 21,5 % |
| Meta Platforms (META) | 01.09.2026 | 556,10 | 15,8 Mio. | 1,03x | 6,7 % |
| Micron (MU) | 05.10.2026 | 1.055,56 | 18,2 Mio. | 0,69x (duenn) | 18,5 % |
| Micron (MU) | 01.10.2026 | 1.022,90 | 45,7 Mio. | 1,83x (Kapitulation) | 15,9 % |
| Micron (MU) | 24.09.2026 | 1.044,00 | 22,1 Mio. | 0,87x | 17,6 % |
| Microsoft (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 29,1 % |
| Microsoft (MSFT) | 18.09.2026 | 491,10 | 39,6 Mio. | 1,97x (Kapitulation) | 29,1 % |
| Microsoft (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 28,5 % |
| Microsoft II (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 3,3 % |
| Microsoft II (MSFT) | 18.09.2026 | 491,10 | 39,6 Mio. | 1,97x (Kapitulation) | 3,3 % |
| Microsoft II (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 2,5 % |
| Oracle (ORCL) | 28.09.2026 | 131,58 | 36,1 Mio. | 1,08x | 14,3 % |
| Oracle (ORCL) | 24.09.2026 | 133,48 | 56,6 Mio. | 1,78x (Kapitulation) | 15,6 % |
| Oracle (ORCL) | 18.09.2026 | 144,40 | 39,3 Mio. | 1,35x (erhoeht) | 21,9 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 203,46 | 5,37 | 38,3 | 231,58 | 2026-08-20 | 1,06 |
| META | 741,90 | 28,65 | 64,0 | 524,52 | 2026-07-30 | 1,22 |
| MU | 1.063,96 | 41,86 | 57,3 | 915,18 | 2026-08-19 | 0,69 |
| MSFT | 525,18 | 12,17 | 66,2 | 477,15 | 2026-08-18 | 0,77 |
| ORCL | 142,48 | 6,30 | 48,5 | 137,44 | 2026-08-19 | 1,08 |
| NVDA | 238,90 | 5,38 | 66,9 | 227,03 | 2026-09-29 | - |
| AMAT | 542,28 | 17,88 | 69,6 | 533,59 | 2026-10-05 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
