# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-09-22 06:27 UTC. 7 Jahre, 283 Werte, 152729 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 57255 | 54% | 56% | 57% | 60% | 1.81 | 5.26 |
| 0.5 ATR | 39315 | 55% | 56% | 57% | 61% | 1.81 | 5.21 |
| 0.75 ATR | 24303 | 54% | 56% | 56% | 60% | 1.88 | 5.45 |
| 1.0 ATR | 14015 | 54% | 56% | 57% | 60% | 1.91 | 5.64 |
| 1.25 ATR | 7691 | 54% | 56% | 56% | 62% | 1.92 | 5.92 |
| 1.5 ATR | 4273 | 52% | 55% | 55% | 61% | 2.04 | 6.13 |
| 1.75 ATR | 2298 | 53% | 56% | 56% | 64% | 1.89 | 6.32 |
| 2.0 ATR | 1386 | 54% | 55% | 58% | 62% | 1.99 | 6.51 |
| 2.25 ATR | 765 | 51% | 54% | 58% | 61% | 1.98 | 6.21 |
| 2.5 ATR | 431 | 51% | 52% | 56% | 62% | 2.07 | 5.68 |
| 2.75 ATR | 284 | 57% | 59% | 57% | 56% | 1.63 | 6.07 |
| 3.0 ATR | 207 | 46% | 47% | 56% | 56% | 2.20 | 5.37 |
| 3.25 ATR | 140 | 46% | 46% | 49% | 59% | 2.41 | 5.57 |
| 3.5 ATR | 114 | 55% | 54% | 60% | 69% | 1.69 | 4.82 |
| 3.75 ATR | 78 | 38% | 46% | 56% | 62% | 2.21 | 5.10 |
| 4.0 ATR | 48 | 38% | 46% | 44% | 65% | 2.61 | 6.46 |
| 4.25 ATR | 45 | 49% | 58% | 53% | 64% | 1.56 | 3.82 |
| 4.5 ATR | 25 | 56% | 48% | 48% | 60% | 1.70 | 4.32 |
| 4.75 ATR | 16 | 44% | 44% | 56% | 56% | 1.93 | 4.22 |
| 5.0 ATR | 7 | 29% | 14% | 57% | 71% | 2.99 | 6.69 |
| 5.25 ATR | 11 | 36% | 46% | 64% | 64% | 1.22 | 3.21 |
| 5.5 ATR | 4 | 50% | 75% | 75% | 100% | 1.34 | 2.15 |
| 5.75 ATR | 6 | 67% | 67% | 67% | 50% | 1.03 | 3.25 |
| 6.0 ATR | 12 | 67% | 83% | 83% | 67% | 0.72 | 1.39 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 92679 | 52.7% | 51.7% | 0.112% |
| Dienstag | 101106 | 48.8% | 48.6% | -0.034% |
| Mittwoch | 100073 | 49.3% | 49.9% | 0.014% |
| Donnerstag | 98375 | 50.5% | 49.7% | 0.027% |
| Freitag | 97672 | 51.0% | 49.6% | 0.033% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 34216 | 1.5 ATR | 61% | 82% | 118% | 180% | 270% | 62% | 2 |
| 2 ATR | 20151 | 2.4 ATR | 40% | 54% | 78% | 119% | 174% | 34% | 2 |
| 3 ATR | 9520 | 3.4 ATR | 30% | 40% | 58% | 87% | 131% | 19% | 2 |
| 4 ATR | 4463 | 4.4 ATR | 25% | 33% | 48% | 72% | 103% | 11% | 2 |
| 5 ATR | 2237 | 5.4 ATR | 21% | 30% | 42% | 61% | 89% | 7% | 2 |
| 6 ATR | 1191 | 6.4 ATR | 19% | 26% | 37% | 56% | 81% | 6% | 2 |
| 7 ATR | 718 | 7.4 ATR | 17% | 23% | 34% | 50% | 72% | 3% | 2 |
| 8 ATR | 382 | 8.4 ATR | 17% | 23% | 32% | 48% | 67% | 2% | 2 |
| 9 ATR | 231 | 9.5 ATR | 15% | 21% | 30% | 46% | 60% | 1% | 2 |
| 10 ATR | 132 | 10.5 ATR | 14% | 18% | 28% | 44% | 68% | 2% | 2 |
| 11 ATR | 75 | 11.4 ATR | 17% | 22% | 33% | 46% | 65% | 0% | 3 |
| 12 ATR | 62 | 12.4 ATR | 12% | 19% | 29% | 36% | 49% | 0% | 2 |
| 13 ATR | 31 | 13.5 ATR | 12% | 21% | 31% | 47% | 63% | 0% | 2 |
| 14 ATR | 24 | 14.4 ATR | 14% | 18% | 26% | 34% | 48% | 4% | 2 |
| 15 ATR | 13 | 15.5 ATR | 14% | 19% | 27% | 44% | 47% | 8% | 2 |
| 16 ATR | 15 | 16.6 ATR | 18% | 20% | 29% | 39% | 48% | 0% | 2 |
| 17 ATR | 7 | 17.5 ATR | 13% | 14% | 19% | 40% | 64% | 0% | 2 |
| 18 ATR | 4 | 18.7 ATR | 41% | 50% | 59% | 63% | 65% | 0% | 3 |
| 19 ATR | 3 | 19.6 ATR | 30% | 35% | 43% | 52% | 57% | 0% | 2 |
| 20 ATR | 3 | 20.4 ATR | 33% | 34% | 35% | 45% | 51% | 0% | 2 |
| 21 ATR | 1 | 21.2 ATR | 24% | 24% | 24% | 24% | 24% | 0% | 2 |
| 23 ATR | 3 | 23.4 ATR | 13% | 14% | 17% | 17% | 18% | 0% | 1 |
| 24 ATR | 2 | 24.5 ATR | 13% | 24% | 41% | 59% | 69% | 0% | 1 |
| 25 ATR | 1 | 25.1 ATR | 60% | 60% | 60% | 60% | 60% | 0% | 4 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 1 | 28.5 ATR | 51% | 51% | 51% | 51% | 51% | 0% | 5 |
| 29 ATR | 2 | 29.1 ATR | 25% | 36% | 54% | 72% | 83% | 0% | 38 |
| 30 ATR | 2 | 30.9 ATR | 14% | 17% | 20% | 24% | 26% | 0% | 2 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._