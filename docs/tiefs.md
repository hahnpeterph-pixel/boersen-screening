# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-10-23 21:56 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,1 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 11,7 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 477,15 (18.08.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,7 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 44,4 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Meta Platforms (META) | 35,7 | nein | unauffaellig | + |
| Micron (MU) | 38,2 | nein | unauffaellig | + |
| Microsoft (MSFT) | 52,6 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 52,6 | nein | unauffaellig | + |
| Oracle (ORCL) | 39,1 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 377,24, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Take-Two**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,44 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 203,69 steht nur -3,98 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,22 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 877,55 steht nur 0,35 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,20 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 210,96 | 209,00 | 0,9 % | 210,18 | 5,98 | 38,1 | k.A. (noch nie) | 198,22 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 377,24 | 465,00 | -18,9 % | 372,80 | 20,56 | 26,1 | 52,1 (130 Faelle, 37,6 % der Serien) | 331,67 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,44 x ATR | 0,22 | **71,86 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,22 x ATR | 0,11 | **61,21 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,10 x ATR | 0,55 | **105,02 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 11,67 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,20 x ATR | 0,10 | **60,23 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,75 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 203,69 | 6,31 | 190,90 | 15,9x | 183,67 | 10,2x |
| Meta Platforms (META) | 642,62 | 25,28 | 582,70 | 10,7x | 473,92 | 3,8x |
| Micron (MU) | 877,55 | 50,33 | 748,59 | 6,8x | 637,22 | 3,7x |
| Microsoft (MSFT) | 524,51 | 11,04 | 493,62 | 17,0x | 455,07 | 7,6x |
| Microsoft II (MSFT) | 524,51 | 11,04 | 493,62 | 17,0x | 455,07 | 7,6x |
| Oracle (ORCL) | 126,16 | 6,60 | 109,56 | 7,6x | 101,30 | 5,1x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 23.10.2026 | 203,53 | 1,6 Mio. | 0,67x (duenn) | -12,4 % |
| Take-Two (TTWO) | 13.10.2026 | 196,30 | 5,2 Mio. | 2,11x (Kapitulation) | -16,6 % |
| Take-Two (TTWO) | 01.10.2026 | 200,44 | 2,7 Mio. | 1,06x | -14,2 % |
| Meta Platforms (META) | 23.10.2026 | 633,27 | 14,7 Mio. | 0,74x (duenn) | 18,1 % |
| Meta Platforms (META) | 20.10.2026 | 681,05 | 17,0 Mio. | 0,85x | 23,8 % |
| Meta Platforms (META) | 08.10.2026 | 711,68 | 16,0 Mio. | 0,72x (duenn) | 27,1 % |
| Micron (MU) | 22.10.2026 | 849,25 | 32,2 Mio. | 1,22x (erhoeht) | -1,2 % |
| Micron (MU) | 01.10.2026 | 1.022,90 | 45,7 Mio. | 1,83x (Kapitulation) | 15,9 % |
| Micron (MU) | 24.09.2026 | 1.044,00 | 22,1 Mio. | 0,87x | 17,6 % |
| Microsoft (MSFT) | 23.10.2026 | 515,70 | 13,6 Mio. | 0,64x (duenn) | 32,5 % |
| Microsoft (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 32,9 % |
| Microsoft (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 29,1 % |
| Microsoft II (MSFT) | 23.10.2026 | 515,70 | 13,6 Mio. | 0,64x (duenn) | 7,9 % |
| Microsoft II (MSFT) | 08.10.2026 | 518,79 | 20,2 Mio. | 0,92x | 8,5 % |
| Microsoft II (MSFT) | 24.09.2026 | 491,22 | 16,7 Mio. | 0,77x (duenn) | 3,3 % |
| Oracle (ORCL) | 22.10.2026 | 122,76 | 36,6 Mio. | 1,20x | 8,2 % |
| Oracle (ORCL) | 16.10.2026 | 127,36 | 36,1 Mio. | 1,18x | 11,5 % |
| Oracle (ORCL) | 08.10.2026 | 134,66 | 42,4 Mio. | 1,23x (erhoeht) | 16,3 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 203,69 | 6,31 | 44,4 | 231,58 | 2026-08-20 | 0,67 |
| META | 642,62 | 25,28 | 35,7 | 524,52 | 2026-07-30 | 0,74 |
| MU | 877,55 | 50,33 | 38,2 | 915,18 | 2026-08-19 | 1,22 |
| MSFT | 524,51 | 11,04 | 52,6 | 477,15 | 2026-08-18 | 0,64 |
| ORCL | 126,16 | 6,60 | 39,1 | 137,44 | 2026-08-19 | 1,20 |
| NVDA | 210,96 | 5,98 | 38,1 | 210,18 | 2026-10-23 | - |
| AMAT | 377,24 | 20,56 | 26,1 | 372,80 | 2026-10-23 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
