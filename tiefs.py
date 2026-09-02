"""
tiefs.py - Markante Tiefs, Volumen und Pruefung der eigenen Kaufregel.

Laeuft unabhaengig von screener.py im selben GitHub-Workflow.
Schreibt docs/tiefs.md

KAUFREGEL (die eigentliche Aufgabe dieses Skripts):
Die Knock-out-Schwelle des Scheins soll UNTER einem markanten Tief des
Basiswerts liegen - mit etwas Abstand, damit ein erneuter Test dieses
Tiefs den Schein nicht sofort ausknockt.

Definition markantes Tief (Swing-Tief):
Seit 22.08.2026 die Umkehr-Regel aus tiefs_regel.py - dieselbe, mit der
marktdaten.py und phasen.py rechnen. Ein Tief zaehlt, sobald eine spaetere
Kerze das HOCH der Tiefkerze ueberschreitet. Solange es abwaerts geht,
gilt immer das TIEFSTE Tief der Strecke.

Die alte Regel (LINKS Tage davor, RECHTS Tage danach) machte ein Tief erst
nach drei ueberstandenen Handelstagen sichtbar - genau in den Tagen, in
denen gekauft wird. Die Parameter links/rechts in watchlist.json werden
nicht mehr ausgewertet und bleiben nur stehen, damit vorhandene
Konfigurationen ohne Aenderung weiterlaufen.

Massgeblich ist das JUENGSTE Tief (aktuelle Trendstruktur). Das tiefste
Tief des Fensters wird nur zur Einordnung mit ausgegeben und geht nicht
in das Urteil ein.

Ist bei einem Wert in watchlist.json ein "chart_tief" gesetzt, gilt
DIESES Tief - der Chart schlaegt das Skript. Das entspricht dem Ablauf
vor jedem Kauf: Report, dann Trade Republic, dann stock3-Chart.

Konfiguration in watchlist.json.
"""

import csv
import json
import os
from datetime import datetime, timezone

import pandas as pd

import kurse
import stand
import tiefs_regel as regel

HIER = os.path.dirname(os.path.abspath(__file__))
WATCHLIST = os.path.join(HIER, "watchlist.json")
AUSGABE = os.path.join(HIER, "docs", "tiefs.md")
RSI_SCHWELLEN = os.path.join(HIER, "docs", "rsi_schwellen.csv")

# Ab wie vielen Faellen eine wertspezifische Schwelle verwendet wird.
# Darunter greift die naechste Stufe der Fallback-Kette - siehe
# rsi_schwelle_kauf().
MIN_FAELLE_SCHWELLE = 3

STANDARD = {
    "fenster_tage": 50,
    "links": 3,
    "rechts": 3,
    "atr_tage": 14,
    "puffer_atr": 2.0,
    "knapp_ab_atr": 1.0,
    "mindestabstand_absolut": 1.0,
    "bezug": "juengstes",
    "unbestaetigtes_tief_zulassen": True,
    "einheit_euro": 150.0,
    "min_einsatz_euro": 50.0,
    "rsi_tage": 14,
    "rsi_schwelle": 70.0,
    # Nur noch Rueckfallwert: die Schwelle kommt seit 02.09.2026
    # wertspezifisch aus docs/rsi_schwellen.csv (Entscheidung 79). Diese
    # Zahl greift, wenn ein Wert dort noch gar nicht vorkommt.
    "rsi_kauf_max": 50.0,
    "hammer_lunte_faktor": 2.0,
    "hammer_koerper_oben": 0.66,
    "hammer_obere_lunte_max": 0.15,
    "hammer_min_spanne_atr": 0.8,
    "ohne_volumen": [],
    "werte": [],
}

# Ein Ticker kann mehrfach vorkommen (z.B. Microsoft und Microsoft II).
# Damit Yahoo nicht zweimal gefragt wird:
_KERZEN_CACHE = {}


def konfig_laden():
    if not os.path.exists(WATCHLIST):
        print(f"WARNUNG: {WATCHLIST} fehlt - nichts zu tun.")
        return STANDARD
    with open(WATCHLIST, encoding="utf-8") as f:
        k = json.load(f)
    for schluessel, wert in STANDARD.items():
        k.setdefault(schluessel, wert)
    return k


def rsi_schwellen_laden():
    """Wertspezifische Kauf-RSI-Schwellen aus docs/rsi_schwellen.csv
    (erzeugt von rsi_schwellen.py im woechentlichen historie.py-Lauf).

    Struktur: (ticker, position) -> (p75, faelle). Position 0 ist der
    wertweite Wert ueber alle Tiefspositionen.

    Fehlt die Datei, bleibt es beim festen Wert aus watchlist.json - eine
    ehrlich als Pauschale gekennzeichnete Zahl ist besser als eine
    geratene wertspezifische.
    """
    tab = {}
    if not os.path.exists(RSI_SCHWELLEN):
        print("WARNUNG: docs/rsi_schwellen.csv fehlt - RSI-Schwelle "
              "faellt auf den festen Wert aus watchlist.json zurueck.")
        return tab
    with open(RSI_SCHWELLEN, encoding="utf-8", newline="") as f:
        for z in csv.DictReader(f):
            try:
                tab[(z["ticker"], int(z["position"]))] = (
                    float(z["rsi_p75"]), int(z["faelle"]))
            except (KeyError, TypeError, ValueError):
                continue
    return tab


def rsi_schwelle_kauf(tab, ticker, position, standard):
    """Die Schwelle nach Entscheidung 79: p75 des RSI an den historischen
    Tiefs DIESES Wertes an GENAU DIESER Tiefsposition.

    Der RSI faellt mit jedem weiteren Tief einer Abwaertsserie
    systematisch - bei Synopsys von 62,4 an Tief 1 auf 37,2 an Tief 4.
    Eine ueber alle Positionen gepoolte Schwelle waere an Tief 1 zu
    streng und an Tief 4 zu lasch, eine feste 50 fuer alle Werte beides
    zugleich.

    Fallback-Kette, die Stufe wird im Urteilstext immer mitgefuehrt:
      1. Wert + Tiefsposition, ab MIN_FAELLE_SCHWELLE Faellen
      2. Wert, alle Tiefspositionen gepoolt
      3. der feste Wert aus watchlist.json

    Rueckgabe: (schwelle, quelle, faelle). faelle ist None auf Stufe 3.
    """
    if position:
        treffer = tab.get((ticker, int(position)))
        if treffer and treffer[1] >= MIN_FAELLE_SCHWELLE:
            return treffer[0], f"Tief {int(position)}", treffer[1]
    treffer = tab.get((ticker, 0))
    if treffer and treffer[1] >= MIN_FAELLE_SCHWELLE:
        return treffer[0], "wertweit", treffer[1]
    return standard, "Pauschale", None


def kerzen_laden(ticker, tage):
    """Durchreiche auf kurse.py. Seit 22.08.2026 holen screener.py,
    marktdaten.py und dieses Skript dieselben Kerzen aus einem Cache,
    statt sie dreimal von Yahoo zu ziehen.

    Die Periode ist bewusst fest auf 400d gesetzt statt aus "tage"
    abgeleitet - nur so treffen alle drei Skripte denselben Cache-
    Eintrag. 400 Tage decken das 50-Tage-Fenster hier mit Abstand ab.
    """
    return kurse.kerzen(ticker, period="400d")


def swing_tiefs(df, links, rechts, fenster_tage, unbestaetigt=False):
    """Swing-Tiefs nach der gemeinsamen Regel aus tiefs_regel.py.

    Bis 22.08.2026 rechnete dieses Skript als einziges noch mit der alten
    3-links-3-rechts-Regel: ein Tief wurde erst nach drei ueberstandenen
    Handelstagen sichtbar - genau in den Tagen, in denen gekauft wird.
    Dadurch meldete docs/tiefs.md andere Tiefs als docs/marktdaten.csv.

    links und rechts werden nicht mehr ausgewertet. Sie bleiben in der
    Signatur und in watchlist.json stehen, damit vorhandene Konfigurationen
    ohne Aenderung weiterlaufen.
    """
    treffer = regel.swing_tiefs(df, fenster_tage=fenster_tage,
                                unbestaetigt=unbestaetigt)
    # Feldnamen angleichen: das Regelmodul liefert i/vol/best, dieses Skript
    # arbeitet historisch mit index/volumen/bestaetigt.
    for t in treffer:
        t["index"] = t["i"]
        t["volumen"] = t.get("vol")
        t["bestaetigt"] = bool(t.get("best"))
    return treffer


def atr(df, tage=14):
    """Average True Range - mittlere Tagesschwankung inkl. Kursluecken."""
    if df is None or len(df) < tage + 1:
        return None
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vortag = schluss.shift(1)
    tr = pd.concat([hoch - tief, (hoch - vortag).abs(), (tief - vortag).abs()],
                   axis=1).max(axis=1)
    wert = tr.tail(tage).mean()
    return None if pd.isna(wert) else float(wert)


def rsi(df, tage=14):
    """RSI nach Wilder-Glaettung (Standardmethode, z.B. stock3, TradingView)."""
    if df is None or len(df) < tage + 1:
        return None
    delta = df["Close"].diff()
    gewinn = delta.clip(lower=0)
    verlust = -delta.clip(upper=0)
    avg_gewinn = gewinn.ewm(alpha=1 / tage, adjust=False).mean()
    avg_verlust = verlust.ewm(alpha=1 / tage, adjust=False).mean()
    letzter_verlust = avg_verlust.iloc[-1]
    if letzter_verlust == 0:
        return 100.0
    rs = avg_gewinn.iloc[-1] / letzter_verlust
    wert = 100 - (100 / (1 + rs))
    return None if pd.isna(wert) else float(wert)


def umkehrkerze(df):
    """Starke bearishe Umkehrkerze: Schlusskurs unter Eroeffnung UND unter
    Vortageshoch UND unter Vortagestief. Unabhaengig vom RSI, weil sie auch
    ohne ueberkauften RSI ein Warnsignal ist (z.B. Gap-down nach Meldung)."""
    if df is None or len(df) < 2:
        return None
    heute, vortag = df.iloc[-1], df.iloc[-2]
    return bool(heute["Close"] < heute["Open"] and
                heute["Close"] < vortag["High"] and
                heute["Close"] < vortag["Low"])


def hammer(df, a, k):
    """Hammer-Kerze als Kaufsignal.

    Lange untere Lunte, kleiner Koerper oben, kaum obere Lunte, und die
    Kerze muss eine relevante Groesse haben - sonst ist jede unauffaellige
    Seitwaertskerze ein Treffer. Vorher soll es abwaerts gegangen sein.
    """
    if df is None or len(df) < 6:
        return False
    z = df.iloc[-1]
    o, h, t, c = float(z["Open"]), float(z["High"]), float(z["Low"]), float(z["Close"])
    spanne = h - t
    if spanne <= 0:
        return False
    koerper = abs(c - o)
    unten = min(o, c) - t
    oben = h - max(o, c)
    if a and spanne < float(k["hammer_min_spanne_atr"]) * a:
        return False
    if koerper > 0 and unten < float(k["hammer_lunte_faktor"]) * koerper:
        return False
    if (max(o, c) - t) < float(k["hammer_koerper_oben"]) * spanne:
        return False
    if oben > float(k["hammer_obere_lunte_max"]) * spanne:
        return False
    return bool(c < float(df["Close"].iloc[-6]))


def hoeheres_hoch(df):
    """Zweites Kaufsignal: Tageshoch ueber dem Hoch des Vortags."""
    if df is None or len(df) < 2:
        return False
    return bool(float(df["High"].iloc[-1]) > float(df["High"].iloc[-2]))


def urteil_kauf(sig_hammer, sig_hoch, r, rsi_max, kurs, trigger,
                quelle="Pauschale", faelle=None):
    """Der RSI ueber der Schwelle ist eine WARNUNG, keine Sperre: der Wert
    bleibt Kandidat und taucht weiter in Block 1 auf. Die Ampel steht auf
    '!' statt '+', damit der Chart-Blick vor dem Kauf mit dieser Frage im
    Kopf passiert - nicht, damit der Wert aussortiert wird."""
    teile = []
    if sig_hammer:
        teile.append("Hammer")
    if sig_hoch:
        teile.append("hoeheres Hoch")
    marke = trigger is not None and kurs is not None and kurs <= trigger
    if marke:
        teile.append("Marke erreicht")
    if not teile:
        return "warten", "-"
    text = " + ".join(teile)
    herkunft = quelle + (f", n={faelle}" if faelle else "")
    if r is not None and r > rsi_max:
        return (f"{text} — CHART PRUEFEN, aber RSI {de(r, 1)} ueber "
                f"{de(rsi_max, 1)} ({herkunft})"), "!"
    return f"{text} — CHART PRUEFEN", "+"


def urteil_ueberhitzt(rsi_wert, schwelle, kerze):
    if kerze:
        return "VERKAUFSSIGNAL (Umkehrkerze)"
    if rsi_wert is None:
        return "k.A."
    if rsi_wert >= schwelle:
        return "ueberhitzt (RSI)"
    if rsi_wert >= schwelle - 10:
        return "beobachten"
    return "unauffaellig"


def ampel_ueberhitzt(rsi_wert, schwelle, kerze):
    if kerze:
        return "X"
    if rsi_wert is None:
        return "-"
    if rsi_wert >= schwelle:
        return "!!"
    if rsi_wert >= schwelle - 10:
        return "!"
    return "+"


def durchschnittsvolumen(df, bis_index, tage=20):
    if "Volume" not in df.columns:
        return None
    teil = df["Volume"].iloc[max(0, bis_index - tage):bis_index].dropna()
    return None if teil.empty else float(teil.mean())


def abstand(tief, ko):
    """Wie weit liegt der KO unter dem Tief? Positiv = KO darunter = gut."""
    if tief is None or ko is None or tief == 0:
        return None
    return (tief - ko) / tief * 100.0


def urteil(einheiten, soll, knapp):
    """einheiten = Abstand KO zum Tief, gemessen in ATR."""
    if einheiten is None:
        return "k.A."
    if einheiten < 0:
        return "REGELBRUCH (KO ueber Tief)"
    if einheiten < knapp:
        return "zu knapp"
    if einheiten < soll:
        return "knapp"
    return "OK"


def ampel(einheiten, soll, knapp):
    if einheiten is None:
        return "-"
    if einheiten < 0:
        return "X"
    if einheiten < knapp:
        return "!!"
    if einheiten < soll:
        return "!"
    return "+"


def einsatz(einheiten, soll, einheit, minimum, regel1_ok):
    """Regel 2+3: Mindesteinsatz bei Puffer ~0, volle Einheit ab SOLL x ATR,
    dazwischen linear."""
    if not regel1_ok:
        return 0.0, 0.0, "Regel 1 verletzt - kein Kauf"
    if einheiten is None:
        return None, None, "keine ATR-Daten"
    faktor = max(0.0, min(1.0, einheiten / soll))
    betrag = round(minimum + (einheit - minimum) * faktor, 2)
    return betrag, faktor, ""


def de(x, nk=2):
    if x is None:
        return "k.A."
    return f"{x:,.{nk}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def stk(x):
    if x is None:
        return "k.A."
    if x >= 1_000_000:
        return de(x / 1_000_000, 1) + " Mio."
    return de(x / 1_000, 0) + " Tsd."


def stand_hinweis(werte):
    """Melden, wenn dieses Skript aelter rechnet als marktdaten.csv.

    Vergleicht je Wert das Datum der letzten Kerze, auf der hier gerechnet
    wurde, mit dem Stand in docs/marktdaten.csv. Weicht etwas ab, steht es
    oben im Bericht - dann weiss man, dass tiefs.md und marktdaten.csv
    gerade nicht denselben Tag meinen.
    """
    bekannt = stand.vergleichsstaende(os.path.join(HIER, "docs",
                                                   "marktdaten.csv"))
    if not bekannt:
        return []
    aelter = []
    for w in werte:
        t = w.get("ticker")
        df = kerzen_laden(t, 400)
        if df is None or df.empty:
            continue
        eigen = str(df.index[-1].date())
        gespeichert = bekannt.get(t, "")
        if gespeichert and eigen < gespeichert:
            aelter.append((t, eigen, gespeichert))
    if not aelter:
        return []
    L = ["", f"> **Aelter als marktdaten.csv: {len(aelter)} Werte.** Yahoo "
         f"lieferte fuer diesen Lauf eine aeltere letzte Kerze als beim "
         f"Schreiben von marktdaten.csv. Dort bleibt der bessere Stand "
         f"erhalten, hier nicht - dieses Skript rechnet jedes Mal neu aus "
         f"den Kerzen. Die Angaben zu diesen Werten sind also aelter als "
         f"im Report:", ""]
    for t, eigen, gespeichert in sorted(aelter):
        L.append(f"> - {t}: hier {eigen}, marktdaten.csv {gespeichert}")
    L.append("")
    return L


def main():
    k = konfig_laden()
    werte = k["werte"]
    if not werte:
        print("Keine Werte in watchlist.json - Abbruch.")
        return

    soll = float(k["puffer_atr"])
    knapp = float(k["knapp_ab_atr"])
    atr_tage = int(k["atr_tage"])
    rsi_tage = int(k.get("rsi_tage", 14))
    rsi_schwelle = float(k.get("rsi_schwelle", 70.0))
    rsi_kauf_max = float(k.get("rsi_kauf_max", 50.0))
    rsi_tab = rsi_schwellen_laden()
    ohne_vol = set(k.get("ohne_volumen", []))
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    kopf = [
        "# Tiefs, Volumen und Kaufregel-Check",
        "",
        f"_Erstellt {jetzt}. Fenster: letzte {k['fenster_tage']} Kalendertage. "
        f"Tiefs nach der Umkehr-Regel (tiefs_regel.py): ein Tief zaehlt, "
        f"sobald eine spaetere Kerze das Hoch der Tiefkerze ueberschreitet. "
        f"Solange es abwaerts geht, gilt das tiefste Tief der Strecke. "
        f"Gerechnet wird auf abgeschlossenen Tageskerzen._",
        "",
        "## Kaufregel",
        "",
        f"Die Knock-out-Schwelle soll **unter** einem markanten Tief liegen, mit "
        f"mindestens **{de(soll, 1)} x ATR({atr_tage})** Abstand. Die ATR ist die "
        f"mittlere Tagesschwankung des Basiswerts - ein fester Prozentsatz taugt "
        f"nicht, weil er bei ruhigen und bei volatilen Werten voellig "
        f"Unterschiedliches bedeutet.",
        "",
        "Massgeblich ist das **juengste** Tief. Das tiefste Tief des Fensters "
        "steht nur zur Einordnung mit dabei und geht nicht in das Urteil ein.",
        "",
        "_Ist in `watchlist.json` ein `chart_tief` gesetzt, gilt dieses statt des "
        "automatisch gefundenen - im Report mit 'Chart' markiert. Der Chart "
        "schlaegt das Skript._",
        "",
        ("_Als juengstes Tief zaehlt auch das Tief des zuletzt abgeschlossenen "
         "Tages, sofern es unter den Vortagen liegt - im Report mit 'unbest.' "
         "markiert, weil die Bestaetigung durch Folgetage noch aussteht._"
         if k.get("unbestaetigtes_tief_zulassen", True) else
         "_Es zaehlen nur durch Folgetage bestaetigte Tiefs._"),
        "",
        f"**Regel 1 (harte Sperre):** Der KO muss mindestens "
        f"{de(k['mindestabstand_absolut'], 2)} unter dem Tief liegen - in der "
        f"Waehrung des Basiswerts. Verhindert nur, dass der KO auf dem Tief "
        f"klebt; als alleiniges Mass taugt sie nicht.",
        "",
        f"**Regel 2+3 (Positionsgroesse):** {de(k['min_einsatz_euro'], 0)} EUR bei "
        f"gerade noch erfuelltem Puffer, {de(k['einheit_euro'], 0)} EUR ab "
        f"{de(soll, 1)} x ATR, dazwischen linear. Bezugstief ist das "
        f"**{k.get('bezug', 'juengstes')}** Tief.",
        "",
        "### Bestehende Positionen",
        "",
        "| Wert | KO | juengstes Tief | tiefstes Tief | Abstand | Regel 1 | Urteil | |",
        "|---|---|---|---|---|---|---|---|",
    ]

    empfehlung = [
        "", "### Empfohlene KO-Schwelle", "",
        f"Tief minus {de(soll, 1)} x ATR. Die Hebelangabe ist das, was sich bei diesem "
        f"KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel "
        f"zulaesst.",
        "",
        "| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |",
        "|---|---|---|---|---|---|---|",
    ]

    groesse = [
        "", "### Positionsgroesse nach Regel 2", "",
        "| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |",
        "|---|---|---|---|---|---|",
    ]

    ueberhitzung = [
        "", "### Ueberhitzung — Verkaufssignal bestehender Positionen", "",
        f"Nur fuer Positionen mit `typ: Bestand`. RSI({rsi_tage}) nach "
        f"Wilder-Glaettung; ab {de(rsi_schwelle, 0)} gilt der Basiswert als "
        f"ueberkauft. Die Umkehrkerze (Schlusskurs unter Eroeffnung UND unter "
        f"Vortageshoch UND unter Vortagestief) ist ein eigenstaendiges "
        f"Warnsignal, unabhaengig vom RSI-Stand.",
        "",
        "| Wert | RSI | Umkehrkerze | Urteil | |",
        "|---|---|---|---|---|",
    ]

    kandidaten = [
        "", "### Kaufkandidaten — Umkehr abwarten", "",
        f"Umkehr = Hammer-Kerze ODER hoeheres Hoch als der Vortag. "
        f"Die RSI-Schwelle ist wertspezifisch (Entscheidung 79): p75 des "
        f"RSI an den historischen Tiefs dieses Wertes an der aktuellen "
        f"Tiefsposition, aus docs/rsi_schwellen.csv. Ist diese Zelle mit "
        f"weniger als {MIN_FAELLE_SCHWELLE} Faellen besetzt, gilt der "
        f"wertweite Wert ueber alle Tiefspositionen, danach die Pauschale "
        f"{de(rsi_kauf_max, 0)}. Die Spalte Schwelle nennt die verwendete "
        f"Stufe. RSI darueber ist eine WARNUNG, keine Sperre - der Wert "
        f"bleibt Kandidat. "
        f"Der KO-Vorschlag ist Tief minus {de(soll, 1)} x ATR - die tatsaechliche "
        f"Schwelle waehlst du erst nach der Kaufentscheidung in Trade Republic.",
        "",
        "| Wert | Kurs | Marke | Abstand | Tief | ATR | RSI | Schwelle | "
        "KO-Vorschlag | Einsatz | Signal | |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    excel = [
        "", "## Fuer die Excel — Blatt 'Report'", "",
        "_Diese Zeilen in die gelben Spalten uebertragen. Reihenfolge wie dort._",
        "",
        "| Ticker | Kurs | ATR(14) | RSI | Chart-Tief | Datum Tief | Vol. rel. |",
        "|---|---|---|---|---|---|---|",
    ]

    detail = ["", "## Tiefs im Detail mit Volumen", "",
              "| Wert | Datum | Tief | Volumen | rel. zu \u00d8 20 T | Tief -> KO |",
              "|---|---|---|---|---|---|"]
    warnungen = []
    ueberhitzt_warnungen = []
    kauf_warnungen = []
    fehlend = []
    _excel_doppelt = set()  # ein Ticker nur einmal, auch bei zwei Tranchen

    for eintrag in werte:
        ticker = eintrag["ticker"]
        name = eintrag.get("name", ticker)
        ko = eintrag.get("ko")
        art = eintrag.get("typ", "Bestand")
        etikett = f"{name} ({ticker})" + ("" if art == "Bestand" else f" _{art}_")
        print(f"{ticker} ...")

        df = kerzen_laden(ticker, k["fenster_tage"])
        treffer = swing_tiefs(df, k["links"], k["rechts"], k["fenster_tage"],
                              bool(k.get("unbestaetigtes_tief_zulassen", True)))
        a = atr(df, atr_tage)
        kurs = float(df["Close"].iloc[-1]) if df is not None and len(df) else None

        if art != "Bestand":
            r = rsi(df, rsi_tage)
            # Position des aktuellen Tiefs in der laufenden Abwaertsserie -
            # dieselbe Zaehlung wie in der Fortsetzungskette. Leer, wenn
            # keine Serie laeuft; dann greift die wertweite Stufe.
            pos_akt = regel.tiefserie(df)[0]
            grenze, quelle, faelle = rsi_schwelle_kauf(
                rsi_tab, ticker, pos_akt, rsi_kauf_max)
            sig_h = hammer(df, a, k)
            sig_hh = hoeheres_hoch(df)
            trig = eintrag.get("trigger_kurs")
            sig_text, sig_ampel = urteil_kauf(sig_h, sig_hh, r, grenze,
                                              kurs, trig, quelle, faelle)
            ct = eintrag.get("chart_tief")
            basis = ct if ct is not None else (
                treffer[0]["tief"] if treffer else None)
            ko_vor = (basis - soll * a) if (basis is not None and a) else None
            if ko_vor is not None and basis:
                puffer_k = (basis - ko_vor) / a
                betrag_k, _, _ = einsatz(puffer_k, soll, float(k["einheit_euro"]),
                                         float(k["min_einsatz_euro"]), True)
            else:
                betrag_k = None
            ab_marke = (None if (trig is None or kurs is None)
                        else (kurs - trig) / trig * 100.0)
            kandidaten.append(
                f"| {etikett} | {de(kurs)} | {de(trig) if trig else '-'} | "
                f"{de(ab_marke, 1) + ' %' if ab_marke is not None else '-'} | "
                f"{de(basis) if basis else 'k.A.'} | {de(a)} | "
                f"{de(r, 1) if r is not None else 'k.A.'} | "
                f"{de(grenze, 1)} ({quelle}"
                f"{f', n={faelle}' if faelle else ''}) | "
                f"{de(ko_vor) if ko_vor else '-'} | "
                f"**{de(betrag_k, 2) if betrag_k else '-'} EUR** | "
                f"{sig_text} | {sig_ampel} |")
            # Bis 02.09.2026 stand hier nur "+": ein Wert mit RSI ueber der
            # Schwelle bekam die Ampel "!" und verschwand damit aus der
            # Pruefliste - er fiel praktisch aus Block 1, obwohl der RSI
            # laut Regel nur warnen soll. Beide Ampeln kommen jetzt in die
            # Liste, die Warnung steht im Text.
            if sig_ampel in ("+", "!"):
                kauf_warnungen.append(
                    f"- **{name}**{' _(RSI-Warnung)_' if sig_ampel == '!' else ''}"
                    f": {sig_text}. Kurs {de(kurs)}, "
                    f"Marke {de(trig) if trig else '-'}.")
            if ticker in _excel_doppelt:
                continue
            _excel_doppelt.add(ticker)
            if ct is not None:
                excel.append(
                    f"| {ticker} | {de(kurs)} | {de(a)} | "
                    f"{de(r, 1) if r is not None else 'k.A.'} | {de(ct)} | "
                    f"{eintrag.get('chart_tief_datum', '-')} | - |")
            else:
                dat = f"{treffer[0]['datum']:%Y-%m-%d}" if treffer else "-"
                excel.append(
                    f"| {ticker} | {de(kurs)} | {de(a)} | "
                    f"{de(r, 1) if r is not None else 'k.A.'} | "
                    f"{de(basis) if basis else '-'} | {dat} | - |")
            continue

        if art == "Bestand":
            r = rsi(df, rsi_tage)
            kerze = umkehrkerze(df)
            u_urteil = urteil_ueberhitzt(r, rsi_schwelle, kerze)
            ueberhitzung.append(
                f"| {etikett} | {de(r, 1) if r is not None else 'k.A.'} | "
                f"{'ja' if kerze else ('nein' if kerze is not None else 'k.A.')} | "
                f"{u_urteil} | {ampel_ueberhitzt(r, rsi_schwelle, kerze)} |")
            if kerze or (r is not None and r >= rsi_schwelle):
                grund = "Umkehrkerze" if kerze else f"RSI {de(r, 1)}"
                ueberhitzt_warnungen.append(f"- **{name}**: {grund} — {u_urteil}.")

        if not treffer:
            # Zwei sehr verschiedene Faelle sauber trennen: gar keine
            # Kursdaten (Yahoo liefert fuer XAUUSD=X seit Monaten nichts,
            # delistete Werte fallen ueber Nacht aus) oder Daten vorhanden,
            # aber kein Tief im Fenster. Frueher stand in beiden Faellen
            # derselbe Text - und der verwies auf links/rechts, die seit
            # der Umstellung auf die Umkehr-Regel gar nicht mehr gelten.
            if df is None or len(df) < 2:
                kopf.append(f"| {etikett} | {de(ko)} | KEINE KURSDATEN "
                            f"| | | - | k.A. | - |")
                fehlend.append(
                    f"- **{name}** ({ticker}): keine Kursdaten von Yahoo. "
                    f"Der Wert wird uebersprungen, alle Angaben fehlen. "
                    f"Bei Edelmetallen liegt es am Spot-Ticker - der Future "
                    f"waere ein Ersatz, notiert aber hoeher (Contango), "
                    f"deshalb wird hier NICHT automatisch umgeschaltet: "
                    f"die KO-Pruefung wuerde sonst falsch rechnen.")
            else:
                kopf.append(f"| {etikett} | {de(ko)} | kein Swing-Tief im Fenster "
                            f"| | | - | k.A. | - |")
                fehlend.append(
                    f"- **{name}**: kein Swing-Tief in den letzten "
                    f"{k['fenster_tage']} Kalendertagen. Der Wert laeuft seit "
                    f"Wochen aufwaerts, ohne dass eine Abwaertsstrecke "
                    f"begonnen haette.")
            continue

        juengstes = treffer[0]
        tiefstes = min(treffer, key=lambda t: t["tief"])
        bezug = juengstes if k.get("bezug", "juengstes") == "juengstes" else tiefstes

        ct = eintrag.get("chart_tief")
        aus_chart = ct is not None
        if aus_chart:
            try:
                cd = pd.to_datetime(eintrag.get("chart_tief_datum"))
            except Exception:
                cd = juengstes["datum"]
            bezug = {"datum": cd, "tief": float(ct), "volumen": None,
                     "index": juengstes["index"], "bestaetigt": True,
                     "chart": True}

        def in_atr(tief):
            if a in (None, 0) or ko is None:
                return None
            return (tief - ko) / a

        e_neu, e_tief = in_atr(juengstes["tief"]), in_atr(tiefstes["tief"])
        massgeblich = in_atr(bezug["tief"])

        mind_abs = float(k["mindestabstand_absolut"])
        regel1 = None if ko is None else (bezug["tief"] - ko) >= mind_abs
        r1txt = "-" if regel1 is None else ("erfuellt" if regel1 else "VERLETZT")

        bez_text = (f"{de(bezug['tief'])} ({bezug['datum']:%d.%m.}, Chart)"
                    if aus_chart else
                    f"{de(juengstes['tief'])} ({juengstes['datum']:%d.%m.}"
                    f"{'' if juengstes.get('bestaetigt', True) else ', unbest.'})")
        kopf.append(
            f"| {etikett} | {de(ko)} | {bez_text} | "
            f"{de(tiefstes['tief'])} ({tiefstes['datum']:%d.%m.}) | "
            f"{de(massgeblich, 1) + ' x ATR' if massgeblich is not None else 'k.A.'} | "
            f"{r1txt} | "
            f"{urteil(massgeblich, soll, knapp)} | "
            f"{ampel(massgeblich, soll, knapp)} |")

        betrag, faktor, hinweis = einsatz(
            massgeblich, soll, float(k["einheit_euro"]),
            float(k["min_einsatz_euro"]), regel1 is not False)
        groesse.append(
            f"| {etikett} | {bez_text} | "
            f"{de(massgeblich, 2) + ' x ATR' if massgeblich is not None else 'k.A.'} | "
            f"{de(faktor, 2) if faktor is not None else '-'} | "
            f"**{de(betrag, 2) if betrag is not None else 'k.A.'} EUR** | "
            f"{hinweis if hinweis else 'kaufbar'} |")

        if massgeblich is not None and massgeblich < knapp:
            if regel1 is False:
                folge = ("Regel 1 ist verletzt - der KO liegt nicht "
                         "mindestens {} unter dem Bezugstief. Kein "
                         "Nachkauf.".format(de(mind_abs)))
            else:
                folge = ("Nach Regel 2 bedeutet das reduzierten Einsatz, "
                         "kein Ausschluss.")
            warnungen.append(
                f"- **{name}**: Die KO-Schwelle {de(ko)} liegt nur "
                f"{de(massgeblich, 2)} x ATR unter dem Tief {de(bezug['tief'])} "
                f"vom {bezug['datum']:%d.%m.%Y}. {folge}")

        avg0 = durchschnittsvolumen(df, juengstes["index"], 20) if ticker not in ohne_vol else None
        rel0 = (juengstes["volumen"] / avg0) if (avg0 and juengstes["volumen"]) else None
        if ticker not in _excel_doppelt:
            excel.append(
                f"| {ticker} | {de(kurs)} | {de(a)} | "
                f"{de(r, 1) if r is not None else 'k.A.'} | {de(bezug['tief'])} | "
                f"{bezug['datum']:%Y-%m-%d} | "
                f"{de(rel0) if rel0 else '-'} |")
            _excel_doppelt.add(ticker)

        if a and kurs and ko is not None:
            luft = (kurs - ko) / a
            if luft < knapp:
                warnungen.append(
                    f"- **{name}**: Der Kurs {de(kurs)} steht nur "
                    f"{de(luft, 2)} x ATR ueber dem KO {de(ko)}. Eine "
                    f"Tagesschwankung reicht rechnerisch fuer den Totalverlust.")

        if a and kurs:
            def vorschlag(tief):
                empf = tief - soll * a
                if empf <= 0 or kurs <= empf:
                    return "-", "-"
                hebel = kurs / (kurs - empf)
                return de(empf), de(hebel, 1) + "x"
            k_neu, h_neu = vorschlag(juengstes["tief"])
            k_alt, h_alt = vorschlag(tiefstes["tief"])
            empfehlung.append(
                f"| {etikett} | {de(kurs)} | {de(a)} | {k_neu} | {h_neu} | "
                f"{k_alt} | {h_alt} |")

        vol_ok = ticker not in ohne_vol
        for t in treffer[:3]:
            avg = durchschnittsvolumen(df, t["index"], 20) if vol_ok else None
            rel = (t["volumen"] / avg) if (avg and t["volumen"] and vol_ok) else None
            if not vol_ok:
                relt = "n/a"
            elif rel is None:
                relt = "k.A."
            elif rel >= 1.5:
                relt = f"{de(rel)}x (Kapitulation)"
            elif rel >= 1.2:
                relt = f"{de(rel)}x (erhoeht)"
            elif rel >= 0.8:
                relt = f"{de(rel)}x"
            else:
                relt = f"{de(rel)}x (duenn)"
            ab = abstand(t["tief"], ko)
            detail.append(
                f"| {etikett} | {t['datum']:%d.%m.%Y} | {de(t['tief'])} | "
                f"{stk(t['volumen']) if vol_ok else 'n/a'} | {relt} | "
                f"{de(ab, 1) + ' %' if ab is not None else '-'} |")

    zeilen = kopf

    # Konsistenzhinweis gegen marktdaten.csv. Dieses Skript rechnet bei
    # jedem Lauf komplett aus den Kerzen neu und legt kein Zwischenergebnis
    # je Wert ab - es kann einen bei Yahoo verlorenen Handelstag also nicht
    # zurueckholen, so wie marktdaten.py es seit dem 26.08.2026 kann. Was
    # es kann: merken, dass es aelter rechnet, und das sichtbar machen,
    # statt still von marktdaten.csv abzuweichen. Genau diese stille
    # Abweichung gab es schon einmal (siehe swing_tiefs weiter oben).
    zeilen += stand_hinweis(werte)

    zeilen += ["", f"_Legende: `+` erfuellt (ab {de(soll,1)} x ATR), `!` knapp, "
                   f"`!!` zu knapp (unter {de(knapp,1)} x ATR), `X` Regelbruch._"]
    zeilen += ueberhitzung
    zeilen += ["", f"_Legende: `+` unauffaellig, `!` beobachten (ab "
                   f"{de(rsi_schwelle - 10, 0)} RSI), `!!` ueberkauft (ab "
                   f"{de(rsi_schwelle, 0)} RSI), `X` Umkehrkerze — reines "
                   f"Warnsignal, kein automatischer Verkauf._"]
    if kauf_warnungen:
        zeilen += ["", "## Kaufsignal — bitte pruefen", ""] + kauf_warnungen
    if ueberhitzt_warnungen:
        zeilen += ["", "## Verkaufssignal — bitte pruefen", ""] + ueberhitzt_warnungen
    if warnungen:
        zeilen += ["", "## Achtung", ""] + warnungen
    if fehlend:
        zeilen += ["", "## Ohne Befund", ""] + fehlend
    if len(kandidaten) > 6:
        zeilen += kandidaten
        zeilen += ["", "_Legende: `+` Signal da, `!` Signal da aber RSI zu hoch, "
                       "`-` warten._"]
    zeilen += groesse
    zeilen += ["", "_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters "
                   "steht in der Tabelle oben weiterhin zur Einordnung, geht aber "
                   "nicht in die Bewertung ein._"]
    zeilen += empfehlung
    zeilen += ["", "_'nach Trendtief' orientiert sich am juengsten Tief und laesst "
                   "mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief "
                   "des Fensters und ueberlebt auch einen Rueckfall dorthin._"]
    zeilen += detail
    if len(excel) > 6:
        zeilen += excel
    zeilen += [
        "",
        "---",
        "",
        "_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. "
        "Volumen ist das Tagesvolumen der jeweiligen Referenzboerse; bei Spot- "
        "und Futures-Tickern liefert Yahoo keine brauchbaren Werte, dort steht "
        "n/a. Keine Anlageberatung._",
    ]

    os.makedirs(os.path.dirname(AUSGABE), exist_ok=True)
    with open(AUSGABE, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")
    print(f"Geschrieben: {AUSGABE}")


if __name__ == "__main__":
    main()
