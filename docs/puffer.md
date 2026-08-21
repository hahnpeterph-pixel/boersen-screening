# Puffer-Analyse - wie viel ATR braucht die KO-Schwelle?

_Erstellt 2026-08-21 22:37 UTC. Swing-Tief = tiefer als die 3 Tage davor und die 3 danach. Puffer immer in ATR(14) zum Zeitpunkt des Tiefs._

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
| alle Tiefs | 11964 | 61% | 0.00 | 0.61 | 1.79 | 2.66 | 5.06 |
| nur tiefer als das vorherige Tief | 5461 | 62% | 0.00 | 0.52 | 1.72 | 2.60 | 5.16 |

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
| 5 Handelstage | 0.00 | 0.39 | 0.82 | 99% |
| 10 Handelstage | 0.00 | 1.72 | 2.60 | 92% |
| 20 Handelstage | 0.18 | 3.29 | 4.50 | 80% |

_Ein Knock-out ist ein Totalverlust, kein Teilverlust. Ein Puffer, der 80% der Faelle abdeckt, heisst: jeder fuenfte Trade endet bei null._

## Teil C - welches Bezugstief lohnt sich?

_Fiktiver Trade je Swing-Tief: Einstieg am Bestaetigungstag, Ausstieg nach 5 Handelstagen, Knock-out zaehlt als -100%. Die Rendite ist die des Scheins, nicht des Basiswerts - sie ergibt sich aus dem Abstand zum KO. 'Abstand' ist der Weg vom Einstieg bis zur Schwelle in ATR und misst den Hebelverlust: je groesser, desto traeger der Schein._

| Bezugstief | Puffer | Faelle | Ausfallquote | Abstand Einstieg-KO | Rendite der Ueberlebenden | Erwartungswert |
|---|---|---|---|---|---|---|
| tiefstes 90 Tage | 3 ATR | 11841 | 1.9% | 9.12 ATR | +2.8% | **+0.8%** |
| tiefstes 60 Tage | 3 ATR | 11841 | 2.4% | 8.02 ATR | +3.2% | **+0.7%** |
| tiefstes 90 Tage | 2 ATR | 11841 | 3.9% | 8.12 ATR | +4.4% | **+0.3%** |
| tiefstes 60 Tage | 2 ATR | 11841 | 4.7% | 7.02 ATR | +5.1% | **+0.1%** |
| juengstes Tief | 3 ATR | 11841 | 6.7% | 4.60 ATR | +7.2% | **+0.0%** |
| tiefstes 90 Tage | 1 ATR | 11841 | 7.3% | 7.12 ATR | +7.6% | **-0.3%** |
| tiefstes 60 Tage | 1 ATR | 11841 | 8.8% | 6.02 ATR | +9.2% | **-0.5%** |
| juengstes Tief | 2 ATR | 11841 | 13.2% | 3.60 ATR | +13.4% | **-1.6%** |
| juengstes Tief | 1 ATR | 11841 | 25.3% | 2.60 ATR | +29.6% | **-3.2%** |

## Teil D - woran erkennt man ein Tief, das haelt?

_Ein Tief 'haelt', wenn es in den 10 Handelstagen nach der Bestaetigung um hoechstens 1.0 ATR unterschritten wird. Alle Merkmale sind am Einstiegstag bekannt - kein Blick in die Zukunft. 'Unterschied' zeigt die Abweichung von der Grundquote: nur wo er deutlich positiv ist, hilft das Merkmal bei der Auswahl._

| Merkmal | Auspraegung | Faelle | Haltequote | Unterschied |
|---|---|---|---|---|
| Alle Faelle | Grundquote | 8775 | 74.7% |  |
| Stellung in der Tiefpunktfolge | 1. Tief der Folge | 4658 | 73.2% | -1.5 Punkte |
| Stellung in der Tiefpunktfolge | 2. Tief | 2249 | 75.3% | +0.6 Punkte |
| Stellung in der Tiefpunktfolge | 3. Tief | 1048 | 77.3% | +2.6 Punkte |
| Stellung in der Tiefpunktfolge | 4. Tief oder spaeter | 820 | **78.2%** | +3.5 Punkte |
| RSI am Tief | unter 30 | 738 | **82.1%** | +7.4 Punkte |
| RSI am Tief | 30 bis 40 | 2115 | 77.1% | +2.4 Punkte |
| RSI am Tief | 40 bis 50 | 2933 | 73.5% | -1.2 Punkte |
| RSI am Tief | ueber 50 | 2989 | 72.3% | -2.4 Punkte |
| RSI-Divergenz | ja | 834 | 77.3% | +2.6 Punkte |
| Hammer-Kerze | ja | 2257 | 73.1% | -1.6 Punkte |
| Hoeheres Tief als das vorherige | ja | 4653 | 73.2% | -1.5 Punkte |
| Index ueber seiner EMA(50) | ja | 6653 | 75.0% | +0.3 Punkte |
| RSI-Divergenz | nein | 7941 | 74.4% | -0.3 Punkte |
| Hammer-Kerze | nein | 6518 | 75.3% | +0.6 Punkte |
| Hoeheres Tief als das vorherige | nein | 4122 | 76.4% | +1.7 Punkte |
| Index ueber seiner EMA(50) | nein | 2122 | 73.9% | -0.8 Punkte |
| Tieferes Tief MIT RSI-Divergenz | beides | 834 | 77.3% | +2.6 Punkte |
| Falltiefe vom 60-Tage-Hoch | unter 3 ATR | 2110 | 72.1% | -2.6 Punkte |
| Falltiefe vom 60-Tage-Hoch | 3 bis 6 ATR | 3530 | 73.9% | -0.8 Punkte |
| Falltiefe vom 60-Tage-Hoch | 6 bis 10 ATR | 2370 | 77.3% | +2.6 Punkte |
| Falltiefe vom 60-Tage-Hoch | ueber 10 ATR | 765 | **77.8%** | +3.1 Punkte |
| Volumen am Tief | unter Schnitt | 4167 | 72.1% | -2.6 Punkte |
| Volumen am Tief | 1,0 bis 1,5x | 2919 | 75.8% | +1.1 Punkte |
| Volumen am Tief | 1,5 bis 2,5x | 1288 | **78.0%** | +3.3 Punkte |
| Volumen am Tief | ueber 2,5x | 401 | **83.3%** | +8.6 Punkte |
| Lage zur EMA(200) | mehr als 2 ATR darunter | 3137 | 77.3% | +2.6 Punkte |
| Lage zur EMA(200) | bis 2 ATR darunter | 1321 | 76.7% | +2.0 Punkte |
| Lage zur EMA(200) | ueber der EMA(200) | 4317 | 72.2% | -2.5 Punkte |
| Anstieg bis zur Bestaetigung | unter 0,5 ATR | 680 | **53.7%** | -21.0 Punkte |
| Anstieg bis zur Bestaetigung | 0,5 bis 1 ATR | 1849 | **63.0%** | -11.7 Punkte |
| Anstieg bis zur Bestaetigung | 1 bis 2 ATR | 3839 | 75.5% | +0.8 Punkte |
| Anstieg bis zur Bestaetigung | ueber 2 ATR | 2407 | **88.4%** | +13.7 Punkte |

_Ein Merkmal mit wenigen Punkten Unterschied ist bei mehreren tausend Faellen noch kein Vorteil, sondern Rauschen. Erst zweistellige Unterschiede taugen als Auswahlkriterium._

_Vorsicht bei 'Anstieg bis zur Bestaetigung': ein Teil des Effekts ist reine Geometrie. Wer weiter oben einsteigt, hat mehr Abstand nach unten und unterschreitet das Tief seltener - dafuer sitzt der KO weiter weg und der Hebel ist kleiner. Der Vorteil ist also nicht geschenkt, sondern bezahlt._

## Teil E - Filter kombiniert, mit Gegenrechnung

_'Haltequote' wie in Teil D. 'Einstieg' ist der Abstand des Kaufs zum Tief in ATR, 'Restpotenzial' der weitere Anstieg bis zum Hoch der Aufwaertsphase. Beide gehoeren zusammen gelesen: ein spaeter Einstieg hebt die Haltequote und senkt gleichzeitig, was noch zu holen ist._

| Filter | Faelle | Haltequote | Ausfall | Einstieg | Restpotenzial | Dauer | **Erwartungswert** |
|---|---|---|---|---|---|---|---|
| ohne Filter | 8775 | 74.7% | 12.7% | 1.43 ATR | 1.36 ATR | 5 Tage | **-2.04%** |
| RSI unter 30 | 738 | 82.1% | 9.1% | 1.33 ATR | 1.64 ATR | 8 Tage | **+3.26%** |
| Volumen ab 2,5x | 401 | 83.3% | 9.2% | 1.54 ATR | 1.57 ATR | 7 Tage | **-0.50%** |
| Anstieg ab 1 ATR | 6246 | 80.5% | 9.8% | 1.77 ATR | 1.42 ATR | 5 Tage | **-0.99%** |
| RSI + Volumen | 122 | 83.6% | 7.4% | 1.44 ATR | 1.93 ATR | 10 Tage | **-1.26%** |
| RSI + Anstieg | 502 | 87.1% | 8.0% | 1.70 ATR | 1.75 ATR | 9 Tage | **+2.11%** |
| Volumen + Anstieg | 300 | 86.3% | 8.3% | 1.88 ATR | 1.46 ATR | 6 Tage | **-1.84%** |
| alle drei | 86 | 88.4% | 7.0% | 1.81 ATR | 1.96 ATR | 10 Tage | **-1.51%** |
| hoeheres Tief | 4653 | 73.2% | 13.2% | 1.44 ATR | 1.30 ATR | 5 Tage | **-2.40%** |
| hoeheres Tief + RSI unter 30 | 33 | 97.0% | 3.0% | 0.96 ATR | 1.62 ATR | 8 Tage | **+16.96%** |
| Markt ueber EMA(50) | 6653 | 75.0% | 12.2% | 1.44 ATR | 1.33 ATR | 5 Tage | **-1.46%** |
| Markt + RSI unter 30 | 405 | 77.3% | 12.1% | 1.26 ATR | 1.44 ATR | 6 Tage | **-0.50%** |

_Alle Werte sind Mediane. Restpotenzial in ATR laesst sich direkt gegen den KO-Abstand halten: liegt der KO 2 ATR unter dem Einstieg und das Restpotenzial bei 2 ATR, ist das Chance-Risiko-Verhaeltnis 1:1._

## Teil F - wie lange steigt es, wenn das Tief haelt?

_Die Aufwaertsphase endet, sobald der Kurs 1.5 ATR unter sein bisheriges Hoch faellt. Laengstens 60 Handelstage. Nur Faelle, in denen das Tief gehalten hat._

| Gruppe | Faelle | Dauer Median | Dauer 75% | Anstieg Median | Anstieg 75% | ueber 2 ATR |
|---|---|---|---|---|---|---|
| alle haltenden Tiefs | 6555 | **8 Tage** | 15 Tage | 2.02 ATR | 3.91 ATR | 50% |
| Einstieg unter 1 ATR ueber dem Tief | 1530 | **9 Tage** | 16 Tage | 2.32 ATR | 4.08 ATR | 57% |
| Einstieg 1 bis 2 ATR | 2898 | **8 Tage** | 15 Tage | 2.07 ATR | 3.95 ATR | 51% |
| Einstieg ueber 2 ATR | 2127 | **6 Tage** | 13 Tage | 1.66 ATR | 3.74 ATR | 44% |
| zusaetzlich RSI unter 30 | 606 | **11 Tage** | 19 Tage | 2.06 ATR | 3.94 ATR | 51% |

_Die Dauer misst, wie lange der Kurs bis zu seinem Hoch brauchte - nicht, wie lange man haette halten sollen. Wer bis zum Hoch bleibt, erwischt es nur im Rueckblick._

## Teil G - Ausstiegsregel und Verteilung der Ergebnisse

_Dieselben Faelle, drei Ausstiegsregeln. Der KO wirkt durchgehend. 'Gewinner' ist der Anteil positiver Trades, 'bestes Zehntel' deren mittlere Rendite, 'Anteil am Gewinn' wie viel des gesamten Bruttogewinns aus diesem Zehntel stammt. Steht dort ein Wert nahe 100%, traegt eine kleine Minderheit alles - dann ist die Trefferquote nebensaechlich und es kommt allein darauf an, die Gewinner laufen zu lassen._

| Menge | Ausstieg | Faelle | Gewinner | Ausfall | Median | Mittel | bestes Zehntel | Anteil am Gewinn | Dauer |
|---|---|---|---|---|---|---|---|---|---|
| alle Tiefs | fest nach 5 Tagen | 8775 | 53% | 5.2% | +3.5% | **+2.9%** | +94% | 47% | 5 Tage |
| alle Tiefs | Momentum (Rueckfall 1,5 ATR) | 8775 | 39% | 4.6% | -17.6% | **+4.4%** | +189% | 62% | 10 Tage |
| alle Tiefs | RSI ab 70 | 8775 | 54% | 38.8% | +15.0% | **+15.4%** | +218% | 39% | 19 Tage |
| RSI unter 30 | fest nach 5 Tagen | 738 | 58% | 3.7% | +7.5% | **+6.5%** | +80% | 40% | 5 Tage |
| RSI unter 30 | Momentum (Rueckfall 1,5 ATR) | 738 | 44% | 4.2% | -8.8% | **+12.7%** | +199% | 56% | 14 Tage |
| RSI unter 30 | RSI ab 70 | 738 | 51% | 39.6% | +5.9% | **+18.6%** | +227% | 36% | 34 Tage |
| Bodenbildung | fest nach 5 Tagen | 660 | 56% | 4.2% | +5.4% | **+6.3%** | +102% | 46% | 5 Tage |
| Bodenbildung | Momentum (Rueckfall 1,5 ATR) | 660 | 37% | 4.7% | -20.5% | **+1.9%** | +195% | 65% | 9 Tage |
| Bodenbildung | RSI ab 70 | 660 | 52% | 43.6% | +24.8% | **+21.0%** | +242% | 37% | 20 Tage |
| Bodenbildung + RSI unter 30 | - | 19 | zu wenige Faelle | | | | | | |

_Bodenbildung heisst hier: mindestens 4 ATR vom 60-Tage-Hoch gefallen, das neue Tief liegt hoechstens 1 ATR vom vorherigen entfernt (kein freier Fall mehr), und das Volumen der letzten fuenf Tage lag an Anstiegstagen hoeher als an Ruecksetzertagen._

_Der Erwartungswert ist eine Rechengroesse, keine Prognose: er unterstellt festen Ausstieg nach 5 Tagen ohne Verkaufssignal, ohne Gebuehren und ohne Auswahl nach RSI oder Analysten. Er taugt zum Vergleich der Varianten untereinander, nicht als erwartete Depotrendite._