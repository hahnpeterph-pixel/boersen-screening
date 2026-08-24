# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-08-24 16:49 UTC. Fenster: letzte 90 Kalendertage. Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. Solange es abwaerts geht, gilt das tiefste Tief der Strecke. Gerechnet wird auf abgeschlossenen Tageskerzen._

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
| Micron (MU) | 859,80 | 915,18 (19.08., Chart) | 737,88 (29.07.) | 1,0 x ATR | erfuellt | zu knapp | !! |
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 13,3 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,9 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | KEINE KURSDATEN | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 49,8 | nein | unauffaellig | + |
| Meta Platforms (META) | 41,3 | nein | unauffaellig | + |
| Micron (MU) | 49,0 | ja | VERKAUFSSIGNAL (Umkehrkerze) | X |
| Microsoft (MSFT) | 64,6 | nein | beobachten | ! |
| Microsoft II (MSFT) | 64,6 | nein | beobachten | ! |
| Oracle (ORCL) | 50,0 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Verkaufssignal — bitte pruefen

- **Micron**: Umkehrkerze — VERKAUFSSIGNAL (Umkehrkerze).

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,31 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,34 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,98 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Der Kurs 915,68 steht nur 0,99 x ATR ueber dem KO 859,80. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,23 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

## Ohne Befund

- **Gold (Spot)** (XAUUSD=X): keine Kursdaten von Yahoo. Der Wert wird uebersprungen, alle Angaben fehlen. Bei Edelmetallen liegt es am Spot-Ticker - der Future waere ein Ersatz, notiert aber hoeher (Contango), deshalb wird hier NICHT automatisch umgeschaltet: die KO-Pruefung wuerde sonst falsch rechnen.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. RSI ueber 50 ist eine Warnung, keine Sperre. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 210,16 | 209,00 | 0,6 % | 208,62 | 5,79 | 46,2 | 197,04 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 482,15 | 465,00 | 3,7 % | 473,67 | 26,22 | 41,4 | 421,24 | **150,00 EUR** | warten | - |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,31 x ATR | 0,15 | **65,30 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,34 x ATR | 0,17 | **66,89 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,98 x ATR | 0,49 | **98,87 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 13,26 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,23 x ATR | 0,12 | **61,63 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,91 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 241,25 | 9,02 | 218,51 | 10,6x | 187,96 | 4,5x |
| Meta Platforms (META) | 556,43 | 16,78 | 503,71 | 10,6x | 490,93 | 8,5x |
| Micron (MU) | 915,68 | 56,66 | 774,28 | 6,5x | 624,55 | 3,1x |
| Microsoft (MSFT) | 488,87 | 9,72 | 459,09 | 16,4x | 329,76 | 3,1x |
| Microsoft II (MSFT) | 488,87 | 9,72 | 459,09 | 16,4x | 329,76 | 3,1x |
| Oracle (ORCL) | 143,57 | 6,31 | 128,63 | 9,6x | 101,87 | 3,4x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 24.08.2026 | 236,55 | 892 Tsd. | 0,39x (duenn) | 3,3 % |
| Take-Two (TTWO) | 20.08.2026 | 231,58 | 2,4 Mio. | 1,10x | 1,2 % |
| Take-Two (TTWO) | 17.08.2026 | 241,04 | 1,7 Mio. | 0,79x (duenn) | 5,1 % |
| Meta Platforms (META) | 19.08.2026 | 537,27 | 17,0 Mio. | 1,00x | 3,4 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 1,1 % |
| Meta Platforms (META) | 17.07.2026 | 626,00 | 22,3 Mio. | 1,07x | 17,1 % |
| Micron (MU) | 24.08.2026 | 887,60 | 17,8 Mio. | 0,45x (duenn) | 3,1 % |
| Micron (MU) | 19.08.2026 | 915,18 | 26,9 Mio. | 0,65x (duenn) | 6,1 % |
| Micron (MU) | 06.08.2026 | 827,00 | 35,8 Mio. | 0,78x (duenn) | -4,0 % |
| Microsoft (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 27,2 % |
| Microsoft (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 27,0 % |
| Microsoft (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | 7,7 % |
| Microsoft II (MSFT) | 21.08.2026 | 478,53 | 22,5 Mio. | 0,61x (duenn) | 0,8 % |
| Microsoft II (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 0,5 % |
| Microsoft II (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | -25,8 % |
| Oracle (ORCL) | 24.08.2026 | 141,26 | 7,9 Mio. | 0,27x (duenn) | 20,2 % |
| Oracle (ORCL) | 19.08.2026 | 137,43 | 26,6 Mio. | 0,86x | 18,0 % |
| Oracle (ORCL) | 11.08.2026 | 144,24 | 28,8 Mio. | 0,80x (duenn) | 21,9 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 241,25 | 9,02 | 49,8 | 231,58 | 2026-08-20 | 0,39 |
| META | 556,43 | 16,78 | 41,3 | 524,52 | 2026-07-30 | 1,00 |
| MU | 915,68 | 56,66 | 49,0 | 915,18 | 2026-08-19 | 0,45 |
| MSFT | 488,87 | 9,72 | 64,6 | 477,15 | 2026-08-18 | 0,61 |
| ORCL | 143,57 | 6,31 | 50,0 | 137,44 | 2026-08-19 | 0,27 |
| NVDA | 210,16 | 5,79 | 46,2 | 208,62 | 2026-08-24 | - |
| AMAT | 482,15 | 26,22 | 41,4 | 473,67 | 2026-08-24 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
