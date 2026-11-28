# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-11-28 07:55 UTC. 20 Jahre, 244 Werte, 353293 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 134901 | 55% | 56% | 58% | 62% | 1.74 | 5.15 |
| 0.5 ATR | 92332 | 55% | 57% | 58% | 62% | 1.75 | 5.16 |
| 0.75 ATR | 56846 | 55% | 57% | 58% | 62% | 1.78 | 5.33 |
| 1.0 ATR | 31782 | 55% | 56% | 57% | 62% | 1.85 | 5.55 |
| 1.25 ATR | 17201 | 55% | 56% | 57% | 62% | 1.89 | 5.68 |
| 1.5 ATR | 8950 | 54% | 56% | 57% | 62% | 1.92 | 5.79 |
| 1.75 ATR | 4634 | 54% | 54% | 58% | 63% | 1.98 | 5.92 |
| 2.0 ATR | 2557 | 54% | 54% | 57% | 64% | 1.93 | 5.92 |
| 2.25 ATR | 1415 | 52% | 53% | 57% | 63% | 2.01 | 5.96 |
| 2.5 ATR | 833 | 52% | 54% | 57% | 61% | 1.93 | 5.45 |
| 2.75 ATR | 558 | 53% | 54% | 57% | 60% | 1.88 | 5.02 |
| 3.0 ATR | 394 | 51% | 50% | 60% | 59% | 1.82 | 5.16 |
| 3.25 ATR | 252 | 45% | 46% | 54% | 65% | 2.14 | 5.32 |
| 3.5 ATR | 180 | 49% | 49% | 54% | 61% | 1.95 | 4.73 |
| 3.75 ATR | 137 | 52% | 54% | 59% | 59% | 1.76 | 5.15 |
| 4.0 ATR | 90 | 39% | 50% | 51% | 63% | 2.14 | 4.97 |
| 4.25 ATR | 71 | 44% | 52% | 49% | 54% | 1.88 | 5.06 |
| 4.5 ATR | 48 | 46% | 46% | 46% | 58% | 1.76 | 4.28 |
| 4.75 ATR | 28 | 50% | 50% | 64% | 57% | 1.10 | 3.71 |
| 5.0 ATR | 17 | 35% | 24% | 53% | 53% | 1.55 | 5.59 |
| 5.25 ATR | 19 | 42% | 42% | 63% | 58% | 1.63 | 4.17 |
| 5.5 ATR | 13 | 46% | 54% | 62% | 92% | 1.48 | 5.28 |
| 5.75 ATR | 12 | 58% | 58% | 58% | 50% | 1.04 | 3.89 |
| 6.0 ATR | 23 | 61% | 61% | 52% | 74% | 0.78 | 3.47 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 208888 | 50.8% | 50.2% | 0.027% |
| Dienstag | 227929 | 50.2% | 49.8% | 0.036% |
| Mittwoch | 227822 | 49.9% | 49.9% | 0.039% |
| Donnerstag | 223806 | 50.6% | 49.5% | 0.023% |
| Freitag | 222462 | 50.4% | 49.0% | 0.033% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 76676 | 1.5 ATR | 62% | 83% | 118% | 178% | 266% | 62% | 2 |
| 2 ATR | 44982 | 2.4 ATR | 40% | 54% | 78% | 118% | 174% | 34% | 2 |
| 3 ATR | 21219 | 3.4 ATR | 30% | 40% | 57% | 87% | 128% | 18% | 2 |
| 4 ATR | 10073 | 4.4 ATR | 24% | 33% | 47% | 70% | 102% | 10% | 2 |
| 5 ATR | 4937 | 5.4 ATR | 21% | 28% | 41% | 60% | 87% | 7% | 2 |
| 6 ATR | 2547 | 6.4 ATR | 18% | 25% | 37% | 55% | 79% | 5% | 2 |
| 7 ATR | 1480 | 7.4 ATR | 17% | 23% | 33% | 50% | 71% | 3% | 2 |
| 8 ATR | 754 | 8.4 ATR | 16% | 22% | 32% | 48% | 67% | 2% | 2 |
| 9 ATR | 482 | 9.5 ATR | 15% | 21% | 30% | 46% | 69% | 2% | 2 |
| 10 ATR | 249 | 10.5 ATR | 14% | 19% | 27% | 41% | 62% | 3% | 2 |
| 11 ATR | 174 | 11.5 ATR | 14% | 18% | 30% | 46% | 71% | 2% | 3 |
| 12 ATR | 114 | 12.5 ATR | 13% | 21% | 30% | 43% | 60% | 3% | 2 |
| 13 ATR | 61 | 13.5 ATR | 18% | 22% | 31% | 43% | 62% | 0% | 2 |
| 14 ATR | 48 | 14.5 ATR | 13% | 15% | 23% | 35% | 55% | 2% | 2 |
| 15 ATR | 31 | 15.5 ATR | 9% | 17% | 25% | 41% | 61% | 6% | 2 |
| 16 ATR | 28 | 16.6 ATR | 13% | 17% | 29% | 37% | 47% | 0% | 2 |
| 17 ATR | 19 | 17.4 ATR | 13% | 17% | 30% | 43% | 72% | 10% | 2 |
| 18 ATR | 9 | 18.4 ATR | 28% | 30% | 31% | 56% | 63% | 0% | 2 |
| 19 ATR | 8 | 19.6 ATR | 22% | 27% | 31% | 38% | 48% | 0% | 2 |
| 20 ATR | 5 | 20.5 ATR | 37% | 41% | 55% | 59% | 74% | 0% | 1 |
| 21 ATR | 5 | 21.4 ATR | 26% | 28% | 41% | 71% | 88% | 0% | 3 |
| 22 ATR | 6 | 22.7 ATR | 15% | 18% | 22% | 32% | 40% | 0% | 2 |
| 23 ATR | 7 | 23.4 ATR | 16% | 17% | 26% | 31% | 36% | 0% | 1 |
| 24 ATR | 3 | 24.4 ATR | 13% | 15% | 18% | 47% | 65% | 0% | 2 |
| 25 ATR | 1 | 25.1 ATR | 60% | 60% | 60% | 60% | 60% | 0% | 4 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 1 | 27.6 ATR | 76% | 76% | 76% | 76% | 76% | 0% | 1 |
| 28 ATR | 2 | 28.7 ATR | 35% | 38% | 42% | 47% | 49% | 0% | 4 |
| 29 ATR | 3 | 29.2 ATR | 14% | 16% | 18% | 54% | 76% | 0% | 2 |
| 30 ATR | 11 | 34.3 ATR | 10% | 16% | 28% | 48% | 56% | 0% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._