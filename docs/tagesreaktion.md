# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-08-30 12:52 UTC. 7 Jahre, 216 Werte, 115847 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 44256 | 55% | 56% | 57% | 60% | 1.80 | 5.20 |
| 0.5 ATR | 30184 | 54% | 56% | 56% | 60% | 1.82 | 5.18 |
| 0.75 ATR | 18205 | 54% | 55% | 56% | 60% | 1.88 | 5.38 |
| 1.0 ATR | 10409 | 54% | 56% | 56% | 60% | 1.90 | 5.57 |
| 1.25 ATR | 5616 | 54% | 56% | 56% | 62% | 1.89 | 5.90 |
| 1.5 ATR | 3012 | 50% | 53% | 54% | 60% | 2.09 | 6.09 |
| 1.75 ATR | 1623 | 52% | 55% | 56% | 64% | 1.90 | 6.27 |
| 2.0 ATR | 975 | 54% | 54% | 58% | 62% | 1.96 | 6.32 |
| 2.25 ATR | 539 | 51% | 54% | 59% | 60% | 1.96 | 6.23 |
| 2.5 ATR | 305 | 49% | 49% | 53% | 63% | 2.00 | 5.52 |
| 2.75 ATR | 198 | 58% | 61% | 59% | 56% | 1.48 | 5.09 |
| 3.0 ATR | 153 | 48% | 48% | 60% | 54% | 2.20 | 5.24 |
| 3.25 ATR | 95 | 45% | 43% | 45% | 57% | 2.42 | 5.30 |
| 3.5 ATR | 88 | 59% | 54% | 61% | 69% | 1.61 | 4.71 |
| 3.75 ATR | 62 | 44% | 47% | 52% | 55% | 1.79 | 3.75 |
| 4.0 ATR | 30 | 37% | 43% | 37% | 57% | 2.20 | 5.22 |
| 4.25 ATR | 33 | 42% | 58% | 54% | 64% | 1.46 | 3.62 |
| 4.5 ATR | 20 | 50% | 45% | 45% | 55% | 1.86 | 4.25 |
| 4.75 ATR | 13 | 38% | 38% | 54% | 54% | 2.05 | 4.19 |
| 5.0 ATR | 5 | 40% | 20% | 60% | 80% | 1.55 | 6.61 |
| 5.25 ATR | 9 | 22% | 33% | 56% | 67% | 1.63 | 3.96 |
| 5.5 ATR | 3 | 67% | 100% | 100% | 100% | 1.04 | 1.53 |
| 5.75 ATR | 4 | 50% | 50% | 50% | 50% | 1.24 | 3.58 |
| 6.0 ATR | 10 | 60% | 80% | 80% | 80% | 0.74 | 1.45 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 70666 | 52.9% | 51.7% | 0.108% |
| Dienstag | 77002 | 49.3% | 48.8% | -0.037% |
| Mittwoch | 76277 | 49.8% | 50.2% | 0.019% |
| Donnerstag | 75196 | 50.8% | 50.0% | 0.025% |
| Freitag | 74596 | 51.3% | 50.0% | 0.030% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 25757 | 1.5 ATR | 61% | 83% | 118% | 180% | 270% | 62% | 2 |
| 2 ATR | 15374 | 2.4 ATR | 41% | 55% | 79% | 120% | 175% | 34% | 2 |
| 3 ATR | 7139 | 3.4 ATR | 31% | 41% | 58% | 89% | 132% | 20% | 2 |
| 4 ATR | 3295 | 4.4 ATR | 25% | 34% | 49% | 73% | 104% | 11% | 2 |
| 5 ATR | 1657 | 5.4 ATR | 21% | 30% | 43% | 61% | 88% | 7% | 2 |
| 6 ATR | 874 | 6.4 ATR | 20% | 26% | 38% | 58% | 80% | 6% | 2 |
| 7 ATR | 519 | 7.4 ATR | 17% | 24% | 35% | 51% | 68% | 3% | 2 |
| 8 ATR | 279 | 8.4 ATR | 17% | 23% | 31% | 47% | 62% | 2% | 2 |
| 9 ATR | 167 | 9.5 ATR | 15% | 21% | 30% | 43% | 60% | 1% | 2 |
| 10 ATR | 97 | 10.5 ATR | 14% | 17% | 26% | 40% | 67% | 2% | 2 |
| 11 ATR | 60 | 11.4 ATR | 18% | 23% | 32% | 45% | 60% | 0% | 3 |
| 12 ATR | 42 | 12.4 ATR | 12% | 20% | 31% | 42% | 51% | 0% | 2 |
| 13 ATR | 25 | 13.5 ATR | 19% | 27% | 34% | 48% | 63% | 0% | 3 |
| 14 ATR | 17 | 14.4 ATR | 16% | 19% | 27% | 37% | 75% | 12% | 2 |
| 15 ATR | 10 | 15.5 ATR | 18% | 21% | 27% | 43% | 52% | 10% | 2 |
| 16 ATR | 12 | 16.5 ATR | 19% | 22% | 29% | 35% | 48% | 0% | 2 |
| 17 ATR | 5 | 17.5 ATR | 12% | 14% | 19% | 43% | 60% | 0% | 2 |
| 18 ATR | 3 | 18.7 ATR | 57% | 59% | 62% | 64% | 65% | 0% | 4 |
| 19 ATR | 2 | 19.6 ATR | 45% | 48% | 52% | 56% | 59% | 0% | 2 |
| 20 ATR | 2 | 20.3 ATR | 37% | 40% | 45% | 50% | 53% | 0% | 4 |
| 21 ATR | 1 | 21.2 ATR | 24% | 24% | 24% | 24% | 24% | 0% | 2 |
| 23 ATR | 3 | 23.4 ATR | 13% | 14% | 17% | 17% | 18% | 0% | 1 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 1 | 28.5 ATR | 51% | 51% | 51% | 51% | 51% | 0% | 5 |
| 29 ATR | 1 | 29.2 ATR | 90% | 90% | 90% | 90% | 90% | 0% | 75 |
| 30 ATR | 1 | 31.1 ATR | 13% | 13% | 13% | 13% | 13% | 0% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._