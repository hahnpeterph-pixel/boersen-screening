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
import yfinance as yf

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
    (["KC=F"], "Kaffee", "Future"),
    (["CC=F"], "Kakao", "Future"),
    (["SB=F"], "Zucker", "Future"),
]

WAEHRUNG = [(["EURUSD=X"], "EUR/USD", "Spot")]

# ── Aktien: NASDAQ-100, Dow 30, DAX 40. Statisch, aendert sich selten.
# Am 21.08.2026 entfernt, weil bei Yahoo keine Daten mehr (uebernommen
# oder delistet): ANSS, EA, WBA, 1COV.DE.
US = """AAPL ABNB ADBE ADI ADP ADSK AEP AMAT AMD AMGN AMZN ARM ASML AVGO
AXP AZN BA BIIB BKNG BKR CAT CDNS CDW CEG CHTR CMCSA COST CPRT CRM CRWD CSCO
CSGP CSX CTAS CTSH DASH DDOG DIS DXCM EXC FANG FAST FTNT GEHC GILD GOOG
GOOGL GS HD HON IBM IDXX ILMN INTC INTU ISRG JNJ JPM KDP KHC KLAC KO LIN LRCX
LULU MAR MCD MCHP MDB MDLZ MELI META MMM MNST MRK MRNA MRVL MSFT MU NFLX NKE
NVDA NXPI ODFL ON ORCL ORLY PANW PAYX PCAR PDD PEP PG PLTR PYPL QCOM REGN ROP
ROST SBUX SHW SNPS SPGI TEAM TMUS TRV TSLA TTD TTWO TXN UNH V VRSK VRTX VZ
WBD WDAY WMT XEL ZS""".split()

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
    try:
        df = yf.Ticker(ticker).history(period="400d", interval="1d",
                                       auto_adjust=False)
    except Exception as e:
        print(f"  {ticker}: Abruf fehlgeschlagen ({e})")
        return None
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < 30:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


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


def swing_tiefs(df, fenster=True):
    """Tiefs nach der Umkehr-Regel (ab 22.08.2026, ersetzt die alte 3-links-
    3-rechts-Regel).

    Ein Tief ist das Ende einer Abwaertsstrecke. Es zaehlt in dem Moment, in
    dem der Kurs das HOCH der Tiefkerze ueberschreitet - dann ist die Umkehr
    belegt. Danach laeuft eine Aufwaertsstrecke, bis der Kurs das TIEF der
    Hoechstkerze unterschreitet; ab dort wird das naechste Tief gesucht.

    Der Unterschied zur alten Regel ist praktisch: dort musste ein Tief drei
    Handelstage ueberstehen, bevor es sichtbar wurde. Genau in diesen drei
    Tagen will man aber kaufen - nah am frischen Tief. Hier reicht ein
    einziger Tag mit einem Hoch ueber dem Hoch der Tiefkerze.

    Solange es abwaerts geht, gilt immer das TIEFSTE Tief der Strecke. Ein
    hoeheres Zwischentief faellt damit heraus, sobald ein tieferes folgt,
    bevor die Umkehr belegt ist.

    Gerechnet wird auf abgeschlossenen Tageskerzen - beim Morgenlauf um
    04:17 MESZ ist die letzte Zeile die abgeschlossene US-Sitzung des
    Vortags. Laeuft das Skript waehrend der US-Sitzung, ist die letzte
    Kerze noch offen und das Ergebnis vorlaeufig.

    Das juengste Tief, dessen Kerzenhoch noch nicht ueberschritten wurde,
    wird als unbestaetigt mitgegeben (best=0).
    """
    hoch, tief = df["High"].values, df["Low"].values
    daten = df.index
    vols = df["Volume"].values if "Volume" in df.columns else [None] * len(df)
    grenze = daten[-1] - pd.Timedelta(days=FENSTER_TAGE)

    treffer = []
    richtung = "ab"      # wir starten in einer Abwaertsstrecke
    kandidat = 0         # tiefstes Tief der laufenden Abwaertsstrecke
    gipfel = 0           # hoechstes Hoch der laufenden Aufwaertsstrecke

    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i          # neues, tieferes Tief - das alte faellt raus
            elif hoch[i] > hoch[kandidat]:
                treffer.append({"i": kandidat, "datum": daten[kandidat],
                                "tief": float(tief[kandidat]), "vol": vols[kandidat],
                                "best": True})
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i            # Aufwaertsstrecke laeuft weiter
            elif tief[i] < tief[gipfel]:
                richtung, kandidat = "ab", i

    # Das laufende, noch nicht belegte Tief mitgeben - unbestaetigt.
    if richtung == "ab" and not any(t["i"] == kandidat for t in treffer):
        treffer.append({"i": kandidat, "datum": daten[kandidat],
                        "tief": float(tief[kandidat]), "vol": vols[kandidat],
                        "best": False})

    if not fenster:
        return sorted(treffer, key=lambda t: t["datum"])
    treffer = [t for t in treffer if t["datum"] >= grenze]
    treffer.sort(key=lambda t: t["datum"], reverse=True)
    return treffer


def swing_tiefs_alle(df):
    """Alle Swing-Tiefs der Historie, chronologisch - ohne 90-Tage-Fenster.

    Die Tiefserie kann laenger zurueckreichen als das Fenster: bei Cadence
    begann sie am 05.06.2026, also 78 Tage vor dem Lauf. Wird hier auf 90
    Tage gekuerzt, faellt der Anfang irgendwann still weg und die Serie
    wird zu kurz gezaehlt.
    """
    return swing_tiefs(df, fenster=False)


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
    zum letzten Tief der Abwaertsserie. Ohne dasselbe Hoch als Anker ist
    ein Soll/Ist-Vergleich wertlos - die Falltiefe vom 60-Tage-Hoch misst
    etwas anderes.

    Ermittelt wird deshalb: das bestaetigte Hoch, das der laufenden Serie
    absteigender Tiefs vorausging, und daraus Tiefe (in ATR) und Dauer
    (in Handelstagen) bis zum juengsten Tief.

    Die Hochs entstehen nach derselben Umkehr-Regel wie die Tiefs, nur
    gespiegelt: ein Hoch gilt, sobald der Kurs das TIEF der Hoechstkerze
    unterschreitet.
    """
    if not tiefe_liste or a in (None, 0):
        return None, None, None

    hoch, tief = df["High"].values, df["Low"].values
    hochs = []
    richtung, kandidat, gipfel = "ab", 0, 0
    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i
            elif hoch[i] > hoch[kandidat]:
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i
            elif tief[i] < tief[gipfel]:
                hochs.append(gipfel)
                richtung, kandidat = "ab", i

    # Serie absteigender Tiefs, vom juengsten rueckwaerts. tiefe_liste ist
    # nach Datum absteigend sortiert, das juengste steht vorn.
    serie = [tiefe_liste[0]]
    for k in range(1, len(tiefe_liste)):
        if tiefe_liste[k]["tief"] > serie[-1]["tief"]:
            serie.append(tiefe_liste[k])
        else:
            break
    beginn = serie[-1]["i"]

    davor = [i for i in hochs if i < beginn]
    if not davor:
        return None, None, None
    h_i = davor[-1]
    juengstes = tiefe_liste[0]
    tiefe_atr = (float(hoch[h_i]) - juengstes["tief"]) / a
    dauer = juengstes["i"] - h_i
    return float(hoch[h_i]), round(tiefe_atr, 2), int(dauer)


def swing_hochs(df):
    """Bestaetigte Swing-Hochs, chronologisch.

    Spiegelbild zu swing_tiefs und dieselbe Zustandsmaschine: ein Hoch gilt,
    sobald der Kurs das TIEF der Hoechstkerze unterschreitet. Gebraucht wird
    das fuer den Abbruch der Tiefserie - die Abwaertsstrecke endet erst,
    wenn eine Erholung ein vorangegangenes Hoch ueberschreitet.
    """
    hoch, tief = df["High"].values, df["Low"].values
    daten = df.index
    treffer = []
    richtung, kandidat, gipfel = "ab", 0, 0
    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i
            elif hoch[i] > hoch[kandidat]:
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i
            elif tief[i] < tief[gipfel]:
                treffer.append({"i": gipfel, "datum": daten[gipfel],
                                "hoch": float(hoch[gipfel])})
                richtung, kandidat = "ab", i
    return treffer


def tiefserie_neu(df, variante="vorheriges_hoch"):
    """Laufende Abwaertsserie nach der Regel vom 22.08.2026.

    Gezaehlt werden NUR neue Tiefststaende seit dem letzten Hoch. Ein Tief,
    das ueber dem laufenden Tiefstand liegt, zaehlt nicht mit - die Serie
    laeuft weiter. Beendet ist die Strecke erst, wenn eine Erholung ein
    vorangegangenes Hoch ueberschreitet.

    Die alte Zaehlung (tiefserie) brach ab, sobald ein Tief hoeher lag als
    das juengere, und kam bei Cadence am 22.08.2026 auf 3 statt 5.

    variante:
      "vorheriges_hoch"  Serie endet, wenn ein Hoch das unmittelbar
                         vorangegangene Hoch ueberschreitet (Dow, Standard).
      "starthoch"        Serie endet erst ueber dem Hoch, an dem die
                         Strecke begonnen hat - traeger.

    Beide laufen parallel mit, bis sich an echten Trades zeigt, welche
    Variante traegt. Rueckgabe: (anzahl, startdatum, tiefstwert).
    """
    tiefs = sorted(swing_tiefs_alle(df), key=lambda t: t["datum"])
    hochs = swing_hochs(df)
    if not tiefs:
        return "", "", ""

    punkte = ([{"art": "T", **t} for t in tiefs] +
              [{"art": "H", **h} for h in hochs])
    punkte.sort(key=lambda p: (p["datum"], 0 if p["art"] == "T" else 1))

    anzahl, start, lauf_min = 0, None, None
    letztes_hoch, starthoch = None, None

    for p in punkte:
        if p["art"] == "H":
            grenze = starthoch if variante == "starthoch" else letztes_hoch
            if grenze is not None and p["hoch"] > grenze:
                anzahl, start, lauf_min = 0, None, None
                starthoch = None
            letztes_hoch = p["hoch"]
            if starthoch is None:
                starthoch = p["hoch"]
        else:
            if lauf_min is None or p["tief"] < lauf_min:
                anzahl += 1
                lauf_min = p["tief"]
                if start is None:
                    start = p["datum"]
    if not anzahl:
        return "", "", ""
    return anzahl, f"{start:%Y-%m-%d}", round(lauf_min, 4)


def tiefserie(tiefe_liste):
    """Wie viele Tiefs hat die LAUFENDE absteigende Serie?

    Die Excel leitet das bisher aus tief1 bis tief3 ab und ist damit bei
    drei gedeckelt - eine laengere Treppe sieht sie nicht. Hier wird
    direkt gezaehlt, ueber alle Tiefs im Fenster.

    Gezaehlt wird vom juengsten Tief rueckwaerts, solange jedes aeltere
    Tief HOEHER liegt als das juengere. Das erste hoehere beendet die
    Serie - ab dort begann die Abwaertsstrecke.
    """
    if not tiefe_liste:
        return "", ""
    serie = 1
    for k in range(1, len(tiefe_liste)):
        if tiefe_liste[k]["tief"] > tiefe_liste[k - 1]["tief"]:
            serie += 1
        else:
            break
    # Das oberste Tief der Serie mitgeben - dort begann die Treppe
    start = tiefe_liste[serie - 1]
    return serie, f"{start['datum']:%Y-%m-%d}"


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


def umkehrkerze(df):
    """Bearishes Warnsignal: Schluss unter Eroeffnung UND unter
    Vortageshoch UND unter Vortagestief."""
    h, v = df.iloc[-1], df.iloc[-2]
    return bool(h["Close"] < h["Open"] and h["Close"] < v["High"]
                and h["Close"] < v["Low"])


def z(x, nk=4):
    return "" if x is None else f"{round(float(x), nk)}"


# ── Hauptlauf ──────────────────────────────────────────────────────
def main():
    jetzt = datetime.now(timezone.utc)
    zeilen, fehler = [], []

    for kette, name, art in UNIVERSUM:
        df, ticker = None, kette[0]
        for kandidat in kette:
            df = kerzen(kandidat)
            if df is not None:
                ticker = kandidat
                break
        if df is None:
            fehler.append(" oder ".join(kette))
            print(f"  {'/'.join(kette)}: keine Daten")
            continue
        if ticker != kette[0]:
            print(f"  {kette[0]} leer -> Rueckfall auf {ticker}")

        a = atr(df)
        tr = swing_tiefs(df)
        kurs = float(df["Close"].iloc[-1])
        letzte = df.iloc[-1]
        mitvol = ticker not in OHNE_VOLUMEN

        r = {
            "ticker": ticker, "name": name, "art": art,
            "wunschticker": kette[0],
            "rueckfall": int(ticker != kette[0]),
            "datum": f"{df.index[-1]:%Y-%m-%d}",
            "kurs": z(kurs), "open": z(letzte["Open"]),
            "high": z(letzte["High"]), "low": z(letzte["Low"]),
            "atr14": z(a), "rsi14": z(rsi(df), 2),
            "ema50": z(ema(df, 50)), "ema200": z(ema(df, 200)),
            "hammer": int(hammer(df, a)),
            "hoeheres_hoch": int(hoeheres_hoch(df)),
            "umkehrkerze": int(umkehrkerze(df)),
            "hoch60": z(hoch60(df)),
            "vol_druck5": (z(vol_druck5(df), 2) if mitvol else ""),
        }
        anzahl, takt = tief_takt(tr, df)
        r["tiefs_anzahl"] = anzahl
        r["tiefs_abstand"] = z(takt, 1) if takt is not None else ""
        serie, serie_start, serie_tief = tiefserie_neu(df)
        r["tiefs_serie"] = serie
        r["tiefs_serie_start"] = serie_start
        r["tiefs_serie_tief"] = serie_tief
        s2, s2_start, _ = tiefserie_neu(df, "starthoch")
        r["tiefs_serie_starthoch"] = s2
        r["tiefs_serie_starthoch_start"] = s2_start
        alt, alt_start = tiefserie(tr)
        r["tiefs_serie_alt"] = alt
        r["tiefs_serie_alt_start"] = alt_start
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
        zeilen.append(r)
        print(f"  {ticker}: ok")

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
