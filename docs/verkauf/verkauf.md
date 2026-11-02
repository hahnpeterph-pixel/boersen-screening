# Verkaufs-Check - Stufe 1 (Stand 2026-11-02 17:55 UTC)

Parallellauf. Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss. Entscheidungspunkt = Hoch seit Kauf hoechstens 3 Tage alt, Anstieg mind. 1 ATR. Ganz weg = Kurs faellt auf den Einstieg, bevor ein neues Hoch kommt; halb weg = die Haelfte des Anstiegs geht verloren, bevor ein neues Hoch kommt.

Werte: 270 · Kaeufe: 90735 · Entscheidungspunkte: 1547314

## Wie weit gelaufen - Rueckfallquote je Wert (Median ueber die Werte)

| Lauf-Stand | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| frueh | 50 % / 49 % | 71 % / 73 % |
| mittel | 42 % / 43 % | 65 % / 65 % |
| weit | 28 % / 30 % | 49 % / 52 % |
| sehr weit | 12 % / 12 % | 27 % / 27 % |

## Schon weit gelaufen: Rueckfall nach bereits abgegebenem Anteil

| Schon abgegeben | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |
|---|---|---|
| 0-10 % | 5 % / 4 % | 11 % / 10 % |
| 10-25 % | 14 % / 13 % | 31 % / 30 % |
| 25-40 % | 28 % / 27 % | 60 % / 60 % |
| ueber 40 % | 59 % / 60 % | 92 % / 93 % |

## Merkmale einzeln - nur wenn schon mind. der uebliche Anstieg gelaufen ist

Werte = mind. 10 Faelle mit UND ohne Merkmal in beiden Zeitraeumen. Verglichen wird nur bei gleicher bereits abgegebener Rueckgabe (0-10 / 10-25 / 25-40 / ueber 40 % des Anstiegs). Plus = Rueckfall in beiden Zeitraeumen mind. 8 Prozentpunkte HAEUFIGER mit Merkmal (spricht fuer Verkauf), Minus = seltener. Diff = Median ueber die Werte (bis 2022 / ab 2023).

### Gewinn ganz weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 264 | 5 | 1 | 1.2 / 0.3 |
| Rot + Volumen | 264 | 10 | 1 | 1.7 / 1.2 |
| Alarm 187 | 264 | 0 | 0 | -1.3 / -2.5 |
| Hoch heute | 264 | 0 | 0 | -0.2 / 0.6 |
| RSI hoch | 264 | 0 | 4 | -3.1 / -3.0 |
| Weit ueber EMA50 | 262 | 0 | 4 | -3.6 / -3.5 |
| Schneller Anstieg | 264 | 0 | 0 | 0.3 / -0.5 |
| Kauf mit 2+ Punkten | 263 | 0 | 0 | -0.2 / -0.4 |

### halber Gewinn weg

| Merkmal | Werte | Plus | Minus | Diff |
|---|---|---|---|---|
| Rote Kerze | 264 | 1 | 0 | 1.6 / 1.4 |
| Rot + Volumen | 264 | 7 | 2 | 1.9 / 1.9 |
| Alarm 187 | 264 | 0 | 0 | -0.5 / -0.3 |
| Hoch heute | 264 | 0 | 4 | -1.5 / -0.5 |
| RSI hoch | 264 | 2 | 17 | -5.0 / -6.2 |
| Weit ueber EMA50 | 262 | 0 | 22 | -4.7 / -5.8 |
| Schneller Anstieg | 264 | 1 | 0 | 0.3 / 0.6 |
| Kauf mit 2+ Punkten | 263 | 0 | 0 | -0.1 / -0.6 |

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
| halten | 49 / 50 % | 69 | 14 % | 161 / 264 |
| ruecksetzer_t | 9 / 8 % | 16 | 11 % | 28 / 264 |
| alarm187 | 18 / 19 % | 19 | 20 % | - |
| nachlauf25 | 12 / 16 % | 15 | 19 % | 29 / 264 |
| nachlauf33 | 12 / 17 % | 16 | 19 % | 42 / 264 |
| nachlauf40 | 14 / 17 % | 18 | 17 % | 51 / 264 |
| nachlauf33_frueh | 7 / 10 % | 8 | 21 % | 17 / 264 |

### Puffer 3 ATR

| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |
|---|---|---|---|---|
| halten | 45 / 53 % | 84 | 12 % | 169 / 264 |
| ruecksetzer_t | 7 / 6 % | 16 | 9 % | 22 / 264 |
| alarm187 | 18 / 21 % | 24 | 16 % | - |
| nachlauf25 | 12 / 16 % | 18 | 15 % | 21 / 264 |
| nachlauf33 | 13 / 16 % | 20 | 15 % | 32 / 264 |
| nachlauf40 | 13 / 15 % | 22 | 14 % | 37 / 264 |
| nachlauf33_frueh | 7 / 9 % | 10 | 16 % | 10 / 264 |

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
| frueh | 0-10 % | -0.2 / - ATR (0/1) |
| frueh | 10-25 % | 0.6 / 0.3 ATR (0/0) |
| frueh | 25-40 % | 0.9 / - ATR (0/4) |
| frueh | 40-100 % | 0.6 / 1.5 ATR (0/3) |
| frueh | unter Einstieg | 0.2 / 1.0 ATR (0/6) |
| mittel | 0-10 % | 0.2 / 0.3 ATR (15/195) |
| mittel | 10-25 % | 0.3 / 0.3 ATR (20/245) |
| mittel | 25-40 % | 0.4 / 0.2 ATR (15/220) |
| mittel | 40-100 % | 0.5 / 0.3 ATR (19/264) |
| mittel | unter Einstieg | 0.5 / 0.3 ATR (35/254) |
| weit | 0-10 % | 0.1 / 0.3 ATR (27/212) |
| weit | 10-25 % | 0.3 / 0.3 ATR (24/237) |
| weit | 25-40 % | 0.4 / 0.4 ATR (19/198) |
| weit | 40-100 % | 0.5 / 0.5 ATR (26/258) |
| weit | unter Einstieg | 0.5 / 0.4 ATR (32/227) |
| sehr weit | 0-10 % | 0.1 / 0.1 ATR (47/239) |
| sehr weit | 10-25 % | 0.2 / 0.3 ATR (26/193) |
| sehr weit | 25-40 % | 0.4 / 0.5 ATR (18/136) |
| sehr weit | 40-100 % | 0.4 / 0.8 ATR (26/216) |
| sehr weit | unter Einstieg | 0.2 / 0.5 ATR (30/145) |
