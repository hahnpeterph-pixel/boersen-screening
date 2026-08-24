# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-08-24 17:37 UTC. 7 Jahre, 165 Werte, 88169 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 33758 | 54% | 55% | 56% | 59% | 1.82 | 5.21 |
| 0.5 ATR | 22903 | 55% | 55% | 56% | 60% | 1.82 | 5.13 |
| 0.75 ATR | 13852 | 54% | 55% | 56% | 59% | 1.89 | 5.38 |
| 1.0 ATR | 7946 | 54% | 55% | 56% | 60% | 1.92 | 5.57 |
| 1.25 ATR | 4253 | 54% | 56% | 57% | 62% | 1.88 | 5.83 |
| 1.5 ATR | 2312 | 51% | 53% | 54% | 60% | 2.09 | 6.01 |
| 1.75 ATR | 1244 | 52% | 55% | 57% | 64% | 1.89 | 6.13 |
| 2.0 ATR | 734 | 53% | 55% | 58% | 62% | 1.94 | 6.37 |
| 2.25 ATR | 385 | 53% | 56% | 58% | 61% | 1.91 | 6.13 |
| 2.5 ATR | 232 | 50% | 49% | 55% | 60% | 1.98 | 5.01 |
| 2.75 ATR | 150 | 59% | 63% | 60% | 54% | 1.42 | 5.08 |
| 3.0 ATR | 120 | 47% | 45% | 61% | 48% | 2.33 | 5.39 |
| 3.25 ATR | 63 | 48% | 44% | 46% | 57% | 2.09 | 5.32 |
| 3.5 ATR | 65 | 60% | 55% | 63% | 71% | 1.37 | 3.58 |
| 3.75 ATR | 51 | 47% | 45% | 53% | 53% | 1.79 | 3.76 |
| 4.0 ATR | 23 | 35% | 48% | 44% | 61% | 1.95 | 4.43 |
| 4.25 ATR | 24 | 38% | 58% | 46% | 58% | 1.51 | 3.91 |
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
| Montag | 54191 | 53.2% | 51.7% | 0.124% |
| Dienstag | 58663 | 49.3% | 48.6% | -0.034% |
| Mittwoch | 58099 | 49.9% | 49.9% | 0.022% |
| Donnerstag | 57192 | 50.6% | 50.1% | 0.020% |
| Freitag | 56730 | 51.1% | 49.9% | 0.028% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 19696 | 1.5 ATR | 61% | 82% | 118% | 181% | 270% | 62% | 2 |
| 2 ATR | 11650 | 2.4 ATR | 41% | 55% | 79% | 120% | 175% | 34% | 2 |
| 3 ATR | 5378 | 3.4 ATR | 31% | 41% | 59% | 89% | 134% | 20% | 2 |
| 4 ATR | 2526 | 4.4 ATR | 25% | 34% | 49% | 74% | 105% | 12% | 2 |
| 5 ATR | 1297 | 5.4 ATR | 21% | 30% | 44% | 62% | 89% | 7% | 2 |
| 6 ATR | 642 | 6.4 ATR | 19% | 26% | 38% | 59% | 79% | 5% | 2 |
| 7 ATR | 413 | 7.4 ATR | 17% | 24% | 36% | 52% | 72% | 3% | 2 |
| 8 ATR | 209 | 8.4 ATR | 18% | 24% | 31% | 47% | 62% | 2% | 2 |
| 9 ATR | 112 | 9.5 ATR | 15% | 20% | 28% | 41% | 59% | 1% | 2 |
| 10 ATR | 77 | 10.5 ATR | 14% | 17% | 25% | 42% | 72% | 3% | 2 |
| 11 ATR | 43 | 11.4 ATR | 17% | 22% | 32% | 44% | 69% | 0% | 2 |
| 12 ATR | 31 | 12.4 ATR | 14% | 20% | 31% | 44% | 48% | 0% | 2 |
| 13 ATR | 23 | 13.5 ATR | 19% | 25% | 34% | 48% | 63% | 0% | 3 |
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