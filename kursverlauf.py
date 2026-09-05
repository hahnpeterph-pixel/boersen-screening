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
WEITERE = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F", "CL=F", "BZ=F", "NG=F",
           "ZW=F", "CC=F", "SB=F", "EURUSD=X"]

UNIVERSUM = list(dict.fromkeys(US + DAX + WEITERE))


# Ein Tag zaehlt nur als Handelstag, wenn ihn mindestens dieser Anteil
# der Werte hat. Grund: Rohstoff- und Waehrungsnotierungen laufen fast
# rund um die Uhr. Beim Lauf am 25.08.2026 um 23:04 UTC - das ist bereits
# der 26.08. in Mitteleuropa - hatte EUR/USD schon eine Kerze vom naechsten
# Tag, die 162 von 163 Werten fehlte. Aus so einer Spalte wird im Blatt
# Rueckblick ein falscher Spaltenversatz: "5 Handelstage spaeter" wuerde
# einen Tag mitzaehlen, den es fuer diesen Wert nie gab. Betroffen waren
# drei Spalten, zwei davon am Rand des Zeitfensters.
MINDESTBESETZUNG = 0.20


def reihen() -> tuple[list[str], dict[str, dict[str, float]]]:
    """Schlusskurse je Wert, plus die gemeinsame Liste der Handelstage.

    Die Tage werden ueber ALLE Werte gesammelt, nicht je Wert einzeln:
    XETRA und NYSE haben verschiedene Feiertage, und eine gemeinsame
    Spaltenachse ist Voraussetzung dafuer, dass der Spaltenversatz
    "N Handelstage spaeter" ueberhaupt eine feste Bedeutung hat. Fehlt
    einem Wert ein Tag, bleibt die Zelle leer statt zu verrutschen.
    """
    je_wert: dict[str, dict[str, float]] = {}
    alle_tage: set[str] = set()
    jetzt = datetime.now(timezone.utc)
    for i, t in enumerate(UNIVERSUM, 1):
        df = kurse.kerzen(t, period="400d")
        if df is None or df.empty:
            continue

        # Yahoo "erfolgreich" heisst nicht zwangslaeufig aktuell (siehe
        # marktdaten.py, 01.09.2026). kursverlauf.py hatte diese Pruefung
        # bisher nicht - der Kerzen-Fix vom 04.09.2026 allein loeste das
        # nicht, weil er nur unfertige HEUTIGE Kerzen abfaengt, nicht
        # einen Yahoo-Datensatz, der komplett auf dem Vortag haengen
        # bleibt. Fund vom 05.09.2026: die Datei hing weiterhin einen Tag
        # zurueck. Dieselbe Freshness-Pruefung wie in marktdaten.py.
        if t.endswith(".DE") or t == "ASML":
            kandidaten_quellen = [("Yahoo", df)]
            df_stooq = kurse.kerzen_stooq(t)
            if df_stooq is not None:
                kandidaten_quellen.append(("Stooq", df_stooq))
            df_td = kurse.kerzen_twelvedata(t)
            if df_td is not None:
                kandidaten_quellen.append(("Twelve Data", df_td))
            bester_name, bestes_df = max(
                kandidaten_quellen, key=lambda x: x[1].index[-1])
            if bester_name != "Yahoo":
                print(f"  {t}: Yahoo veraltet ({df.index[-1].date()}), "
                      f"{bester_name} aktueller ({bestes_df.index[-1].date()}) "
                      f"- {bester_name} verwendet")
                df = bestes_df

        df = unfertige_heutige_kerze_verwerfen(df, t, jetzt)
        if df.empty:
            continue
        letzte = df.tail(TAGE)
        werte = {str(d.date()): round(float(c), 4)
                 for d, c in zip(letzte.index, letzte["Close"])}
        je_wert[t] = werte
        alle_tage.update(werte)
        if i % 25 == 0:
            print(f"  {i}/{len(UNIVERSUM)} ...")

    if not je_wert:
        return [], {}

    # Duenn besetzte Tage aus der Achse werfen, siehe MINDESTBESETZUNG.
    schwelle = len(je_wert) * MINDESTBESETZUNG
    gezaehlt = {d: sum(1 for w in je_wert.values() if d in w) for d in alle_tage}
    behalten = sorted(d for d, n in gezaehlt.items() if n >= schwelle)
    verworfen = sorted(d for d, n in gezaehlt.items() if n < schwelle)
    if verworfen:
        print(f"  {len(verworfen)} Tage verworfen (unter "
              f"{MINDESTBESETZUNG:.0%} der Werte): "
              + ", ".join(f"{d} ({gezaehlt[d]})" for d in verworfen))
    return behalten, je_wert


def schreiben(tage: list[str], je_wert: dict[str, dict[str, float]]) -> None:
    DOCS.mkdir(exist_ok=True)
    with open(CSV_AUS, "w", newline="", encoding="utf-8") as f:
        s = csv.writer(f)
        s.writerow(["ticker"] + tage)
        for t in sorted(je_wert):
            s.writerow([t] + [je_wert[t].get(d, "") for d in tage])
    print(f"Geschrieben: {CSV_AUS} ({len(je_wert)} Werte, {len(tage)} Handelstage)")


def main() -> None:
    kurse.aufraeumen()
    tage, je_wert = reihen()
    if not je_wert:
        print("Keine Kursdaten erhalten - nichts geschrieben.")
        return
    schreiben(tage, je_wert)
    print(f"Zeitraum {tage[0]} bis {tage[-1]}. "
          f"Erstellt {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC.")


if __name__ == "__main__":
    main()
