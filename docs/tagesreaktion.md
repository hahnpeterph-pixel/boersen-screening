# Tagesreaktion - was folgt auf einen harten Verlusttag?

_Erstellt 2026-10-03 20:51 UTC. 20 Jahre, 284 Werte, 411138 Verlusttage._

_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des Verlusttags._

## Gepoolt ueber alle Werte

| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | hoeher 60T | tiefer 20T Median | tiefer 20T p90 |
|---|---|---|---|---|---|---|---|
| 0.25 ATR | 157652 | 55% | 56% | 58% | 61% | 1.76 | 5.19 |
| 0.5 ATR | 107552 | 55% | 56% | 58% | 62% | 1.77 | 5.20 |
| 0.75 ATR | 65806 | 55% | 56% | 58% | 62% | 1.81 | 5.35 |
| 1.0 ATR | 37114 | 55% | 56% | 57% | 62% | 1.87 | 5.57 |
| 1.25 ATR | 19817 | 55% | 56% | 57% | 62% | 1.90 | 5.69 |
| 1.5 ATR | 10291 | 54% | 55% | 57% | 62% | 1.94 | 5.83 |
| 1.75 ATR | 5335 | 53% | 54% | 58% | 62% | 1.98 | 5.94 |
| 2.0 ATR | 2952 | 54% | 55% | 58% | 63% | 1.95 | 5.90 |
| 2.25 ATR | 1622 | 52% | 53% | 57% | 62% | 2.01 | 5.92 |
| 2.5 ATR | 958 | 52% | 53% | 57% | 61% | 1.93 | 5.34 |
| 2.75 ATR | 623 | 53% | 54% | 56% | 59% | 1.88 | 5.07 |
| 3.0 ATR | 438 | 50% | 50% | 58% | 58% | 1.94 | 5.20 |
| 3.25 ATR | 269 | 46% | 47% | 54% | 65% | 2.11 | 5.36 |
| 3.5 ATR | 199 | 52% | 50% | 56% | 63% | 1.78 | 4.63 |
| 3.75 ATR | 157 | 50% | 53% | 57% | 58% | 1.77 | 5.10 |
| 4.0 ATR | 98 | 38% | 48% | 49% | 60% | 2.20 | 5.00 |
| 4.25 ATR | 77 | 46% | 52% | 48% | 54% | 1.88 | 4.96 |
| 4.5 ATR | 54 | 43% | 43% | 46% | 59% | 1.78 | 4.40 |
| 4.75 ATR | 30 | 50% | 50% | 63% | 57% | 1.10 | 3.52 |
| 5.0 ATR | 18 | 33% | 28% | 50% | 50% | 1.64 | 5.50 |
| 5.25 ATR | 22 | 46% | 46% | 64% | 59% | 1.61 | 4.05 |
| 5.5 ATR | 13 | 46% | 54% | 62% | 92% | 1.48 | 5.28 |
| 5.75 ATR | 12 | 58% | 58% | 58% | 50% | 1.04 | 3.89 |
| 6.0 ATR | 29 | 59% | 62% | 59% | 69% | 0.75 | 4.18 |

_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - keine Sammelklassen, Fallzahl in jeder Zeile._

## Wochentage

_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte Reihenfolge nicht entscheidbar._

| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | mittlere Tagesrendite |
|---|---|---|---|---|
| Montag | 244384 | 50.6% | 50.0% | 0.023% |
| Dienstag | 264519 | 50.1% | 49.6% | 0.030% |
| Mittwoch | 264377 | 49.9% | 49.8% | 0.034% |
| Donnerstag | 260385 | 50.4% | 49.3% | 0.020% |
| Freitag | 258394 | 50.3% | 48.9% | 0.030% |

## Wie weit werden grosse Laeufe korrigiert?

_Ein Lauf ist die Strecke von einem Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._

| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | p75 | p90 | ganz zurueck | Korrektur Tage |
|---|---|---|---|---|---|---|---|---|---|
| 1 ATR | 88722 | 1.5 ATR | 62% | 83% | 118% | 179% | 266% | 62% | 2 |
| 2 ATR | 52246 | 2.4 ATR | 40% | 54% | 78% | 118% | 174% | 34% | 2 |
| 3 ATR | 24761 | 3.4 ATR | 30% | 40% | 58% | 87% | 128% | 18% | 2 |
| 4 ATR | 11731 | 4.4 ATR | 24% | 33% | 48% | 71% | 102% | 11% | 2 |
| 5 ATR | 5754 | 5.4 ATR | 21% | 28% | 41% | 61% | 88% | 7% | 2 |
| 6 ATR | 2927 | 6.4 ATR | 19% | 26% | 37% | 55% | 78% | 4% | 2 |
| 7 ATR | 1681 | 7.4 ATR | 17% | 23% | 33% | 50% | 70% | 3% | 2 |
| 8 ATR | 857 | 8.4 ATR | 16% | 22% | 32% | 48% | 68% | 2% | 2 |
| 9 ATR | 531 | 9.5 ATR | 15% | 21% | 30% | 46% | 70% | 3% | 2 |
| 10 ATR | 288 | 10.4 ATR | 14% | 19% | 27% | 41% | 66% | 3% | 2 |
| 11 ATR | 191 | 11.5 ATR | 14% | 18% | 30% | 45% | 70% | 3% | 3 |
| 12 ATR | 127 | 12.4 ATR | 13% | 21% | 30% | 43% | 60% | 2% | 2 |
| 13 ATR | 69 | 13.5 ATR | 18% | 23% | 31% | 43% | 62% | 0% | 3 |
| 14 ATR | 52 | 14.5 ATR | 13% | 15% | 23% | 36% | 56% | 4% | 2 |
| 15 ATR | 33 | 15.5 ATR | 9% | 17% | 23% | 40% | 59% | 6% | 2 |
| 16 ATR | 29 | 16.6 ATR | 13% | 18% | 29% | 42% | 50% | 0% | 2 |
| 17 ATR | 19 | 17.4 ATR | 13% | 17% | 30% | 43% | 72% | 10% | 2 |
| 18 ATR | 9 | 18.4 ATR | 28% | 30% | 31% | 56% | 63% | 0% | 2 |
| 19 ATR | 9 | 19.6 ATR | 23% | 26% | 29% | 37% | 47% | 0% | 2 |
| 20 ATR | 5 | 20.5 ATR | 37% | 41% | 55% | 59% | 74% | 0% | 1 |
| 21 ATR | 6 | 21.4 ATR | 25% | 26% | 35% | 64% | 85% | 0% | 2 |
| 22 ATR | 6 | 22.7 ATR | 15% | 18% | 22% | 32% | 40% | 0% | 2 |
| 23 ATR | 8 | 23.4 ATR | 14% | 17% | 22% | 28% | 36% | 0% | 2 |
| 24 ATR | 3 | 24.4 ATR | 13% | 15% | 18% | 47% | 65% | 0% | 2 |
| 25 ATR | 2 | 25.1 ATR | 48% | 50% | 54% | 57% | 59% | 0% | 10 |
| 26 ATR | 2 | 26.4 ATR | 17% | 19% | 22% | 25% | 27% | 0% | 1 |
| 27 ATR | 2 | 27.4 ATR | 43% | 49% | 58% | 67% | 73% | 0% | 3 |
| 28 ATR | 2 | 28.7 ATR | 35% | 38% | 42% | 47% | 49% | 0% | 4 |
| 29 ATR | 3 | 29.2 ATR | 14% | 16% | 18% | 54% | 76% | 0% | 2 |
| 30 ATR | 11 | 34.3 ATR | 10% | 16% | 28% | 48% | 56% | 0% | 1 |

_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf mit Datum in `docs/laeufe_roh.csv`._


---

_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._