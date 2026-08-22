# Historie - Halteraten und Einstieg

_Erstellt 2026-08-22 17:16 UTC. 3 Jahre, 170 Werte, 9604 auswertbare Tiefs aus abgeschlossenen Sequenzen (211 aus laufenden ausgeschlossen)._

_Tiefs nach der Umkehr-Regel aus `tiefs_regel.py`. Eine Abwaertsserie zaehlt nur neue Tiefststaende; sie endet erst, wenn ein hoeheres Tief kommt UND danach ein hoeheres Hoch ueber dem Hoch vor dem tiefsten Tief. HAELT heisst: ab dem Bestaetigungstag bis zum naechsten bestaetigten Swing-Hoch nicht mehr als der genannte Puffer unter das Tief gerutscht. Prozentzahlen sind Anteile der Faelle, in denen das Tief hielt. ANSTIEG ist der Median der erreichten Bewegung bis zum naechsten Hoch, in ATR - die Ertragsseite._

## Grundrate ueber alles

| Puffer | haelt |
|---|---|
| 0.5 ATR | 85% |
| 1.0 ATR | 90% |
| 1.5 ATR | 93% |
| 2.0 ATR | 95% |
| 2.5 ATR | 97% |
| 3.0 ATR | 98% |

_Mit den laufenden Sequenzen waeren es bei 1,0 ATR 90% statt 90% - laufende Sequenzen hatten noch keine Gelegenheit zu brechen und schoenen die Quote._

## Nach Position in der Serie

_Die Leitfrage: haelt das erste Tief seltener als ein spaeteres? y ist die werttypische Anzahl Tiefs je Sequenz dieses Wertes._

### Alle Werte

| Position | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 1 (erstes) | 4139 | 84% | 90% | 93% | 95% | 97% | 97% | 0.99 ATR |
| 2 bis y | 1983 | 85% | 90% | 94% | 96% | 97% | 98% | 1.04 ATR |
| y+1 | 1509 | 86% | 91% | 93% | 95% | 97% | 98% | 1.01 ATR |
| ueber y+1 | 1973 | 85% | 90% | 93% | 95% | 97% | 98% | 0.96 ATR |

_Nicht ausgewertet wird, ob es das LETZTE Tief der Serie war: eine Serie endet per Definition mit ihrem letzten Tief, also haelt dieses immer. Die Zahl waere 100 Prozent und sagte nichts - im Moment der Kaufentscheidung ist ohnehin nicht erkennbar, ob ein Tief das letzte sein wird._

## Nach Abstand beim Einstieg

_Wie weit hatte sich der Kurs am Bestaetigungstag schon vom Tief geloest? Die These: ein Tief, von dem der Kurs sich geloest hat, ist bestaetigt - ein frisches ist ein Kandidat._

### Abstand in ATR

| Abstand | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| bis 0,4 | 600 | 58% | 72% | 82% | 89% | 93% | 96% | 1.04 ATR |
| 0,4 bis 0,8 | 1995 | 77% | 85% | 90% | 93% | 96% | 97% | 1.01 ATR |
| 0,8 bis 1,2 | 2646 | 86% | 91% | 93% | 95% | 97% | 98% | 0.97 ATR |
| ueber 1,2 | 4363 | 92% | 94% | 96% | 97% | 98% | 98% | 1.00 ATR |

## Nach RSI, relativ zum eigenen Median

_Korrelation zwischen Position in der Serie und relativem RSI: -0.55. Ist sie hoch, sagt der RSI nichts, was die Position nicht schon sagt._

### RSI-Abstand zum eigenen Kauf-Median

| RSI-Lage | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 8+ unter Median | 2742 | 86% | 91% | 94% | 96% | 97% | 98% | 0.99 ATR |
| 3 bis 8 unter | 1279 | 86% | 91% | 93% | 96% | 97% | 98% | 0.98 ATR |
| um den Median | 1649 | 85% | 90% | 94% | 95% | 97% | 97% | 1.01 ATR |
| ueber Median | 3934 | 84% | 89% | 93% | 95% | 97% | 98% | 1.01 ATR |

## Nach einem Knock-out

_Haelt das naechste Tief desselben Wertes besser als der Durchschnitt? Nur das entscheidet, ob ein KO eine Gelegenheit eroeffnet._

- Puffer 1.0 ATR: 959 ausgeknockte Faelle, 950 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 90% gegen 90% im Durchschnitt, Anstieg 0.99 ATR.
- Puffer 2.0 ATR: 451 ausgeknockte Faelle, 446 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 96% gegen 95% im Durchschnitt, Anstieg 1.00 ATR.

_Der Verlust aus dem ersten Trade zaehlt voll, unabhaengig davon, ob ein zweiter folgt. Liegt die Folgequote nicht deutlich ueber der Grundrate, rechtfertigt ein moeglicher Wiedereinstieg keinen engeren Puffer._

---

_Keine Anlageberatung. Historische Kursverlaeufe, gemessen mit der Regel aus `tiefs_regel.py`._