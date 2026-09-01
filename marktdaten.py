"""
marktdaten.py - reiner Marktdaten-Abzug. Kennt KEINE Positionen.

Laeuft werktags im GitHub-Workflow und schreibt:
  docs/marktdaten.csv   eine Zeile je Wert, maschinenlesbar
  docs/marktdaten.md    kurze Uebersicht zum Reinschauen

Bewusst OHNE: Knock-out-Schwellen, Positionsgroessen, Regelpruefung,
Depotstand. All das aendert sich staendig und wird ausserhalb gerechnet.
Dadurch muss diese Datei nie wieder angefasst werden, egal was sich am
Depot aendert.

Geliefert wird je Wert:
  Kurs, ATR(14), RSI(14), EUR/USD,
  die drei juengsten Swing-Tiefs mit Datum und Volumenverhaeltnis,
  Kerzensignale: Hammer, hoeheres Hoch, bearishe Umkehrkerze,
  EMA(50) und EMA(200) auf Tagesbasis.
"""

import csv
import os
from datetime import datetime, timezone

import pandas as pd
import numpy as np

import kurse
import stand
import tiefs_regel as regel

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
CSV_AUS = os.path.join(DOCS, "marktdaten.csv")
MD_AUS = os.path.join(DOCS, "marktdaten.md")

FENSTER_TAGE = 90
# LINKS/RECHTS gehoerten zur alten 3-links-3-rechts-Tiefsuche und werden
# von der Umkehr-Regel nicht mehr gebraucht. Bleiben stehen, weil tiefs.py
# und watchlist.json sie weiterhin fuehren.
LINKS = RECHTS = 3
ATR_TAGE = RSI_TAGE = 14

# ── Rohstoffe ──────────────────────────────────────────────────────
# Erster Eintrag wird versucht, bei Fehlschlag der zweite (Rueckfallkette).
# Lauf vom 21.08.2026: die vier Edelmetall-Spot-Ticker lieferten bei Yahoo
# KEINE Daten. Deshalb Future als Rueckfall.
#
# WICHTIG fuer die KO-Pruefung: Zertifikate auf Edelmetalle referenzieren
# in der Regel SPOT, nicht den Future. Der Future notiert hoeher (Contango).
# Gemessene Basis am 21.08.2026: GC=F 4.639,20 gegen Spot 4.603,11,
# also +36,09 Punkte. Wird der Future genutzt, muss die Basis fuer die
# KO-Rechnung abgezogen werden - das passiert ausserhalb dieses Skripts.
ROHSTOFFE = [
    (["XAUUSD=X", "GC=F"], "Gold", "Spot/Future"),
    (["XAGUSD=X", "SI=F"], "Silber", "Spot/Future"),
    (["XPTUSD=X", "PL=F"], "Platin", "Spot/Future"),
    (["XPDUSD=X", "PA=F"], "Palladium", "Spot/Future"),
    (["BZ=F"], "Brent Oel", "Future"),
    (["CL=F"], "WTI Oel", "Future"),
    (["NG=F"], "Erdgas", "Future"),
    (["HG=F"], "Kupfer", "Future"),
    (["ZW=F"], "Weizen", "Future"),
    (["ZC=F"], "Mais", "Future"),
    # KC=F (Kaffee) am 24.08.2026 entfernt: ueber Trade Republic nicht handelbar.
    (["CC=F"], "Kakao", "Future"),
    (["SB=F"], "Zucker", "Future"),
]

WAEHRUNG = [(["EURUSD=X"], "EUR/USD", "Spot")]

# ── Aktien: NASDAQ-100, Dow 30, DAX 40, S&P-100-Ergaenzung. Statisch,
# aendert sich selten.
# Am 21.08.2026 entfernt, weil bei Yahoo keine Daten mehr (uebernommen
# oder delistet): ANSS, EA, WBA, 1COV.DE.
# Am 24.08.2026 entfernt: GOOG (Alphabet Class C) nach Entscheidung 68 -
# derselbe Basiswert wie GOOGL, doppelter Einsatz bei gleichem Risiko.
# Am 30.08.2026 ergaenzt: 47 S&P-100-Mitglieder, die weder im Dow 30 noch
# im NASDAQ-100 stehen (ueberwiegend NYSE-Finanzwerte, Industrie- und
# Gesundheitswerte) - Peter wollte den S&P 100 als dritten grossen
# US-Index mit abgedeckt haben. BRK-B mit Bindestrich, nicht BRKB wie in
# manchen ETF-Bestandslisten - das ist Yahoos Schreibweise, ohne die
# schlaegt der Kursabruf fehl. HONA (Honeywell Aerospace) ist der
# Spin-off vom 29.06.2026 und hat entsprechend kaum Historie vor diesem
# Datum - Fallzahlen in historie.py/hochs.py werden fuer diesen einen
# Wert lange duenn bleiben, das ist kein Fehler.
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

UNIVERSUM = ([([t], t, "Aktie") for t in dict.fromkeys(US)]
             + [([t], t, "Aktie") for t in dict.fromkeys(DAX)]
             + ROHSTOFFE + WAEHRUNG)

# Ticker ohne brauchbares Volumen bei Yahoo
OHNE_VOLUMEN = {"XAUUSD=X", "XAGUSD=X", "XPTUSD=X", "XPDUSD=X", "EURUSD=X"}


# ── Berechnungen ───────────────────────────────────────────────────
def kerzen(ticker):
    """Durchreiche. Der Abruf liegt seit 22.08.2026 in kurse.py, damit
    screener.py, tiefs.py und dieses Skript dieselben Kerzen benutzen,
    statt sie dreimal zu holen."""
    return kurse.kerzen(ticker, period="400d")


def atr(df, tage=ATR_TAGE):
    h, t, c = df["High"], df["Low"], df["Close"]
    v = c.shift(1)
    tr = pd.concat([h - t, (h - v).abs(), (t - v).abs()], axis=1).max(axis=1)
    w = tr.tail(tage).mean()
    return None if pd.isna(w) else float(w)


def rsi(df, tage=RSI_TAGE):
    d = df["Close"].diff()
    g = d.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    v = (-d.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    if v.iloc[-1] == 0:
        return 100.0
    w = 100 - 100 / (1 + g.iloc[-1] / v.iloc[-1])
    return None if pd.isna(w) else float(w)


def ema(df, tage):
    w = df["Close"].ewm(span=tage, adjust=False).mean().iloc[-1]
    return None if pd.isna(w) else float(w)


def swing_tiefs(df):
    """Swing-Tiefs im 90-Tage-Fenster. Regel siehe tiefs_regel.py."""
    return regel.swing_tiefs(df, fenster_tage=FENSTER_TAGE)


def tief_takt(treffer, df):
    """Wie oft dreht dieser Wert im Fenster - und wie eng liegen die Tiefs?

    Die Umkehr-Regel kennt keine Mindestbewegung, jede Drehung zaehlt. Wie
    viele Tiefs dabei herauskommen, sagt also etwas ueber den Wert selbst:
    ein ruhiger Titel dreht selten, ein nervoeser alle paar Tage. Ohne diese
    Zahl laesst sich nicht beurteilen, ob drei Tiefs in zwei Wochen bei
    diesem Papier normal sind oder auffaellig.

    Gibt (Anzahl bestaetigter Tiefs, mittlerer Abstand in Handelstagen)
    zurueck. Der Abstand wird ueber die Zeilenabstaende im Kursdatensatz
    gemessen, zaehlt also nur Handelstage, keine Wochenenden.
    """
    best = sorted((t["i"] for t in treffer if t.get("best")), reverse=True)
    if len(best) < 2:
        return len(best), None
    abstaende = [best[k] - best[k + 1] for k in range(len(best) - 1)]
    return len(best), round(sum(abstaende) / len(abstaende), 1)


def korrektur_ist(df, tiefe_liste, a):
    """Die LAUFENDE Korrektur, mit demselben Anker wie phasen.py.

    Das Soll aus der Phasen-Analyse misst vom letzten bestaetigten Hoch bis
    zum letzten Tief der Abwaertsserie. Ohne dasselbe Hoch als Anker ist ein
    Soll/Ist-Vergleich wertlos - die Falltiefe vom 60-Tage-Hoch misst etwas
    anderes.

    Bis 22.08.2026 trug diese Funktion eine eigene Kopie der Pivot-Suche UND
    der alten Serienabgrenzung, die beim ersten nicht-tieferen Tief abbrach.
    Bei Cadence ankerte sie dadurch auf dem 06.08. statt auf dem 03.06. und
    meldete 4,03 ATR statt 11,27 - also ziemlich genau ein Drittel. Genau der
    Fehler, vor dem der eigene Kommentar warnte.

    Serie und Hochs kommen jetzt aus tiefs_regel, damit Ist und Soll
    dieselbe Definition benutzen.
    """
    if not tiefe_liste or a in (None, 0):
        return None, None, None

    seqs = regel.sequenzen(df)
    if not seqs or not seqs[-1]["laufend"]:
        return None, None, None
    lauf = seqs[-1]
    beginn = lauf["start_i"]

    davor = [h["i"] for h in regel.swing_hochs(df) if h["i"] < beginn]
    if not davor:
        # Die Serie beginnt vor dem ersten erkannten Hoch der geladenen
        # Historie - dann gibt es keinen Anker. Seit die Serien laenger
        # werden duerfen, ist das kein rein theoretischer Fall mehr: bei
        # 400 Tagen Historie und einer Serie ueber mehrere Monate kann der
        # Anfang aus dem Fenster fallen. Lieber leer als falsch verankert.
        return None, None, None
    h_i = davor[-1]
    hoch = df["High"].values
    juengstes = tiefe_liste[0]
    tiefe_atr = (float(hoch[h_i]) - juengstes["tief"]) / a
    dauer = juengstes["i"] - h_i
    return float(hoch[h_i]), round(tiefe_atr, 2), int(dauer)


def tiefserie(df, variante=regel.STANDARD):
    """Laufende Abwaertsserie. Beide Varianten in tiefs_regel.py."""
    return regel.tiefserie(df, variante)


def ruecksetzer_ist(df, a):
    """Ist HEUTE ein bestaetigter, noch nicht erholter Ruecksetzer nach
    einem Hoch aktiv?

    Bewusst NICHT korrektur_ist()/sequenzen() wiederverwendet: ein Tief
    zaehlt dort erst als Pivot, wenn eine SPAETERE Kerze das Hoch der
    Tiefkerze durchbricht - das kann laenger dauern als die ersten paar
    Tage eines Ruecksetzers, um die es hier geht. Der Befund vom
    30.08.2026 (Notiz 6: "rote Kerze + hohes Volumen" traegt) galt nur fuer
    Tag 0-3 nach der schnelleren Bestaetigung aus hochs.py/ruecksetzer.py -
    ein Tief unter dem Tief der Hochkerze reicht, kein Pivot noetig. Mit
    der langsameren Pivot-Bestaetigung waere Tag 0 hier oft schon Tag 3
    oder spaeter, und genau das Fenster, in dem das Signal galt, waere
    verpasst.

    Gibt None zurueck, wenn kein aktiver Ruecksetzer laeuft (gerade erst
    ein neues Hoch ohne folgendes tieferes Tief, oder der letzte
    Ruecksetzer ist schon wieder bis auf 0,25 ATR ans alte Hoch
    herangekommen). Sonst ein Dict mit hoch_datum, tag, rueckstand_atr.
    """
    if a in (None, 0):
        return None
    seqs = regel.aufwaertssequenzen(df)
    if not seqs:
        return None
    alle_hochs = sorted(i for s in seqs for i in s["hochs"])
    if not alle_hochs:
        return None
    i = alle_hochs[-1]
    hoch_preis = float(df["High"].values[i])
    tief, hoch_arr = df["Low"].values, df["High"].values
    n = len(df)
    b = None
    for j in range(i + 1, n):
        if tief[j] < tief[i]:
            b = j
            break
    if b is None:
        return None
    for j in range(b, n):
        if hoch_arr[j] >= hoch_preis - 0.25 * a:
            return None
    rueckstand = max(0.0, (hoch_preis - float(tief[b:].min())) / a)
    return {"hoch_datum": f"{df.index[i]:%Y-%m-%d}", "tag": (n - 1) - b,
            "rueckstand_atr": round(rueckstand, 2)}


def schwellen_laden():
    """Wertspezifische Volumen-Schwelle aus dem woechentlichen
    ruecksetzer.py-Lauf (docs/ruecksetzer_schwellen.csv). Fehlt die Datei
    oder ein Wert darin (etwa neu aufgenommene Ticker ohne ausreichende
    Historie), bleibt die Achtung-Pruefung fuer diesen Wert schlicht aus -
    besser keine Warnung als eine geratene Schwelle."""
    pfad = os.path.join(DOCS, "ruecksetzer_schwellen.csv")
    if not os.path.exists(pfad):
        return {}
    try:
        s = pd.read_csv(pfad)
        return dict(zip(s["ticker"], s["vol_rel_schwelle"]))
    except Exception:  # noqa: BLE001
        return {}


FRUEHFENSTER_TAGE = 3  # dieselbe Grenze wie in ruecksetzer.py - nur in
                        # diesem Fenster war "rote Kerze + hohes Volumen"
                        # tragfaehig (Notiz 6, 30.08.2026)


def vol_rel(df, bis, tage=20):
    if "Volume" not in df.columns:
        return None
    teil = df["Volume"].iloc[max(0, bis - tage):bis].dropna()
    if teil.empty or teil.mean() == 0:
        return None
    v = df["Volume"].iloc[bis]
    return None if pd.isna(v) else float(v) / float(teil.mean())


def hoch60(df, tage=60):
    """Hoechstes Hoch der letzten Handelstage. Basis fuer die Falltiefe -
    ohne sie laesst sich ein Boden nicht von einer Konsolidierung nahe am
    Hoch unterscheiden."""
    teil = df["High"].tail(tage).dropna()
    return None if teil.empty else float(teil.max())


def vol_druck5(df, tage=5):
    """Verhaeltnis des Volumens an Anstiegs- zu Ruecksetzertagen der letzten
    Tage. Ueber 1 heisst: an den gruenen Tagen wurde mehr gehandelt - die
    Kaeufer sind zurueck. Dritter Baustein der Bodenbildung."""
    if "Volume" not in df.columns or len(df) < tage + 2:
        return None
    d = df["Close"].diff().tail(tage)
    v = df["Volume"].tail(tage)
    auf = float(v[d > 0].sum())
    ab = float(v[d <= 0].sum())
    return None if ab <= 0 else auf / ab


def hammer(df, a):
    """Lange untere Lunte, kleiner Koerper oben, kaum obere Lunte,
    relevante Groesse, vorher abwaerts."""
    if len(df) < 6:
        return False
    z = df.iloc[-1]
    o, h, t, c = (float(z["Open"]), float(z["High"]),
                  float(z["Low"]), float(z["Close"]))
    sp = h - t
    if sp <= 0:
        return False
    koerper, unten, oben = abs(c - o), min(o, c) - t, h - max(o, c)
    if a and sp < 0.8 * a:
        return False
    if koerper > 0 and unten < 2.0 * koerper:
        return False
    if (max(o, c) - t) < 0.66 * sp:
        return False
    if oben > 0.15 * sp:
        return False
    return bool(c < float(df["Close"].iloc[-6]))


def hoeheres_hoch(df):
    return bool(float(df["High"].iloc[-1]) > float(df["High"].iloc[-2]))


def unfertige_heutige_kerze_verwerfen(df, ticker, jetzt_utc):
    """Wirft die letzte Zeile weg, wenn sie auf heute datiert ist, aber der
    zugehoerige Markt zum Abrufzeitpunkt noch gar nicht sicher geschlossen
    hatte - sonst landet ein mitten im Handel abgegriffener Kurs als
    vermeintlicher Tagesschluss in ATR/RSI/Tiefsserie.

    Am 01.09.2026 um 07:16 UTC beobachtet: ein manueller Lauf traf XETRA
    16 Minuten nach Eroeffnung. Yahoo lieferte anstandslos eine Kerze fuer
    diesen Tag - mit einer Handelsspanne von nur 16 Minuten, nicht einem
    ganzen Tag. Betroffen waren alle DAX-Werte, ASML UND alle Rohstoffe
    samt EUR/USD, weil diese praktisch rund um die Uhr handeln und deshalb
    JEDER Abrufzeitpunkt schon "Kurse von heute" liefert.

    Schwelle bewusst je Markt getrennt, nicht pauschal "heutige Kerze immer
    verwerfen" - das wuerde auch den eigentlichen Zweck der 19:00- und
    22:15-Uhr-Laeufe zunichtemachen, die ja genau den frischen Schluss vom
    selben Tag einsammeln sollen. Europaeische Werte (XETRA-Schluss
    15:30/16:30 UTC) gelten ab 17:00 UTC als sicher fertig, alles andere
    (US-Boersen, Rohstoffe, FX - spaetester Schluss ueblicherweise 21:00
    UTC) erst ab 21:00 UTC.
    """
    letztes_datum = df.index[-1].date()
    if letztes_datum != jetzt_utc.date():
        return df
    europaeisch = ticker.endswith(".DE") or ticker == "ASML"
    schwelle = 17 if europaeisch else 21
    if jetzt_utc.hour < schwelle:
        return df.iloc[:-1]
    return df


def kein_neues_tief(df):
    """Fruehere, weichere Alternative zu 'Tief bestaetigt' (Y-Spalte/tief1_best).

    'Tief bestaetigt' feuert erst, wenn eine spaetere Kerze das Hoch der
    Tiefkerze durchbricht - das kann Tage oder Prozente nach dem eigentlichen
    Wendepunkt liegen (siehe Honeywell, 27.08.2026: guter Verlauf, Einstieg
    verpasst, weil die Bestaetigung zu spaet kam). Dieses Signal fragt
    stattdessen nur: ist das heutige Tagestief hoeher als das gestrige?
    Kein Ausbruch noetig, nur das Ausbleiben eines neuen, tieferen Tiefs.

    Bewusst einen einzigen Tag Rueckblick, kein Schwellenwert ueber mehrere
    Tage - Peter zieht lieber einmal zu frueh nach als einmal zu spaet."""
    return bool(float(df["Low"].iloc[-1]) > float(df["Low"].iloc[-2]))


def umkehrkerze(df):
    """Bearishes Warnsignal: Schluss unter Eroeffnung UND unter
    Vortageshoch UND unter Vortagestief."""
    h, v = df.iloc[-1], df.iloc[-2]
    return bool(h["Close"] < h["Open"] and h["Close"] < v["High"]
                and h["Close"] < v["Low"])


def schluss_unter_vortagestief(df):
    """Peters direkter Wunsch vom 31.08.2026: heutiger Schlusskurs unter
    dem Tagestief von GESTERN. Keine Verkaufsregel, nur ein Pruefanlass -
    bewusst schaerfer als kein_neues_tief() (die vergleicht zwei Tagestiefs
    miteinander, hier geht es um den Schlusskurs gegen das Tagestief davor,
    ein deutlicherer Bruch)."""
    return bool(float(df["Close"].iloc[-1]) < float(df["Low"].iloc[-2]))


def rueckgang_3tage(df):
    """Kursveraenderung der letzten 3 Handelstage in Prozent (Schluss
    gegen Schluss vor 3 Tagen). Immer berechnet, unabhaengig von einer
    Schwelle - die Einordnung passiert in rueckgang_schwelle()."""
    close = df["Close"]
    if len(close) < 4:
        return None
    alt, neu = float(close.iloc[-4]), float(close.iloc[-1])
    if alt == 0:
        return None
    return (neu - alt) / alt * 100


def rueckgang_schwelle(df, tage=3, perzentil=10):
    """Wertspezifische Schwelle fuer 'ungewoehnlicher Ruckgang ueber
    mehrere Tage' (Peter, 31.08.2026: "keine feste Prozentmarke, lieber
    schauen was es an besseren Marken gibt").

    Eine feste Marke wie 5 Prozent passt nicht auf 218 sehr verschieden
    schwankende Werte: Ruhige Werte wie Linde oder Xcel Energy haben ihr
    eigenes 10.-Perzentil bei einem 3-Tage-Rueckgang um -2,6 Prozent,
    Micron dagegen bei -9,8 Prozent - eine einzige Marke waere fuer die
    einen zu eng, fuer die anderen zu lasch (mit echten Depotdaten
    gegengerechnet, 31.08.2026).

    Deshalb hier wertspezifisch aus der bereits geladenen 400-Tage-Reihe
    berechnet: das perzentil-te Perzentil (10 = das untere Zehntel, ein
    ungewoehnlich schlechter 3-Tage-Lauf fuer GENAU DIESEN Wert) der
    rollierenden tage-Tage-Renditen. Kein separates Skript noetig, die
    Reihe liegt in main() ohnehin schon vor.
    """
    close = df["Close"]
    if len(close) < tage + 30:
        return None
    ret = (close / close.shift(tage) - 1) * 100
    ret = ret.dropna()
    if len(ret) < 30:
        return None
    return float(np.percentile(ret, perzentil))


def z(x, nk=4):
    return "" if x is None else f"{round(float(x), nk)}"


# ── Hauptlauf ──────────────────────────────────────────────────────
def main():
    kurse.aufraeumen()
    jetzt = datetime.now(timezone.utc)
    zeilen, fehler = [], []
    schwellen = schwellen_laden()

    for kette, name, art in UNIVERSUM:
        df, ticker, quelle = None, kette[0], ""
        for kandidat in kette:
            df = kerzen(kandidat)
            if df is not None:
                ticker = kandidat
                # Yahoo "erfolgreich" heisst nicht zwangslaeufig aktuell -
                # am 01.09.2026 blieben alle 39 DAX-Werte plus ASML tagelang
                # auf dem Freitagsschluss haengen, ohne dass kerzen() je
                # einen Fehler warf. Deshalb hier bei europaeischen Werten
                # (das beobachtete Muster) zwei weitere Quellen einholen
                # und die insgesamt aktuellste nehmen - nicht nur Stooq,
                # das blockierte GitHub Actions offenbar pauschal (Fragen
                # 43/44, 01.09.2026), deshalb zusaetzlich Twelve Data.
                if kandidat.endswith(".DE") or kandidat == "ASML":
                    kandidaten_quellen = [("Yahoo", df)]
                    df_stooq = kurse.kerzen_stooq(kandidat)
                    if df_stooq is not None:
                        kandidaten_quellen.append(("Stooq", df_stooq))
                    df_td = kurse.kerzen_twelvedata(kandidat)
                    if df_td is not None:
                        kandidaten_quellen.append(("Twelve Data", df_td))
                    bester_name, bestes_df = max(
                        kandidaten_quellen, key=lambda x: x[1].index[-1])
                    if bester_name != "Yahoo":
                        print(f"  {kandidat}: Yahoo veraltet "
                              f"({df.index[-1].date()}), {bester_name} "
                              f"aktueller ({bestes_df.index[-1].date()}) "
                              f"- {bester_name} verwendet")
                        df, quelle = bestes_df, bester_name
                break
            # Stooq/Twelve Data als Zwischenstufe (30.08./01.09.2026,
            # Fragen 43/44), BEVOR der naechste Kandidat der Kette
            # versucht wird - bei Gold/Silber/Platin/Palladium heisst das:
            # Spot vor Yahoo-Future. Liefert keine der beiden etwas,
            # faellt die Schleife normal weiter zum naechsten Kandidaten
            # durch (unveraendertes Verhalten).
            df = kurse.kerzen_stooq(kandidat)
            if df is not None:
                ticker, quelle = kandidat, "Stooq"
                print(f"  {kandidat}: Kurse von Stooq (Yahoo lieferte nichts)")
                break
            df = kurse.kerzen_twelvedata(kandidat)
            if df is not None:
                ticker, quelle = kandidat, "Twelve Data"
                print(f"  {kandidat}: Kurse von Twelve Data (Yahoo/Stooq lieferten nichts)")
                break
        if df is None:
            fehler.append(" oder ".join(kette))
            print(f"  {'/'.join(kette)}: keine Daten")
            continue
        if ticker != kette[0]:
            print(f"  {kette[0]} leer -> Rueckfall auf {ticker}")

        df_vorher = len(df)
        df = unfertige_heutige_kerze_verwerfen(df, ticker, jetzt)
        if len(df) < df_vorher:
            print(f"  {ticker}: heutige Kerze verworfen (Markt zum Abrufzeitpunkt "
                  f"{jetzt:%H:%M} UTC noch nicht sicher geschlossen)")

        a = atr(df)
        tr = swing_tiefs(df)
        kurs = float(df["Close"].iloc[-1])
        letzte = df.iloc[-1]
        mitvol = ticker not in OHNE_VOLUMEN

        r = {
            "ticker": ticker, "name": name, "art": art,
            "wunschticker": kette[0],
            "rueckfall": int(ticker != kette[0]),
            # Yahoo oder Stooq (30.08.2026, Frage 44) - ohne diese Spalte
            # waere ein Wechsel der Datenquelle unsichtbar, obwohl er die
            # Basis fuer ATR/RSI/Tiefserie fuer diesen Tag aendert.
            "anbieter": quelle or "Yahoo",
            # Woher die Kerzen tatsaechlich kommen. Weicht das vom Ticker
            # ab, steht dahinter eine Ausnahme in kurse.KURSQUELLE - und
            # die Waehrung dieser Zeile ist dann eine andere als die des
            # Kursziels in analysten.csv. Ohne diese Spalte waere der
            # Unterschied in der Datei nicht zu sehen.
            "kursquelle": kurse.quelle(ticker),
            "kurswaehrung": kurse.waehrung(ticker),
            "datum": f"{df.index[-1]:%Y-%m-%d}",
            "kurs": z(kurs), "open": z(letzte["Open"]),
            "high": z(letzte["High"]), "low": z(letzte["Low"]),
            "atr14": z(a), "rsi14": z(rsi(df), 2),
            "ema50": z(ema(df, 50)), "ema200": z(ema(df, 200)),
            "hammer": int(hammer(df, a)),
            "hoeheres_hoch": int(hoeheres_hoch(df)),
            "kein_neues_tief": int(kein_neues_tief(df)),
            "umkehrkerze": int(umkehrkerze(df)),
            "hoch60": z(hoch60(df)),
            "vol_druck5": (z(vol_druck5(df), 2) if mitvol else ""),
        }
        anzahl, takt = tief_takt(tr, df)
        r["tiefs_anzahl"] = anzahl
        r["tiefs_abstand"] = z(takt, 1) if takt is not None else ""
        serie, serie_start, serie_tief = tiefserie(df)
        r["tiefs_serie"] = serie
        r["tiefs_serie_start"] = serie_start
        r["tiefs_serie_tief"] = serie_tief
        # Vergleichsvariante "vorheriges Hoch". Laeuft mit, bis sich an echten
        # Trades zeigt, welche Lesart traegt - nicht fuer Entscheidungen benutzen.
        # Bis 24.08.2026 hiess die Spalte tiefs_serie_dow, obwohl sie NICHT die
        # Dow-Zaehlung enthielt. Die massgebliche Dow-Zaehlung steht in
        # tiefs_serie.
        d, d_start, _ = tiefserie(df, "vorheriges_hoch")
        r["tiefs_serie_vorheriges_hoch"] = d
        r["tiefs_serie_vorheriges_hoch_start"] = d_start
        k_hoch, k_atr, k_tage = korrektur_ist(df, tr, a)
        r["korr_hoch"] = z(k_hoch)
        r["korr_ist_atr"] = z(k_atr, 2) if k_atr is not None else ""
        r["korr_ist_tage"] = k_tage if k_tage is not None else ""
        for n in (1, 2, 3):
            t = tr[n - 1] if len(tr) >= n else None
            r[f"tief{n}"] = z(t["tief"]) if t else ""
            r[f"tief{n}_datum"] = f"{t['datum']:%Y-%m-%d}" if t else ""
            r[f"tief{n}_best"] = (int(t["best"]) if t else "")
            r[f"tief{n}_volrel"] = (z(vol_rel(df, t["i"]), 2)
                                    if (t and mitvol) else "")

        rs = ruecksetzer_ist(df, a)
        if rs is not None:
            heute_vol = vol_rel(df, len(df) - 1) if mitvol else None
            heute_kerze = "rot" if float(letzte["Close"]) < float(letzte["Open"]) else "gruen"
            schwelle = schwellen.get(ticker)
            r["ruecksetzer_hoch_datum"] = rs["hoch_datum"]
            r["ruecksetzer_tag"] = rs["tag"]
            r["ruecksetzer_atr"] = z(rs["rueckstand_atr"], 2)
            r["ruecksetzer_vol_rel"] = z(heute_vol, 2) if heute_vol is not None else ""
            r["ruecksetzer_kerze"] = heute_kerze
            r["ruecksetzer_achtung"] = int(bool(
                rs["tag"] <= FRUEHFENSTER_TAGE and heute_kerze == "rot"
                and schwelle is not None and heute_vol is not None
                and heute_vol >= schwelle))
        else:
            r["ruecksetzer_hoch_datum"] = ""
            r["ruecksetzer_tag"] = ""
            r["ruecksetzer_atr"] = ""
            r["ruecksetzer_vol_rel"] = ""
            r["ruecksetzer_kerze"] = ""
            r["ruecksetzer_achtung"] = 0

        # Peters Zusatzcheck vom 31.08.2026 - unabhaengig von einer
        # laufenden Ruecksetzer-Episode, gilt fuer jeden Wert einzeln.
        r["vortagestief_verletzt"] = int(schluss_unter_vortagestief(df))
        r3 = rueckgang_3tage(df)
        schwelle3 = rueckgang_schwelle(df)
        r["rueckgang_3tage_pct"] = z(r3, 2) if r3 is not None else ""
        r["rueckgang_3tage_schwelle"] = z(schwelle3, 2) if schwelle3 is not None else ""
        r["rueckgang_3tage_achtung"] = int(bool(
            r3 is not None and schwelle3 is not None and r3 <= schwelle3))

        zeilen.append(r)
        print(f"  {ticker}: ok")

    # ── Standpruefung ─────────────────────────────────────────────
    # Ein Wert kann eine aeltere letzte Kerze haben als die uebrigen.
    # Am 25.08.2026 traf das alle 39 DAX-Werte und ASML: sie standen auf
    # dem Schlusskurs vom Freitag, waehrend die 120 US-Werte den Montag
    # trugen. Yahoo hatte die vorlaeufige Tageskerze der europaeischen
    # Boersen ueber Nacht durch die offizielle Abrechnung ersetzt, und
    # die lag noch nicht vor. Der Lauf vom Vorabend hatte den Montag noch.
    #
    # Verglichen wird nur unter Aktien. Rohstoffe und Devisen handeln
    # rund um die Uhr und tragen regelmaessig schon den Folgetag - das
    # ist kein Rueckstand und darf nicht als einer gemeldet werden.
    # Schutzregel VOR der Standwarnung: erst die bessere Fassung je Wert
    # bestimmen, dann beurteilen, ob noch etwas zurueckhaengt. Andersherum
    # wuerde die Warnung Werte melden, die gleich darauf ersetzt werden.
    zeilen, _gehalten = stand.zusammenfuehren(zeilen, CSV_AUS)

    aktien = [r for r in zeilen if r.get("art") == "Aktie" and r.get("datum")]
    neuester = max((r["datum"] for r in aktien), default="")
    zurueck = []
    for r in zeilen:
        eigen = r.get("datum") or ""
        alt_ = bool(neuester and r.get("art") == "Aktie" and eigen < neuester)
        r["stand_zurueck"] = int(alt_)
        if alt_:
            zurueck.append(r)
    if zurueck:
        print(f"  ! STANDWARNUNG: {len(zurueck)} von {len(aktien)} Aktien "
              f"haengen zurueck. Neuester Handelstag {neuester}.")
        for r in sorted(zurueck, key=lambda x: (x["datum"], x["ticker"])):
            print(f"      {r['ticker']:10s} letzte Kerze {r['datum']}")

    os.makedirs(DOCS, exist_ok=True)
    felder = list(zeilen[0].keys()) if zeilen else []
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")

    fx = next((r["kurs"] for r in zeilen if r["ticker"] == "EURUSD=X"), "")
    sig = [r for r in zeilen if r["hammer"] or r["umkehrkerze"]]
    md = [
        "# Marktdaten", "",
        f"_Erstellt {jetzt:%Y-%m-%d %H:%M} UTC. {len(zeilen)} Werte, "
        f"Fenster {FENSTER_TAGE} Kalendertage. EUR/USD {fx}._", "",
        "Reiner Datenabzug. Knock-out-Schwellen, Positionsgroessen und "
        "Regelpruefung werden bewusst NICHT hier gerechnet - sie aendern "
        "sich staendig und wuerden diese Datei pflegebeduerftig machen.",
        "", "Vollstaendige Daten: `docs/marktdaten.csv`", "",
    ]
    if zurueck:
        md += [
            f"> **Standwarnung: {len(zurueck)} von {len(aktien)} Aktien "
            f"haengen zurueck.** Neuester Handelstag {neuester}. Fuer die "
            "folgenden Werte gelten Kurs, ATR, RSI und Tiefs NICHT fuer "
            "diesen Tag. Die Spalte `stand_zurueck` in der CSV markiert "
            "sie ebenfalls.", ">",
            "> | Wert | letzte Kerze |", "> |---|---|",
        ] + [f"> | {r['ticker']} | {r['datum']} |"
             for r in sorted(zurueck, key=lambda x: (x["datum"], x["ticker"]))]
        md += [""]
    md += [
        "## Kerzensignale von gestern", "",
        "| Wert | Kurs | Hammer | hoeheres Hoch | Umkehrkerze | RSI |",
        "|---|---|---|---|---|---|",
    ]
    for r in sig:
        md.append(f"| {r['name']} ({r['ticker']}) | {r['kurs']} | "
                  f"{'ja' if r['hammer'] else '-'} | "
                  f"{'ja' if r['hoeheres_hoch'] else '-'} | "
                  f"{'ja' if r['umkehrkerze'] else '-'} | {r['rsi14']} |")
    if not sig:
        md.append("| _keine_ | | | | | |")
    if fehler:
        md += ["", "## Ohne Daten", "", ", ".join(fehler)]
    md += ["", "---", "",
           "_Kursdaten von Yahoo Finance ueber yfinance. Bei Spot-Tickern "
           "(Edelmetalle, Waehrungen) liefert Yahoo kein Volumen - die "
           "Volumenspalten bleiben dort leer. Keine Anlageberatung._"]
    with open(MD_AUS, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Geschrieben: {MD_AUS}")


if __name__ == "__main__":
    main()
