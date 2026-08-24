# Quellencheck - Ersatz fuer die Aggregat-Werte

_Erstellt 2026-08-24 17:55 UTC. Einmalige Diagnose, kein Teil des taeglichen Laufs._

## Kurzfassung

- **Test A:** 2 von 4 Werten liefern ueber die US-Notierung ueberhaupt benannte Ratings juenger als 120 Tage. Davon **1 mit mindestens 3 Banken** - nur die sind ein brauchbarer Ersatz.
- **Test B:** 0 Werte haben ueber alle vier Monatsfenster identische Zahlen (Aggregat eingefroren), 4 bewegen sich.

Lesehilfe: Ein Wert taugt als Ersatz, wenn Test A genug Banken liefert UND der Firmenname der US-Notierung tatsaechlich zur deutschen Aktie passt. Der Name kommt ungeprueft von Yahoo - bitte durchsehen, bevor etwas davon in den Screener wandert.

## Test A - benannte Ratings ueber die US-Notierung

| Ticker | Name | bisher | US-Papier | Name laut Yahoo | Banken frisch | Zeilen gesamt | juengstes Rating | Beispiele |
|---|---|---|---|---|---|---|---|---|
| CCEP | Coca-Cola Europacific Partners | Einzelratings | CCEP.AS | Coca-Cola Europacific Partners  | **4** | 161 | 2026-08-13 | 2026-08-13 UBS: Neutral<br>2026-08-06 Barclays: Overweight<br>2026-08-05 Evercore ISI Group: Outperform<br>2026-08-03 Wells Fargo: Overweight |
| AZN | AstraZeneca PLC | Aggregat | AZN.L | ASTRAZENECA PLC ORD SHS $0.25 | **1** | 1 | 2026-08-24 | 2026-08-24 CICC: Outperform |
| ASML | ASML Holding N.V. - New York Re | Einzelratings | ASML.AS | ASML HOLDING | **0** | 0 | - | - |
| NXPI | NXP Semiconductors N.V. | Einzelratings | NXPI.AS | ? | **0** | 0 | - | - |

## Test B - bewegt sich Yahoos Aggregat?

_Kaufen/Halten/Verkaufen je Monatsfenster. `0m` ist der laufende Monat. Identische Zahlen ueber alle Fenster heissen: die Zaehlung wird nicht fortgeschrieben und ist als Kaufkriterium wertlos._

| Ticker | Name | 0m | -1m | -2m | -3m | Urteil |
|---|---|---|---|---|---|---|
| AZN | AstraZeneca PLC | 9/1/0 | 8/2/0 | 9/1/0 | 9/1/0 | bewegt sich |
| ASML | ASML Holding N.V. - New York Re | 39/4/1 | 40/3/1 | 39/3/2 | 38/5/1 | bewegt sich |
| CCEP | Coca-Cola Europacific Partners | 8/4/0 | 8/4/0 | 8/4/0 | 7/4/0 | bewegt sich |
| NXPI | NXP Semiconductors N.V. | 22/7/1 | 23/6/1 | 23/6/1 | 25/6/1 | bewegt sich |

## Fertige Zeilen fuer analysten_extern.csv

_Nur Werte aus Test A mit mindestens 3 frischen Banken. Kopiervorlage - erst uebernehmen, wenn der Firmenname oben stimmt. Die Kursziele fehlen bewusst: sie stuenden in USD und wuerden gegen die Euro-Kurse gerechnet Unsinn ergeben._

```
ticker,bank,datum,einstufung,kursziel,quelle
CCEP,UBS,2026-08-13,Neutral,,Yahoo/CCEP.AS
CCEP,Barclays,2026-08-06,Overweight,,Yahoo/CCEP.AS
CCEP,Evercore ISI Group,2026-08-05,Outperform,,Yahoo/CCEP.AS
CCEP,Wells Fargo,2026-08-03,Overweight,,Yahoo/CCEP.AS
```

_Achtung: oben stehen nur die vier juengsten Banken je Wert. Wenn ein Wert als Ersatz taugt, gehoert die Abfrage in den Screener statt in eine Handdatei - dann kommen alle Banken automatisch mit._
