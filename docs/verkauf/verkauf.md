# Verkaufs-Check - Stufe 1 (Stand 2026-09-27 07:39 UTC)

Parallellauf. Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss. Entscheidungspunkt = Hoch seit Kauf hoechstens 3 Tage alt, Anstieg mind. 1 ATR. Ganz weg = Kurs faellt auf den Einstieg, bevor ein neues Hoch kommt; halb weg = die Haelfte des Anstiegs geht verloren, bevor ein neues Hoch kommt.

Werte: 271 · Kaeufe: 93271 · Entscheidungspunkte: 1586979

## Wie weit gelaufen - Rueckfallquote je Wert (Median ueber die Werte)

| Lauf-Stand | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| frueh | 51 % / 52 % | 73 % / 75 % |
| mittel | 42 % / 43 % | 65 % / 64 % |
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
| Rote Kerze | 265 | 5 | 1 | 0.7 / -0.1 |
| Rot + Volumen | 265 | 9 | 1 | 1.7 / 0.4 |
| Alarm 187 | 265 | 0 | 0 | -1.3 / -2.6 |
| Hoch heute | 265 | 0 | 0 | -0.3 / 0.5 |
| RSI hoch | 265 | 0 | 3 | -2.9 / -3.2 |
| Weit ueber EMA50 | 263 | 0 | 4 | -3.7 / -3.9 |
| Schneller Anstieg | 265 | 0 | 0 | 0.3 / -0.3 |
| Kauf mit 2+ Punkten | 264 | 0 | 0 | -0.2 / -0.2 |

### halber Gewinn weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 265 | 1 | 1 | 1.2 / 1.4 |
| Rot + Volumen | 265 | 6 | 1 | 1.8 / 1.2 |
| Alarm 187 | 265 | 0 | 2 | -0.6 / -0.6 |
| Hoch heute | 265 | 0 | 2 | -1.5 / -0.7 |
| RSI hoch | 265 | 2 | 18 | -5.1 / -5.5 |
| Weit ueber EMA50 | 263 | 0 | 27 | -4.9 / -6.2 |
| Schneller Anstieg | 265 | 2 | 0 | 0.3 / 0.9 |
| Kauf mit 2+ Punkten | 264 | 0 | 0 | -0.2 / -1.0 |

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
| halten | 46 / 49 % | 69 | 14 % | 157 / 265 |
| ruecksetzer_t | 10 / 8 % | 16 | 12 % | 30 / 265 |
| alarm187 | 17 / 19 % | 18 | 19 % | - |
| nachlauf25 | 13 / 15 % | 15 | 19 % | 32 / 265 |
| nachlauf33 | 13 / 16 % | 16 | 19 % | 46 / 265 |
| nachlauf40 | 15 / 17 % | 18 | 18 % | 55 / 265 |
| nachlauf33_frueh | 8 / 9 % | 8 | 21 % | 17 / 265 |

### Puffer 3 ATR

| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |
|---|---|---|---|---|
| halten | 44 / 54 % | 83 | 11 % | 168 / 265 |
| ruecksetzer_t | 7 / 7 % | 16 | 9 % | 22 / 265 |
| alarm187 | 17 / 19 % | 24 | 15 % | - |
| nachlauf25 | 12 / 15 % | 18 | 15 % | 24 / 265 |
| nachlauf33 | 13 / 15 % | 19 | 15 % | 34 / 265 |
| nachlauf40 | 13 / 17 % | 21 | 14 % | 37 / 265 |
| nachlauf33_frueh | 8 / 9 % | 10 | 16 % | 12 / 265 |

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
| frueh | 25-40 % | 0.6 / - ATR (0/2) |
| frueh | 40-100 % | 0.5 / -0.0 ATR (0/1) |
| frueh | unter Einstieg | 0.6 / -1.4 ATR (1/7) |
| mittel | 0-10 % | 0.2 / 0.3 ATR (16/189) |
| mittel | 10-25 % | 0.3 / 0.3 ATR (22/239) |
| mittel | 25-40 % | 0.4 / 0.3 ATR (13/215) |
| mittel | 40-100 % | 0.4 / 0.4 ATR (18/264) |
| mittel | unter Einstieg | 0.4 / 0.4 ATR (30/258) |
| weit | 0-10 % | 0.1 / 0.3 ATR (23/211) |
| weit | 10-25 % | 0.3 / 0.3 ATR (23/233) |
| weit | 25-40 % | 0.4 / 0.3 ATR (21/193) |
| weit | 40-100 % | 0.5 / 0.5 ATR (23/255) |
| weit | unter Einstieg | 0.5 / 0.2 ATR (32/220) |
| sehr weit | 0-10 % | 0.0 / 0.1 ATR (52/241) |
| sehr weit | 10-25 % | 0.2 / 0.2 ATR (27/186) |
| sehr weit | 25-40 % | 0.3 / 0.5 ATR (25/133) |
| sehr weit | 40-100 % | 0.4 / 0.7 ATR (28/215) |
| sehr weit | unter Einstieg | 0.2 / 0.3 ATR (29/142) |
