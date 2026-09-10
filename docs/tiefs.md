# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-09-10 11:12 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Take-Two (TTWO) | 228,82 | 231,58 (20.08., Chart) | 206,00 (11.06.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 518,85 | 524,52 (30.07., Chart) | 524,49 (30.07.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,3 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 13,0 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,8 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 28,9 | nein | unauffaellig | + |
| Meta Platforms (META) | 70,4 | nein | ueberhitzt (RSI) | !! |
| Micron (MU) | 60,6 | nein | beobachten | ! |
| Microsoft (MSFT) | 54,6 | nein | unauffaellig | + |
| Microsoft II (MSFT) | 54,6 | nein | unauffaellig | + |
| Oracle (ORCL) | 62,4 | nein | beobachten | ! |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **Applied Materials**: hoeheres Hoch — CHART PRUEFEN. Kurs 468,85, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Meta Platforms**: RSI 70,4 — ueberhitzt (RSI).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,34 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 211,14 steht nur -2,16 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,28 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,23 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. Die Spalte Schwelle ist wertspezifisch (Entscheidung 79): p75 des RSI an den historischen Tiefs dieses Wertes an genau der Tiefsposition, an der er heute steht, mit Fallzahl und Anteil der Abwaertsserien, die so weit kamen. Keine Mindestfallzahl, keine Pauschale, kein Pooling ueber Werte. Der RSI loest KEIN Urteil und keine Ampel aus - RSI und Schwelle nebeneinander sind die Einordnung, entschieden wird am Chart. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 223,67 | 209,00 | 7,0 % | 223,46 | 7,56 | 54,3 | k.A. (noch nie) | 208,34 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 468,85 | 465,00 | 0,8 % | 426,13 | 15,61 | 44,4 | 36,2 (8 Faelle, 5,7 % der Serien) | 394,92 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,34 x ATR | 0,17 | **66,87 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,28 x ATR | 0,14 | **64,24 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,26 x ATR | 0,63 | **112,82 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 13,04 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,23 x ATR | 0,11 | **61,43 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,81 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 211,14 | 8,18 | 192,16 | 11,1x | 189,64 | 9,8x |
| Meta Platforms (META) | 653,69 | 19,90 | 516,29 | 4,8x | 484,68 | 3,9x |
| Micron (MU) | 1.027,77 | 44,08 | 830,72 | 5,2x | 649,72 | 2,7x |
| Microsoft (MSFT) | 491,65 | 9,89 | 470,03 | 22,7x | 329,43 | 3,0x |
| Microsoft II (MSFT) | 491,65 | 9,89 | 470,03 | 22,7x | 329,43 | 3,0x |
| Oracle (ORCL) | 161,63 | 6,48 | 147,39 | 11,4x | 101,53 | 2,7x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 09.09.2026 | 208,52 | 2,2 Mio. | 0,85x | -9,7 % |
| Take-Two (TTWO) | 01.09.2026 | 214,14 | 2,8 Mio. | 1,03x | -6,9 % |
| Take-Two (TTWO) | 27.08.2026 | 225,10 | 4,2 Mio. | 1,85x (Kapitulation) | -1,7 % |
| Meta Platforms (META) | 01.09.2026 | 556,10 | 15,8 Mio. | 1,03x | 6,7 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 1,1 % |
| Micron (MU) | 03.09.2026 | 918,88 | 24,2 Mio. | 0,86x | 6,4 % |
| Micron (MU) | 24.08.2026 | 887,61 | 30,0 Mio. | 0,77x (duenn) | 3,1 % |
| Micron (MU) | 19.08.2026 | 915,18 | 26,9 Mio. | 0,65x (duenn) | 6,1 % |
| Microsoft (MSFT) | 09.09.2026 | 489,80 | 12,9 Mio. | 0,58x (duenn) | 28,9 % |
| Microsoft (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 29,5 % |
| Microsoft (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 27,2 % |
| Microsoft II (MSFT) | 09.09.2026 | 489,80 | 12,9 Mio. | 0,58x (duenn) | 3,0 % |
| Microsoft II (MSFT) | 02.09.2026 | 493,81 | 15,3 Mio. | 0,61x (duenn) | 3,8 % |
| Microsoft II (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 0,8 % |
| Oracle (ORCL) | 09.09.2026 | 160,36 | 27,4 Mio. | 1,17x | 29,7 % |
| Oracle (ORCL) | 02.09.2026 | 139,72 | 21,9 Mio. | 0,97x | 19,3 % |
| Oracle (ORCL) | 24.08.2026 | 141,25 | 14,2 Mio. | 0,49x (duenn) | 20,2 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 211,14 | 8,18 | 28,9 | 231,58 | 2026-08-20 | 0,85 |
| META | 653,69 | 19,90 | 70,4 | 524,52 | 2026-07-30 | 1,03 |
| MU | 1.027,77 | 44,08 | 60,6 | 915,18 | 2026-08-19 | 0,86 |
| MSFT | 491,65 | 9,89 | 54,6 | 477,15 | 2026-08-18 | 0,58 |
| ORCL | 161,63 | 6,48 | 62,4 | 137,44 | 2026-08-19 | 1,17 |
| NVDA | 223,67 | 7,56 | 54,3 | 223,46 | 2026-09-09 | - |
| AMAT | 468,85 | 15,61 | 44,4 | 426,13 | 2026-09-03 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
