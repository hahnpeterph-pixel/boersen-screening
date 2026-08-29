# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-08-29 03:43 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,1 x ATR | erfuellt | knapp | ! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 13,2 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,9 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 45,8 | nein | unauffaellig | + |
| Meta Platforms (META) | 49,6 | nein | unauffaellig | + |
| Micron (MU) | 50,7 | nein | unauffaellig | + |
| Microsoft (MSFT) | 73,1 | nein | ueberhitzt (RSI) | !! |
| Microsoft II (MSFT) | 73,1 | nein | ueberhitzt (RSI) | !! |
| Oracle (ORCL) | 56,1 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **Applied Materials**: Marke erreicht — CHART PRUEFEN. Kurs 461,67, Marke 465,00.

## Verkaufssignal — bitte pruefen

- **Microsoft**: RSI 73,1 — ueberhitzt (RSI).
- **Microsoft II**: RSI 73,1 — ueberhitzt (RSI).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,34 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Take-Two**: Der Kurs 235,39 steht nur 0,81 x ATR ueber dem KO 228,82. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,30 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,23 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. RSI ueber 50 ist eine Warnung, keine Sperre. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 217,55 | 209,00 | 4,1 % | 216,82 | 6,87 | 52,3 | 203,07 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 461,67 | 465,00 | -0,7 % | 460,52 | 23,10 | 37,6 | 414,33 | **150,00 EUR** | Marke erreicht — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,34 x ATR | 0,17 | **67,10 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,30 x ATR | 0,15 | **65,18 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 1,08 x ATR | 0,54 | **104,01 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 13,19 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,23 x ATR | 0,12 | **61,57 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,94 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 235,39 | 8,07 | 208,96 | 8,9x | 189,86 | 5,2x |
| Meta Platforms (META) | 578,02 | 18,68 | 499,91 | 7,4x | 487,13 | 6,4x |
| Micron (MU) | 932,86 | 51,27 | 785,08 | 6,3x | 635,35 | 3,1x |
| Microsoft (MSFT) | 513,53 | 9,77 | 458,99 | 9,4x | 329,66 | 2,8x |
| Microsoft II (MSFT) | 513,53 | 9,77 | 458,99 | 9,4x | 329,66 | 2,8x |
| Oracle (ORCL) | 150,85 | 6,27 | 128,70 | 6,8x | 101,95 | 3,1x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 27.08.2026 | 225,10 | 4,2 Mio. | 1,85x (Kapitulation) | -1,7 % |
| Take-Two (TTWO) | 25.08.2026 | 232,44 | 1,6 Mio. | 0,69x (duenn) | 1,6 % |
| Take-Two (TTWO) | 20.08.2026 | 231,58 | 2,4 Mio. | 1,10x | 1,2 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 1,1 % |
| Meta Platforms (META) | 17.07.2026 | 626,00 | 22,3 Mio. | 1,07x | 17,1 % |
| Micron (MU) | 24.08.2026 | 887,61 | 30,0 Mio. | 0,77x (duenn) | 3,1 % |
| Micron (MU) | 19.08.2026 | 915,18 | 26,9 Mio. | 0,65x (duenn) | 6,1 % |
| Micron (MU) | 06.08.2026 | 827,00 | 35,8 Mio. | 0,78x (duenn) | -4,0 % |
| Microsoft (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 27,2 % |
| Microsoft (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 27,0 % |
| Microsoft (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | 7,7 % |
| Microsoft II (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 0,8 % |
| Microsoft II (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 0,5 % |
| Microsoft II (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | -25,8 % |
| Oracle (ORCL) | 24.08.2026 | 141,25 | 14,2 Mio. | 0,49x (duenn) | 20,2 % |
| Oracle (ORCL) | 19.08.2026 | 137,43 | 26,6 Mio. | 0,86x | 18,0 % |
| Oracle (ORCL) | 11.08.2026 | 144,24 | 28,8 Mio. | 0,80x (duenn) | 21,9 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 235,39 | 8,07 | 45,8 | 231,58 | 2026-08-20 | 1,85 |
| META | 578,02 | 18,68 | 49,6 | 524,52 | 2026-07-30 | 1,00 |
| MU | 932,86 | 51,27 | 50,7 | 915,18 | 2026-08-19 | 0,77 |
| MSFT | 513,53 | 9,77 | 73,1 | 477,15 | 2026-08-18 | 0,61 |
| ORCL | 150,85 | 6,27 | 56,1 | 137,44 | 2026-08-19 | 0,49 |
| NVDA | 217,55 | 6,87 | 52,3 | 216,82 | 2026-08-28 | - |
| AMAT | 461,67 | 23,10 | 37,6 | 460,52 | 2026-08-28 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
