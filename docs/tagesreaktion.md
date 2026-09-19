# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-09-19 07:07 UTC. 7 Jahre, 223 Werte, 120084 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 45591 | 55% | 56% | 56% | 60% | 1.80 | 5.19 |
| 0.5 ATR | 31248 | 55% | 56% | 56% | 60% | 1.81 | 5.17 |
| 0.75 ATR | 18939 | 54% | 55% | 56% | 59% | 1.89 | 5.40 |
| 1.0 ATR | 10823 | 54% | 56% | 56% | 60% | 1.89 | 5.59 |
| 1.25 ATR | 5867 | 54% | 56% | 56% | 61% | 1.89 | 5.92 |
| 1.5 ATR | 3186 | 51% | 53% | 54% | 60% | 2.10 | 6.10 |
| 1.75 ATR | 1707 | 52% | 55% | 56% | 63% | 1.91 | 6.34 |
| 2.0 ATR | 1041 | 54% | 55% | 58% | 61% | 1.96 | 6.32 |
| 2.25 ATR | 573 | 52% | 54% | 58% | 60% | 1.98 | 6.29 |
| 2.5 ATR | 329 | 51% | 50% | 54% | 61% | 2.03 | 5.30 |
| 2.75 ATR | 220 | 59% | 61% | 58% | 55% | 1.51 | 6.11 |
| 3.0 ATR | 165 | 47% | 47% | 58% | 54% | 2.30 | 5.47 |
| 3.25 ATR | 107 | 47% | 46% | 45% | 57% | 2.42 | 5.65 |
| 3.5 ATR | 90 | 59% | 53% | 61% | 68% | 1.56 | 4.70 |
| 3.75 ATR | 61 | 44% | 48% | 52% | 54% | 1.79 | 3.92 |
| 4.0 ATR | 33 | 36% | 42% | 36% | 58% | 2.40 | 5.77 |
| 4.25 ATR | 36 | 44% | 58% | 56% | 64% | 1.50 | 3.56 |
| 4.5 ATR | 20 | 50% | 45% | 45% | 55% | 1.86 | 4.25 |
| 4.75 ATR | 15 | 40% | 40% | 60% | 60% | 2.05 | 4.25 |
| 5.0 ATR | 5 | 40% | 20% | 60% | 80% | 1.55 | 6.61 |
| 5.25 ATR | 10 | 30% | 40% | 60% | 60% | 1.43 | 3.58 |
| 5.5 ATR | 3 | 67% | 100% | 100% | 100% | 1.04 | 1.53 |
| 5.75 ATR | 4 | 50% | 50% | 50% | 50% | 1.24 | 3.58 |
| 6.0 ATR | 11 | 64% | 82% | 82% | 73% | 0.75 | 1.43 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 72999 | 52.4% | 51.2% | 0.105% |
| Dienstag | 79589 | 48.8% | 48.4% | -0.041% |
| Mittwoch | 78836 | 49.2% | 49.7% | 0.014% |
| Donnerstag | 77689 | 50.3% | 49.5% | 0.023% |
| Freitag | 77103 | 50.9% | 49.6% | 0.030% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 26529 | 1.5 ATR | 61% | 82% | 118% | 180% | 270% | 62% | 2 |
| 2 ATR | 15795 | 2.4 ATR | 40% | 55% | 79% | 120% | 176% | 34% | 2 |
| 3 ATR | 7386 | 3.4 ATR | 31% | 41% | 59% | 89% | 133% | 20% | 2 |
| 4 ATR | 3416 | 4.4 ATR | 25% | 34% | 49% | 73% | 105% | 12% | 2 |
| 5 ATR | 1727 | 5.4 ATR | 21% | 30% | 43% | 62% | 89% | 7% | 2 |
| 6 ATR | 905 | 6.4 ATR | 20% | 26% | 38% | 58% | 81% | 6% | 2 |
| 7 ATR | 540 | 7.4 ATR | 17% | 24% | 35% | 51% | 72% | 3% | 2 |
| 8 ATR | 293 | 8.4 ATR | 18% | 23% | 32% | 48% | 64% | 3% | 2 |
| 9 ATR | 183 | 9.5 ATR | 15% | 21% | 30% | 43% | 60% | 0% | 2 |
| 10 ATR | 100 | 10.5 ATR | 14% | 17% | 27% | 42% | 70% | 3% | 2 |
| 11 ATR | 63 | 11.4 ATR | 18% | 23% | 34% | 47% | 69% | 0% | 3 |
| 12 ATR | 45 | 12.4 ATR | 10% | 19% | 30% | 37% | 50% | 0% | 2 |
| 13 ATR | 26 | 13.5 ATR | 19% | 27% | 34% | 48% | 63% | 0% | 3 |
| 14 ATR | 18 | 14.4 ATR | 14% | 18% | 26% | 37% | 53% | 6% | 2 |
| 15 ATR | 10 | 15.5 ATR | 18% | 21% | 27% | 43% | 52% | 10% | 2 |
| 16 ATR | 12 | 16.5 ATR | 19% | 22% | 29% | 35% | 48% | 0% | 2 |
| 17 ATR | 6 | 17.4 ATR | 12% | 15% | 28% | 42% | 69% | 0% | 2 |
| 18 ATR | 4 | 18.7 ATR | 41% | 50% | 59% | 63% | 65% | 0% | 3 |
| 19 ATR | 2 | 19.6 ATR | 45% | 48% | 52% | 56% | 59% | 0% | 2 |
| 20 ATR | 2 | 20.3 ATR | 37% | 40% | 45% | 50% | 53% | 0% | 4 |
| 21 ATR | 1 | 21.2 ATR | 24% | 24% | 24% | 24% | 24% | 0% | 2 |
| 23 ATR | 3 | 23.4 ATR | 13% | 14% | 17% | 17% | 18% | 0% | 1 |
| 24 ATR | 2 | 24.5 ATR | 13% | 24% | 41% | 59% | 69% | 0% | 1 |
| 25 ATR | 1 | 25.1 ATR | 60% | 60% | 60% | 60% | 60% | 0% | 4 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 1 | 28.5 ATR | 51% | 51% | 51% | 51% | 51% | 0% | 5 |
| 29 ATR | 2 | 29.1 ATR | 25% | 36% | 54% | 72% | 83% | 0% | 38 |
| 30 ATR | 1 | 31.1 ATR | 13% | 13% | 13% | 13% | 13% | 0% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._