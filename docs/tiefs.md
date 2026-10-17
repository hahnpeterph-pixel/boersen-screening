# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-10-17 00:29 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 196,30 (13.10.) | 0,4 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,2 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 377,39 (23.07.) | 11,0 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 377,39 (23.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,6 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 45,8 | nein | unauffaellig | + |
| Meta Platforms (META) | 50,2 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Micron (MU) | 34,0 | nein | unauffaellig | + |
| Microsoft (MSFT) | 57,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft II (MSFT) | 57,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Oracle (ORCL) | 39,7 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch — CHART PRUEFEN. Kurs 214,13, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 409,29, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Meta Platforms**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft II**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,42 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 205,28 steht nur -3,55 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,26 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 878,84 steht nur 0,40 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,19 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 214,13 | 209,00 | 2,5 % | 212,85 | 5,76 | 37,5 | 64,6 (328 Faelle, 100,0 % der Serien) | 201,33 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 409,29 | 465,00 | -12,0 % | 407,52 | 20,62 | 29,2 | k.A. (noch nie) | 366,28 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,42 x ATR | 0,21 | **70,79 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,26 x ATR | 0,13 | **62,82 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,17 x ATR | 0,59 | **108,60 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 10,98 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,19 x ATR | 0,10 | **59,63 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,56 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 205,28 | 6,64 | 183,02 | 9,2x | 183,02 | 9,2x |
| Meta Platforms (META) | 709,33 | 22,11 | 658,48 | 14,0x | 480,26 | 3,1x |
| Micron (MU) | 878,84 | 47,25 | 763,50 | 7,6x | 643,38 | 3,7x |
| Microsoft (MSFT) | 529,05 | 11,74 | 500,95 | 18,8x | 353,91 | 3,0x |
| Microsoft II (MSFT) | 529,05 | 11,74 | 500,95 | 18,8x | 353,91 | 3,0x |
| Oracle (ORCL) | 128,23 | 6,94 | 113,48 | 8,7x | 100,62 | 4,6x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 13.10.2026 | 196,30 | 5,2 Mio. | 2,11x (Kapitulation) | -16,6 % |
| Take-Two (TTWO) | 01.10.2026 | 200,44 | 2,7 Mio. | 1,06x | -14,2 % |
| Take-Two (TTWO) | 28.09.2026 | 199,46 | 2,1 Mio. | 0,73x (duenn) | -14,7 % |
| Meta Platforms (META) | 16.10.2026 | 702,71 | 20,4 Mio. | 0,92x | 26,2 % |
| Meta Platforms (META) | 08.10.2026 | 711,68 | 16,0 Mio. | 0,72x (duenn) | 27,1 % |
| Meta Platforms (META) | 18.09.2026 | 660,80 | 27,6 Mio. | 1,53x (Kapitulation) | 21,5 % |
| Micron (MU) | 15.10.2026 | 858,00 | 39,1 Mio. | 1,48x (erhoeht) | -0,2 % |
| Micron (MU) | 01.10.2026 | 1.022,90 | 45,7 Mio. | 1,83x (Kapitulation) | 15,9 % |
| Micron (MU) | 24.09.2026 | 1.044,00 | 22,1 Mio. | 0,87x | 17,6 % |
| Microsoft (MSFT) | 16.10.2026 | 524,43 | 24,1 Mio. | 1,05x | 33,6 % |
| Microsoft (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 32,9 % |
| Microsoft (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 29,1 % |
| Microsoft II (MSFT) | 16.10.2026 | 524,43 | 24,1 Mio. | 1,05x | 9,4 % |
| Microsoft II (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 8,5 % |
| Microsoft II (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 3,3 % |
| Oracle (ORCL) | 16.10.2026 | 127,36 | 34,8 Mio. | 1,13x | 11,5 % |
| Oracle (ORCL) | 08.10.2026 | 134,66 | 42,4 Mio. | 1,23x (erhoeht) | 16,3 % |
| Oracle (ORCL) | 28.09.2026 | 131,58 | 36,1 Mio. | 1,08x | 14,3 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 205,28 | 6,64 | 45,8 | 231,58 | 2026-08-20 | 2,11 |
| META | 709,33 | 22,11 | 50,2 | 524,52 | 2026-07-30 | 0,92 |
| MU | 878,84 | 47,25 | 34,0 | 915,18 | 2026-08-19 | 1,48 |
| MSFT | 529,05 | 11,74 | 57,3 | 477,15 | 2026-08-18 | 1,05 |
| ORCL | 128,23 | 6,94 | 39,7 | 137,44 | 2026-08-19 | 1,13 |
| NVDA | 214,13 | 5,76 | 37,5 | 212,85 | 2026-10-15 | - |
| AMAT | 409,29 | 20,62 | 29,2 | 407,52 | 2026-10-16 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
