# Puffer-Analyse - wie viel ATR braucht die KO-Schwelle?

_Erstellt 2026-08-21 22:19 UTC. Swing-Tief = tiefer als die 3 Tage davor und die 3 danach. Puffer immer in ATR(14) zum Zeitpunkt des Tiefs._

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
| alle Tiefs | 11816 | 61% | 0.00 | 0.61 | 1.78 | 2.64 | 5.03 |
| nur tiefer als das vorherige Tief | 5403 | 62% | 0.00 | 0.52 | 1.72 | 2.60 | 5.19 |

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
| 5 Handelstage | 0.00 | 0.39 | 0.83 | 99% |
| 10 Handelstage | 0.00 | 1.72 | 2.60 | 92% |
| 20 Handelstage | 0.18 | 3.29 | 4.49 | 80% |

_Ein Knock-out ist ein Totalverlust, kein Teilverlust. Ein Puffer, der 80% der Faelle abdeckt, heisst: jeder fuenfte Trade endet bei null._

## Teil C - welches Bezugstief lohnt sich?

_Fiktiver Trade je Swing-Tief: Einstieg am Bestaetigungstag, Ausstieg nach 5 Handelstagen, Knock-out zaehlt als -100%. Die Rendite ist die des Scheins, nicht des Basiswerts - sie ergibt sich aus dem Abstand zum KO. 'Abstand' ist der Weg vom Einstieg bis zur Schwelle in ATR und misst den Hebelverlust: je groesser, desto traeger der Schein._

| Bezugstief | Puffer | Faelle | Ausfallquote | Abstand Einstieg-KO | Rendite der Ueberlebenden | Erwartungswert |
|---|---|---|---|---|---|---|
| tiefstes 90 Tage | 3 ATR | 11693 | 2.0% | 9.08 ATR | +2.8% | **+0.8%** |
| tiefstes 60 Tage | 3 ATR | 11693 | 2.4% | 7.99 ATR | +3.2% | **+0.7%** |
| tiefstes 90 Tage | 2 ATR | 11693 | 3.9% | 8.08 ATR | +4.4% | **+0.3%** |
| tiefstes 60 Tage | 2 ATR | 11693 | 4.7% | 6.99 ATR | +5.1% | **+0.1%** |
| juengstes Tief | 3 ATR | 11693 | 6.7% | 4.60 ATR | +7.2% | **+0.0%** |
| tiefstes 90 Tage | 1 ATR | 11693 | 7.3% | 7.08 ATR | +7.6% | **-0.3%** |
| tiefstes 60 Tage | 1 ATR | 11693 | 8.8% | 5.99 ATR | +9.2% | **-0.5%** |
| juengstes Tief | 2 ATR | 11693 | 13.3% | 3.60 ATR | +13.5% | **-1.6%** |
| juengstes Tief | 1 ATR | 11693 | 25.3% | 2.60 ATR | +29.7% | **-3.2%** |

## Teil D - woran erkennt man ein Tief, das haelt?

_Ein Tief 'haelt', wenn es in den 10 Handelstagen nach der Bestaetigung um hoechstens 1.0 ATR unterschritten wird. Alle Merkmale sind am Einstiegstag bekannt - kein Blick in die Zukunft. 'Unterschied' zeigt die Abweichung von der Grundquote: nur wo er deutlich positiv ist, hilft das Merkmal bei der Auswahl._

| Merkmal | Auspraegung | Faelle | Haltequote | Unterschied |
|---|---|---|---|---|
| Alle Faelle | Grundquote | 8663 | 74.7% |  |
| Stellung in der Tiefpunktfolge | 1. Tief der Folge | 4591 | 73.1% | -1.6 Punkte |
| Stellung in der Tiefpunktfolge | 2. Tief | 2220 | 75.5% | +0.8 Punkte |
| Stellung in der Tiefpunktfolge | 3. Tief | 1037 | 77.3% | +2.6 Punkte |
| Stellung in der Tiefpunktfolge | 4. Tief oder spaeter | 815 | **78.0%** | +3.3 Punkte |
| RSI am Tief | unter 30 | 733 | **82.0%** | +7.3 Punkte |
| RSI am Tief | 30 bis 40 | 2094 | 77.1% | +2.4 Punkte |
| RSI am Tief | 40 bis 50 | 2890 | 73.5% | -1.2 Punkte |
| RSI am Tief | ueber 50 | 2946 | 72.4% | -2.3 Punkte |
| RSI-Divergenz | ja | 823 | 77.4% | +2.7 Punkte |
| Hammer-Kerze | ja | 2236 | 73.0% | -1.7 Punkte |
| RSI-Divergenz | nein | 7840 | 74.4% | -0.3 Punkte |
| Hammer-Kerze | nein | 6427 | 75.3% | +0.6 Punkte |
| Falltiefe vom 60-Tage-Hoch | unter 3 ATR | 2067 | 72.2% | -2.5 Punkte |
| Falltiefe vom 60-Tage-Hoch | 3 bis 6 ATR | 3470 | 73.8% | -0.9 Punkte |
| Falltiefe vom 60-Tage-Hoch | 6 bis 10 ATR | 2362 | 77.2% | +2.5 Punkte |
| Falltiefe vom 60-Tage-Hoch | ueber 10 ATR | 764 | **77.7%** | +3.1 Punkte |
| Volumen am Tief | unter Schnitt | 4115 | 72.2% | -2.5 Punkte |
| Volumen am Tief | 1,0 bis 1,5x | 2869 | 75.7% | +1.0 Punkte |
| Volumen am Tief | 1,5 bis 2,5x | 1279 | **78.0%** | +3.3 Punkte |
| Volumen am Tief | ueber 2,5x | 400 | **83.2%** | +8.6 Punkte |
| Lage zur EMA(200) | mehr als 2 ATR darunter | 3130 | 77.3% | +2.6 Punkte |
| Lage zur EMA(200) | bis 2 ATR darunter | 1312 | 76.7% | +2.0 Punkte |
| Lage zur EMA(200) | ueber der EMA(200) | 4221 | 72.2% | -2.5 Punkte |
| Anstieg bis zur Bestaetigung | unter 0,5 ATR | 674 | **54.0%** | -20.7 Punkte |
| Anstieg bis zur Bestaetigung | 0,5 bis 1 ATR | 1842 | **63.1%** | -11.6 Punkte |
| Anstieg bis zur Bestaetigung | 1 bis 2 ATR | 3786 | 75.5% | +0.8 Punkte |
| Anstieg bis zur Bestaetigung | ueber 2 ATR | 2361 | **88.3%** | +13.6 Punkte |

_Ein Merkmal mit wenigen Punkten Unterschied ist bei mehreren tausend Faellen noch kein Vorteil, sondern Rauschen. Erst zweistellige Unterschiede taugen als Auswahlkriterium._

_Vorsicht bei 'Anstieg bis zur Bestaetigung': ein Teil des Effekts ist reine Geometrie. Wer weiter oben einsteigt, hat mehr Abstand nach unten und unterschreitet das Tief seltener - dafuer sitzt der KO weiter weg und der Hebel ist kleiner. Der Vorteil ist also nicht geschenkt, sondern bezahlt._

_Der Erwartungswert ist eine Rechengroesse, keine Prognose: er unterstellt festen Ausstieg nach 5 Tagen ohne Verkaufssignal, ohne Gebuehren und ohne Auswahl nach RSI oder Analysten. Er taugt zum Vergleich der Varianten untereinander, nicht als erwartete Depotrendite._