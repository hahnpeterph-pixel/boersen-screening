# Tiefs, Volumen und Kaufregel-Check

_Erstellt 2026-08-21 13:12 UTC. Fenster: letzte 50 Kalendertage. Ein Swing-Tief ist ein Tag, dessen Tagestief unter dem der 3 Tage davor und der 3 Tage danach liegt. Der laufende Tag zaehlt nie mit._

## Kaufregel

Die Knock-out-Schwelle soll **unter** einem markanten Tief liegen, mit mindestens **2,0 x ATR(14)** Abstand. Die ATR ist die mittlere Tagesschwankung des Basiswerts - ein fester Prozentsatz taugt nicht, weil er bei ruhigen und bei volatilen Werten voellig Unterschiedliches bedeutet.

Geprueft wird gegen zwei Bezugspunkte: das **juengste bestaetigte** Swing-Tief (aktuelle Trendstruktur) und das **tiefste** Tief im Fenster (strenger Massstab). Das Urteil richtet sich nach dem strengeren.

_Als juengstes Tief zaehlt auch das Tief des zuletzt abgeschlossenen Tages, sofern es unter den Vortagen liegt - im Report mit 'unbest.' markiert, weil die Bestaetigung durch Folgetage noch aussteht._

**Regel 1 (harte Sperre):** Der KO muss mindestens 1,00 unter dem Tief liegen - in der Waehrung des Basiswerts. Verhindert nur, dass der KO auf dem Tief klebt; als alleiniges Mass taugt sie nicht.

**Regel 2+3 (Positionsgroesse):** 50 EUR bei gerade noch erfuelltem Puffer, 150 EUR ab 2,0 x ATR, dazwischen linear. Bezugstief ist das **juengstes** Tief.

### Bestehende Positionen

| Wert | KO | juengstes Tief | tiefstes Tief | Abstand | Regel 1 | Urteil | |
|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) | 180,58 | 215,66 (20.08., unbest.) | 190,01 (29.07.) | 5,6 x ATR | erfuellt | OK | + |
| Applied Materials (AMAT) | 434,18 | 487,47 (20.08., unbest.) | 436,33 (29.07.) | 1,9 x ATR | erfuellt | knapp | ! |
| ASML (Amsterdam) (ASML.AS) | 1.450,24 | 1.333,80 (29.07.) | 1.333,80 (29.07.) | -2,2 x ATR | VERLETZT | REGELBRUCH (KO ueber Tief) | X |
| Take-Two (TTWO) | 228,77 | 231,58 (20.08., unbest.) | 228,20 (06.08.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Meta Platforms (META) | 520,39 | 524,49 (30.07.) | 524,49 (30.07.) | 0,2 x ATR | erfuellt | zu knapp | !! |
| Micron (MU) | 861,26 | 737,88 (29.07.) | 737,88 (29.07.) | -2,1 x ATR | VERLETZT | REGELBRUCH (KO ueber Tief) | X |
| Microsoft (MSFT) | 348,28 | 377,39 (23.07.) | 373,35 (09.07.) | 2,4 x ATR | erfuellt | OK | + |
| Oracle (ORCL) | 112,69 | 114,50 (28.07.) | 114,50 (28.07.) | 0,3 x ATR | erfuellt | zu knapp | !! |
| Gold (GC=F) | 4.171,71 | 4.315,00 (14.08.) | 3.964,20 (17.07.) | 1,6 x ATR | erfuellt | knapp | ! |

_Legende: `+` erfuellt (ab 2,0 x ATR), `!` knapp, `!!` zu knapp (unter 1,0 x ATR), `X` Regelbruch._

### Ueberhitzung — Verkaufssignal bestehender Positionen

Nur fuer Positionen mit `typ: Bestand`. RSI(14) nach Wilder-Glaettung; ab 70 gilt der Basiswert als ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges Warnsignal, unabhaengig vom RSI-Stand.

| Wert | RSI | Umkehrkerze | Urteil | |
|---|---|---|---|---|
| NVIDIA (NVDA) | 53,4 | nein | unauffaellig | + |
| Applied Materials (AMAT) | 43,8 | nein | unauffaellig | + |
| ASML (Amsterdam) (ASML.AS) | 48,6 | nein | unauffaellig | + |
| Take-Two (TTWO) | 48,7 | nein | unauffaellig | + |
| Meta Platforms (META) | 37,0 | nein | unauffaellig | + |
| Micron (MU) | 55,2 | nein | unauffaellig | + |
| Microsoft (MSFT) | 61,6 | nein | beobachten | ! |
| Oracle (ORCL) | 48,8 | nein | unauffaellig | + |
| Gold (GC=F) | 74,3 | nein | ueberhitzt (RSI) | !! |

_Legende: `+` unauffaellig, `!` beobachten (ab 60 RSI), `!!` ueberkauft (ab 70 RSI), `X` Umkehrkerze — reines Warnsignal, kein automatischer Verkauf._

## Verkaufssignal — bitte pruefen

- **Gold**: RSI 74,3 — ueberhitzt (RSI).

## Achtung

- **ASML (Amsterdam)**: Die KO-Schwelle 1.450,24 liegt nur -2,22 x ATR unter dem Tief 1.333,80 vom 29.07.2026. Regel 1 ist verletzt - der KO liegt nicht mindestens 1,00 unter dem Bezugstief. Kein Nachkauf.
- **Take-Two**: Die KO-Schwelle 228,77 liegt nur 0,31 x ATR unter dem Tief 231,58 vom 20.08.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Meta Platforms**: Die KO-Schwelle 520,39 liegt nur 0,21 x ATR unter dem Tief 524,49 vom 30.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.
- **Micron**: Die KO-Schwelle 861,26 liegt nur -2,10 x ATR unter dem Tief 737,88 vom 29.07.2026. Regel 1 ist verletzt - der KO liegt nicht mindestens 1,00 unter dem Bezugstief. Kein Nachkauf.
- **Oracle**: Die KO-Schwelle 112,69 liegt nur 0,26 x ATR unter dem Tief 114,50 vom 28.07.2026. Nach Regel 2 bedeutet das reduzierten Einsatz, kein Ausschluss.

### Positionsgroesse nach Regel 2

| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |
|---|---|---|---|---|---|
| NVIDIA (NVDA) | 215,66 (20.08., unbest.) | 5,57 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Applied Materials (AMAT) | 487,47 (20.08., unbest.) | 1,93 x ATR | 0,96 | **146,32 EUR** | kaufbar |
| ASML (Amsterdam) (ASML.AS) | 1.333,80 (29.07.) | -2,22 x ATR | 0,00 | **0,00 EUR** | Regel 1 verletzt - kein Kauf |
| Take-Two (TTWO) | 231,58 (20.08., unbest.) | 0,31 x ATR | 0,16 | **65,55 EUR** | kaufbar |
| Meta Platforms (META) | 524,49 (30.07.) | 0,21 x ATR | 0,11 | **60,70 EUR** | kaufbar |
| Micron (MU) | 737,88 (29.07.) | -2,10 x ATR | 0,00 | **0,00 EUR** | Regel 1 verletzt - kein Kauf |
| Microsoft (MSFT) | 377,39 (23.07.) | 2,44 x ATR | 1,00 | **150,00 EUR** | kaufbar |
| Oracle (ORCL) | 114,50 (28.07.) | 0,26 x ATR | 0,13 | **62,92 EUR** | kaufbar |
| Gold (GC=F) | 4.315,00 (14.08.) | 1,55 x ATR | 0,78 | **127,55 EUR** | kaufbar |

_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters steht in der Tabelle oben weiterhin zur Einordnung, geht aber nicht in die Bewertung ein._

### Empfohlene KO-Schwelle

Tief minus 2,0 x ATR. Die Hebelangabe ist das, was sich bei diesem KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel zulaesst.

| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |
|---|---|---|---|---|---|---|
| NVIDIA (NVDA) | 216,85 | 6,30 | 203,07 | 15,7x | 177,42 | 5,5x |
| Applied Materials (AMAT) | 496,21 | 27,66 | 432,14 | 7,7x | 381,00 | 4,3x |
| ASML (Amsterdam) (ASML.AS) | 1.514,40 | 52,53 | 1.228,74 | 5,3x | 1.228,74 | 5,3x |
| Take-Two (TTWO) | 240,15 | 9,03 | 213,51 | 9,0x | 210,13 | 8,0x |
| Meta Platforms (META) | 545,83 | 19,18 | 486,14 | 9,1x | 486,14 | 9,1x |
| Micron (MU) | 974,33 | 58,70 | 620,47 | 2,8x | 620,47 | 2,8x |
| Microsoft (MSFT) | 481,15 | 11,91 | 353,57 | 3,8x | 349,53 | 3,7x |
| Oracle (ORCL) | 142,07 | 6,99 | 100,53 | 3,4x | 100,53 | 3,4x |
| Gold (GC=F) | 4.639,20 | 92,38 | 4.130,24 | 9,1x | 3.779,44 | 5,4x |

_'nach Trendtief' orientiert sich am juengsten Tief und laesst mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief des Fensters und ueberlebt auch einen Rueckfall dorthin._

## Tiefs im Detail mit Volumen

| Wert | Datum | Tief | Volumen | rel. zu Ø 20 T | Tief -> KO |
|---|---|---|---|---|---|
| NVIDIA (NVDA) | 20.08.2026 | 215,66 | 92,3 Mio. | 0,78x (duenn) | 16,3 % |
| NVIDIA (NVDA) | 11.08.2026 | 216,20 | 101,3 Mio. | 0,80x (duenn) | 16,5 % |
| NVIDIA (NVDA) | 29.07.2026 | 190,01 | 147,7 Mio. | 1,13x | 5,0 % |
| Applied Materials (AMAT) | 20.08.2026 | 487,47 | 6,6 Mio. | 0,82x | 10,9 % |
| Applied Materials (AMAT) | 29.07.2026 | 436,33 | 10,2 Mio. | 1,09x | 0,5 % |
| Applied Materials (AMAT) | 17.07.2026 | 513,22 | 10,3 Mio. | 0,83x | 15,4 % |
| ASML (Amsterdam) (ASML.AS) | 29.07.2026 | 1.333,80 | 742 Tsd. | 1,07x | -8,7 % |
| ASML (Amsterdam) (ASML.AS) | 17.07.2026 | 1.491,00 | 921 Tsd. | 1,21x (erhoeht) | 2,7 % |
| ASML (Amsterdam) (ASML.AS) | 08.07.2026 | 1.496,60 | 608 Tsd. | 0,73x (duenn) | 3,1 % |
| Take-Two (TTWO) | 20.08.2026 | 231,58 | 2,4 Mio. | 1,10x | 1,2 % |
| Take-Two (TTWO) | 13.08.2026 | 239,52 | 1,7 Mio. | 0,77x (duenn) | 4,5 % |
| Take-Two (TTWO) | 06.08.2026 | 228,20 | 4,0 Mio. | 2,21x (Kapitulation) | -0,3 % |
| Meta Platforms (META) | 30.07.2026 | 524,49 | 42,3 Mio. | 2,22x (Kapitulation) | 0,8 % |
| Meta Platforms (META) | 09.07.2026 | 577,07 | 26,6 Mio. | 1,43x (erhoeht) | 9,8 % |
| Micron (MU) | 29.07.2026 | 737,88 | 69,8 Mio. | 1,55x (Kapitulation) | -16,7 % |
| Micron (MU) | 17.07.2026 | 804,00 | 63,3 Mio. | 1,21x (erhoeht) | -7,1 % |
| Micron (MU) | 07.07.2026 | 891,66 | 52,4 Mio. | 0,90x | 3,4 % |
| Microsoft (MSFT) | 23.07.2026 | 377,39 | 30,4 Mio. | 0,70x (duenn) | 7,7 % |
| Microsoft (MSFT) | 09.07.2026 | 373,35 | 31,1 Mio. | 0,64x (duenn) | 6,7 % |
| Oracle (ORCL) | 28.07.2026 | 114,50 | 32,7 Mio. | 0,82x | 1,6 % |
| Gold (GC=F) | 14.08.2026 | 4.315,00 | 1 Tsd. | 0,11x (duenn) | 3,3 % |
| Gold (GC=F) | 29.07.2026 | 4.017,90 | 90 Tsd. | 225,29x (Kapitulation) | -3,8 % |
| Gold (GC=F) | 17.07.2026 | 3.964,20 | 0 Tsd. | 0,17x (duenn) | -5,2 % |

---

_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. Volumen ist das Tagesvolumen der jeweiligen Referenzboerse. Keine Anlageberatung._
