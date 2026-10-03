# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-10-03 04:27 UTC. 20 Jahre, 283 Werte, 414222 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 156199 | 55% | 56% | 58% | 61% | 1.78 | 5.26 |
| 0.5 ATR | 107268 | 55% | 56% | 58% | 61% | 1.79 | 5.28 |
| 0.75 ATR | 66597 | 55% | 56% | 57% | 62% | 1.82 | 5.44 |
| 1.0 ATR | 38124 | 55% | 56% | 57% | 62% | 1.88 | 5.64 |
| 1.25 ATR | 20734 | 55% | 56% | 57% | 62% | 1.92 | 5.79 |
| 1.5 ATR | 11128 | 54% | 55% | 57% | 62% | 1.96 | 5.94 |
| 1.75 ATR | 5817 | 53% | 55% | 57% | 62% | 1.99 | 6.10 |
| 2.0 ATR | 3264 | 54% | 55% | 57% | 63% | 2.00 | 6.03 |
| 2.25 ATR | 1791 | 52% | 53% | 57% | 61% | 2.00 | 6.13 |
| 2.5 ATR | 1078 | 52% | 53% | 56% | 60% | 2.04 | 5.62 |
| 2.75 ATR | 694 | 52% | 53% | 55% | 57% | 1.98 | 5.50 |
| 3.0 ATR | 470 | 50% | 49% | 57% | 59% | 2.04 | 5.39 |
| 3.25 ATR | 295 | 44% | 45% | 52% | 63% | 2.28 | 5.20 |
| 3.5 ATR | 215 | 51% | 51% | 56% | 62% | 1.88 | 4.81 |
| 3.75 ATR | 166 | 48% | 52% | 58% | 58% | 1.78 | 5.10 |
| 4.0 ATR | 106 | 40% | 48% | 49% | 59% | 2.24 | 5.57 |
| 4.25 ATR | 89 | 46% | 54% | 52% | 60% | 1.87 | 5.55 |
| 4.5 ATR | 56 | 43% | 41% | 45% | 61% | 1.76 | 4.39 |
| 4.75 ATR | 34 | 44% | 50% | 62% | 59% | 1.67 | 4.38 |
| 5.0 ATR | 18 | 28% | 28% | 56% | 56% | 1.64 | 5.12 |
| 5.25 ATR | 25 | 52% | 44% | 60% | 60% | 1.59 | 4.23 |
| 5.5 ATR | 13 | 46% | 54% | 62% | 92% | 1.48 | 5.28 |
| 5.75 ATR | 11 | 64% | 64% | 54% | 46% | 1.15 | 4.06 |
| 6.0 ATR | 30 | 63% | 67% | 60% | 63% | 0.75 | 3.89 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 244226 | 50.6% | 49.9% | 0.025% |
| Dienstag | 265361 | 50.1% | 49.5% | 0.032% |
| Mittwoch | 264961 | 49.9% | 49.7% | 0.034% |
| Donnerstag | 260590 | 50.6% | 49.3% | 0.027% |
| Freitag | 258848 | 50.4% | 48.8% | 0.036% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 90510 | 1.5 ATR | 62% | 83% | 118% | 179% | 268% | 62% | 2 |
| 2 ATR | 52721 | 2.4 ATR | 40% | 54% | 78% | 118% | 174% | 34% | 2 |
| 3 ATR | 25087 | 3.4 ATR | 29% | 40% | 57% | 86% | 127% | 18% | 2 |
| 4 ATR | 11945 | 4.4 ATR | 24% | 32% | 47% | 70% | 102% | 10% | 2 |
| 5 ATR | 5885 | 5.4 ATR | 21% | 28% | 41% | 60% | 88% | 7% | 2 |
| 6 ATR | 2972 | 6.4 ATR | 18% | 25% | 36% | 54% | 78% | 5% | 2 |
| 7 ATR | 1727 | 7.4 ATR | 16% | 23% | 33% | 49% | 72% | 4% | 2 |
| 8 ATR | 898 | 8.4 ATR | 16% | 22% | 32% | 48% | 70% | 3% | 2 |
| 9 ATR | 534 | 9.5 ATR | 14% | 21% | 30% | 46% | 65% | 2% | 2 |
| 10 ATR | 286 | 10.4 ATR | 14% | 18% | 26% | 40% | 61% | 2% | 2 |
| 11 ATR | 188 | 11.5 ATR | 14% | 19% | 29% | 42% | 64% | 1% | 2 |
| 12 ATR | 131 | 12.4 ATR | 12% | 19% | 29% | 42% | 59% | 2% | 2 |
| 13 ATR | 72 | 13.5 ATR | 12% | 20% | 30% | 44% | 62% | 1% | 2 |
| 14 ATR | 54 | 14.4 ATR | 11% | 14% | 22% | 35% | 53% | 4% | 2 |
| 15 ATR | 33 | 15.3 ATR | 10% | 17% | 25% | 38% | 49% | 3% | 2 |
| 16 ATR | 30 | 16.5 ATR | 14% | 17% | 29% | 45% | 50% | 0% | 2 |
| 17 ATR | 18 | 17.4 ATR | 13% | 16% | 32% | 43% | 74% | 6% | 2 |
| 18 ATR | 8 | 18.7 ATR | 30% | 31% | 45% | 60% | 64% | 0% | 3 |
| 19 ATR | 9 | 19.5 ATR | 23% | 26% | 29% | 43% | 47% | 0% | 2 |
| 20 ATR | 5 | 20.5 ATR | 33% | 35% | 41% | 55% | 72% | 0% | 2 |
| 21 ATR | 5 | 21.4 ATR | 25% | 25% | 28% | 41% | 56% | 0% | 2 |
| 22 ATR | 3 | 22.8 ATR | 24% | 28% | 34% | 37% | 38% | 0% | 3 |
| 23 ATR | 8 | 23.4 ATR | 14% | 17% | 22% | 28% | 36% | 0% | 2 |
| 24 ATR | 4 | 24.3 ATR | 8% | 10% | 15% | 33% | 59% | 0% | 2 |
| 25 ATR | 2 | 25.1 ATR | 48% | 50% | 54% | 57% | 59% | 0% | 10 |
| 26 ATR | 3 | 26.7 ATR | 17% | 19% | 22% | 26% | 28% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 2 | 28.7 ATR | 35% | 38% | 42% | 47% | 49% | 0% | 4 |
| 29 ATR | 3 | 29.2 ATR | 14% | 16% | 18% | 54% | 76% | 0% | 2 |
| 30 ATR | 10 | 33.0 ATR | 3% | 10% | 21% | 30% | 59% | 10% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._