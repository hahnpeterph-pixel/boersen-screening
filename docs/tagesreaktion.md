# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-10-03 07:09 UTC. 20 Jahre, 283 Werte, 412330 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 155965 | 55% | 56% | 58% | 62% | 1.77 | 5.26 |
| 0.5 ATR | 106959 | 55% | 56% | 58% | 61% | 1.79 | 5.26 |
| 0.75 ATR | 66294 | 55% | 56% | 58% | 62% | 1.82 | 5.42 |
| 1.0 ATR | 37847 | 55% | 56% | 57% | 62% | 1.87 | 5.61 |
| 1.25 ATR | 20482 | 55% | 56% | 57% | 62% | 1.91 | 5.74 |
| 1.5 ATR | 10975 | 54% | 56% | 57% | 62% | 1.96 | 5.88 |
| 1.75 ATR | 5699 | 53% | 55% | 58% | 62% | 1.97 | 6.02 |
| 2.0 ATR | 3165 | 54% | 55% | 58% | 63% | 1.98 | 5.94 |
| 2.25 ATR | 1754 | 52% | 53% | 57% | 62% | 2.00 | 5.94 |
| 2.5 ATR | 1038 | 51% | 53% | 56% | 61% | 2.01 | 5.44 |
| 2.75 ATR | 668 | 52% | 53% | 55% | 58% | 1.92 | 5.15 |
| 3.0 ATR | 452 | 50% | 49% | 56% | 59% | 2.03 | 5.34 |
| 3.25 ATR | 284 | 45% | 44% | 54% | 64% | 2.22 | 5.29 |
| 3.5 ATR | 204 | 50% | 51% | 55% | 63% | 1.89 | 4.87 |
| 3.75 ATR | 159 | 48% | 51% | 58% | 57% | 1.79 | 5.10 |
| 4.0 ATR | 108 | 42% | 49% | 51% | 61% | 2.08 | 5.03 |
| 4.25 ATR | 86 | 45% | 52% | 49% | 57% | 1.89 | 5.29 |
| 4.5 ATR | 59 | 44% | 42% | 46% | 58% | 1.77 | 4.38 |
| 4.75 ATR | 33 | 46% | 52% | 61% | 58% | 1.23 | 4.38 |
| 5.0 ATR | 20 | 35% | 30% | 55% | 55% | 1.64 | 5.32 |
| 5.25 ATR | 24 | 50% | 46% | 62% | 58% | 1.44 | 3.86 |
| 5.5 ATR | 13 | 46% | 54% | 62% | 92% | 1.48 | 5.28 |
| 5.75 ATR | 12 | 67% | 67% | 58% | 42% | 1.04 | 3.89 |
| 6.0 ATR | 30 | 60% | 63% | 60% | 67% | 0.75 | 3.97 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 243220 | 50.7% | 50.1% | 0.025% |
| Dienstag | 264300 | 50.2% | 49.6% | 0.032% |
| Mittwoch | 264049 | 50.0% | 49.8% | 0.034% |
| Donnerstag | 259648 | 50.7% | 49.5% | 0.027% |
| Freitag | 257851 | 50.5% | 49.0% | 0.036% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 90205 | 1.5 ATR | 62% | 83% | 118% | 179% | 267% | 62% | 2 |
| 2 ATR | 52566 | 2.4 ATR | 40% | 54% | 78% | 118% | 174% | 34% | 2 |
| 3 ATR | 24960 | 3.4 ATR | 29% | 40% | 57% | 86% | 127% | 18% | 2 |
| 4 ATR | 11879 | 4.4 ATR | 24% | 32% | 47% | 70% | 102% | 10% | 2 |
| 5 ATR | 5841 | 5.4 ATR | 21% | 28% | 41% | 60% | 88% | 7% | 2 |
| 6 ATR | 2944 | 6.4 ATR | 18% | 25% | 36% | 54% | 78% | 5% | 2 |
| 7 ATR | 1718 | 7.4 ATR | 16% | 22% | 33% | 49% | 71% | 4% | 2 |
| 8 ATR | 899 | 8.4 ATR | 16% | 22% | 31% | 47% | 68% | 2% | 2 |
| 9 ATR | 530 | 9.4 ATR | 15% | 21% | 30% | 46% | 65% | 2% | 2 |
| 10 ATR | 286 | 10.4 ATR | 14% | 19% | 27% | 41% | 66% | 3% | 2 |
| 11 ATR | 181 | 11.4 ATR | 14% | 19% | 29% | 42% | 65% | 1% | 2 |
| 12 ATR | 126 | 12.4 ATR | 13% | 20% | 30% | 41% | 58% | 2% | 2 |
| 13 ATR | 68 | 13.5 ATR | 16% | 21% | 30% | 44% | 62% | 0% | 2 |
| 14 ATR | 54 | 14.4 ATR | 13% | 15% | 24% | 35% | 54% | 4% | 2 |
| 15 ATR | 33 | 15.3 ATR | 10% | 17% | 25% | 38% | 49% | 3% | 2 |
| 16 ATR | 28 | 16.6 ATR | 13% | 17% | 29% | 38% | 51% | 0% | 2 |
| 17 ATR | 18 | 17.4 ATR | 13% | 16% | 30% | 43% | 76% | 11% | 2 |
| 18 ATR | 6 | 18.7 ATR | 30% | 30% | 43% | 61% | 64% | 0% | 3 |
| 19 ATR | 8 | 19.5 ATR | 22% | 26% | 28% | 35% | 48% | 0% | 2 |
| 20 ATR | 6 | 20.6 ATR | 34% | 36% | 48% | 58% | 72% | 0% | 2 |
| 21 ATR | 5 | 21.4 ATR | 25% | 25% | 28% | 41% | 59% | 0% | 2 |
| 22 ATR | 5 | 22.8 ATR | 15% | 18% | 21% | 34% | 42% | 0% | 1 |
| 23 ATR | 8 | 23.4 ATR | 14% | 17% | 22% | 28% | 36% | 0% | 2 |
| 24 ATR | 3 | 24.4 ATR | 13% | 15% | 18% | 47% | 65% | 0% | 2 |
| 25 ATR | 2 | 25.1 ATR | 48% | 50% | 54% | 57% | 59% | 0% | 10 |
| 26 ATR | 3 | 26.7 ATR | 17% | 19% | 22% | 26% | 28% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 2 | 28.7 ATR | 35% | 38% | 42% | 47% | 49% | 0% | 4 |
| 29 ATR | 3 | 29.2 ATR | 14% | 16% | 18% | 54% | 76% | 0% | 2 |
| 30 ATR | 10 | 33.0 ATR | 9% | 14% | 25% | 39% | 59% | 10% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._