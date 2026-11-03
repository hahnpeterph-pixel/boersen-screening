# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-03 12:46 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 183,86 (30.10.) | 0,5 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 537,27 (19.08.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 827,00 (06.08.) | 1,1 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 10,1 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 118,43 (02.11.) | 3,0 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 34,8 | nein | unauffaellig | + |
| Meta Platforms (META) | 31,7 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Micron (MU) | 37,4 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 40,1 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft II (MSFT) | 40,1 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Oracle (ORCL) | 38,3 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch + Marke erreicht — CHART PRUEFEN. Kurs 202,06, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 374,53, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Meta Platforms**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Microsoft II**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).
- **Oracle**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,48 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 192,10 steht nur -6,35 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,24 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 833,59 steht nur -0,51 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,18 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Oracle**: Der Kurs 119,22 steht nur 0,78 x ATR ueber dem KO 112,72. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 202,06 | 209,00 | -3,3 % | 200,92 | 6,74 | 33,3 | 51,1 (111 Faelle, 33,9 % der Serien) | 187,45 | **150,00 EUR** | hoeheres Hoch + Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 374,53 | 465,00 | -19,5 % | 373,25 | 20,98 | 33,3 | k.A. (noch nie) | 331,29 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,48 x ATR | 0,24 | **73,86 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,24 x ATR | 0,12 | **62,04 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,08 x ATR | 0,54 | **104,08 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 10,08 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,18 x ATR | 0,09 | **58,84 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,98 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 192,10 | 5,78 | 172,29 | 9,7x | 172,29 | 9,7x |
| Meta Platforms (META) | 606,73 | 23,54 | 559,33 | 12,8x | 490,19 | 5,2x |
| Micron (MU) | 833,59 | 51,20 | 726,84 | 7,8x | 724,60 | 7,6x |
| Microsoft (MSFT) | 507,12 | 12,79 | 479,39 | 18,3x | 451,58 | 9,1x |
| Microsoft II (MSFT) | 507,12 | 12,79 | 479,39 | 18,3x | 451,58 | 9,1x |
| Oracle (ORCL) | 119,22 | 8,30 | 101,83 | 6,9x | 101,83 | 6,9x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 30.10.2026 | 183,86 | 3,6 Mio. | 1,58x (Kapitulation) | -24,5 % |
| Take-Two (TTWO) | 13.10.2026 | 196,30 | 5,2 Mio. | 2,11x (Kapitulation) | -16,6 % |
| Take-Two (TTWO) | 01.10.2026 | 200,44 | 2,7 Mio. | 1,06x | -14,2 % |
| Meta Platforms (META) | 02.11.2026 | 606,41 | 19,4 Mio. | 0,84x | 14,4 % |
| Meta Platforms (META) | 28.10.2026 | 609,00 | 35,1 Mio. | 1,69x (Kapitulation) | 14,8 % |
| Meta Platforms (META) | 20.10.2026 | 681,05 | 17,0 Mio. | 0,85x | 23,8 % |
| Micron (MU) | 02.11.2026 | 829,24 | 29,7 Mio. | 1,14x | -3,7 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Micron (MU) | 01.10.2026 | 1.022,90 | 45,7 Mio. | 1,83x (Kapitulation) | 15,9 % |
| Microsoft (MSFT) | 02.11.2026 | 504,96 | 34,6 Mio. | 1,57x (Kapitulation) | 31,0 % |
| Microsoft (MSFT) | 23.10.2026 | 515,70 | 13,7 Mio. | 0,64x (duenn) | 32,5 % |
| Microsoft (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 32,9 % |
| Microsoft II (MSFT) | 02.11.2026 | 504,96 | 34,6 Mio. | 1,57x (Kapitulation) | 6,0 % |
| Microsoft II (MSFT) | 23.10.2026 | 515,70 | 13,7 Mio. | 0,64x (duenn) | 7,9 % |
| Microsoft II (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 8,5 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,5 Mio. | 1,85x (Kapitulation) | 4,8 % |
| Oracle (ORCL) | 26.10.2026 | 123,75 | 23,0 Mio. | 0,78x (duenn) | 8,9 % |
| Oracle (ORCL) | 22.10.2026 | 122,76 | 36,6 Mio. | 1,20x | 8,2 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 192,10 | 5,78 | 34,8 | 231,58 | 2026-08-20 | 1,58 |
| META | 606,73 | 23,54 | 31,7 | 524,52 | 2026-07-30 | 0,84 |
| MU | 833,59 | 51,20 | 37,4 | 915,18 | 2026-08-19 | 1,14 |
| MSFT | 507,12 | 12,79 | 40,1 | 477,15 | 2026-08-18 | 1,57 |
| ORCL | 119,22 | 8,30 | 38,3 | 137,44 | 2026-08-19 | 1,85 |
| NVDA | 202,06 | 6,74 | 33,3 | 200,92 | 2026-10-30 | - |
| AMAT | 374,53 | 20,98 | 33,3 | 373,25 | 2026-11-02 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
