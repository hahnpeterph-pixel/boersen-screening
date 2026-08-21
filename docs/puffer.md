# Puffer-Analyse - wie viel ATR braucht die KO-Schwelle?

_Erstellt 2026-08-21 22:12 UTC. Swing-Tief = tiefer als die 3 Tage davor und die 3 danach. Puffer immer in ATR(14) zum Zeitpunkt des Tiefs._

## Teil A - die eigenen Trades

_Bezugstief ist das juengste bestaetigte Swing-Tief vor dem Kauf. 'Unterschritten' misst, wie weit der Basiswert waehrend der Haltedauer darunter ging. 0,00 heisst: das Tief hat gehalten._

| Position | Basiswert | Kauf | Verkauf | Bezugstief | ATR | tiefster Kurs | unterschritten |
|---|---|---|---|---|---|---|---|
| Microsoft | MSFT | 2026-07-22 | 2026-08-10 | 372.65 | 11.74 | 376.68 | **0.00 ATR** |
| Oracle | ORCL | 2026-07-21 | 2026-08-10 | 137.07 | 8.3 | 114.5 | **2.72 ATR** |
| NVIDIA | NVDA | 2026-08-03 | 2026-08-21 | 197.97 | 7.47 | 196.85 | **0.15 ATR** |
| Rheinmetall | RHM.DE | 2026-08-11 | 2026-08-17 | 936.2 | 54.74 | 1128.0 | **0.00 ATR** |
| Gold | XAUUSD=X | 2026-08-14 | 2026-08-20 | - | - | - | keine Kursdaten |
| ASML | ASML | 2026-08-20 | 2026-08-21 | 1530.64 | 72.66 | 1741.01 | **0.00 ATR** |
| Applied Materials | AMAT | 2026-08-20 | 2026-08-21 | 435.86 | 34.91 | 483.13 | **0.00 ATR** |
| Take-Two | TTWO | 2026-08-20 | 2026-08-21 | 239.52 | 8.19 | 231.58 | **0.97 ATR** |
| Micron | MU | 2026-08-20 | 2026-08-21 | 737.88 | 71.07 | 929.07 | **0.00 ATR** |
| Gold II | XAUUSD=X | 2026-08-21 | 2026-08-21 | - | - | - | keine Kursdaten |

Von 8 Trades haben 5 das Bezugstief gehalten. Groesste Unterschreitung: 2.72 ATR.

## Teil B - alle Swing-Tiefs im Universum

_3 Jahre Kurshistorie. Gemessen wird die tiefste Unterschreitung innerhalb der naechsten 10 Handelstage - das entspricht ungefaehr der realen Haltedauer._

| Menge | Faelle | Tief haelt | Median | 75% | 90% | 95% | 99% |
|---|---|---|---|---|---|---|---|
| alle Tiefs | 11829 | 61% | 0.00 | 0.61 | 1.78 | 2.65 | 5.03 |
| nur tiefer als das vorherige Tief | 5411 | 62% | 0.00 | 0.52 | 1.72 | 2.61 | 5.19 |

### Welcher Puffer deckt wie viel ab?

| Puffer | alle Tiefs | nur tiefer als das vorherige |
|---|---|---|
| 1,0 ATR | 82% | 83% |
| 2,0 ATR | 92% | 92% |
| 3,0 ATR | 96% | 96% |
| 4,0 ATR | 98% | 98% |

### Nach Haltedauer

_Je laenger gehalten wird, desto mehr Zeit hat der Kurs, das Tief zu testen. Deshalb haengt der noetige Puffer an der Haltedauer._

| Fenster | Median | 90% | 95% | 2 ATR decken ab |
|---|---|---|---|---|
| 5 Handelstage | 0.00 | 0.40 | 0.83 | 99% |
| 10 Handelstage | 0.00 | 1.72 | 2.61 | 92% |
| 20 Handelstage | 0.18 | 3.29 | 4.50 | 80% |

_Ein Knock-out ist ein Totalverlust, kein Teilverlust. Ein Puffer, der 80% der Faelle abdeckt, heisst: jeder fuenfte Trade endet bei null._

## Teil C - welches Bezugstief lohnt sich?

_Fiktiver Trade je Swing-Tief: Einstieg am Bestaetigungstag, Ausstieg nach 5 Handelstagen, Knock-out zaehlt als -100%. Die Rendite ist die des Scheins, nicht des Basiswerts - sie ergibt sich aus dem Abstand zum KO. 'Abstand' ist der Weg vom Einstieg bis zur Schwelle in ATR und misst den Hebelverlust: je groesser, desto traeger der Schein._

| Bezugstief | Puffer | Faelle | Ausfallquote | Abstand Einstieg-KO | Rendite der Ueberlebenden | Erwartungswert |
|---|---|---|---|---|---|---|
| tiefstes 90 Tage | 3 ATR | 11706 | 2.0% | 9.08 ATR | +2.8% | **+0.8%** |
| tiefstes 60 Tage | 3 ATR | 11706 | 2.4% | 7.99 ATR | +3.2% | **+0.7%** |
| tiefstes 90 Tage | 2 ATR | 11706 | 3.9% | 8.08 ATR | +4.4% | **+0.3%** |
| tiefstes 60 Tage | 2 ATR | 11706 | 4.7% | 6.99 ATR | +5.1% | **+0.1%** |
| juengstes Tief | 3 ATR | 11706 | 6.7% | 4.60 ATR | +7.2% | **+0.0%** |
| tiefstes 90 Tage | 1 ATR | 11706 | 7.3% | 7.08 ATR | +7.6% | **-0.3%** |
| tiefstes 60 Tage | 1 ATR | 11706 | 8.8% | 5.99 ATR | +9.2% | **-0.5%** |
| juengstes Tief | 2 ATR | 11706 | 13.3% | 3.60 ATR | +13.4% | **-1.6%** |
| juengstes Tief | 1 ATR | 11706 | 25.4% | 2.60 ATR | +29.7% | **-3.2%** |

_Der Erwartungswert ist eine Rechengroesse, keine Prognose: er unterstellt festen Ausstieg nach 5 Tagen ohne Verkaufssignal, ohne Gebuehren und ohne Auswahl nach RSI oder Analysten. Er taugt zum Vergleich der Varianten untereinander, nicht als erwartete Depotrendite._