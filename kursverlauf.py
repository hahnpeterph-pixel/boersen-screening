"""
kursverlauf.py - Schlusskurse je Wert und Handelstag, damit sich jeder Kauf
im Nachhinein messen laesst.

Wozu:
Das Orderbuch weiss, WARUM und WANN gekauft wurde (Blaetter Entscheidungen
und Transaktionen), aber nicht, was danach passiert ist. Ohne diese
Rueckkopplung bleibt jede Begruendung unbelegt - man erfaehrt nie, ob
"Chartentscheidung" besser traegt als "Bauchgefuehl", oder ob Kaeufe vor
der eigenen 16:30-Regel schlechter laufen. Genau das soll das Blatt
Rueckblick beantworten, und dafuer braucht es je Wert den Kurs an Tag 5,
21 und 63 nach dem Kauf.

Warum die Trades NICHT hier stehen:
Positionsdaten gehoeren nicht ins oeffentliche Repo (Entscheidung 58, und
das alte Repo musste am 24.08.2026 genau deswegen neu aufgesetzt werden).
Dieses Skript schreibt deshalb ausschliesslich oeffentliche Marktdaten:
Schlusskurse je Wert und Tag, ohne jeden Bezug zu einer Position. Die
Verknuepfung mit den eigenen Kaeufen passiert erst in der Excel-Mappe.

Format bewusst breit statt lang:
Eine Zeile je Wert, eine Spalte je Handelstag. Das sind rund 210 Zeilen
statt 20.000 - handlich zum Einfuegen in die Mappe, und der Nachschlag
"Kurs N Handelstage nach dem Kauf" wird zu einem simplen Spaltenversatz
statt zu einer Datumsrechnerei mit Wochenenden und Feiertagen.

Ticker-Liste eigenstaendig, nicht aus universe.json:
Historisch gewachsen wie in marktdaten.py, deshalb dasselbe Risiko -
wird das eine Skript ergaenzt, muss das andere von Hand nachgezogen
werden. Am 04.09.2026 aufgefallen: die S&P-100-Ergaenzung vom 30.08.2026
fehlte hier, GE Vernova und 46 weitere Werte waren im Tagesverlust-Block
unsichtbar. US-Liste jetzt deckungsgleich mit marktdaten.py.

Schreibt:
  docs/kursverlauf.csv
"""

from __future__ import annotations

import csv
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import kurse

# Ticker mit praktisch durchgehendem Handel (XETRA + der einzige ASML-
# Sonderfall) gelten erst spaeter am Tag als sicher geschlossen. Uebernommen
# aus marktdaten.py (unfertige_heutige_kerze_verwerfen), wo dieselbe
# Schwelle seit dem 01.09.2026 verhindert, dass eine mitten im Handel
# abgegriffene Kerze als Tagesschluss durchgeht.
def _europaeisch(ticker: str) -> bool:
    return ticker.endswith(".DE") or ticker == "ASML"


def unfertige_heutige_kerze_verwerfen(df, ticker, jetzt_utc):
    """Wirft die letzte Zeile weg, wenn sie auf heute datiert ist, der
    zugehoerige Markt zum Abrufzeitpunkt aber noch nicht sicher
    geschlossen hatte.

    Bis 03.09.2026 hatte NUR marktdaten.py diesen Schutz. kursverlauf.py
    rief dieselben Kerzen ab, ohne die letzte Zeile zu pruefen - der
    05:00-UTC-Lauf traf europaeische Werte mitten im Handel und schrieb
    einen Bruchteilstag als vermeintlichen Schlusskurs in die Spalte.
    Peters Frage vom 04.09.2026 ("Was fehlt uns durch Marktdaten?") hat
    das aufgedeckt.
    """
    letztes_datum = df.index[-1].date()
    if letztes_datum != jetzt_utc.date():
        return df
    schwelle = 17 if _europaeisch(ticker) else 21
    if jetzt_utc.hour < schwelle:
        return df.iloc[:-1]
    return df

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
CSV_AUS = DOCS / "kursverlauf.csv"
# Getrennte Dateien statt einer breiten OHLC-Datei: so bleibt
# kursverlauf.csv fuer alle bisherigen Leser unveraendert (gleiche Spalten,
# gleiche Bedeutung) und nichts bricht. Eine gemeinsame Datei mit einer
# zusaetzlichen "feld"-Spalte haette jeden Konsumenten angefasst.
CSV_TIEF = DOCS / "kursverlauf_tief.csv"
CSV_HOCH = DOCS / "kursverlauf_hoch.csv"
# Eroeffnungskurse ab 07.09.2026. Ohne sie laesst sich "rote Kerze" nicht
# projektueblich bestimmen (Schluss unter EROEFFNUNG, so wie rote_kerze()
# in marktdaten.py). Der Ersatz ueber den Vortagsschluss lieferte am
# 07.09.2026 bei Xcel Energy ein falsches Ergebnis: der 31.08. schloss
# unter dem Vortagsschluss, war als Kerze aber gruen.
CSV_EROEFF = DOCS / "kursverlauf_eroeffnung.csv"

# 130 Handelstage sind rund ein halbes Jahr. Der laengste Rueckblick im
# Blatt Rueckblick geht ueber 63 Handelstage; damit bleibt Platz fuer
# Kaeufe, die schon einige Wochen zurueckliegen, ohne die Datei unnoetig
# aufzublaehen.
TAGE = 130

US = """AAPL ABNB ADBE ADI ADP ADSK AEP AMAT AMD AMGN AMZN ARM ASML AVGO
AXP AZN BA BIIB BKNG BKR CAT CDNS CDW CEG CHTR CMCSA COST CPRT CRM CRWD CSCO
CSGP CSX CTAS CTSH DASH DDOG DIS DXCM EXC FANG FAST FTNT GEHC GILD
GOOGL GS HD HON IBM IDXX ILMN INTC INTU ISRG JNJ JPM KDP KHC KLAC KO LIN LRCX
LULU MAR MCD MCHP MDB MDLZ MELI META MMM MNST MRK MRNA MRVL MSFT MU NFLX NKE
NVDA NXPI ODFL ON ORCL ORLY PANW PAYX PCAR PDD PEP PG PLTR PYPL QCOM REGN ROP
ROST SBUX SHW SNPS SPGI TEAM TMUS TRV TSLA TTD TTWO TXN UNH V VRSK VRTX VZ
WBD WDAY WMT XEL ZS
ABBV ABT ACN AMT BAC BLK BMY BNY BRK-B C CL COF COP CVS DE DHR DUK EMR FDX
GD GE GEV GM HONA LLY LMT LOW MA MDT MO MS NEE NOW PFE PM RTX SCHW SO SPG T
TMO UBER UNP UPS USB WFC XOM""".split()

DAX = """ADS.DE AIR.DE ALV.DE BAS.DE BAYN.DE BEI.DE BMW.DE BNR.DE CBK.DE CON.DE
DTG.DE DBK.DE DB1.DE DHL.DE DTE.DE EOAN.DE FRE.DE HNR1.DE HEI.DE HEN3.DE
IFX.DE MBG.DE MRK.DE MTX.DE MUV2.DE P911.DE PAH3.DE QIA.DE RHM.DE RWE.DE SAP.DE
SRT3.DE SIE.DE ENR.DE SHL.DE SY1.DE VOW3.DE VNA.DE ZAL.DE""".split()

# Rohstoffe und Waehrung bewusst mit drin: Gold wurde gehandelt (zwei
# Positionen im August 2026), also muss es auch auswertbar sein.
# ZC=F (Mais) am 09.09.2026 ergaenzt. Die Vollstaendigkeitspruefung im
# Workflow meldete "ZC=F: keine Zeile" - der Ticker steht in marktdaten.py,
# fehlte hier aber. Das ist derselbe Listen-Auseinanderlauf, der schon bei
# KC=F (Kaffee) aufgefallen ist, nur andersherum: KC=F steht hier und
# fehlt in marktdaten.py. Beide Listen muessen deckungsgleich sein, sonst
# schlaegt die Pruefung taeglich fehl, ohne dass ein echter Fehler
# vorliegt.
WEITERE = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F", "CL=F", "BZ=F", "NG=F",
           "ZW=F", "CC=F", "SB=F", "KC=F", "ZC=F", "EURUSD=X"]

UNIVERSUM = list(dict.fromkeys(US + DAX + WEITERE))


# Ein Tag zaehlt nur als Handelstag, wenn ihn mindestens dieser Anteil
# der Werte hat. Grund: Rohstoff- und Waehrungsnotierungen laufen fast
# rund um die Uhr. Beim Lauf am 25.08.2026 um 23:04 UTC - das ist bereits
# der 26.08. in Mitteleuropa - hatte EUR/USD schon eine Kerze vom naechsten
# Tag, die 162 von 163 Werten fehlte. Aus so einer Spalte wird im Blatt
# Rueckblick ein falscher Spaltenversatz: "5 Handelstage spaeter" wuerde
# einen Tag mitzaehlen, den es fuer diesen Wert nie gab. Betroffen waren
# drei Spalten, zwei davon am Rand des Zeitfensters.
# Am 09.09.2026 von 0.20 auf 0.10 gesenkt. Bei 218 Werten lag die alte
# Schwelle bei 43,6 - an US-Feiertagen handeln aber nur die 41
# europaeischen Werte (18,8 %). Der Lauf vom 09.09.2026 verwarf deshalb
# 25.05., 19.06., 03.07. und 07.09.2026 mit jeweils 41 Werten, also
# vollwertige XETRA-Handelstage. Die Artefakte, gegen die die Schwelle
# gedacht war, haben ein bis dreizehn Werte (unter 6 %) und fallen auch
# bei 0.10 zuverlaessig heraus.
MINDESTBESETZUNG = 0.10


def reihen() -> tuple[list[str], dict, dict, dict, dict]:
    """Schlusskurse je Wert, plus die gemeinsame Liste der Handelstage.

    Die Tage werden ueber ALLE Werte gesammelt, nicht je Wert einzeln:
    XETRA und NYSE haben verschiedene Feiertage, und eine gemeinsame
    Spaltenachse ist Voraussetzung dafuer, dass der Spaltenversatz
    "N Handelstage spaeter" ueberhaupt eine feste Bedeutung hat. Fehlt
    einem Wert ein Tag, bleibt die Zelle leer statt zu verrutschen.
    """
    je_wert: dict[str, dict[str, float]] = {}
    je_tief: dict[str, dict[str, float]] = {}
    je_hoch: dict[str, dict[str, float]] = {}
    je_eroeff: dict[str, dict[str, float]] = {}
    alle_tage: set[str] = set()
    roh: dict[str, "pd.DataFrame"] = {}
    jetzt = datetime.now(timezone.utc)
    for i, t in enumerate(UNIVERSUM, 1):
        df = kurse.kerzen(t, period="400d")
        if df is None or df.empty:
            continue

        # Rohdaten sammeln. Die Aktualitaetspruefung folgt weiter unten,
        # erst nachdem die unfertige heutige Kerze entfernt wurde - sonst
        # verzerren die rund um die Uhr notierten Rohstoffe und EUR/USD
        # den Vergleichsstand.
        roh[t] = unfertige_heutige_kerze_verwerfen(df, t, jetzt)
        if roh[t].empty:
            del roh[t]
            continue
        if i % 25 == 0:
            print(f"  {i}/{len(UNIVERSUM)} ...")

    if not roh:
        return [], {}, {}, {}, {}

    # Vergleichsstand JE MARKTGRUPPE, nicht ueber alle Werte hinweg.
    #
    # Zwei Fehlversuche fuehrten hierher. Erst war der Maszstab das
    # Maximum ueber alle Werte: am 09.09.2026 um 04:56 UTC hatten
    # Rohstoffe und EUR/USD schon eine Kerze vom 09.09., der Rest stand
    # korrekt auf dem 08.09. - 208 von 218 galten als veraltet, Twelve
    # Data lief nach acht Abrufen in sein Minutenlimit und lieferte fuer
    # alle einen 429. Dann der haeufigste Tag ueber alle Werte: besser,
    # aber bei einem Feiertag in nur EINEM Markt zieht die Mehrheit den
    # Maszstab und die andere Gruppe gilt faelschlich als veraltet.
    #
    # Jede Gruppe hat ihren eigenen Handelskalender, also auch ihren
    # eigenen Sollstand. Damit ist ein US-Feiertag kein Sonderfall mehr,
    # sondern ergibt sich von selbst: die US-Gruppe steht dann eben auf
    # dem Vortag, die europaeische auf heute, und beide sind vollstaendig.
    def _gruppe(ticker: str) -> str:
        if ticker.endswith(".DE") or ticker == "ASML":
            return "Europa"
        if ticker.endswith("=F") or ticker.endswith("=X"):
            return "Rohstoffe/Devisen"
        return "USA"

    from collections import Counter, defaultdict

    # Sollstand vorrangig aus marktdaten.csv, je Ticker.
    #
    # Der Gruppen-Sollstand allein reicht nicht: Haengen ALLE Werte einer
    # Gruppe (genau der Fall vom 08./09.09.2026, als alle 40 deutschen
    # Aktien auf dem 04.09. standen), ist der haeufigste Tag der Gruppe
    # eben dieser veraltete Tag - und niemand faellt auf. marktdaten.py
    # laeuft im selben Workflow vorher und fuehrt je Ticker den
    # tatsaechlich letzten Handelstag, inklusive Feiertagen. Das ist der
    # belastbare Maszstab. Fehlt die Datei (Einzellauf, Test), faellt die
    # Pruefung auf den Gruppenmodus zurueck.
    soll_je_ticker: dict[str, str] = {}
    markt = DOCS / "marktdaten.csv"
    if markt.exists():
        with open(markt, newline="", encoding="utf-8") as f:
            for z in csv.DictReader(f):
                if z.get("ticker") and z.get("datum"):
                    soll_je_ticker[z["ticker"]] = z["datum"]

    je_gruppe = defaultdict(list)
    for t in roh:
        je_gruppe[_gruppe(t)].append(t)

    nachzuegler = []
    for gruppe, tickers in sorted(je_gruppe.items()):
        modus = Counter(roh[t].index[-1].date() for t in tickers).most_common(1)[0][0]
        hinten = []
        for t in tickers:
            ist = str(roh[t].index[-1].date())
            soll = soll_je_ticker.get(t) or str(modus)
            if ist < soll:
                hinten.append(t)
        quelle = "marktdaten.csv" if soll_je_ticker else "Gruppenmodus"
        print(f"  {gruppe}: Sollstand {modus} ({quelle}), "
              f"{len(tickers) - len(hinten)}/{len(tickers)} aktuell")
        nachzuegler += hinten

    # Harte Obergrenze. Twelve Data erlaubt im Gratistarif 8 Abrufe je
    # Minute und 800 je Tag. Selbst wenn die Erkennung noch einmal
    # danebengreift, kann sie das Tageskontingent nicht verbrennen.
    MAX_NACHSCHLAG = 60
    if len(nachzuegler) > MAX_NACHSCHLAG:
        print(f"  {len(nachzuegler)} Nachzuegler - mehr als die Obergrenze "
              f"{MAX_NACHSCHLAG}. Vermutlich ist die Erstquelle grossflaechig "
              f"ausgefallen; kein Nachschlag, um das Kontingent zu schonen.")
        nachzuegler = []
    elif nachzuegler:
        print(f"  {len(nachzuegler)} Nachzuegler - Zweitquelle wird befragt")

    # Stooq ist seit dem 09.09.2026 fuer JEDEN Ticker defekt ("Missing
    # column provided to 'parse_dates': 'Date'", 218 von 218) und wird
    # hier deshalb nicht mehr gefragt. In kurse.py bleibt die Funktion
    # unberuehrt, andere Skripte nutzen sie weiter.
    # ERSTE Zweitquelle: die letzte Kerze aus marktdaten.csv.
    #
    # marktdaten.py loest das Aktualitaetsproblem fuer seine eigene Datei
    # bereits zuverlaessig und laeuft im selben Workflow vorher - am
    # 09.09.2026 standen dort alle 218 Werte korrekt auf dem 08.09.,
    # waehrend Yahoo hier fuer 40 davon noch den 04.09. lieferte. Die
    # Datei enthaelt je Ticker genau die vier Felder, die diese Spalte
    # braucht: open, high, low, kurs. Also wird das Ergebnis uebernommen,
    # statt dieselbe Kerze ueber eine externe API noch einmal zu holen.
    # Kostet nichts, kein Kontingent, kein Minutenlimit, keine 429er.
    #
    # Grenze: marktdaten.csv fuehrt nur EINEN Tag je Ticker. Haengt ein
    # Wert mehrere Tage zurueck, schliesst das nur die juengste Luecke -
    # den Rest meldet die Vollstaendigkeitspruefung weiterhin.
    aus_marktdaten = 0
    if markt.exists():
        with open(markt, newline="", encoding="utf-8") as f:
            zeilen_md = {z["ticker"]: z for z in csv.DictReader(f)}
        rest = []
        for t in nachzuegler:
            z = zeilen_md.get(t)
            if not z or not z.get("datum"):
                rest.append(t)
                continue
            try:
                tag = pd.Timestamp(z["datum"])
                neue = pd.DataFrame(
                    {"Open": [float(z["open"])], "High": [float(z["high"])],
                     "Low": [float(z["low"])], "Close": [float(z["kurs"])]},
                    index=[tag])
            except (KeyError, TypeError, ValueError):
                rest.append(t)
                continue
            if tag <= roh[t].index[-1]:
                rest.append(t)
                continue
            roh[t] = pd.concat([roh[t], neue])
            aus_marktdaten += 1
        if aus_marktdaten:
            print(f"  {aus_marktdaten} Werte aus marktdaten.csv ergaenzt")
        nachzuegler = rest
        if nachzuegler:
            print(f"  {len(nachzuegler)} weiterhin offen - Twelve Data wird befragt")

    offen = []
    for n, t in enumerate(nachzuegler):
        if n and n % 8 == 0:
            print(f"    Minutenlimit - 60 s Pause ({n}/{len(nachzuegler)})")
            time.sleep(60)
        df_td = kurse.kerzen_twelvedata(t)
        if df_td is not None:
            df_td = unfertige_heutige_kerze_verwerfen(df_td, t, jetzt)
            if not df_td.empty and df_td.index[-1] > roh[t].index[-1]:
                print(f"  {t}: Yahoo veraltet ({roh[t].index[-1].date()}), "
                      f"Twelve Data aktueller ({df_td.index[-1].date()})")
                roh[t] = df_td
                continue
        offen.append(t)
    if offen:
        # Sichtbar machen, nicht verschweigen. Der Prueflauf im Workflow
        # bricht daran ab - hier steht, welche Werte es betrifft.
        print(f"  NICHT AKTUALISIERT ({len(offen)}): " + ", ".join(sorted(offen)))

    for t, df in roh.items():
        if df.empty:
            continue
        letzte = df.tail(TAGE)
        # Ab 05.09.2026 zusaetzlich Tagestief und Tageshoch. Grund: Ein
        # Turbo knockt INTRADAY aus, nicht zum Schluss. Die Historie in
        # historie.py rechnet laengst mit High/Low - nur diese Datei kannte
        # bisher ausschliesslich Schlusskurse. Dadurch war weder erkennbar,
        # ob ein Bezugstief im Tagesverlauf schon beruehrt wurde (bei
        # Alphabet A am 04.09.2026 ging es um 0,11 Punkte), noch tauchten
        # Tage im Tagesverlust-Block auf, die intraday 8 % verloren und bei
        # -4 % schlossen - also genau die Tage, an denen enge KOs sterben.
        werte = {str(d.date()): round(float(c), 4)
                 for d, c in zip(letzte.index, letzte["Close"])}
        je_wert[t] = werte
        je_tief[t] = {str(d.date()): round(float(v), 4)
                      for d, v in zip(letzte.index, letzte["Low"])}
        je_hoch[t] = {str(d.date()): round(float(v), 4)
                      for d, v in zip(letzte.index, letzte["High"])}
        je_eroeff[t] = {str(d.date()): round(float(v), 4)
                        for d, v in zip(letzte.index, letzte["Open"])}
        alle_tage.update(werte)

    if not je_wert:
        # Fuenf Werte, weil main() fuenf entpackt - die alte Fassung gab
        # zwei zurueck und haette hier mit ValueError abgebrochen, statt
        # die vorgesehene Meldung auszugeben (Fund 09.09.2026).
        return [], {}, {}, {}, {}

    # Duenn besetzte Tage aus der Achse werfen, siehe MINDESTBESETZUNG.
    schwelle = len(je_wert) * MINDESTBESETZUNG
    gezaehlt = {d: sum(1 for w in je_wert.values() if d in w) for d in alle_tage}
    behalten = sorted(d for d, n in gezaehlt.items() if n >= schwelle)
    verworfen = sorted(d for d, n in gezaehlt.items() if n < schwelle)
    if verworfen:
        print(f"  {len(verworfen)} Tage verworfen (unter "
              f"{MINDESTBESETZUNG:.0%} der Werte): "
              + ", ".join(f"{d} ({gezaehlt[d]})" for d in verworfen))
    return behalten, je_wert, je_tief, je_hoch, je_eroeff


def _eine_datei(pfad, tage: list[str], je_wert: dict) -> None:
    with open(pfad, "w", newline="", encoding="utf-8") as f:
        s = csv.writer(f)
        s.writerow(["ticker"] + tage)
        for t in sorted(je_wert):
            s.writerow([t] + [je_wert[t].get(d, "") for d in tage])
    print(f"Geschrieben: {pfad} ({len(je_wert)} Werte, {len(tage)} Handelstage)")


def schreiben(tage: list[str], je_wert: dict, je_tief: dict,
              je_hoch: dict, je_eroeff: dict) -> None:
    DOCS.mkdir(exist_ok=True)
    _eine_datei(CSV_AUS, tage, je_wert)
    # Dieselbe Tagesachse wie die Schlusskursdatei - dadurch sind die drei
    # Dateien spaltenweise deckungsgleich und lassen sich ohne Abgleich
    # nebeneinanderlegen.
    _eine_datei(CSV_TIEF, tage, je_tief)
    _eine_datei(CSV_HOCH, tage, je_hoch)
    _eine_datei(CSV_EROEFF, tage, je_eroeff)


def main() -> None:
    kurse.aufraeumen()
    tage, je_wert, je_tief, je_hoch, je_eroeff = reihen()
    if not je_wert:
        print("Keine Kursdaten erhalten - nichts geschrieben.")
        return
    schreiben(tage, je_wert, je_tief, je_hoch, je_eroeff)
    print(f"Zeitraum {tage[0]} bis {tage[-1]}. "
          f"Erstellt {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC.")


if __name__ == "__main__":
    main()
