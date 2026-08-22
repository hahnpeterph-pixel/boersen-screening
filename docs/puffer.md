# Puffer-Analyse - wie viel ATR braucht die KO-Schwelle?

_Erstellt 2026-08-22 18:34 UTC. Swing-Tief = tiefer als die 3 Tage davor und die 3 danach. Puffer immer in ATR(14) zum Zeitpunkt des Tiefs._

## Teil A - die eigenen Trades

_Bezugstief ist das juengste bestaetigte Swing-Tief vor dem Kauf. 'Unterschritten' misst, wie weit der Basiswert waehrend der Haltedauer darunter ging. 0,00 heisst: das Tief hat gehalten._

| Position | Basiswert | Kauf | Verkauf | Bezugstief | ATR | tiefster Kurs | unterschritten |
|---|---|---|---|---|---|---|---|
| Microsoft | MSFT | 2026-07-22 | 2026-08-10 | 372.65 | 11.74 | 376.68 | **0.00 ATR** |
| Oracle | ORCL | 2026-07-21 | 2026-08-10 | 137.07 | 8.3 | 114.5 | **2.72 ATR** |
| NVIDIA | NVDA | 2026-08-03 | 2026-08-21 | 197.97 | 7.47 | 196.85 | **0.15 ATR** |
| Rheinmetall | RHM.DE | 2026-08-11 | 2026-08-17 | 936.2 | 54.74 | 1128.0 | **0.00 ATR** |
| Gold | XAUUSD=X | 2026-08-14 | 2026-08-20 | - | - | - | keine Kursdaten |
| ASML | ASML | 2026-08-20 | 2026-08-21 | 1530.64 | 72.66 | 1741.0 | **0.00 ATR** |
| Applied Materials | AMAT | 2026-08-20 | 2026-08-21 | 435.86 | 34.91 | 483.13 | **0.00 ATR** |
| Take-Two | TTWO | 2026-08-20 | 2026-08-21 | 239.52 | 8.19 | 231.58 | **0.97 ATR** |
| Micron | MU | 2026-08-20 | 2026-08-21 | 737.88 | 71.07 | 929.07 | **0.00 ATR** |
| Gold II | XAUUSD=X | 2026-08-21 | 2026-08-21 | - | - | - | keine Kursdaten |

Von 8 Trades haben 5 das Bezugstief gehalten. Groesste Unterschreitung: 2.72 ATR.

## Teil B - alle Swing-Tiefs im Universum

_7 Jahre Kurshistorie. Gemessen wird die tiefste Unterschreitung innerhalb der naechsten 10 Handelstage - das entspricht ungefaehr der realen Haltedauer._

| Menge | Faelle | Tief haelt | Median | 75% | 90% | 95% | 99% |
|---|---|---|---|---|---|---|---|
| alle Tiefs | 27705 | 61% | 0.00 | 0.59 | 1.75 | 2.54 | 4.93 |
| nur tiefer als das vorherige Tief | 12468 | 62% | 0.00 | 0.56 | 1.74 | 2.63 | 5.21 |

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
| 10 Handelstage | 0.00 | 1.74 | 2.63 | 92% |
| 20 Handelstage | 0.13 | 3.20 | 4.51 | 80% |

_Ein Knock-out ist ein Totalverlust, kein Teilverlust. Ein Puffer, der 80% der Faelle abdeckt, heisst: jeder fuenfte Trade endet bei null._

## Teil C - welches Bezugstief lohnt sich?

_Fiktiver Trade je Swing-Tief: Einstieg am Bestaetigungstag, Ausstieg nach 5 Handelstagen, Knock-out zaehlt als -100%. Die Rendite ist die des Scheins, nicht des Basiswerts - sie ergibt sich aus dem Abstand zum KO. 'Abstand' ist der Weg vom Einstieg bis zur Schwelle in ATR und misst den Hebelverlust: je groesser, desto traeger der Schein._

| Bezugstief | Puffer | Faelle | Ausfallquote | Abstand Einstieg-KO | Rendite der Ueberlebenden | Erwartungswert |
|---|---|---|---|---|---|---|
| tiefstes 90 Tage | 3 ATR | 27582 | 1.6% | 9.34 ATR | +2.5% | **+0.9%** |
| tiefstes 60 Tage | 3 ATR | 27582 | 2.1% | 8.14 ATR | +3.0% | **+0.8%** |
| tiefstes 90 Tage | 2 ATR | 27582 | 3.1% | 8.34 ATR | +3.9% | **+0.7%** |
| tiefstes 60 Tage | 2 ATR | 27582 | 3.9% | 7.14 ATR | +4.7% | **+0.6%** |
| tiefstes 90 Tage | 1 ATR | 27582 | 5.9% | 7.34 ATR | +6.8% | **+0.5%** |
| tiefstes 60 Tage | 1 ATR | 27582 | 7.6% | 6.14 ATR | +8.5% | **+0.3%** |
| juengstes Tief | 3 ATR | 27582 | 6.0% | 4.59 ATR | +6.6% | **+0.2%** |
| juengstes Tief | 2 ATR | 27582 | 12.5% | 3.59 ATR | +12.7% | **-1.4%** |
| juengstes Tief | 1 ATR | 27582 | 24.4% | 2.59 ATR | +28.1% | **-3.1%** |

## Teil D - woran erkennt man ein Tief, das haelt?

_Ein Tief 'haelt', wenn es in den 10 Handelstagen nach der Bestaetigung um hoechstens 1.0 ATR unterschritten wird. Alle Merkmale sind am Einstiegstag bekannt - kein Blick in die Zukunft. 'Unterschied' zeigt die Abweichung von der Grundquote: nur wo er deutlich positiv ist, hilft das Merkmal bei der Auswahl._

| Merkmal | Auspraegung | Faelle | Haltequote | Unterschied |
|---|---|---|---|---|
| Alle Faelle | Grundquote | 24548 | 75.7% |  |
| Stellung in der Tiefpunktfolge | 1. Tief der Folge | 13299 | 74.6% | -1.2 Punkte |
| Stellung in der Tiefpunktfolge | 2. Tief | 6242 | 75.8% | +0.0 Punkte |
| Stellung in der Tiefpunktfolge | 3. Tief | 2861 | 77.5% | +1.7 Punkte |
| Stellung in der Tiefpunktfolge | 4. Tief oder spaeter | 2146 | **80.6%** | +4.8 Punkte |
| RSI am Tief | unter 30 | 1740 | **81.1%** | +5.4 Punkte |
| RSI am Tief | 30 bis 40 | 5823 | 77.3% | +1.6 Punkte |
| RSI am Tief | 40 bis 50 | 8252 | 75.1% | -0.7 Punkte |
| RSI am Tief | ueber 50 | 8733 | 74.2% | -1.5 Punkte |
| RSI-Divergenz | ja | 2257 | 78.7% | +3.0 Punkte |
| Hammer-Kerze | ja | 6578 | 74.6% | -1.2 Punkte |
| Hoeheres Tief als das vorherige | ja | 13288 | 74.6% | -1.2 Punkte |
| Index ueber seiner EMA(50) | ja | 17613 | 76.5% | +0.8 Punkte |
| RSI-Divergenz | nein | 22291 | 75.4% | -0.3 Punkte |
| Hammer-Kerze | nein | 17970 | 76.2% | +0.4 Punkte |
| Hoeheres Tief als das vorherige | nein | 11260 | 77.1% | +1.4 Punkte |
| Index ueber seiner EMA(50) | nein | 6935 | 73.7% | -2.1 Punkte |
| Tieferes Tief MIT RSI-Divergenz | beides | 2257 | 78.7% | +3.0 Punkte |
| Falltiefe vom 60-Tage-Hoch | unter 3 ATR | 6365 | 73.9% | -1.8 Punkte |
| Falltiefe vom 60-Tage-Hoch | 3 bis 6 ATR | 10126 | 75.2% | -0.6 Punkte |
| Falltiefe vom 60-Tage-Hoch | 6 bis 10 ATR | 6346 | 78.0% | +2.2 Punkte |
| Falltiefe vom 60-Tage-Hoch | ueber 10 ATR | 1711 | 77.7% | +2.0 Punkte |
| Volumen am Tief | unter Schnitt | 11700 | 73.9% | -1.8 Punkte |
| Volumen am Tief | 1,0 bis 1,5x | 8315 | 76.3% | +0.6 Punkte |
| Volumen am Tief | 1,5 bis 2,5x | 3497 | 78.5% | +2.8 Punkte |
| Volumen am Tief | ueber 2,5x | 1036 | **82.6%** | +6.9 Punkte |
| Lage zur EMA(200) | mehr als 2 ATR darunter | 7835 | 77.4% | +1.6 Punkte |
| Lage zur EMA(200) | bis 2 ATR darunter | 3719 | 77.3% | +1.6 Punkte |
| Lage zur EMA(200) | ueber der EMA(200) | 12994 | 74.3% | -1.4 Punkte |
| Anstieg bis zur Bestaetigung | unter 0,5 ATR | 1966 | **53.1%** | -22.7 Punkte |
| Anstieg bis zur Bestaetigung | 0,5 bis 1 ATR | 4985 | **64.3%** | -11.4 Punkte |
| Anstieg bis zur Bestaetigung | 1 bis 2 ATR | 10845 | 76.9% | +1.2 Punkte |
| Anstieg bis zur Bestaetigung | ueber 2 ATR | 6752 | **88.8%** | +13.1 Punkte |

_Ein Merkmal mit wenigen Punkten Unterschied ist bei mehreren tausend Faellen noch kein Vorteil, sondern Rauschen. Erst zweistellige Unterschiede taugen als Auswahlkriterium._

_Vorsicht bei 'Anstieg bis zur Bestaetigung': ein Teil des Effekts ist reine Geometrie. Wer weiter oben einsteigt, hat mehr Abstand nach unten und unterschreitet das Tief seltener - dafuer sitzt der KO weiter weg und der Hebel ist kleiner. Der Vorteil ist also nicht geschenkt, sondern bezahlt._

## Teil E - Filter kombiniert, mit Gegenrechnung

_'Haltequote' wie in Teil D. 'Einstieg' ist der Abstand des Kaufs zum Tief in ATR, 'Restpotenzial' der weitere Anstieg bis zum Hoch der Aufwaertsphase. Beide gehoeren zusammen gelesen: ein spaeter Einstieg hebt die Haltequote und senkt gleichzeitig, was noch zu holen ist._

| Filter | Faelle | Haltequote | Ausfall | Einstieg | Restpotenzial | Dauer | **Erwartungswert** |
|---|---|---|---|---|---|---|---|
| ohne Filter | 24548 | 75.7% | 11.9% | 1.44 ATR | 1.39 ATR | 5 Tage | **-1.49%** |
| RSI unter 30 | 1740 | 81.1% | 8.6% | 1.40 ATR | 1.62 ATR | 7 Tage | **+2.65%** |
| Volumen ab 2,5x | 1036 | 82.6% | 8.1% | 1.54 ATR | 1.55 ATR | 7 Tage | **+1.37%** |
| Anstieg ab 1 ATR | 17597 | 81.5% | 9.1% | 1.78 ATR | 1.41 ATR | 5 Tage | **-0.81%** |
| RSI + Volumen | 251 | 85.7% | 6.0% | 1.52 ATR | 1.82 ATR | 10 Tage | **+3.43%** |
| RSI + Anstieg | 1207 | 85.7% | 6.8% | 1.75 ATR | 1.62 ATR | 7 Tage | **+1.60%** |
| Volumen + Anstieg | 756 | 87.7% | 6.3% | 1.90 ATR | 1.50 ATR | 6 Tage | **+1.21%** |
| alle drei | 175 | 92.0% | 4.0% | 1.87 ATR | 1.79 ATR | 9 Tage | **+3.47%** |
| hoeheres Tief | 13288 | 74.6% | 12.6% | 1.44 ATR | 1.34 ATR | 5 Tage | **-2.12%** |
| hoeheres Tief + RSI unter 30 | 65 | 87.7% | 4.6% | 1.02 ATR | 1.57 ATR | 8 Tage | **+9.36%** |
| Markt ueber EMA(50) | 17613 | 76.5% | 11.1% | 1.47 ATR | 1.33 ATR | 5 Tage | **-1.70%** |
| Markt + RSI unter 30 | 842 | 81.1% | 9.0% | 1.34 ATR | 1.51 ATR | 7 Tage | **+0.35%** |

_Alle Werte sind Mediane. Restpotenzial in ATR laesst sich direkt gegen den KO-Abstand halten: liegt der KO 2 ATR unter dem Einstieg und das Restpotenzial bei 2 ATR, ist das Chance-Risiko-Verhaeltnis 1:1._

## Teil F - wie lange steigt es, wenn das Tief haelt?

_Die Aufwaertsphase endet, sobald der Kurs 1.5 ATR unter sein bisheriges Hoch faellt. Laengstens 60 Handelstage. Nur Faelle, in denen das Tief gehalten hat._

| Gruppe | Faelle | Dauer Median | Dauer 75% | Anstieg Median | Anstieg 75% | ueber 2 ATR |
|---|---|---|---|---|---|---|
| alle haltenden Tiefs | 18591 | **8 Tage** | 16 Tage | 2.01 ATR | 3.92 ATR | 50% |
| Einstieg unter 1 ATR ueber dem Tief | 4250 | **10 Tage** | 17 Tage | 2.42 ATR | 4.22 ATR | 59% |
| Einstieg 1 bis 2 ATR | 8342 | **8 Tage** | 16 Tage | 2.01 ATR | 3.92 ATR | 50% |
| Einstieg ueber 2 ATR | 5999 | **6 Tage** | 14 Tage | 1.68 ATR | 3.74 ATR | 44% |
| zusaetzlich RSI unter 30 | 1412 | **10 Tage** | 19 Tage | 2.10 ATR | 3.98 ATR | 52% |

_Die Dauer misst, wie lange der Kurs bis zu seinem Hoch brauchte - nicht, wie lange man haette halten sollen. Wer bis zum Hoch bleibt, erwischt es nur im Rueckblick._

## Teil G - Ausstiegsregel und Verteilung der Ergebnisse

_Dieselben Faelle, drei Ausstiegsregeln. Der KO wirkt durchgehend. 'Gewinner' ist der Anteil positiver Trades, 'bestes Zehntel' deren mittlere Rendite, 'Anteil am Gewinn' wie viel des gesamten Bruttogewinns aus diesem Zehntel stammt. Steht dort ein Wert nahe 100%, traegt eine kleine Minderheit alles - dann ist die Trefferquote nebensaechlich und es kommt allein darauf an, die Gewinner laufen zu lassen._

| Menge | Ausstieg | Faelle | Gewinner | Ausfall | Median | Mittel | bestes Zehntel | Anteil am Gewinn | Dauer |
|---|---|---|---|---|---|---|---|---|---|
| alle Tiefs | fest nach 5 Tagen | 24548 | 54% | 4.7% | +3.6% | **+3.0%** | +91% | 46% | 5 Tage |
| alle Tiefs | Momentum (Rueckfall 1,5 ATR) | 24548 | 40% | 3.5% | -16.2% | **+6.5%** | +192% | 61% | 10 Tage |
| alle Tiefs | RSI ab 70 | 24548 | 54% | 38.5% | +15.6% | **+14.8%** | +213% | 38% | 20 Tage |
| RSI unter 30 | fest nach 5 Tagen | 1740 | 56% | 3.2% | +5.6% | **+5.5%** | +88% | 43% | 5 Tage |
| RSI unter 30 | Momentum (Rueckfall 1,5 ATR) | 1740 | 44% | 2.8% | -8.6% | **+14.9%** | +209% | 57% | 13 Tage |
| RSI unter 30 | RSI ab 70 | 1740 | 52% | 37.6% | +16.1% | **+21.7%** | +231% | 37% | 37 Tage |
| Bodenbildung | fest nach 5 Tagen | 1741 | 55% | 4.1% | +3.8% | **+5.1%** | +93% | 46% | 5 Tage |
| Bodenbildung | Momentum (Rueckfall 1,5 ATR) | 1741 | 39% | 3.8% | -17.3% | **+4.0%** | +186% | 62% | 10 Tage |
| Bodenbildung | RSI ab 70 | 1741 | 52% | 41.8% | +15.6% | **+16.6%** | +224% | 37% | 23 Tage |
| Bodenbildung + RSI unter 30 | fest nach 5 Tagen | 34 | 68% | 2.9% | +8.9% | **+18.3%** | +109% | 35% | 5 Tage |
| Bodenbildung + RSI unter 30 | Momentum (Rueckfall 1,5 ATR) | 34 | 44% | 0.0% | -8.4% | **+20.3%** | +231% | 55% | 14 Tage |
| Bodenbildung + RSI unter 30 | RSI ab 70 | 34 | 47% | 41.2% | -24.0% | **+24.7%** | +228% | 28% | 35 Tage |

_Bodenbildung heisst hier: mindestens 4 ATR vom 60-Tage-Hoch gefallen, das neue Tief liegt hoechstens 1 ATR vom vorherigen entfernt (kein freier Fall mehr), und das Volumen der letzten fuenf Tage lag an Anstiegstagen hoeher als an Ruecksetzertagen._

_Der Erwartungswert ist eine Rechengroesse, keine Prognose: er unterstellt festen Ausstieg nach 5 Tagen ohne Verkaufssignal, ohne Gebuehren und ohne Auswahl nach RSI oder Analysten. Er taugt zum Vergleich der Varianten untereinander, nicht als erwartete Depotrendite._