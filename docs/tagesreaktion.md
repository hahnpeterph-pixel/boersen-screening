# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-08-24 18:16 UTC. 7 Jahre, 165 Werte, 88144 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 33775 | 54% | 55% | 56% | 59% | 1.82 | 5.21 |
| 0.5 ATR | 22902 | 55% | 55% | 56% | 60% | 1.82 | 5.13 |
| 0.75 ATR | 13859 | 54% | 55% | 56% | 59% | 1.89 | 5.39 |
| 1.0 ATR | 7916 | 54% | 55% | 56% | 59% | 1.92 | 5.58 |
| 1.25 ATR | 4253 | 54% | 56% | 57% | 62% | 1.88 | 5.83 |
| 1.5 ATR | 2301 | 51% | 53% | 54% | 60% | 2.09 | 5.98 |
| 1.75 ATR | 1245 | 52% | 55% | 57% | 64% | 1.89 | 6.14 |
| 2.0 ATR | 729 | 53% | 55% | 58% | 62% | 1.94 | 6.33 |
| 2.25 ATR | 383 | 52% | 56% | 59% | 61% | 1.91 | 6.17 |
| 2.5 ATR | 231 | 50% | 49% | 54% | 60% | 1.98 | 5.01 |
| 2.75 ATR | 150 | 59% | 63% | 60% | 54% | 1.42 | 5.08 |
| 3.0 ATR | 119 | 47% | 45% | 60% | 48% | 2.32 | 5.41 |
| 3.25 ATR | 63 | 48% | 44% | 46% | 57% | 2.09 | 5.32 |
| 3.5 ATR | 66 | 59% | 54% | 62% | 70% | 1.44 | 3.79 |
| 3.75 ATR | 51 | 47% | 45% | 55% | 55% | 1.78 | 3.70 |
| 4.0 ATR | 24 | 33% | 46% | 42% | 62% | 1.98 | 4.39 |
| 4.25 ATR | 23 | 39% | 61% | 48% | 61% | 1.46 | 3.97 |
| 4.5 ATR | 18 | 50% | 44% | 44% | 56% | 1.86 | 4.28 |
| 4.75 ATR | 10 | 30% | 30% | 50% | 40% | 2.37 | 4.42 |
| 5.0 ATR | 4 | 50% | 25% | 75% | 100% | 1.39 | 6.67 |
| 5.25 ATR | 7 | 29% | 29% | 57% | 57% | 1.64 | 4.71 |
| 5.5 ATR | 2 | 50% | 100% | 100% | 100% | 0.62 | 0.96 |
| 5.75 ATR | 4 | 50% | 50% | 50% | 50% | 1.24 | 3.58 |
| 6.0 ATR | 9 | 56% | 78% | 78% | 78% | 0.75 | 1.48 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 54216 | 53.1% | 51.7% | 0.124% |
| Dienstag | 58663 | 49.3% | 48.7% | -0.035% |
| Mittwoch | 58099 | 49.9% | 49.9% | 0.022% |
| Donnerstag | 57199 | 50.7% | 50.0% | 0.020% |
| Freitag | 56732 | 51.1% | 49.9% | 0.028% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 19679 | 1.5 ATR | 61% | 83% | 118% | 181% | 270% | 62% | 2 |
| 2 ATR | 11649 | 2.4 ATR | 41% | 55% | 79% | 120% | 175% | 34% | 2 |
| 3 ATR | 5381 | 3.4 ATR | 31% | 41% | 59% | 89% | 134% | 20% | 2 |
| 4 ATR | 2519 | 4.4 ATR | 25% | 34% | 49% | 74% | 105% | 12% | 2 |
| 5 ATR | 1299 | 5.4 ATR | 21% | 30% | 44% | 61% | 88% | 7% | 2 |
| 6 ATR | 647 | 6.4 ATR | 19% | 26% | 38% | 59% | 78% | 5% | 2 |
| 7 ATR | 411 | 7.4 ATR | 18% | 24% | 36% | 52% | 72% | 3% | 2 |
| 8 ATR | 211 | 8.4 ATR | 17% | 24% | 31% | 47% | 62% | 2% | 2 |
| 9 ATR | 113 | 9.4 ATR | 15% | 20% | 28% | 45% | 59% | 1% | 2 |
| 10 ATR | 76 | 10.5 ATR | 14% | 17% | 26% | 43% | 72% | 3% | 2 |
| 11 ATR | 43 | 11.4 ATR | 17% | 22% | 32% | 44% | 69% | 0% | 2 |
| 12 ATR | 31 | 12.4 ATR | 14% | 20% | 31% | 44% | 48% | 0% | 2 |
| 13 ATR | 23 | 13.5 ATR | 20% | 27% | 34% | 48% | 63% | 0% | 3 |
| 14 ATR | 13 | 14.4 ATR | 16% | 21% | 30% | 37% | 56% | 8% | 3 |
| 15 ATR | 6 | 15.6 ATR | 16% | 21% | 24% | 40% | 81% | 17% | 2 |
| 16 ATR | 11 | 16.6 ATR | 19% | 21% | 30% | 39% | 48% | 0% | 2 |
| 17 ATR | 3 | 17.5 ATR | 12% | 12% | 14% | 28% | 37% | 0% | 2 |
| 18 ATR | 3 | 18.7 ATR | 57% | 59% | 62% | 64% | 65% | 0% | 4 |
| 19 ATR | 2 | 19.6 ATR | 45% | 48% | 52% | 56% | 59% | 0% | 2 |
| 20 ATR | 1 | 20.4 ATR | 55% | 55% | 55% | 55% | 55% | 0% | 6 |
| 21 ATR | 1 | 21.2 ATR | 24% | 24% | 24% | 24% | 24% | 0% | 2 |
| 23 ATR | 2 | 23.4 ATR | 12% | 13% | 14% | 16% | 17% | 0% | 2 |
| 26 ATR | 1 | 26.7 ATR | 16% | 16% | 16% | 16% | 16% | 0% | 1 |
| 27 ATR | 1 | 27.2 ATR | 40% | 40% | 40% | 40% | 40% | 0% | 5 |
| 28 ATR | 1 | 28.5 ATR | 51% | 51% | 51% | 51% | 51% | 0% | 5 |
| 29 ATR | 1 | 29.2 ATR | 90% | 90% | 90% | 90% | 90% | 0% | 75 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._