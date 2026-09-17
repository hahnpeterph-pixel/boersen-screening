# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-09-17 22:00 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 207,77 (17.09.) | 0,4 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,3 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 12,6 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,1 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 36,0 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 74,0 | nein | ueberhitzt (RSI) | !! |
| Micron (MU) | 53,8 | nein | unauffaellig | + |
| Microsoft (MSFT) | 55,6 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 55,6 | nein | unauffaellig | + |
| Oracle (ORCL) | 52,2 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch — CHART PRUEFEN. Kurs 219,34, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 417,40, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Meta Platforms**: RSI 74,0 — ueberhitzt (RSI).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,36 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 210,62 steht nur -2,36 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,27 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,22 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 219,34 | 209,00 | 4,9 % | 208,93 | 6,49 | 51,7 | 51,6 (35 Faelle, 28,5 % der Serien) | 195,95 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 417,40 | 465,00 | -10,2 % | 411,51 | 17,35 | 33,8 | 36,2 (8 Faelle, 5,7 % der Serien) | 376,81 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,36 x ATR | 0,18 | **67,90 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,27 x ATR | 0,14 | **63,51 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,29 x ATR | 0,65 | **114,57 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 12,58 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,22 x ATR | 0,11 | **61,03 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,06 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 210,62 | 7,71 | 192,35 | 11,5x | 192,35 | 11,5x |
| Meta Platforms (META) | 682,31 | 20,99 | 625,07 | 11,9x | 482,51 | 3,4x |
| Micron (MU) | 977,50 | 42,89 | 831,87 | 6,7x | 652,11 | 3,0x |
| Microsoft (MSFT) | 497,75 | 10,25 | 466,74 | 16,0x | 328,71 | 2,9x |
| Microsoft II (MSFT) | 497,75 | 10,25 | 466,74 | 16,0x | 328,71 | 2,9x |
| Oracle (ORCL) | 150,59 | 8,08 | 122,85 | 5,4x | 98,35 | 2,9x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 17.09.2026 | 207,77 | 2,6 Mio. | 0,98x | -10,1 % |
| Take-Two (TTWO) | 09.09.2026 | 208,52 | 2,2 Mio. | 0,85x | -9,7 % |
| Take-Two (TTWO) | 01.09.2026 | 214,14 | 2,8 Mio. | 1,03x | -6,9 % |
| Meta Platforms (META) | 17.09.2026 | 667,05 | 15,7 Mio. | 0,87x | 22,2 % |
| Meta Platforms (META) | 01.09.2026 | 556,10 | 15,8 Mio. | 1,03x | 6,7 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Micron (MU) | 16.09.2026 | 917,64 | 20,2 Mio. | 0,80x (duenn) | 6,3 % |
| Micron (MU) | 14.09.2026 | 902,60 | 27,1 Mio. | 1,04x | 4,7 % |
| Micron (MU) | 03.09.2026 | 918,88 | 24,2 Mio. | 0,86x | 6,4 % |
| Microsoft (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 28,5 % |
| Microsoft (MSFT) | 10.09.2026 | 486,00 | 16,0 Mio. | 0,73x (duenn) | 28,3 % |
| Microsoft (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 29,5 % |
| Microsoft II (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 2,5 % |
| Microsoft II (MSFT) | 10.09.2026 | 486,00 | 16,0 Mio. | 0,73x (duenn) | 2,3 % |
| Microsoft II (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 3,8 % |
| Oracle (ORCL) | 16.09.2026 | 139,00 | 34,4 Mio. | 1,22x (erhoeht) | 18,9 % |
| Oracle (ORCL) | 02.09.2026 | 139,72 | 21,9 Mio. | 0,97x | 19,3 % |
| Oracle (ORCL) | 24.08.2026 | 141,25 | 14,2 Mio. | 0,49x (duenn) | 20,2 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 210,62 | 7,71 | 36,0 | 231,58 | 2026-08-20 | 0,98 |
| META | 682,31 | 20,99 | 74,0 | 524,52 | 2026-07-30 | 0,87 |
| MU | 977,50 | 42,89 | 53,8 | 915,18 | 2026-08-19 | 0,80 |
| MSFT | 497,75 | 10,25 | 55,6 | 477,15 | 2026-08-18 | 0,81 |
| ORCL | 150,59 | 8,08 | 52,2 | 137,44 | 2026-08-19 | 1,22 |
| NVDA | 219,34 | 6,49 | 51,7 | 208,93 | 2026-09-14 | - |
| AMAT | 417,40 | 17,35 | 33,8 | 411,51 | 2026-09-16 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
