# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-09-26 00:39 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 200,55 (25.09.) | 0,4 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,2 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 373,35 (09.07.) | 11,8 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 373,35 (09.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,2 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 32,6 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 71,3 | nein | ueberhitzt (RSI) | !! |
| Micron (MU) | 63,2 | nein | beobachten | ! |
| Microsoft (MSFT) | 63,2 | nein | beobachten | ! |
| Microsoft II (MSFT) | 63,2 | nein | beobachten | ! |
| Oracle (ORCL) | 40,6 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch — CHART PRUEFEN. Kurs 225,07, Marke 209,00.
- **Applied Materials**: hoeheres Hoch — CHART PRUEFEN. Kurs 485,00, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Meta Platforms**: RSI 71,3 — ueberhitzt (RSI).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,41 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 201,44 steht nur -4,10 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,19 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,21 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 225,07 | 209,00 | 7,7 % | 221,09 | 5,22 | 55,2 | 65,2 (123 Faelle, 100,0 % der Serien) | 210,64 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 485,00 | 465,00 | 4,3 % | 460,55 | 18,23 | 55,7 | 62,0 (139 Faelle, 100,0 % der Serien) | 424,09 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,41 x ATR | 0,21 | **70,65 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,19 x ATR | 0,10 | **59,58 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,24 x ATR | 0,62 | **112,13 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 11,78 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,21 x ATR | 0,10 | **60,33 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,21 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 201,44 | 6,68 | 187,18 | 14,1x | 187,18 | 14,1x |
| Meta Platforms (META) | 751,66 | 29,58 | 601,64 | 5,0x | 465,33 | 2,6x |
| Micron (MU) | 1.082,28 | 44,57 | 954,86 | 8,5x | 648,74 | 2,5x |
| Microsoft (MSFT) | 516,17 | 10,94 | 469,34 | 11,0x | 351,47 | 3,1x |
| Microsoft II (MSFT) | 516,17 | 10,94 | 469,34 | 11,0x | 351,47 | 3,1x |
| Oracle (ORCL) | 137,10 | 7,70 | 118,07 | 7,2x | 99,09 | 3,6x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 25.09.2026 | 200,55 | 2,1 Mio. | 0,70x (duenn) | -14,1 % |
| Take-Two (TTWO) | 21.09.2026 | 204,00 | 2,6 Mio. | 0,93x | -12,2 % |
| Take-Two (TTWO) | 09.09.2026 | 208,52 | 2,2 Mio. | 0,85x | -9,7 % |
| Meta Platforms (META) | 18.09.2026 | 660,80 | 27,6 Mio. | 1,53x (Kapitulation) | 21,5 % |
| Meta Platforms (META) | 01.09.2026 | 556,10 | 15,8 Mio. | 1,03x | 6,7 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Micron (MU) | 24.09.2026 | 1.044,00 | 22,1 Mio. | 0,87x | 17,6 % |
| Micron (MU) | 16.09.2026 | 917,64 | 20,2 Mio. | 0,80x (duenn) | 6,3 % |
| Micron (MU) | 14.09.2026 | 902,60 | 27,1 Mio. | 1,04x | 4,7 % |
| Microsoft (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 29,1 % |
| Microsoft (MSFT) | 18.09.2026 | 491,10 | 39,6 Mio. | 1,97x (Kapitulation) | 29,1 % |
| Microsoft (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 28,5 % |
| Microsoft II (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 3,3 % |
| Microsoft II (MSFT) | 18.09.2026 | 491,10 | 39,6 Mio. | 1,97x (Kapitulation) | 3,3 % |
| Microsoft II (MSFT) | 16.09.2026 | 487,23 | 16,7 Mio. | 0,81x | 2,5 % |
| Oracle (ORCL) | 24.09.2026 | 133,48 | 56,6 Mio. | 1,78x (Kapitulation) | 15,6 % |
| Oracle (ORCL) | 18.09.2026 | 144,40 | 39,3 Mio. | 1,35x (erhoeht) | 21,9 % |
| Oracle (ORCL) | 16.09.2026 | 139,00 | 34,4 Mio. | 1,22x (erhoeht) | 18,9 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 201,44 | 6,68 | 32,6 | 231,58 | 2026-08-20 | 0,70 |
| META | 751,66 | 29,58 | 71,3 | 524,52 | 2026-07-30 | 1,53 |
| MU | 1.082,28 | 44,57 | 63,2 | 915,18 | 2026-08-19 | 0,87 |
| MSFT | 516,17 | 10,94 | 63,2 | 477,15 | 2026-08-18 | 0,77 |
| ORCL | 137,10 | 7,70 | 40,6 | 137,44 | 2026-08-19 | 1,78 |
| NVDA | 225,07 | 5,22 | 55,2 | 221,09 | 2026-09-24 | - |
| AMAT | 485,00 | 18,23 | 55,7 | 460,55 | 2026-09-24 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
