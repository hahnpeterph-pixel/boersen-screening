# Historie - Halteraten und Einstieg

_Erstellt 2026-08-22 17:53 UTC. 3 Jahre, 170 Werte, 8963 auswertbare Tiefs aus abgeschlossenen Sequenzen (12 aus laufenden ausgeschlossen)._

_Tiefs nach der Umkehr-Regel aus `tiefs_regel.py`. Eine Abwaertsserie zaehlt nur neue Tiefststaende; sie endet erst, wenn ein hoeheres Tief kommt UND danach ein hoeheres Hoch ueber dem Hoch vor dem tiefsten Tief. HAELT heisst: der Puffer wurde ab dem Bestaetigungstag drei Monate lang nicht unterschritten. ANSTIEG ist der Median des hoechsten Punktes nach dem Einstieg, in ATR - die Ertragsseite._

## Grundrate ueber alles

| Puffer | haelt 3 Monate | nie wieder durchbrochen | Median Tage bis Bruch |
|---|---|---|---|
| 0.5 ATR | 30% | 16% | 11 |
| 1.0 ATR | 36% | 20% | 16 |
| 1.5 ATR | 43% | 24% | 22 |
| 2.0 ATR | 49% | 28% | 29 |
| 2.5 ATR | 55% | 31% | 36 |
| 3.0 ATR | 60% | 35% | 44 |

_Gemessen ab dem Bestaetigungstag bis zum Ende der Historie, ohne festes Fenster - der KO kann schlagen, solange die Position offen ist. HAELT 3 MONATE heisst: der Puffer wurde in den ersten 63 Handelstagen nie unterschritten. NIE WIEDER DURCHBROCHEN heisst: auch danach nicht. MEDIAN TAGE BIS BRUCH zaehlt nur die Faelle, die gebrochen wurden. Tiefs mit weniger als 63 Handelstagen Resthistorie sind ausgeschlossen, sonst wuerden sie als 'haelt' gezaehlt, ohne die Gelegenheit gehabt zu haben. Alle folgenden Tabellen nennen den Anteil, der drei Monate haelt._

## Nach Position in der Serie

_Die Leitfrage: haelt das erste Tief seltener als ein spaeteres? y ist die werttypische Anzahl Tiefs je Sequenz dieses Wertes._

### Absolut - das wievielte Tief der Serie

| Position | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| Tief 1 | 3843 | 28% | 34% | 41% | 47% | 54% | 58% | 16.83 ATR |
| Tief 2 | 2175 | 31% | 37% | 43% | 49% | 56% | 61% | 16.03 ATR |
| Tief 3 | 1269 | 31% | 37% | 44% | 51% | 56% | 62% | 15.75 ATR |
| Tief 4 | 734 | 31% | 38% | 43% | 50% | 55% | 61% | 14.46 ATR |
| Tief 5 | 410 | 32% | 39% | 45% | 52% | 57% | 61% | 13.10 ATR |
| Tief 6+ | 532 | 34% | 42% | 47% | 53% | 58% | 63% | 12.96 ATR |

_Darunter dieselbe Frage relativ zur werttypischen Anzahl y dieses Wertes._

### Relativ zur werttypischen Anzahl

| Position | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 1 (erstes) | 3843 | 28% | 34% | 41% | 47% | 54% | 58% | 16.83 ATR |
| 2 bis y | 1824 | 29% | 35% | 41% | 47% | 53% | 58% | 14.72 ATR |
| y+1 | 1416 | 30% | 37% | 45% | 52% | 57% | 63% | 16.61 ATR |
| ueber y+1 | 1880 | 34% | 41% | 47% | 53% | 58% | 63% | 14.70 ATR |

_Nicht ausgewertet wird, ob es das LETZTE Tief der Serie war: eine Serie endet per Definition mit ihrem letzten Tief, also haelt dieses immer. Die Zahl waere 100 Prozent und sagte nichts - im Moment der Kaufentscheidung ist ohnehin nicht erkennbar, ob ein Tief das letzte sein wird._

## Nach Abstand beim Einstieg

_Wie weit hatte sich der Kurs am Bestaetigungstag schon vom Tief geloest? Die These: ein Tief, von dem der Kurs sich geloest hat, ist bestaetigt - ein frisches ist ein Kandidat._

### Abstand in ATR

| Abstand | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| bis 0,4 | 560 | 14% | 21% | 29% | 34% | 41% | 48% | 14.12 ATR |
| 0,4 bis 0,8 | 1850 | 21% | 28% | 36% | 43% | 50% | 55% | 15.24 ATR |
| 0,8 bis 1,2 | 2469 | 27% | 33% | 40% | 48% | 54% | 59% | 16.40 ATR |
| ueber 1,2 | 4084 | 37% | 43% | 50% | 55% | 60% | 65% | 15.95 ATR |

## Nach RSI, relativ zum eigenen Median

_Korrelation zwischen Position in der Serie und relativem RSI: -0.55. Ist sie hoch, sagt der RSI nichts, was die Position nicht schon sagt._

### RSI-Abstand zum eigenen Kauf-Median

| RSI-Lage | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 8+ unter Median | 2588 | 36% | 43% | 50% | 56% | 61% | 67% | 15.87 ATR |
| 3 bis 8 unter | 1195 | 29% | 37% | 44% | 50% | 57% | 62% | 15.72 ATR |
| um den Median | 1520 | 27% | 33% | 41% | 46% | 52% | 57% | 15.04 ATR |
| ueber Median | 3660 | 26% | 32% | 39% | 45% | 51% | 56% | 16.23 ATR |

## Nach einem Knock-out

_Haelt das naechste Tief desselben Wertes besser als der Durchschnitt? Nur das entscheidet, ob ein KO eine Gelegenheit eroeffnet._

- Puffer 1.0 ATR: 5639 ausgeknockte Faelle, 5255 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 23% gegen 36% im Durchschnitt, Anstieg 13.11 ATR.
- Puffer 2.0 ATR: 4506 ausgeknockte Faelle, 4210 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 25% gegen 49% im Durchschnitt, Anstieg 11.76 ATR.

_Der Verlust aus dem ersten Trade zaehlt voll, unabhaengig davon, ob ein zweiter folgt. Liegt die Folgequote nicht deutlich ueber der Grundrate, rechtfertigt ein moeglicher Wiedereinstieg keinen engeren Puffer._

---

_Keine Anlageberatung. Historische Kursverlaeufe, gemessen mit der Regel aus `tiefs_regel.py`._