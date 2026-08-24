# Quellencheck - Ersatz fuer die Aggregat-Werte

_Erstellt 2026-08-24 17:12 UTC. Einmalige Diagnose, kein Teil des taeglichen Laufs._

## Kurzfassung

- **Test A:** 0 von 1 Werten liefern ueber die US-Notierung ueberhaupt benannte Ratings juenger als 120 Tage. Davon **0 mit mindestens 3 Banken** - nur die sind ein brauchbarer Ersatz.
- **Test B:** 0 Werte haben ueber alle vier Monatsfenster identische Zahlen (Aggregat eingefroren), 1 bewegen sich.

Lesehilfe: Ein Wert taugt als Ersatz, wenn Test A genug Banken liefert UND der Firmenname der US-Notierung tatsaechlich zur deutschen Aktie passt. Der Name kommt ungeprueft von Yahoo - bitte durchsehen, bevor etwas davon in den Screener wandert.

## Test A - benannte Ratings ueber die US-Notierung

| Ticker | Name | bisher | US-Papier | Name laut Yahoo | Banken frisch | Zeilen gesamt | juengstes Rating | Beispiele |
|---|---|---|---|---|---|---|---|---|
| AZN | AstraZeneca PLC | Aggregat | - | - | - | - | - | bereits US-notiert |

## Test B - bewegt sich Yahoos Aggregat?

_Kaufen/Halten/Verkaufen je Monatsfenster. `0m` ist der laufende Monat. Identische Zahlen ueber alle Fenster heissen: die Zaehlung wird nicht fortgeschrieben und ist als Kaufkriterium wertlos._

| Ticker | Name | 0m | -1m | -2m | -3m | Urteil |
|---|---|---|---|---|---|---|
| AZN | AstraZeneca PLC | 9/1/0 | 8/2/0 | 9/1/0 | 9/1/0 | bewegt sich |

## Fertige Zeilen fuer analysten_extern.csv

_Nur Werte aus Test A mit mindestens 3 frischen Banken. Kopiervorlage - erst uebernehmen, wenn der Firmenname oben stimmt. Die Kursziele fehlen bewusst: sie stuenden in USD und wuerden gegen die Euro-Kurse gerechnet Unsinn ergeben._

```
ticker,bank,datum,einstufung,kursziel,quelle
# kein Wert erreicht 3 frische Banken
```

_Achtung: oben stehen nur die vier juengsten Banken je Wert. Wenn ein Wert als Ersatz taugt, gehoert die Abfrage in den Screener statt in eine Handdatei - dann kommen alle Banken automatisch mit._
