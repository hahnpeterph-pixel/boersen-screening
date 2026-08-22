# Historie - Halteraten und Einstieg

_Erstellt 2026-08-22 17:59 UTC. 3 Jahre, 170 Werte, 8961 auswertbare Tiefs aus abgeschlossenen Sequenzen (12 aus laufenden ausgeschlossen)._

_Tiefs nach der Umkehr-Regel aus `tiefs_regel.py`. Eine Abwaertsserie zaehlt nur neue Tiefststaende; sie endet erst, wenn ein hoeheres Tief kommt UND danach ein hoeheres Hoch ueber dem Hoch vor dem tiefsten Tief. HAELT heisst: der Puffer wurde ab dem Bestaetigungstag drei Monate lang nicht unterschritten. ANSTIEG ist der Median des hoechsten Punktes nach dem Einstieg, in ATR - die Ertragsseite._

## Grundrate ueber alles

| Puffer | haelt 3 Monate | nie wieder durchbrochen | Median Tage bis Bruch |
|---|---|---|---|
| 0.5 ATR | 30% | 16% | 11 |
| 1.0 ATR | 36% | 20% | 16 |
| 1.5 ATR | 43% | 24% | 22 |
| 2.0 ATR | 49% | 28% | 29 |
| 2.5 ATR | 55% | 31% | 36 |
| 3.0 ATR | 60% | 35% | 44 |

_Gemessen ab dem Bestaetigungstag bis zum Ende der Historie, ohne festes Fenster - der KO kann schlagen, solange die Position offen ist. HAELT 3 MONATE heisst: der Puffer wurde in den ersten 63 Handelstagen nie unterschritten. NIE WIEDER DURCHBROCHEN heisst: auch danach nicht. MEDIAN TAGE BIS BRUCH zaehlt nur die Faelle, die gebrochen wurden. Tiefs mit weniger als 63 Handelstagen Resthistorie sind ausgeschlossen, sonst wuerden sie als 'haelt' gezaehlt, ohne die Gelegenheit gehabt zu haben. Alle folgenden Tabellen nennen den Anteil, der drei Monate haelt._

## Nach Position in der Serie

_Die Leitfrage: haelt das erste Tief seltener als ein spaeteres? y ist die werttypische Anzahl Tiefs je Sequenz dieses Wertes._

### Absolut - das wievielte Tief der Serie

| Position | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| Tief 1 | 3837 | 27% | 34% | 41% | 47% | 54% | 58% | 16.87 ATR |
| Tief 2 | 2181 | 31% | 37% | 43% | 49% | 56% | 61% | 16.06 ATR |
| Tief 3 | 1270 | 31% | 37% | 44% | 51% | 56% | 61% | 15.71 ATR |
| Tief 4 | 735 | 31% | 38% | 43% | 50% | 55% | 61% | 14.19 ATR |
| Tief 5 | 405 | 32% | 40% | 45% | 52% | 57% | 61% | 12.86 ATR |
| Tief 6+ | 533 | 34% | 42% | 47% | 53% | 58% | 63% | 12.90 ATR |

_Darunter dieselbe Frage relativ zur werttypischen Anzahl y dieses Wertes._

### Relativ zur werttypischen Anzahl

| Position | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 1 (erstes) | 3837 | 27% | 34% | 41% | 47% | 54% | 58% | 16.87 ATR |
| 2 bis y | 1857 | 30% | 36% | 42% | 47% | 54% | 59% | 14.86 ATR |
| y+1 | 1405 | 30% | 37% | 45% | 51% | 57% | 62% | 16.73 ATR |
| ueber y+1 | 1862 | 34% | 41% | 47% | 53% | 58% | 63% | 14.49 ATR |

_Nicht ausgewertet wird, ob es das LETZTE Tief der Serie war: eine Serie endet per Definition mit ihrem letzten Tief, also haelt dieses immer. Die Zahl waere 100 Prozent und sagte nichts - im Moment der Kaufentscheidung ist ohnehin nicht erkennbar, ob ein Tief das letzte sein wird._

## Nach Abstand beim Einstieg

_Wie weit hatte sich der Kurs am Bestaetigungstag schon vom Tief geloest? Die These: ein Tief, von dem der Kurs sich geloest hat, ist bestaetigt - ein frisches ist ein Kandidat._

### Abstand in ATR

| Abstand | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| bis 0,4 | 559 | 14% | 21% | 29% | 34% | 41% | 47% | 14.21 ATR |
| 0,4 bis 0,8 | 1847 | 21% | 28% | 36% | 43% | 50% | 55% | 15.20 ATR |
| 0,8 bis 1,2 | 2472 | 27% | 33% | 40% | 48% | 54% | 58% | 16.35 ATR |
| ueber 1,2 | 4083 | 37% | 43% | 50% | 55% | 60% | 65% | 15.99 ATR |

## Nach RSI, relativ zum eigenen Median

_Korrelation zwischen Position in der Serie und relativem RSI: -0.55. Ist sie hoch, sagt der RSI nichts, was die Position nicht schon sagt._

### RSI-Abstand zum eigenen Kauf-Median

| RSI-Lage | Faelle | 0.5 ATR | 1.0 ATR | 1.5 ATR | 2.0 ATR | 2.5 ATR | 3.0 ATR | Anstieg |
|---|---|---|---|---|---|---|---|---|
| 8+ unter Median | 2582 | 36% | 43% | 50% | 56% | 62% | 67% | 15.90 ATR |
| 3 bis 8 unter | 1201 | 29% | 37% | 44% | 51% | 57% | 63% | 15.79 ATR |
| um den Median | 1519 | 27% | 33% | 41% | 46% | 51% | 56% | 15.03 ATR |
| ueber Median | 3659 | 26% | 32% | 39% | 45% | 51% | 56% | 16.24 ATR |

## Nach einem Knock-out

_Haelt das naechste Tief desselben Wertes besser als der Durchschnitt? Nur das entscheidet, ob ein KO eine Gelegenheit eroeffnet._

- Puffer 1.0 ATR: 5638 ausgeknockte Faelle, 5255 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 23% gegen 36% im Durchschnitt, Anstieg 13.10 ATR.
- Puffer 2.0 ATR: 4505 ausgeknockte Faelle, 4210 mit einem Folgetief binnen 20 Handelstagen. Davon hielten 25% gegen 49% im Durchschnitt, Anstieg 11.76 ATR.

_Der Verlust aus dem ersten Trade zaehlt voll, unabhaengig davon, ob ein zweiter folgt. Liegt die Folgequote nicht deutlich ueber der Grundrate, rechtfertigt ein moeglicher Wiedereinstieg keinen engeren Puffer._

## Je Wert

_Der eigene Grundwert des Papiers und der Unterschied zwischen erstem und spaeterem Tief, jeweils bei 2 ATR Puffer. Die vollstaendige Aufschluesselung nach Position und Puffer steht in `halteraten_werte.csv`. Fallzahlen unter 5 werden nicht ausgewiesen._

| Wert | Tiefs | alle | Tief 1 | Tief 2 | Tief 3 | Tief 4+ | Anstieg |
|---|---|---|---|---|---|---|---|
| AAPL | 51 | 59% | 50% | 54% | 57% | 100% | 23.5 ATR |
| ABNB | 55 | 45% | 43% | 44% | 50% | - | 13.3 ATR |
| ADBE | 58 | 14% | 5% | 23% | 11% | 20% | 3.0 ATR |
| ADI | 63 | 59% | 52% | 56% | 67% | 78% | 39.6 ATR |
| ADP | 58 | 47% | 50% | 57% | 62% | 21% | 11.3 ATR |
| ADS.DE | 60 | 43% | 33% | 27% | 60% | 64% | 7.2 ATR |
| ADSK | 51 | 39% | 32% | 54% | 38% | 38% | 6.1 ATR |
| AEP | 60 | 62% | 42% | 69% | 91% | 71% | 31.2 ATR |
| AIR.DE | 58 | 53% | 54% | 50% | 50% | 58% | 21.5 ATR |
| ALV.DE | 61 | 62% | 46% | 71% | 70% | 100% | 37.8 ATR |
| AMAT | 68 | 59% | 53% | 70% | 50% | 67% | 87.2 ATR |
| AMD | 61 | 52% | 64% | 64% | 50% | 29% | 67.2 ATR |
| AMGN | 52 | 52% | 30% | 36% | 50% | 93% | 23.7 ATR |
| AMZN | 66 | 55% | 52% | 69% | 58% | 36% | 15.6 ATR |
| APP | 51 | 65% | 52% | 75% | 80% | 100% | 21.3 ATR |
| ARM | 57 | 54% | 63% | 43% | 67% | 29% | 45.0 ATR |
| ASML | 68 | 63% | 58% | 59% | 78% | 83% | 46.2 ATR |
| AVGO | 64 | 69% | 61% | 67% | 82% | 100% | 37.7 ATR |
| AXON | 50 | 64% | 58% | 77% | 40% | 75% | 55.1 ATR |
| AXP | 61 | 61% | 53% | 81% | 67% | 44% | 13.9 ATR |
| AZN | 67 | 45% | 47% | 33% | 36% | 67% | 25.4 ATR |
| BA | 67 | 27% | 31% | 20% | 0% | 37% | 12.3 ATR |
| BAS.DE | 63 | 54% | 54% | 62% | 44% | 53% | 15.3 ATR |
| BAYN.DE | 55 | 36% | 36% | 33% | 33% | 40% | 31.1 ATR |
| BEI.DE | 45 | 42% | 28% | 45% | 57% | 56% | 4.2 ATR |
| BIIB | 54 | 30% | 45% | 33% | 0% | 18% | 6.5 ATR |
| BKNG | 54 | 41% | 38% | 42% | 50% | 40% | 8.0 ATR |
| BKR | 43 | 56% | 40% | 78% | 57% | 71% | 26.8 ATR |
| BMW.DE | 62 | 35% | 48% | 31% | 40% | 22% | 7.7 ATR |
| BNR.DE | 60 | 28% | 33% | 36% | 22% | 15% | 6.3 ATR |
| BTC-USD | 47 | 68% | 73% | 73% | 62% | 50% | 11.6 ATR |
| CAT | 56 | 62% | 54% | 73% | 67% | - | 87.3 ATR |
| CBK.DE | 60 | 60% | 54% | 71% | 50% | 70% | 28.1 ATR |
| CCEP | 58 | 74% | 63% | 73% | 100% | 100% | 31.7 ATR |
| CDNS | 17 | 35% | 25% | 50% | - | - | 10.1 ATR |
| CDW | 45 | 20% | 24% | 10% | 33% | 17% | 6.0 ATR |
| CEG | 56 | 45% | 42% | 36% | 44% | 67% | 16.2 ATR |
| CHTR | 57 | 32% | 39% | 15% | 25% | 43% | 6.4 ATR |
| CL=F | 53 | 47% | 59% | 45% | 43% | 31% | 21.8 ATR |
| CMCSA | 43 | 23% | 42% | 25% | 0% | 19% | 4.7 ATR |
| CON.DE | 61 | 38% | 34% | 53% | 20% | 30% | 24.3 ATR |
| CPRT | 48 | 29% | 25% | 50% | 29% | 0% | 6.6 ATR |
| CRM | 47 | 38% | 37% | 46% | 43% | 25% | 5.2 ATR |
| CSCO | 35 | 77% | 80% | 89% | - | - | 80.2 ATR |
| CSGP | 58 | 40% | 50% | 55% | 50% | 22% | 8.0 ATR |
| CSX | 56 | 64% | 61% | 67% | 71% | 67% | 32.6 ATR |
| CTAS | 61 | 56% | 52% | 61% | 67% | 50% | 8.9 ATR |
| CTSH | 53 | 28% | 39% | 11% | 0% | 35% | 7.8 ATR |
| CVX | 45 | 38% | 33% | 38% | 43% | - | 25.3 ATR |
| DASH | 63 | 57% | 61% | 53% | 55% | 56% | 21.6 ATR |
| DB1.DE | 54 | 59% | 68% | 58% | 67% | 36% | 24.9 ATR |
| DBK.DE | 59 | 64% | 63% | 63% | 60% | 80% | 42.5 ATR |
| DDOG | 54 | 50% | 55% | 38% | 67% | 42% | 38.0 ATR |
| DHL.DE | 59 | 53% | 48% | 29% | 50% | 86% | 31.2 ATR |
| DIS | 50 | 42% | 57% | 31% | 38% | 25% | 8.1 ATR |
| DTG.DE | 59 | 56% | 46% | 60% | 57% | 67% | 16.2 ATR |
| DXCM | 42 | 40% | 44% | 25% | 60% | 38% | 7.2 ATR |
| ENR.DE | 62 | 69% | 67% | 75% | 71% | 67% | 32.0 ATR |
| EOAN.DE | 57 | 56% | 54% | 53% | 75% | 50% | 39.7 ATR |
| EXC | 46 | 63% | 56% | 45% | 57% | 100% | 21.9 ATR |
| FANG | 50 | 48% | 42% | 46% | 62% | 50% | 12.1 ATR |
| FAST | 44 | 68% | 65% | 57% | 80% | 78% | 23.7 ATR |
| FRE.DE | 49 | 59% | 64% | 55% | - | 67% | 29.2 ATR |
| FTNT | 34 | 47% | 54% | 50% | - | 56% | 60.9 ATR |
| GC=F | 40 | 85% | 78% | 92% | - | - | 87.6 ATR |
| GEHC | 44 | 41% | 33% | 56% | 33% | 43% | 4.6 ATR |
| GFS | 55 | 45% | 41% | 38% | 30% | 67% | 31.0 ATR |
| GILD | 56 | 57% | 61% | 60% | 50% | 40% | 31.6 ATR |
| GOOG | 66 | 62% | 62% | 63% | 57% | 67% | 48.2 ATR |
| GOOGL | 67 | 64% | 59% | 70% | 57% | 83% | 49.4 ATR |
| GS | 58 | 76% | 79% | 71% | - | 67% | 37.1 ATR |
| HD | 63 | 43% | 25% | 38% | 73% | 53% | 6.8 ATR |
| HEI.DE | 61 | 61% | 59% | 65% | 50% | - | 13.1 ATR |
| HEN3.DE | 44 | 43% | 32% | 25% | 57% | 100% | 11.4 ATR |
| HON | 59 | 46% | 45% | 43% | 43% | 56% | 14.5 ATR |
| IBM | 44 | 50% | 56% | 40% | 43% | 56% | 23.6 ATR |
| IDXX | 65 | 40% | 54% | 29% | 10% | 47% | 20.4 ATR |
| IFX.DE | 57 | 44% | 46% | 29% | 56% | 50% | 53.3 ATR |
| ILMN | 46 | 57% | 71% | 67% | 50% | 36% | 21.9 ATR |
| INTC | 47 | 64% | 61% | 69% | 75% | 50% | 78.2 ATR |
| INTU | 58 | 33% | 32% | 44% | 29% | 23% | 9.4 ATR |
| ISRG | 55 | 53% | 54% | 54% | 40% | 54% | 12.9 ATR |
| JNJ | 61 | 51% | 58% | 64% | 14% | 43% | 48.7 ATR |
| JPM | 57 | 61% | 57% | 67% | 71% | - | 17.7 ATR |
| KDP | 53 | 53% | 53% | 55% | 20% | 61% | 11.0 ATR |
| KHC | 48 | 35% | 18% | 33% | 14% | 67% | 5.8 ATR |
| KLAC | 66 | 55% | 45% | 62% | 78% | 40% | 93.7 ATR |
| KO | 39 | 72% | 57% | 88% | 100% | - | 38.4 ATR |
| LIN | 46 | 46% | 50% | 38% | 50% | - | 15.0 ATR |
| LRCX | 60 | 72% | 66% | 73% | 67% | 100% | 121.7 ATR |
| LULU | 56 | 29% | 35% | 33% | 14% | 21% | 5.1 ATR |
| MAR | 56 | 48% | 44% | 38% | 64% | - | 32.0 ATR |
| MBG.DE | 62 | 32% | 28% | 24% | 42% | 50% | 4.8 ATR |
| MCD | 60 | 45% | 54% | 27% | 29% | 50% | 9.9 ATR |
| MCHP | 61 | 34% | 28% | 36% | 40% | 42% | 13.4 ATR |
| MDB | 59 | 58% | 54% | 71% | 56% | 50% | 11.2 ATR |
| MDLZ | 66 | 44% | 48% | 38% | 38% | 45% | 6.0 ATR |
| MELI | 62 | 37% | 30% | 47% | 30% | 50% | 9.5 ATR |
| META | 73 | 49% | 43% | 41% | 54% | 69% | 9.2 ATR |
| MMM | 56 | 59% | 57% | 50% | 56% | 80% | 15.1 ATR |
| MNST | 54 | 59% | 60% | 54% | 50% | 70% | 36.5 ATR |
| MRK | 50 | 52% | 40% | 54% | 75% | 56% | 29.0 ATR |
| MRK.DE | 62 | 44% | 32% | 53% | 56% | 44% | 7.8 ATR |
| MRNA | 57 | 47% | 60% | 55% | 29% | 37% | 44.2 ATR |
| MRVL | 48 | 58% | 60% | 40% | 83% | - | 73.2 ATR |
| MSFT | 57 | 39% | 45% | 27% | 22% | 50% | 15.0 ATR |
| MSTR | 57 | 46% | 41% | 67% | 57% | 31% | 6.7 ATR |
| MTX.DE | 49 | 55% | 52% | 54% | 50% | 80% | 10.0 ATR |
| MU | 59 | 61% | 59% | 50% | 62% | 80% | 250.6 ATR |
| MUV2.DE | 51 | 41% | 24% | 47% | 57% | - | 11.2 ATR |
| NFLX | 63 | 41% | 31% | 53% | 50% | 40% | 20.6 ATR |
| NG=F | 57 | 60% | 38% | 56% | 75% | 92% | 21.9 ATR |
| NKE | 71 | 28% | 25% | 25% | 44% | 27% | 3.6 ATR |
| NVDA | 51 | 71% | 71% | 64% | 75% | - | 20.6 ATR |
| NXPI | 60 | 38% | 23% | 41% | 50% | 57% | 18.0 ATR |
| ODFL | 45 | 49% | 42% | 33% | 62% | 83% | 10.6 ATR |
| ON | 60 | 37% | 38% | 38% | 40% | 31% | 27.5 ATR |
| ORCL | 61 | 31% | 30% | 21% | 30% | 43% | 30.1 ATR |
| ORLY | 48 | 71% | 62% | 69% | 83% | 100% | 19.2 ATR |
| P911.DE | 64 | 38% | 41% | 36% | 40% | 35% | 3.9 ATR |
| PAH3.DE | 56 | 30% | 22% | 29% | 30% | 56% | 5.2 ATR |
| PANW | 52 | 40% | 25% | 50% | 50% | 62% | 38.9 ATR |
| PAYX | 61 | 46% | 50% | 60% | 56% | 24% | 10.6 ATR |
| PCAR | 55 | 55% | 59% | 62% | 50% | 42% | 15.6 ATR |
| PEP | 52 | 40% | 26% | 50% | 60% | 36% | 8.0 ATR |
| PG | 61 | 48% | 35% | 33% | 64% | 89% | 7.0 ATR |
| PLTR | 55 | 64% | 52% | 62% | 88% | - | 26.3 ATR |
| PYPL | 64 | 42% | 39% | 44% | 33% | 50% | 10.2 ATR |
| QCOM | 54 | 48% | 41% | 45% | 50% | 60% | 25.4 ATR |
| QIA.DE | 63 | 41% | 36% | 21% | 30% | 71% | 11.1 ATR |
| REGN | 47 | 43% | 48% | 45% | 33% | 33% | 8.2 ATR |
| RHM.DE | 37 | 65% | 62% | 33% | - | 100% | 70.4 ATR |
| ROP | 48 | 46% | 36% | 50% | 60% | 60% | 6.2 ATR |
| ROST | 66 | 68% | 65% | 67% | 70% | 80% | 40.5 ATR |
| RWE.DE | 51 | 57% | 59% | 62% | 43% | 56% | 40.7 ATR |
| SAP.DE | 59 | 47% | 50% | 54% | 29% | 46% | 16.7 ATR |
| SBUX | 52 | 44% | 36% | 50% | 43% | 56% | 10.8 ATR |
| SHL.DE | 53 | 45% | 40% | 30% | 29% | 69% | 5.5 ATR |
| SHW | 69 | 33% | 26% | 25% | 46% | 41% | 6.0 ATR |
| SI=F | 50 | 60% | 57% | 60% | 67% | - | 141.5 ATR |
| SIE.DE | 60 | 55% | 50% | 44% | 60% | 100% | 16.2 ATR |
| SNPS | 23 | 30% | 0% | 33% | - | 57% | 5.7 ATR |
| SPGI | 52 | 44% | 35% | 43% | 60% | 60% | 8.5 ATR |
| SRT3.DE | 54 | 37% | 37% | 25% | 50% | 38% | 4.2 ATR |
| SY1.DE | 59 | 41% | 43% | 50% | 62% | 19% | 8.6 ATR |
| TEAM | 65 | 29% | 28% | 23% | 27% | 35% | 9.8 ATR |
| TMUS | 48 | 52% | 52% | 67% | 50% | 29% | 7.7 ATR |
| TRV | 55 | 56% | 38% | 54% | 100% | - | 30.9 ATR |
| TSLA | 57 | 51% | 46% | 53% | 50% | 62% | 12.0 ATR |
| TTD | 60 | 28% | 28% | 33% | 12% | 33% | 6.9 ATR |
| TTWO | 66 | 47% | 35% | 20% | 69% | 83% | 21.2 ATR |
| TXN | 62 | 50% | 33% | 62% | 67% | 54% | 31.1 ATR |
| UNH | 47 | 34% | 43% | 27% | 0% | 38% | 11.7 ATR |
| V | 42 | 62% | 60% | 64% | 50% | 80% | 22.7 ATR |
| VOW3.DE | 62 | 42% | 26% | 27% | 50% | 79% | 5.9 ATR |
| VRSK | 42 | 38% | 27% | 50% | - | 47% | 6.8 ATR |
| VRTX | 49 | 47% | 45% | 25% | 14% | 100% | 9.7 ATR |
| VZ | 47 | 64% | 62% | 50% | 75% | 83% | 19.3 ATR |
| WBD | 51 | 39% | 45% | 23% | 38% | 50% | 40.4 ATR |
| WDAY | 62 | 34% | 38% | 29% | 22% | 39% | 4.6 ATR |
| WMT | 53 | 79% | 71% | 87% | 100% | - | 25.8 ATR |
| XEL | 50 | 72% | 59% | 80% | 100% | - | 13.3 ATR |
| ZAL.DE | 55 | 36% | 25% | 36% | 38% | 47% | 14.3 ATR |
| ZS | 4 | 50% | - | - | - | - | 6.5 ATR |

---

_Keine Anlageberatung. Historische Kursverlaeufe, gemessen mit der Regel aus `tiefs_regel.py`._