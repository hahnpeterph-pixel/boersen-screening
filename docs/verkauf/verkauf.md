# Verkaufs-Check - Stufe 1 (Stand 2026-10-02 14:42 UTC)

Parallellauf. Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss. Entscheidungspunkt = Hoch seit Kauf hoechstens 3 Tage alt, Anstieg mind. 1 ATR. Ganz weg = Kurs faellt auf den Einstieg, bevor ein neues Hoch kommt; halb weg = die Haelfte des Anstiegs geht verloren, bevor ein neues Hoch kommt.

Werte: 271 · Kaeufe: 93380 · Entscheidungspunkte: 1588625

## Wie weit gelaufen - Rueckfallquote je Wert (Median ueber die Werte)

| Lauf-Stand | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| frueh | 50 % / 50 % | 73 % / 73 % |
| mittel | 42 % / 42 % | 65 % / 65 % |
| weit | 28 % / 30 % | 49 % / 51 % |
| sehr weit | 12 % / 12 % | 26 % / 26 % |

## Schon weit gelaufen: Rueckfall nach bereits abgegebenem Anteil

| Schon abgegeben | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| 0-10 % | 5 % / 4 % | 12 % / 10 % |
| 10-25 % | 14 % / 13 % | 31 % / 30 % |
| 25-40 % | 28 % / 28 % | 60 % / 60 % |
| ueber 40 % | 58 % / 60 % | 92 % / 92 % |

## Merkmale einzeln - nur wenn schon mind. der uebliche Anstieg gelaufen ist

Werte = mind. 10 Faelle mit UND ohne Merkmal in beiden Zeitraeumen. Verglichen wird nur bei gleicher bereits abgegebener Rueckgabe (0-10 / 10-25 / 25-40 / ueber 40 % des Anstiegs). Plus = Rueckfall in beiden Zeitraeumen mind. 8 Prozentpunkte HAEUFIGER mit Merkmal (spricht fuer Verkauf), Minus = seltener. Diff = Median ueber die Werte (bis 2022 / ab 2023).

### Gewinn ganz weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 265 | 5 | 1 | 0.8 / -0.2 |
| Rot + Volumen | 265 | 9 | 1 | 1.7 / 0.5 |
| Alarm 187 | 265 | 0 | 0 | -1.4 / -2.6 |
| Hoch heute | 265 | 0 | 0 | -0.2 / 0.5 |
| RSI hoch | 264 | 0 | 2 | -3.0 / -3.2 |
| Weit ueber EMA50 | 263 | 0 | 5 | -3.7 / -3.9 |
| Schneller Anstieg | 265 | 0 | 0 | 0.3 / -0.2 |
| Kauf mit 2+ Punkten | 264 | 0 | 0 | -0.2 / -0.2 |

### halber Gewinn weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 265 | 1 | 1 | 1.2 / 1.3 |
| Rot + Volumen | 265 | 6 | 1 | 1.8 / 1.2 |
| Alarm 187 | 265 | 0 | 2 | -0.6 / -0.4 |
| Hoch heute | 265 | 0 | 2 | -1.5 / -0.7 |
| RSI hoch | 264 | 2 | 19 | -5.3 / -5.6 |
| Weit ueber EMA50 | 263 | 0 | 27 | -4.8 / -6.4 |
| Schneller Anstieg | 265 | 2 | 0 | 0.3 / 0.9 |
| Kauf mit 2+ Punkten | 264 | 0 | 0 | -0.1 / -1.1 |

### Erklaerung der Merkmale

- **Rote Kerze**: Schluss unter Eroeffnung am Entscheidungstag
- **Rot + Volumen**: Rote Kerze mit ueberdurchschnittlichem Volumen (20-Tage-Schnitt)
- **Alarm 187**: Schluss > 3 ATR ueber Bezugstief, Hoch seit Kauf <= 3 Tage alt, rote Kerze
- **Hoch heute**: Das Hoch seit Kauf ist am Entscheidungstag selbst
- **RSI hoch**: RSI ueber dem RSI an 7 von 10 frueheren Hochs des Werts
- **Weit ueber EMA50**: Abstand zur EMA50 groesser als an 7 von 10 frueheren Hochs
- **Schneller Anstieg**: Anstieg je Tag mehr als 1,5x so schnell wie ueblich
- **Kauf mit 2+ Punkten**: Einstieg hatte mind. 2 Boden-Punkte

## Renditetest Verkaufsregeln

Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss, KO = Bezugstief minus Puffer. Schein ohne Aufgeld, Spread, Gebuehren; Knock-out = -100 %. Hoechstens 126 Handelstage. Je Wert Mittelwert (mind. 10 Kaeufe), dann Median ueber die Werte. 'Je Monat' = Rendite je 21 Handelstage Haltedauer (Geld ist frueher wieder frei). 'Besser als 187' = Werte, bei denen die Regel in BEIDEN Zeitraeumen mehr bringt als der Ausstiegsalarm 187.

### Puffer 2 ATR

| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |
|---|---|---|---|---|
| halten | 46 / 49 % | 69 | 14 % | 159 / 265 |
| ruecksetzer_t | 9 / 8 % | 16 | 12 % | 30 / 265 |
| alarm187 | 17 / 20 % | 18 | 19 % | - |
| nachlauf25 | 12 / 15 % | 15 | 19 % | 30 / 265 |
| nachlauf33 | 13 / 16 % | 16 | 20 % | 45 / 265 |
| nachlauf40 | 15 / 18 % | 18 | 18 % | 53 / 265 |
| nachlauf33_frueh | 8 / 9 % | 8 | 21 % | 19 / 265 |

### Puffer 3 ATR

| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |
|---|---|---|---|---|
| halten | 44 / 53 % | 83 | 11 % | 169 / 265 |
| ruecksetzer_t | 7 / 7 % | 16 | 9 % | 22 / 265 |
| alarm187 | 17 / 19 % | 24 | 15 % | - |
| nachlauf25 | 12 / 15 % | 18 | 15 % | 25 / 265 |
| nachlauf33 | 13 / 15 % | 19 | 15 % | 35 / 265 |
| nachlauf40 | 13 / 17 % | 22 | 14 % | 37 / 265 |
| nachlauf33_frueh | 7 / 9 % | 10 | 17 % | 12 / 265 |

### Regeln

- **halten**: Halten bis Knock-out oder 126 Tage
- **ruecksetzer_t**: Verkauf beim Ruecksetzer um T ATR vom Hoch (Chance A)
- **alarm187**: Verkauf zum Schluss am ersten Tag mit Alarm 187
- **nachlauf25**: Nachlauf: ab ueblichem Anstieg Verkauf, wenn 25 % des Anstiegs weg
- **nachlauf33**: Nachlauf: ab ueblichem Anstieg Verkauf, wenn 33 % des Anstiegs weg
- **nachlauf40**: Nachlauf: ab ueblichem Anstieg Verkauf, wenn 40 % des Anstiegs weg
- **nachlauf33_frueh**: Nachlauf 33 %, aber schon ab halbem ueblichen Anstieg

## Lohnt Halten noch? (Erwartungswert ab heute)

Wie viel kam ab einem Tag in dieser Lage im Schnitt noch dazu, wenn man nach der heutigen Regel weiter haelt (Alarm 187, KO 2 ATR unter Bezugstief, max. 126 T). In ATR, je Wert gemittelt (mind. 20 Tage), Median ueber die Werte, 2019-22 / ab 23. In Klammern: Werte, bei denen es in BEIDEN Zeitraeumen negativ war.

| Gelaufen | schon abgegeben | Halten bringt noch |
|---|---|---|
| frueh | 10-25 % | 0.5 / 0.3 ATR (0/0) |
| frueh | 25-40 % | 0.7 / - ATR (0/2) |
| frueh | 40-100 % | 0.8 / -0.0 ATR (0/1) |
| frueh | unter Einstieg | 0.7 / -1.5 ATR (1/6) |
| mittel | 0-10 % | 0.2 / 0.4 ATR (16/194) |
| mittel | 10-25 % | 0.3 / 0.3 ATR (22/241) |
| mittel | 25-40 % | 0.4 / 0.2 ATR (15/216) |
| mittel | 40-100 % | 0.4 / 0.4 ATR (17/264) |
| mittel | unter Einstieg | 0.4 / 0.4 ATR (31/258) |
| weit | 0-10 % | 0.1 / 0.3 ATR (23/213) |
| weit | 10-25 % | 0.3 / 0.3 ATR (23/232) |
| weit | 25-40 % | 0.4 / 0.4 ATR (20/191) |
| weit | 40-100 % | 0.5 / 0.6 ATR (24/256) |
| weit | unter Einstieg | 0.5 / 0.2 ATR (33/223) |
| sehr weit | 0-10 % | 0.0 / 0.1 ATR (52/241) |
| sehr weit | 10-25 % | 0.2 / 0.3 ATR (27/190) |
| sehr weit | 25-40 % | 0.3 / 0.5 ATR (24/134) |
| sehr weit | 40-100 % | 0.4 / 0.7 ATR (27/216) |
| sehr weit | unter Einstieg | 0.2 / 0.3 ATR (30/145) |
