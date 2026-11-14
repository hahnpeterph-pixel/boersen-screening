# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-11-14 06:32 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 183,86 (30.10.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 537,27 (19.08.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 650,00 (05.11.) | 0,9 x ATR | erfuellt | zu knapp | !! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 7,3 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 0,1 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 109,21 (06.11.) | 2,6 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 64,1 | nein | beobachten | ! |
| Meta Platforms (META) | 47,8 | nein | unauffaellig | + |
| Micron (MU) | 42,5 | nein | unauffaellig | + |
| Microsoft (MSFT) | 48,8 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 48,8 | nein | unauffaellig | + |
| Oracle (ORCL) | 47,1 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **NVIDIA**: hoeheres Hoch + Marke erreicht — CHART PRUEFEN. Kurs 162,85, Marke 209,00.
- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 370,50, Marke 465,00.

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,28 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 227,82 steht nur -0,10 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,27 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,85 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 778,31 steht nur -1,26 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,13 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 162,85 | 209,00 | -22,1 % | 148,80 | 11,00 | 24,9 | 38,3 (20 Faelle, 6,1 % der Serien) | 126,79 | **150,00 EUR** | hoeheres Hoch + Marke erreicht — CHART PRUEFEN | + |
| Applied Materials (AMAT) _Kandidat_ | 370,50 | 465,00 | -20,3 % | 352,23 | 27,32 | 42,6 | 63,0 (343 Faelle, 100,0 % der Serien) | 297,58 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,28 x ATR | 0,14 | **64,05 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,27 x ATR | 0,14 | **63,53 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,85 x ATR | 0,43 | **92,69 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 7,34 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,13 x ATR | 0,06 | **56,44 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 2,61 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 227,82 | 9,82 | 203,52 | 9,4x | 164,22 | 3,6x |
| Meta Platforms (META) | 641,69 | 20,96 | 577,00 | 9,9x | 495,35 | 4,4x |
| Micron (MU) | 778,31 | 64,86 | 620,53 | 4,9x | 520,28 | 3,0x |
| Microsoft (MSFT) | 523,88 | 17,55 | 478,71 | 11,6x | 442,04 | 6,4x |
| Microsoft II (MSFT) | 523,88 | 17,55 | 478,71 | 11,6x | 442,04 | 6,4x |
| Oracle (ORCL) | 125,35 | 9,46 | 102,85 | 5,6x | 90,30 | 3,6x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 12.11.2026 | 223,16 | 3,3 Mio. | 1,01x | -2,5 % |
| Take-Two (TTWO) | 09.11.2026 | 206,36 | 6,1 Mio. | 2,21x (Kapitulation) | -10,9 % |
| Take-Two (TTWO) | 30.10.2026 | 183,86 | 3,6 Mio. | 1,58x (Kapitulation) | -24,5 % |
| Meta Platforms (META) | 12.11.2026 | 618,92 | 10,3 Mio. | 0,42x (duenn) | 16,2 % |
| Meta Platforms (META) | 05.11.2026 | 583,80 | 28,7 Mio. | 1,18x | 11,1 % |
| Meta Platforms (META) | 02.11.2026 | 606,41 | 19,5 Mio. | 0,84x | 14,4 % |
| Micron (MU) | 13.11.2026 | 750,25 | 27,8 Mio. | 0,90x | -14,6 % |
| Micron (MU) | 05.11.2026 | 650,00 | 77,9 Mio. | 2,89x (Kapitulation) | -32,3 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Microsoft (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 32,2 % |
| Microsoft (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 33,6 % |
| Microsoft (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 31,0 % |
| Microsoft II (MSFT) | 13.11.2026 | 513,82 | 26,2 Mio. | 1,00x | 7,6 % |
| Microsoft II (MSFT) | 06.11.2026 | 524,47 | 27,0 Mio. | 1,07x | 9,5 % |
| Microsoft II (MSFT) | 02.11.2026 | 504,96 | 34,7 Mio. | 1,58x (Kapitulation) | 6,0 % |
| Oracle (ORCL) | 13.11.2026 | 121,76 | 22,5 Mio. | 0,53x (duenn) | 7,4 % |
| Oracle (ORCL) | 06.11.2026 | 109,21 | 47,6 Mio. | 1,12x | -3,2 % |
| Oracle (ORCL) | 02.11.2026 | 118,43 | 58,7 Mio. | 1,85x (Kapitulation) | 4,8 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 227,82 | 9,82 | 64,1 | 231,58 | 2026-08-20 | 1,01 |
| META | 641,69 | 20,96 | 47,8 | 524,52 | 2026-07-30 | 0,42 |
| MU | 778,31 | 64,86 | 42,5 | 915,18 | 2026-08-19 | 0,90 |
| MSFT | 523,88 | 17,55 | 48,8 | 477,15 | 2026-08-18 | 1,00 |
| ORCL | 125,35 | 9,46 | 47,1 | 137,44 | 2026-08-19 | 0,53 |
| NVDA | 162,85 | 11,00 | 24,9 | 148,80 | 2026-11-12 | - |
| AMAT | 370,50 | 27,32 | 42,6 | 352,23 | 2026-11-13 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
