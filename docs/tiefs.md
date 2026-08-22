# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-08-22 06:39 UTC. Fenster: letzte 90 Kalendertage. Ein Swing-Tief ist ein Tag, dessen Tagestief unter dem der 3 Tage davor und der 3 Tage danach liegt. Der laufende Tag zaehlt nie mit._

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
| Microsoft (MSFT) | 348,28 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 12,2 x ATR | erfuellt | OK | + |
| Microsoft II (MSFT) | 474,89 | 477,15 (18.08., Chart) | 349,20 (25.06.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Oracle (ORCL) | 112,72 | 137,44 (19.08., Chart) | 114,50 (28.07.) | 3,8 x ATR | erfuellt | OK | + |
| Gold (Spot) (XAUUSD=X) | 4.171,71 | kein Swing-Tief im Fenster | | | - | k.A. | - |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| Take-Two (TTWO) | 48,3 | nein | unauffaellig | + |
| Meta Platforms (META) | 38,7 | nein | unauffaellig | + |
| Micron (MU) | 54,3 | nein | unauffaellig | + |
| Microsoft (MSFT) | 62,4 | nein | beobachten | ! |
| Microsoft II (MSFT) | 62,4 | nein | beobachten | ! |
| Oracle (ORCL) | 52,7 | nein | unauffaellig | + |
| Gold (Spot) (XAUUSD=X) | k.A. | k.A. | k.A. | - |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Kaufsignal — bitte pruefen

- **Applied Materials**: hoeheres Hoch — CHART PRUEFEN. Kurs 492,32, Marke 465,00.

## Achtung

- **Take-Two**: Die KO-Schwelle 228,82 liegt nur 0,30 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Meta Platforms**: Die KO-Schwelle 518,85 liegt nur 0,33 x ATR unter dem Tief 524,52 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 859,80 liegt nur 0,99 x ATR unter dem Tief 915,18 vom 19.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Die KO-Schwelle 474,89 liegt nur 0,21 x ATR unter dem Tief 477,15 vom 18.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Microsoft II**: Der Kurs 483,24 steht nur 0,79 x ATR ueber dem KO 474,89. Eine Tagesschwankung reicht rechnerisch fuer den Totalverlust.

## Ohne Befund

- **Gold (Spot)**: kein bestaetigtes Swing-Tief im Fenster. Entweder laeuft der Wert seit Wochen aufwaerts, oder `links`/`rechts` sind zu gross eingestellt.

### Kaufkandidaten — Umkehr abwarten

Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. RSI ueber 50 ist eine Warnung, keine Sperre. Der KO-Vorschlag ist Tief minus 2,0 x ATR - die tatsaechliche Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.

| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | KO-Vorschlag | Einsatz | Signal | |
|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) _Kandidat_ | 214,72 | 209,00 | 2,7 % | 214,50 | 5,75 | 51,0 | 203,00 | **150,00 EUR** | warten | - |
| Applied Materials (AMAT) _Kandidat_ | 492,32 | 465,00 | 5,9 % | 483,13 | 27,13 | 43,1 | 428,87 | **150,00 EUR** | hoeheres Hoch — CHART PRUEFEN | + |

_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, `-` warten._

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 231,58 (20.08., Chart) | 0,30 x ATR | 0,15 | **65,19 EUR** | kaufbar |
| Meta Platforms (META) | 524,52 (30.07., Chart) | 0,33 x ATR | 0,17 | **66,66 EUR** | kaufbar |
| Micron (MU) | 915,18 (19.08., Chart) | 0,99 x ATR | 0,49 | **99,25 EUR** | kaufbar |
| Microsoft (MSFT) | 477,15 (18.08., Chart) | 12,22 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Microsoft II (MSFT) | 477,15 (18.08., Chart) | 0,21 x ATR | 0,11 | **60,72 EUR** | kaufbar |
| Oracle (ORCL) | 137,44 (19.08., Chart) | 3,81 x ATR | 1,00 | **150,00 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| Take-Two (TTWO) | 239,62 | 9,08 | 221,35 | 13,1x | 187,83 | 4,6x |
| Meta Platforms (META) | 549,90 | 17,02 | 490,45 | 9,2x | 490,45 | 9,2x |
| Micron (MU) | 966,78 | 56,22 | 625,44 | 2,8x | 625,44 | 2,8x |
| Microsoft (MSFT) | 483,24 | 10,54 | 456,06 | 17,8x | 328,11 | 3,1x |
| Microsoft II (MSFT) | 483,24 | 10,54 | 456,06 | 17,8x | 328,11 | 3,1x |
| Oracle (ORCL) | 146,47 | 6,49 | 101,52 | 3,3x | 101,52 | 3,3x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| Take-Two (TTWO) | 13.08.2026 | 239,52 | 1,7 Mio. | 0,77x (duenn) | 4,5 % |
| Take-Two (TTWO) | 06.08.2026 | 228,20 | 4,0 Mio. | 2,21x (Kapitulation) | -0,3 % |
| Take-Two (TTWO) | 23.07.2026 | 228,50 | 1,5 Mio. | 0,63x (duenn) | -0,1 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 1,1 % |
| Meta Platforms (META) | 09.07.2026 | 577,07 | 26,6 Mio. | 1,43x (erhoeht) | 10,1 % |
| Meta Platforms (META) | 25.06.2026 | 540,18 | 17,0 Mio. | 0,87x | 3,9 % |
| Micron (MU) | 29.07.2026 | 737,88 | 69,8 Mio. | 1,55x (Kapitulation) | -16,5 % |
| Micron (MU) | 17.07.2026 | 804,00 | 63,3 Mio. | 1,21x (erhoeht) | -6,9 % |
| Micron (MU) | 07.07.2026 | 891,66 | 52,4 Mio. | 0,90x | 3,6 % |
| Microsoft (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 27,0 % |
| Microsoft (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | 7,7 % |
| Microsoft (MSFT) | 09.07.2026 | 373,35 | 31,1 Mio. | 0,64x (duenn) | 6,7 % |
| Microsoft II (MSFT) | 18.08.2026 | 477,15 | 24,1 Mio. | 0,64x (duenn) | 0,5 % |
| Microsoft II (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | -25,8 % |
| Microsoft II (MSFT) | 09.07.2026 | 373,35 | 31,1 Mio. | 0,64x (duenn) | -27,2 % |
| Oracle (ORCL) | 28.07.2026 | 114,50 | 32,7 Mio. | 0,82x | 1,6 % |
| Oracle (ORCL) | 11.06.2026 | 175,28 | 63,7 Mio. | 2,76x (Kapitulation) | 35,7 % |

## Fuer die Excel — Blatt 'Report'

_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._

| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |
|---|---|---|---|---|---|---|
| TTWO | 239,62 | 9,08 | 48,3 | 231,58 | 2026-08-20 | 0,77 |
| META | 549,90 | 17,02 | 38,7 | 524,52 | 2026-07-30 | 2,22 |
| MU | 966,78 | 56,22 | 54,3 | 915,18 | 2026-08-19 | 1,55 |
| MSFT | 483,24 | 10,54 | 62,4 | 477,15 | 2026-08-18 | 0,64 |
| ORCL | 146,47 | 6,49 | 52,7 | 137,44 | 2026-08-19 | 0,82 |
| NVDA | 214,72 | 5,75 | 51,0 | 214,50 | 2026-08-21 | - |
| AMAT | 492,32 | 27,13 | 43,1 | 483,13 | 2026-08-21 | - |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht n/a. Keine Anlageberatung._
