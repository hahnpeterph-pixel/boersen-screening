# Verkaufs-Check - Stufe 1 (Stand 2026-09-24 19:27 UTC)

Parallellauf. Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss. Entscheidungspunkt = Hoch seit Kauf hoechstens 3 Tage alt, Anstieg mind. 1 ATR. Ganz weg = Kurs faellt auf den Einstieg, bevor ein neues Hoch kommt; halb weg = die Haelfte des Anstiegs geht verloren, bevor ein neues Hoch kommt.

Werte: 270 · Kaeufe: 35558 · Entscheidungspunkte: 600233

## Wie weit gelaufen - Rueckfallquote je Wert (Median ueber die Werte)

| Lauf-Stand | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| frueh | 50 % / 50 % | 70 % / 70 % |
| mittel | 40 % / 42 % | 64 % / 64 % |
| weit | 27 % / 30 % | 48 % / 51 % |
| sehr weit | 13 % / 12 % | 26 % / 27 % |

## Schon weit gelaufen: Rueckfall nach bereits abgegebenem Anteil

| Schon abgegeben | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| 0-10 % | 6 % / 4 % | 12 % / 10 % |
| 10-25 % | 14 % / 13 % | 32 % / 30 % |
| 25-40 % | 27 % / 28 % | 58 % / 60 % |
| ueber 40 % | 58 % / 60 % | 91 % / 92 % |

## Merkmale einzeln - nur wenn schon mind. der uebliche Anstieg gelaufen ist

Werte = mind. 10 Faelle mit UND ohne Merkmal in beiden Zeitraeumen. Verglichen wird nur bei gleicher bereits abgegebener Rueckgabe (0-10 / 10-25 / 25-40 / ueber 40 % des Anstiegs). Plus = Rueckfall in beiden Zeitraeumen mind. 8 Prozentpunkte HAEUFIGER mit Merkmal (spricht fuer Verkauf), Minus = seltener. Diff = Median ueber die Werte (bis 2022 / ab 2023).

### Gewinn ganz weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 264 | 11 | 3 | 1.3 / -0.1 |
| Rot + Volumen | 264 | 17 | 8 | 0.2 / 0.6 |
| Alarm 187 | 264 | 1 | 6 | -1.7 / -2.7 |
| Hoch heute | 264 | 0 | 0 | -0.5 / 0.5 |
| RSI hoch | 264 | 1 | 12 | -3.7 / -3.0 |
| Weit ueber EMA50 | 260 | 1 | 14 | -4.6 / -3.9 |
| Schneller Anstieg | 264 | 4 | 4 | 0.6 / -0.3 |
| Kauf mit 2+ Punkten | 262 | 2 | 0 | 0.1 / -0.5 |

### halber Gewinn weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 264 | 16 | 2 | 2.5 / 1.1 |
| Rot + Volumen | 264 | 13 | 5 | 2.1 / 1.1 |
| Alarm 187 | 264 | 9 | 4 | -0.2 / -0.7 |
| Hoch heute | 264 | 0 | 12 | -1.7 / -0.8 |
| RSI hoch | 264 | 5 | 35 | -4.5 / -5.8 |
| Weit ueber EMA50 | 260 | 2 | 40 | -4.0 / -6.9 |
| Schneller Anstieg | 264 | 7 | 1 | 0.3 / 0.8 |
| Kauf mit 2+ Punkten | 262 | 4 | 1 | -0.1 / -1.1 |

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
| halten | 37 / 49 % | 67 | 13 % | 138 / 264 |
| ruecksetzer_t | 11 / 9 % | 16 | 12 % | 46 / 264 |
| alarm187 | 16 / 20 % | 18 | 20 % | - |
| nachlauf25 | 10 / 16 % | 14 | 20 % | 51 / 264 |
| nachlauf33 | 10 / 17 % | 16 | 19 % | 53 / 264 |
| nachlauf40 | 11 / 17 % | 17 | 18 % | 59 / 264 |
| nachlauf33_frueh | 6 / 9 % | 8 | 21 % | 32 / 264 |

### Puffer 3 ATR

| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |
|---|---|---|---|---|
| halten | 37 / 54 % | 82 | 11 % | 148 / 264 |
| ruecksetzer_t | 8 / 7 % | 16 | 10 % | 36 / 264 |
| alarm187 | 14 / 19 % | 23 | 14 % | - |
| nachlauf25 | 10 / 16 % | 18 | 16 % | 43 / 264 |
| nachlauf33 | 11 / 16 % | 19 | 15 % | 50 / 264 |
| nachlauf40 | 11 / 16 % | 21 | 14 % | 56 / 264 |
| nachlauf33_frueh | 6 / 8 % | 10 | 17 % | 28 / 264 |

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
| frueh | 0-10 % | 0.9 / - ATR (0/1) |
| frueh | 10-25 % | 0.1 / 0.3 ATR (0/0) |
| frueh | 40-100 % | 1.0 / 0.3 ATR (1/3) |
| frueh | unter Einstieg | 0.7 / 0.2 ATR (0/4) |
| mittel | 0-10 % | 0.1 / 0.4 ATR (21/164) |
| mittel | 10-25 % | 0.3 / 0.3 ATR (30/231) |
| mittel | 25-40 % | 0.5 / 0.3 ATR (19/205) |
| mittel | 40-100 % | 0.5 / 0.3 ATR (38/260) |
| mittel | unter Einstieg | 0.4 / 0.4 ATR (43/252) |
| weit | 0-10 % | 0.1 / 0.2 ATR (33/193) |
| weit | 10-25 % | 0.2 / 0.3 ATR (32/203) |
| weit | 25-40 % | 0.3 / 0.3 ATR (30/152) |
| weit | 40-100 % | 0.5 / 0.5 ATR (34/253) |
| weit | unter Einstieg | 0.2 / 0.3 ATR (38/194) |
| sehr weit | 0-10 % | 0.0 / 0.1 ATR (41/205) |
| sehr weit | 10-25 % | 0.3 / 0.4 ATR (21/118) |
| sehr weit | 25-40 % | 0.8 / 0.5 ATR (9/67) |
| sehr weit | 40-100 % | 1.0 / 0.8 ATR (26/163) |
| sehr weit | unter Einstieg | -0.4 / 0.3 ATR (18/72) |
