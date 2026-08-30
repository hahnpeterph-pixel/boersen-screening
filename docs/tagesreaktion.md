# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-08-30 10:56 UTC. 7 Jahre, 211 Werte, 112862 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 43189 | 55% | 56% | 57% | 60% | 1.80 | 5.19 |
| 0.5 ATR | 29420 | 55% | 56% | 57% | 60% | 1.81 | 5.16 |
| 0.75 ATR | 17744 | 54% | 55% | 56% | 60% | 1.89 | 5.37 |
| 1.0 ATR | 10138 | 54% | 56% | 56% | 60% | 1.90 | 5.57 |
| 1.25 ATR | 5434 | 54% | 56% | 56% | 62% | 1.90 | 5.91 |
| 1.5 ATR | 2930 | 50% | 53% | 54% | 60% | 2.10 | 6.07 |
| 1.75 ATR | 1569 | 52% | 55% | 56% | 65% | 1.89 | 6.26 |
| 2.0 ATR | 935 | 54% | 54% | 58% | 62% | 1.96 | 6.41 |
| 2.25 ATR | 517 | 51% | 54% | 58% | 60% | 1.97 | 6.25 |
| 2.5 ATR | 296 | 50% | 50% | 54% | 62% | 1.99 | 5.49 |
| 2.75 ATR | 191 | 58% | 61% | 59% | 56% | 1.47 | 5.11 |
| 3.0 ATR | 144 | 49% | 46% | 58% | 51% | 2.26 | 5.33 |
| 3.25 ATR | 87 | 45% | 45% | 46% | 59% | 2.42 | 4.90 |
| 3.5 ATR | 83 | 58% | 54% | 63% | 70% | 1.58 | 4.29 |
| 3.75 ATR | 60 | 45% | 47% | 52% | 55% | 1.78 | 3.71 |
| 4.0 ATR | 30 | 37% | 43% | 37% | 57% | 2.20 | 5.22 |
| 4.25 ATR | 33 | 42% | 58% | 54% | 64% | 1.46 | 3.62 |
| 4.5 ATR | 20 | 50% | 45% | 45% | 55% | 1.86 | 4.25 |
| 4.75 ATR | 13 | 38% | 38% | 54% | 54% | 2.05 | 4.19 |
| 5.0 ATR | 5 | 40% | 20% | 60% | 80% | 1.55 | 6.61 |
| 5.25 ATR | 9 | 22% | 33% | 56% | 67% | 1.63 | 3.96 |
| 5.5 ATR | 2 | 50% | 100% | 100% | 100% | 0.62 | 0.96 |
| 5.75 ATR | 4 | 50% | 50% | 50% | 50% | 1.24 | 3.58 |
| 6.0 ATR | 9 | 56% | 78% | 78% | 78% | 0.75 | 1.48 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 68985 | 53.0% | 51.8% | 0.113% |
| Dienstag | 75181 | 49.3% | 48.8% | -0.036% |
| Mittwoch | 74472 | 49.8% | 50.1% | 0.017% |
| Donnerstag | 73414 | 50.9% | 50.1% | 0.027% |
| Freitag | 72818 | 51.3% | 50.0% | 0.032% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 25201 | 1.5 ATR | 61% | 83% | 118% | 180% | 270% | 62% | 2 |
| 2 ATR | 15026 | 2.4 ATR | 41% | 55% | 79% | 120% | 175% | 34% | 2 |
| 3 ATR | 6959 | 3.4 ATR | 31% | 41% | 59% | 89% | 132% | 20% | 2 |
| 4 ATR | 3223 | 4.4 ATR | 25% | 34% | 49% | 73% | 104% | 11% | 2 |
| 5 ATR | 1609 | 5.4 ATR | 21% | 30% | 43% | 61% | 87% | 7% | 2 |
| 6 ATR | 850 | 6.4 ATR | 19% | 26% | 38% | 58% | 78% | 5% | 2 |
| 7 ATR | 504 | 7.4 ATR | 17% | 24% | 35% | 51% | 67% | 3% | 2 |
| 8 ATR | 270 | 8.4 ATR | 17% | 23% | 31% | 46% | 61% | 2% | 2 |
| 9 ATR | 158 | 9.5 ATR | 15% | 20% | 29% | 42% | 59% | 1% | 2 |
| 10 ATR | 94 | 10.5 ATR | 14% | 17% | 26% | 42% | 68% | 2% | 2 |
| 11 ATR | 52 | 11.4 ATR | 17% | 20% | 30% | 42% | 58% | 0% | 3 |
| 12 ATR | 39 | 12.4 ATR | 13% | 20% | 30% | 36% | 48% | 0% | 2 |
| 13 ATR | 24 | 13.5 ATR | 19% | 26% | 34% | 48% | 63% | 0% | 3 |
| 14 ATR | 16 | 14.4 ATR | 16% | 18% | 26% | 36% | 54% | 6% | 2 |
| 15 ATR | 6 | 15.6 ATR | 16% | 21% | 24% | 40% | 81% | 17% | 2 |
| 16 ATR | 12 | 16.5 ATR | 19% | 22% | 29% | 35% | 48% | 0% | 2 |
| 17 ATR | 3 | 17.5 ATR | 12% | 12% | 14% | 28% | 37% | 0% | 2 |
| 18 ATR | 3 | 18.7 ATR | 57% | 59% | 62% | 64% | 65% | 0% | 4 |
| 19 ATR | 2 | 19.6 ATR | 45% | 48% | 52% | 56% | 59% | 0% | 2 |
| 20 ATR | 1 | 20.4 ATR | 55% | 55% | 55% | 55% | 55% | 0% | 6 |
| 21 ATR | 1 | 21.2 ATR | 24% | 24% | 24% | 24% | 24% | 0% | 2 |
| 23 ATR | 3 | 23.4 ATR | 13% | 14% | 17% | 17% | 18% | 0% | 1 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 1 | 27.2 ATR | 40% | 40% | 40% | 40% | 40% | 0% | 5 |
| 28 ATR | 1 | 28.5 ATR | 51% | 51% | 51% | 51% | 51% | 0% | 5 |
| 29 ATR | 1 | 29.2 ATR | 90% | 90% | 90% | 90% | 90% | 0% | 75 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._