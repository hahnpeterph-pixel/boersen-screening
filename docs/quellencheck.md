# Quellencheck - Ersatz fuer die Aggregat-Werte

_Erstellt 2026-08-30 10:55 UTC. Einmalige Diagnose, kein Teil des taeglichen Laufs._

## Kurzfassung

- **Test A:** 1 von 41 Werten liefern ueber die US-Notierung ueberhaupt benannte Ratings juenger als 120 Tage. Davon **1 mit mindestens 3 Banken** - nur die sind ein brauchbarer Ersatz.
- **Test B:** 5 Werte haben ueber alle vier Monatsfenster identische Zahlen (Aggregat eingefroren), 35 bewegen sich.

Lesehilfe: Ein Wert taugt als Ersatz, wenn Test A genug Banken liefert UND der Firmenname der US-Notierung tatsaechlich zur deutschen Aktie passt. Der Name kommt ungeprueft von Yahoo - bitte durchsehen, bevor etwas davon in den Screener wandert.

## Test A - benannte Ratings ueber die US-Notierung

| Ticker | Name | bisher | US-Papier | Name laut Yahoo | Banken frisch | Zeilen gesamt | juengstes Rating | Beispiele |
|---|---|---|---|---|---|---|---|---|
| SAP.DE | SAP SE | Aggregat | SAP | SAP  SE | **3** | 164 | 2026-07-27 | 2026-07-27 Barclays: Overweight<br>2026-07-24 BMO Capital: Outperform<br>2026-07-17 TD Cowen: Buy |
| ADS.DE | adidas AG | Aggregat | ADDYY | adidas AG | **0** | 11 | 2023-06-12 | - |
| AIR.DE | Airbus SE | keine | EADSY | Airbus SE | **0** | 8 | 2021-09-29 | - |
| ALV.DE | Allianz SE v | Aggregat | ALIZY | Allianz SE | **0** | 2 | 2021-10-01 | - |
| BAS.DE | BASF SE | Aggregat | BASFY | BASF SE | **0** | 2 | 2020-12-14 | - |
| BAYN.DE | Bayer AG | Aggregat | BAYRY | Bayer A.G. | **0** | 4 | 2020-10-01 | - |
| BEI.DE | BEIERSDORF AG | Aggregat | BDRFY | Beiersdorf  AG | **0** | 2 | 2021-09-28 | - |
| BMW.DE | BAYERISCHE MOTOREN WERKE AG | Aggregat | BMWYY | ? | **0** | 0 | - | - |
| BNR.DE | Brenntag SE | Aggregat | BNTGY | Brenntag SE | **0** | 0 | - | - |
| CAT | Caterpillar, Inc. | Aggregat | - | - | - | - | - | bereits US-notiert |
| CBK.DE | Commerzbank AG | Aggregat | CRZBY | Commerzbank AG | **0** | 1 | 2021-07-27 | - |
| CON.DE | CONTINENTAL AG | Aggregat | CTTAY | Continental AG | **0** | 5 | 2021-03-03 | - |
| DB1.DE | DEUTSCHE BOERSE AG | Aggregat | DBOEY | Deutsche Boerse AG | **0** | 0 | - | - |
| DBK.DE | DEUTSCHE BANK AG | Aggregat | DB | Deutsche Bank AG | **0** | 79 | 2026-04-20 | - |
| DHL.DE | DEUTSCHE POST AG | Aggregat | DHLGY | Deutsche Post AG | **0** | 0 | - | - |
| DTE.DE | DEUTSCHE TELEKOM AG | Aggregat | DTEGY | Deutsche Telekom AG | **0** | 4 | 2021-09-08 | - |
| DTG.DE | Daimler Truck Holding AG | Aggregat | DTRUY | DAIMLER TRUCK HLDG AG | **0** | 0 | - | - |
| ENR.DE | Siemens Energy AG | Aggregat | SMNEY | ? | **0** | 0 | - | - |
| EOAN.DE | E.ON SE | Aggregat | EONGY | E.ON SE | **0** | 1 | 2021-07-15 | - |
| FANG | Diamondback Energy, Inc. | Aggregat | - | - | - | - | - | bereits US-notiert |
| FRE.DE | Fresenius SE & Co. KGaA | Aggregat | FSNUY | Fresenius SE & Co. KGaA | **0** | 1 | 2023-01-03 | - |
| HEI.DE | Heidelberg Materials AG | Aggregat | HDELY | ? | **0** | 0 | - | - |
| HEN3.DE | Henkel AG & Co. KGaA | Aggregat | HENKY | Henkel AG & Co. KGAA | **0** | 3 | 2021-09-09 | - |
| HNR1.DE | HANNOVER RUECK SE NA O.N. | Aggregat | HVRRY | Hannover Re | **0** | 0 | - | - |
| IFX.DE | INFINEON TECHNOLOGIES AG | Aggregat | IFNNY | Infineon Technologies AG | **0** | 6 | 2021-08-04 | - |
| MBG.DE | Mercedes-Benz Group AG | Aggregat | MBGYY | Mercedes Benz Group AG | **0** | 0 | - | - |
| META | Meta Platforms, Inc. | Aggregat | - | - | - | - | - | bereits US-notiert |
| MRK.DE | MERCK KGAA | Aggregat | MKKGY | Merck KGaA | **0** | 0 | - | - |
| MTX.DE | MTU Aero Engines AG | Aggregat | MTUAY | MTU Aero Engines AG | **0** | 3 | 2021-10-06 | - |
| MUV2.DE | MUENCHENER RUECKVERS.-GES. AG | Aggregat | MURGY | Muenchener Rueckver Ges | **0** | 1 | 2021-07-19 | - |
| P911.DE | Dr. Ing. h.c. F. Porsche AG | Aggregat | DRPRY | DR ING H C F PORSCHE AG | **0** | 0 | - | - |
| PAH3.DE | Porsche Automobil Holding SE | Aggregat | POAHY | Porsche Automobile Holding SE | **0** | 0 | - | - |
| RHM.DE | RHEINMETALL AG | Aggregat | RNMBY | Rheinmetall AG | **0** | 0 | - | - |
| RWE.DE | RWE AG | Aggregat | RWEOY | RWE AG | **0** | 1 | 2023-05-12 | - |
| SHL.DE | Siemens Healthineers AG | Aggregat | SMMNY | Siemens Healthineers AG | **0** | 1 | 2021-09-08 | - |
| SIE.DE | SIEMENS AG | Aggregat | SIEGY | Siemens AG | **0** | 5 | 2021-10-15 | - |
| SRT3.DE | SARTORIUS AG | Aggregat | SUVPF | Sartorius AG | **0** | 0 | - | - |
| SY1.DE | Symrise AG | Aggregat | SYIEY | Symrise Ag | **0** | 0 | - | - |
| VNA.DE | Vonovia SE | Aggregat | VONOY | VONOVIA SE | **0** | 0 | - | - |
| VOW3.DE | VOLKSWAGEN AG | Aggregat | VWAGY | Volkswagen AG | **0** | 1 | 2021-04-22 | - |
| ZAL.DE | Zalando SE | Aggregat | ZLNDY | ZALANDO SE | **0** | 1 | 2021-10-14 | - |

## Test B - bewegt sich Yahoos Aggregat?

_Kaufen/Halten/Verkaufen je Monatsfenster. `0m` ist der laufende Monat. Identische Zahlen ueber alle Fenster heissen: die Zaehlung wird nicht fortgeschrieben und ist als Kaufkriterium wertlos._

| Ticker | Name | 0m | -1m | -2m | -3m | Urteil |
|---|---|---|---|---|---|---|
| ADS.DE | adidas AG | 22/8/0 | 23/7/0 | 23/6/0 | 22/7/0 | bewegt sich |
| AIR.DE | Airbus SE | - | - | - | - | keine Daten |
| ALV.DE | Allianz SE v | 7/7/2 | 8/7/2 | 9/7/2 | 9/7/2 | bewegt sich |
| BAS.DE | BASF SE | 10/5/5 | 12/4/5 | 11/5/5 | 10/6/5 | bewegt sich |
| BAYN.DE | Bayer AG | 13/4/1 | 14/3/1 | 14/4/0 | 14/5/0 | bewegt sich |
| BEI.DE | BEIERSDORF AG | 7/10/3 | 7/11/2 | 7/11/2 | 8/10/2 | bewegt sich |
| BMW.DE | BAYERISCHE MOTOREN WERKE AG | 10/9/3 | 10/9/3 | 9/11/3 | 10/9/4 | bewegt sich |
| BNR.DE | Brenntag SE | 2/10/3 | 2/10/2 | 2/10/2 | 3/9/2 | bewegt sich |
| CAT | Caterpillar, Inc. | 14/12/2 | 14/12/2 | 15/11/2 | 15/11/2 | bewegt sich |
| CBK.DE | Commerzbank AG | 7/5/1 | 7/5/1 | 7/5/1 | 7/5/1 | EINGEFROREN (alle Fenster gleich) |
| CON.DE | CONTINENTAL AG | 7/6/0 | 6/7/0 | 10/5/0 | 10/5/0 | bewegt sich |
| DB1.DE | DEUTSCHE BOERSE AG | 8/4/0 | 8/4/0 | 8/4/0 | 8/4/0 | EINGEFROREN (alle Fenster gleich) |
| DBK.DE | DEUTSCHE BANK AG | 8/10/0 | 7/11/0 | 6/10/1 | 6/10/1 | bewegt sich |
| DHL.DE | DEUTSCHE POST AG | 4/13/3 | 5/12/3 | 5/12/3 | 5/12/3 | bewegt sich |
| DTE.DE | DEUTSCHE TELEKOM AG | 17/1/0 | 18/0/0 | 17/0/0 | 17/0/0 | bewegt sich |
| DTG.DE | Daimler Truck Holding AG | 12/4/2 | 12/4/2 | 11/3/3 | 10/4/3 | bewegt sich |
| ENR.DE | Siemens Energy AG | 19/4/2 | 19/3/3 | 19/4/2 | 19/4/2 | bewegt sich |
| EOAN.DE | E.ON SE | 10/6/0 | 9/8/0 | 9/8/0 | 9/9/0 | bewegt sich |
| FANG | Diamondback Energy, Inc. | 24/5/0 | 25/4/0 | 25/4/0 | 25/5/0 | bewegt sich |
| FRE.DE | Fresenius SE & Co. KGaA | 13/1/0 | 13/1/0 | 13/1/0 | 13/1/0 | EINGEFROREN (alle Fenster gleich) |
| HEI.DE | Heidelberg Materials AG | 15/2/3 | 15/2/3 | 15/2/2 | 15/2/2 | bewegt sich |
| HEN3.DE | Henkel AG & Co. KGaA | 7/8/4 | 7/8/4 | 6/9/4 | 6/9/4 | bewegt sich |
| HNR1.DE | HANNOVER RUECK SE NA O.N. | 6/8/1 | 6/7/1 | 6/8/1 | 6/8/1 | bewegt sich |
| IFX.DE | INFINEON TECHNOLOGIES AG | 19/5/0 | 19/4/1 | 19/4/1 | 20/3/1 | bewegt sich |
| MBG.DE | Mercedes-Benz Group AG | 12/9/2 | 12/9/2 | 11/11/2 | 10/12/2 | bewegt sich |
| META | Meta Platforms, Inc. | 55/7/0 | 55/7/0 | 57/6/0 | 57/7/0 | bewegt sich |
| MRK.DE | MERCK KGAA | 5/9/0 | 6/8/0 | 7/7/0 | 10/6/0 | bewegt sich |
| MTX.DE | MTU Aero Engines AG | 10/6/4 | 10/7/3 | 10/7/3 | 10/7/3 | bewegt sich |
| MUV2.DE | MUENCHENER RUECKVERS.-GES. AG | 5/9/3 | 5/9/3 | 5/9/3 | 5/9/3 | EINGEFROREN (alle Fenster gleich) |
| P911.DE | Dr. Ing. h.c. F. Porsche AG | 6/11/4 | 6/11/4 | 6/11/4 | 4/12/5 | bewegt sich |
| PAH3.DE | Porsche Automobil Holding SE | 2/6/2 | 2/6/2 | 2/6/2 | 2/6/2 | EINGEFROREN (alle Fenster gleich) |
| RHM.DE | RHEINMETALL AG | 18/2/1 | 17/3/0 | 18/2/0 | 18/3/0 | bewegt sich |
| RWE.DE | RWE AG | 15/3/0 | 15/3/0 | 14/3/0 | 14/5/0 | bewegt sich |
| SAP.DE | SAP SE | 24/4/0 | 23/4/0 | 23/4/0 | 23/4/0 | bewegt sich |
| SHL.DE | Siemens Healthineers AG | 13/7/0 | 14/6/0 | 15/5/0 | 15/5/0 | bewegt sich |
| SIE.DE | SIEMENS AG | 17/5/2 | 17/5/2 | 17/4/3 | 17/4/3 | bewegt sich |
| SRT3.DE | SARTORIUS AG | 14/5/1 | 13/6/1 | 14/5/1 | 13/6/1 | bewegt sich |
| SY1.DE | Symrise AG | 10/7/0 | 10/8/0 | 12/6/0 | 13/5/0 | bewegt sich |
| VNA.DE | Vonovia SE | 10/5/2 | 11/4/1 | 11/3/1 | 10/4/1 | bewegt sich |
| VOW3.DE | VOLKSWAGEN AG | 13/7/1 | 13/7/1 | 13/8/1 | 12/8/1 | bewegt sich |
| ZAL.DE | Zalando SE | 18/6/0 | 18/5/0 | 18/5/0 | 19/5/0 | bewegt sich |

## Fertige Zeilen fuer analysten_extern.csv

_Nur Werte aus Test A mit mindestens 3 frischen Banken. Kopiervorlage - erst uebernehmen, wenn der Firmenname oben stimmt. Die Kursziele fehlen bewusst: sie stuenden in USD und wuerden gegen die Euro-Kurse gerechnet Unsinn ergeben._

```
ticker,bank,datum,einstufung,kursziel,quelle
SAP.DE,Barclays,2026-07-27,Overweight,,Yahoo/SAP
SAP.DE,BMO Capital,2026-07-24,Outperform,,Yahoo/SAP
SAP.DE,TD Cowen,2026-07-17,Buy,,Yahoo/SAP
```

_Achtung: oben stehen nur die vier juengsten Banken je Wert. Wenn ein Wert als Ersatz taugt, gehoert die Abfrage in den Screener statt in eine Handdatei - dann kommen alle Banken automatisch mit._
