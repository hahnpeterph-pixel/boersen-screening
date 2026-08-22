"""
historie.py - Auswertungen ueber die Kurshistorie. Ersetzt puffer.py und
rueckblick.py.

Laeuft auf Knopfdruck, nicht nachts. Schreibt:
  docs/historie.md      Bericht zum Lesen
  docs/halteraten.csv        gepoolt ueber alle Werte
  docs/puffer_je_tief.csv    eine Zeile JE TIEF - die Rohdaten
  docs/halteraten_werte.csv  je Wert und Tiefsposition, geht in die Excel

Das Repository ist oeffentlich. Dieses Skript rechnet deshalb ausschliesslich
mit oeffentlichen Kursdaten und kennt weder Positionen noch Trades noch den
Depotstand. Die Trade-Nachbetrachtung aus rueckblick.py ist NICHT uebernommen
worden - sie gehoert in das Orderbuch.

Die Leitfrage: WIE OFT HAELT EIN TIEF - und haengt das davon ab, an welcher
Stelle der Abwaertsserie es steht, wie weit der Kurs schon darueber notiert
und wo der RSI steht?

Bis 22.08.2026 lag das in zwei Dateien mit zwei eigenen Tiefsdefinitionen:
puffer.py rechnete 3-links-3-rechts, rueckblick.py trug eine Kopie der
Umkehr-Regel, deren Kommentar auf marktdaten.py verwies - und veraltete
lautlos, als sich marktdaten.py aenderte. Beide sind hier aufgegangen, die
Regel kommt aus tiefs_regel.py.

WAS BEWUSST ENTFALLEN IST

  puffer.py Teil A  rechnete Trades - gehoert nicht in ein oeffentliches
                    Repository und ausserdem ins Orderbuch.
  puffer.py Teil C  verglich drei Bezugsvarianten und stieg fest nach fuenf
                    Handelstagen aus. Beides ist entschieden: gehandelt wird
                    das juengste bestaetigte Tief, und "haelt" heisst bis zum
                    Ende der Aufwaertsstrecke.
  puffer.py Teil D  untersuchte Signalgruppen und Kombinationen. Daraus kam
                    die Erkenntnis, dass der alte Score nichts getrennt hat.
                    Der Score ist neu gefasst, die Frage beantwortet.

DEFINITION "HAELT"

Gemessen wird ab dem BESTAETIGUNGSTAG - dem Tag, an dem eine Kerze das Hoch
der Tiefkerze ueberschreitet. Vorher kann nicht gekauft werden, vorher darf
also auch nicht gemessen werden.

Gemessen wird OHNE festes Fenster: fuer jeden Puffer die Zeit bis zur ersten
Unterschreitung, bis zum Ende der Historie. Ein festes Fenster beantwortet
die falsche Frage - der KO kann schlagen, solange die Position offen ist, und
verkauft wird an der Umkehr oder am Ziel, nicht nach zehn Tagen.

Ausgewiesen werden drei Zahlen je Puffer: der Anteil, der drei Monate haelt,
der Anteil, der NIE wieder durchbrochen wurde, und der Median der Tage bis
zum Bruch.

Die Basispreisdrift bleibt aussen vor: ueber elf Handelstage sind das rund
0,11 ATR. Fuer die Haltequote ist das Rauschen, fuer den Ertrag bei langer
Haltedauer nicht - dort wird sie beruecksichtigt.

Laufende Sequenzen zaehlen nicht mit: ohne Ende ist nicht entscheidbar, ob
das Tief gehalten hat. Die Quote wird zusaetzlich MIT ihnen ausgewiesen,
damit der Unterschied sichtbar bleibt.

Aufruf:  python3 historie.py
         python3 historie.py --jahre 5
         python3 historie.py --teil halterate

KEINE Anlageberatung. Das Skript misst historische Kursverlaeufe.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
MD_AUS = DOCS / "historie.md"
CSV_AUS = DOCS / "halteraten.csv"
CSV_WERT = DOCS / "halteraten_werte.csv"
CSV_ROH = DOCS / "puffer_je_tief.csv"

# Sieben Jahre: zurueck bis August 2019. Damit sind der Corona-Absturz
# (Februar/Maerz 2020) mit Vorlauf, die Erholung und die Zinswende 2022
# enthalten. Fuenf Jahre wuerden Corona knapp verfehlen - der Absturz liegt
# sechseinhalb Jahre zurueck.
#
# Weil sich der Markt seither veraendert hat, wird der Zeitraum zusaetzlich
# je Kalenderjahr aufgeschluesselt. So bleibt sichtbar, ob eine Kennzahl
# stabil ist oder von einer einzelnen Phase getragen wird, statt beides
# stillschweigend zu vermischen.
JAHRE = 7
ATR_TAGE = 14
RSI_TAGE = 14

# Puffervarianten in Viertelschritten bis 4 ATR. Ein grobes Raster verwischt
# genau die Stelle, an der entschieden wird - zwischen 0,75 und 1,25 liegen
# bei manchen Werten mehrere Prozentpunkte.
PUFFER = tuple(round(0.25 * k, 2) for k in range(1, 17))

# Abstand des Einstiegs ueber dem Tief, in Schritten von 0,2 ATR bis 3,0.
# Vier grobe Toepfe wie frueher verstecken, wo genau der Effekt kippt.
ABSTAND_KLASSEN = tuple(
    (round(0.2 * k, 1), round(0.2 * (k + 1), 1),
     f"{0.2 * k:.1f} bis {0.2 * (k + 1):.1f}") for k in range(15)
) + ((3.0, 99.0, "ueber 3,0"),)

# RSI relativ zum eigenen Kauf-Median des Wertes, in Zweierschritten.
# Absolute Schwellen sind ueber Werte hinweg nicht vergleichbar - Nike dreht
# bei 50, Gold bei 63.
RSI_KLASSEN = ((-99.0, -20.0, "20+ unter"),) + tuple(
    (float(u), float(u + 2), f"{u:+d} bis {u + 2:+d}")
    for u in range(-20, 20, 2)
) + ((20.0, 99.0, "20+ ueber"),)

KETTE_TAGE = 20      # Fenster fuer ein neues bestaetigtes Tief nach einem KO
# Statt eines Fensters: wie lange haelt das Tief ueberhaupt?
QUARTAL = 63         # Handelstage = rund drei Monate

# Zielabschlag fuer den Wettlauf Ziel gegen KO: verkauft wird beim
# werttypischen Anstieg minus 10 Prozent. Wer auf den vollen typischen
# Anstieg wartet, verpasst genau die Haelfte der Faelle - der Median ist
# per Definition die Mitte.
ZIEL_ANTEIL = 0.9
MINDESTLAUF = 63     # Tiefs ohne so viel Resthistorie zaehlen nicht mit

# Drei Messfenster, weil die Antwort davon abhaengt und ein einzelnes den
# Blick verstellt:
#
#   kurz  bis zum naechsten bestaetigten Swing-Hoch. Median 4 Handelstage.
#         Zu kurz fuer die Praxis - ein Zwischenhuepfer, nicht das Ende der
#         Strecke. Liefert systematisch zu gute Quoten.
#   fest  10 Handelstage ab dem Tief. Dasselbe Fenster wie puffer_bedarf in
#         phasen.py, nur damit sich beide Zahlen abgleichen lassen.
#   weit  bis zum naechsten TIEFEREN Tief - also nie verkaufen und jeden
#         Rueckschlag aussitzen. Zu spaet und teilweise zirkulaer: gibt es
#         ein tieferes Tief, wurde das aktuelle per Definition unterschritten.
#
# KURZ und WEIT sind Ober- und Untergrenze, nicht Kandidaten. Massgeblich
# ist FEST: zehn Handelstage entsprechen der beobachteten mittleren
# Haltedauer von elf Tagen, und dasselbe Fenster benutzt puffer_bedarf in
# phasen.py - dadurch sind beide Ausgaben zum ersten Mal vergleichbar.
# Nichts wird unterdrueckt. Frueher fielen Zellen unter acht Faellen still
# heraus - das versteckt genau die Raender, an denen es interessant wird.
# Stattdessen steht die Fallzahl in jeder Zeile und die Beurteilung bleibt
# beim Leser.
MIN_FAELLE = 1

# Je Wert wird NICHT zusammengefasst: waren es zehn Tiefs, steht Tief 10 als
# eigene Zeile. Sammelklassen wie "4+" verstecken genau das, worum es geht -
# ob ein Tief tief in einer langen Serie anders haelt als das vierte. Die
# Fallzahl steht in jeder Zeile, damit sichtbar bleibt, worauf eine Zahl
# beruht. Es wird nichts unterdrueckt und nichts gerundet weggelassen.


# ── Kennzahlen ─────────────────────────────────────────────────────

def atr(df: pd.DataFrame, tage: int = ATR_TAGE) -> np.ndarray:
    h, t, c = df["High"], df["Low"], df["Close"]
    vor = c.shift(1)
    tr = pd.concat([h - t, (h - vor).abs(), (t - vor).abs()], axis=1).max(axis=1)
    return tr.rolling(tage).mean().values


def rsi(df: pd.DataFrame, tage: int = RSI_TAGE) -> np.ndarray:
    d = df["Close"].diff()
    auf = d.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    ab = (-d.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    return (100 - 100 / (1 + auf / ab.replace(0, np.nan))).values


def bestaetigungstag(df: pd.DataFrame, i: int) -> int | None:
    """Erster Tag nach dem Tief, dessen Hoch ueber dem Hoch der Tiefkerze
    liegt. Vorher ist das Tief nicht handelbar."""
    hoch = df["High"].values
    for j in range(i + 1, len(df)):
        if hoch[j] > hoch[i]:
            return j
    return None


# ── Faelle bauen ───────────────────────────────────────────────────

def faelle_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Ein Eintrag je zaehlendem Tief einer abgeschlossenen Sequenz."""
    seqs = regel.sequenzen(df)
    if not seqs:
        return []
    hochs = regel.swing_hochs(df)
    a, r = atr(df), rsi(df)
    tief_w, hoch_w = df["Low"].values, df["High"].values
    daten = df.index

    # Werttypische Anzahl Tiefs je Sequenz - das "y" in "Tief x von y".
    abgeschlossen = [s for s in seqs if not s["laufend"]]
    typisch = (float(np.median([s["anzahl"] for s in abgeschlossen]))
               if abgeschlossen else None)
    # Eigener Kauf-RSI-Median, Bezugspunkt fuer die relative RSI-Klasse.
    rsi_an_tiefs = [r[i] for s in seqs for i in s["tiefs"] if np.isfinite(r[i])]
    rsi_median = float(np.median(rsi_an_tiefs)) if rsi_an_tiefs else None

    ergebnis = []
    for s in seqs:
        for pos, i in enumerate(s["tiefs"], start=1):
            atr_i = a[i]
            if not np.isfinite(atr_i) or atr_i <= 0:
                continue
            b = bestaetigungstag(df, i)
            if b is None:
                continue
            ende = next((h["i"] for h in hochs if h["i"] > b), None)
            if ende is None:
                continue      # Aufwaertsstrecke laeuft noch, kein Urteil

            # Resthistorie: ohne genug Zeit danach ist nicht entscheidbar,
            # ob das Tief gehalten hat. Solche Faelle fliegen raus, statt als
            # "haelt" gezaehlt zu werden - das waere die Quote geschoent.
            if len(df) - b < MINDESTLAUF:
                continue

            # Statt sechs feste Schwellen abzuprüfen: den tatsaechlich
            # noetigen Puffer festhalten. Aus der Verteilung laesst sich
            # danach jede Frage beantworten - Median, p75, p90 - statt nur
            # die nach sechs Rasterpunkten.
            nach = tief_w[b:]
            fenster = nach[:QUARTAL + 1]
            benoetigt = max(0.0, (float(tief_w[i]) - float(fenster.min())) / atr_i)
            benoetigt_ganz = max(0.0, (float(tief_w[i]) - float(nach.min())) / atr_i)

            tage = {}
            for pp in PUFFER:
                schwelle = float(tief_w[i]) - pp * atr_i
                treffer = np.flatnonzero(nach < schwelle)
                tage[pp] = int(treffer[0]) if len(treffer) else None

            gipfel = float(hoch_w[b:].max())
            anstieg = (gipfel - float(df["Close"].values[b])) / atr_i
            # Anstieg von Pivot zu Pivot: bis zum naechsten bestaetigten
            # Hoch. Der Median dieser Groesse je Wert ist der werttypische
            # Anstieg und damit die Zielbasis.
            anstieg_pivot = (float(hoch_w[ende]) - float(df["Close"].values[b])) / atr_i

            ergebnis.append({
                "ticker": ticker,
                "datum": f"{daten[i]:%Y-%m-%d}",
                "position": pos,
                "letztes_der_serie": pos == s["anzahl"],
                "serie_laenge": s["anzahl"],
                "typisch": typisch,
                "laufend": s["laufend"],
                # Abstand, den der Kurs am Bestaetigungstag schon ueber dem
                # Tief hat - der Einstiegspunkt eines echten Trades.
                "abstand_atr": (float(df["Close"].values[b]) - float(tief_w[i])) / atr_i,
                "rsi": float(r[i]) if np.isfinite(r[i]) else None,
                "rsi_rel": (float(r[i]) - rsi_median
                            if (rsi_median is not None and np.isfinite(r[i]))
                            else None),
                "tage_bis_bruch": tage,
                "benoetigt_atr": benoetigt,
                "benoetigt_ganz_atr": benoetigt_ganz,
                "resthistorie": len(df) - b,
                "anstieg_atr": anstieg,
                "anstieg_pivot_atr": anstieg_pivot,
                "einstieg": float(df["Close"].values[b]),
                "tief": float(tief_w[i]),
                "atr": atr_i,
                "hoch_reihe": hoch_w[b:],
                "tief_reihe": tief_w[b:],
                "i": i, "b": b, "ende": ende,
            })
    return ergebnis


def pivots_zeigen(ticker: str, df: pd.DataFrame, tage: int = 120) -> None:
    """Alle erkannten Tiefs und Hochs eines Wertes ausgeben, zum Abgleich
    mit dem Chart.

    Gedacht fuer genau den Fall, dass Chartablesung und Skript
    auseinanderlaufen und nicht klar ist, wer recht hat. Ausgegeben wird je
    Wendepunkt das Datum, der Wert, und bei Tiefs der Bestaetigungstag - der
    Tag, an dem eine Kerze das HOCH der Tiefkerze ueberschritten hat. Fehlt
    er, war das Tief nie bestaetigt und zaehlt nicht.

    ZAEHLT sagt, ob das Tief in seine Sequenz eingeht: nur neue
    Tiefststaende zaehlen, ein hoeheres Zwischentief nicht. SEQUENZ nennt
    die laufende Nummer der Abwaertsstrecke - daran ist ablesbar, wo eine
    Strecke endet und die naechste beginnt.

    Geschrieben wird nach docs/pivots_<TICKER>.md. Die erste Fassung gab nur
    ins Log aus - eine Pruefausgabe, deren Ergebnis man abtippen muss, ist
    keine.
    """
    grenze = df.index[-1] - pd.Timedelta(days=tage)
    hoch_w, tief_w = df["High"].values, df["Low"].values
    seqs = regel.sequenzen(df)
    nummer = {}
    for n, s in enumerate(seqs, start=1):
        for pos, i in enumerate(s["tiefs"], start=1):
            nummer[i] = (n, pos, s["anzahl"])

    L = [f"# Wendepunkte {ticker}", "",
         f"_Letzte {tage} Kalendertage bis {df.index[-1]:%Y-%m-%d}. "
         f"Regel aus `tiefs_regel.py`. BESTAETIGT AM ist der Tag, an dem eine "
         f"Kerze das Hoch der Tiefkerze ueberschritten hat - erst dann ist "
         f"das Tief handelbar. ZAEHLT sagt, ob es in seine Sequenz eingeht._",
         "",
         "| Datum | Art | Wert | Hoch der Kerze | bestaetigt am | zaehlt | Sequenz |",
         "|---|---|---|---|---|---|---|"]
    for art, i in regel.pivots(df):
        if df.index[i] < grenze:
            continue
        if art == "tief":
            b = bestaetigungstag(df, i)
            n = nummer.get(i)
            lage = f"Nr. {n[0]}, Tief {n[1]} von {n[2]}" if n else "-"
            L.append(f"| {df.index[i]:%Y-%m-%d} | Tief | {tief_w[i]:.2f} | "
                     f"{hoch_w[i]:.2f} | "
                     f"{f'{df.index[b]:%Y-%m-%d}' if b else '**NIE**'} | "
                     f"{'ja' if i in nummer else 'nein'} | {lage} |")
        else:
            L.append(f"| {df.index[i]:%Y-%m-%d} | Hoch | {hoch_w[i]:.2f} | "
                     f"| | | |")
    L += ["", "## Laufende Serie je Variante", "",
          "| Variante | Tiefs | seit | Tiefstand |", "|---|---|---|---|"]
    for v in regel.VARIANTEN:
        a, d, t = regel.tiefserie(df, v)
        L.append(f"| {v} | {a or '-'} | {d or '-'} | {t or '-'} |")
    L += ["", f"_{len(seqs)} Sequenzen in der geladenen Historie "
              f"({df.index[0]:%Y-%m-%d} bis {df.index[-1]:%Y-%m-%d})._"]

    text = "\n".join(L)
    print(text)
    DOCS.mkdir(exist_ok=True)
    ziel = DOCS / f"pivots_{ticker.replace('=', '_').replace('.', '_')}.md"
    ziel.write_text(text, encoding="utf-8")
    print(f"\nGeschrieben: {ziel}")


# ── Auswertungen ───────────────────────────────────────────────────

def quote(faelle: list[dict], p: float, tage: int | None = QUARTAL) -> float | None:
    """Anteil der Tiefs, die den Puffer p ueberstanden haben.

    tage=QUARTAL  haelt mindestens drei Monate
    tage=None     nie wieder durchbrochen, bis zum Ende der Historie
    """
    if not faelle:
        return None
    treffer = 0
    for f in faelle:
        t = f["tage_bis_bruch"].get(p)
        if t is None or (tage is not None and t > tage):
            treffer += 1
    return 100.0 * treffer / len(faelle)


def wettlauf(faelle: list[dict], puffer: float, ziel_anteil: float = ZIEL_ANTEIL) -> dict:
    """Was kommt zuerst - das Ziel oder die KO-Schwelle?

    Ab dem Bestaetigungstag wird Tag fuer Tag geprueft. Das Ziel ist der
    werttypische Anstieg dieses Wertes mal ziel_anteil, gemessen vom
    Einstiegskurs. Die KO-Schwelle liegt puffer ATR unter dem Tief.

    Anders als die reine Halterate beantwortet das die Frage, auf die es
    ankommt: nicht "haelt das Tief", sondern "verdiene ich, bevor es
    schiefgeht". Ein Tief, das nach acht Wochen bricht, ist belanglos, wenn
    das Ziel nach zwei Wochen erreicht war.

    Innerhalb eines Tages ist die Reihenfolge unbekannt. Werden Ziel und KO
    am selben Tag beruehrt, zaehlt der KO - die vorsichtige Annahme.
    """
    ziel_treffer = ko = offen = 0
    tage_ziel, tage_ko = [], []
    for f in faelle:
        z = f.get("ziel_atr")
        if z is None or not np.isfinite(z) or z <= 0:
            continue
        zielkurs = f["einstieg"] + z * f["atr"]
        koschwelle = f["tief"] - puffer * f["atr"]
        h, t = f["hoch_reihe"], f["tief_reihe"]
        t_z = np.flatnonzero(h >= zielkurs)
        t_k = np.flatnonzero(t <= koschwelle)
        iz = int(t_z[0]) if len(t_z) else None
        ik = int(t_k[0]) if len(t_k) else None
        if ik is not None and (iz is None or ik <= iz):
            ko += 1
            tage_ko.append(ik)
        elif iz is not None:
            ziel_treffer += 1
            tage_ziel.append(iz)
        else:
            offen += 1
    n = ziel_treffer + ko + offen
    if not n:
        return {}
    return {"n": n,
            "ziel_pct": 100.0 * ziel_treffer / n,
            "ko_pct": 100.0 * ko / n,
            "offen_pct": 100.0 * offen / n,
            "tage_ziel": float(np.median(tage_ziel)) if tage_ziel else None,
            "tage_ko": float(np.median(tage_ko)) if tage_ko else None}


def puffer_verteilung(faelle: list[dict]) -> dict:
    """Welchen Puffer haetten diese Tiefs tatsaechlich gebraucht?

    benoetigt_atr = wie weit der Kurs in drei Monaten unter das Tief
    gerutscht ist, in ATR. Null heisst: hat ohne jeden Puffer gehalten.
    """
    x = np.array([f["benoetigt_atr"] for f in faelle])
    if not len(x):
        return {}
    aus = {"ohne_puffer_pct": float((x <= 0.001).mean() * 100)}
    for q in (10, 25, 50, 75, 80, 85, 90, 95, 99):
        aus[f"p{q}"] = float(np.percentile(x, q))
    aus["max"] = float(x.max())
    return aus


def bruchtage(faelle: list[dict], p: float) -> float | None:
    """Median der Tage bis zum Bruch - nur ueber die gebrochenen Faelle."""
    t = [f["tage_bis_bruch"][p] for f in faelle if f["tage_bis_bruch"].get(p) is not None]
    return float(np.median(t)) if t else None


def tabelle(faelle: list[dict], schluessel, ordnung=None) -> list[dict]:
    """Halterate je Gruppe und Puffer."""
    gruppen: dict = {}
    for f in faelle:
        k = schluessel(f)
        if k is not None:
            gruppen.setdefault(k, []).append(f)
    keys = ordnung or sorted(gruppen)
    zeilen = []
    for k in keys:
        g = gruppen.get(k, [])
        if len(g) < MIN_FAELLE:
            continue
        z = {"gruppe": k, "faelle": len(g),
             "anstieg_median": float(np.median([x["anstieg_atr"] for x in g]))}
        for p in PUFFER:
            z[f"p{p}"] = quote(g, p)
        zeilen.append(z)
    return zeilen


def position_wert(f: dict) -> int:
    """Das wievielte Tief der Serie - ohne Sammelklasse."""
    return f["position"]


def position_absolut(f: dict) -> str:
    """Die schlichte Frage: das wievielte Tief der Serie ist es?

    Die relative Fassung (position_klasse) misst gegen die werttypische
    Anzahl und verwischt dabei genau das, worum es geht - ob das dritte Tief
    besser haelt als das erste. Keine Sammelklasse: waren es zehn, steht
    Tief 10 da.
    """
    return f"Tief {f['position']:02d}"


def position_klasse(f: dict) -> str | None:
    """Tief x von y - y ist die werttypische Anzahl, x kann darueber liegen."""
    if f["typisch"] is None:
        return None
    x, y = f["position"], f["typisch"]
    if x == 1:
        return "1 (erstes)"
    if x <= y:
        return "2 bis y"
    if x <= y + 1:
        return "y+1"
    return "ueber y+1"


def klasse(wert, klassen):
    if wert is None:
        return None
    for u, o, name in klassen:
        if u <= wert < o:
            return name
    return None


def korrelation(faelle: list[dict]) -> float | None:
    paare = [(f["position"], f["rsi_rel"]) for f in faelle if f["rsi_rel"] is not None]
    if len(paare) < 30:
        return None
    x, y = zip(*paare)
    return float(np.corrcoef(x, y)[0, 1])


def kette(faelle: list[dict], p: float = 1.0) -> dict:
    """Was taugt der Einstieg NACH einem Knock-out?

    Erste Fassung fragte, ob binnen KETTE_TAGE ueberhaupt ein neues Tief
    entsteht. Die Antwort war 100 Prozent - trivial, denn ein Kurs, der ein
    Tief um mehr als den Puffer unterschritten hat, bildet dabei zwangslaeufig
    ein neues. Die Zahl mass nichts.

    Gemessen wird deshalb die Anschlussfrage: haelt das naechste Tief
    desselben Wertes besser als der Durchschnitt? Nur das entscheidet, ob ein
    KO eine Gelegenheit eroeffnet oder blosser Verlust ist. Der Verlust aus
    Trade 1 zaehlt in beiden Faellen voll.
    """
    nach_ticker: dict = {}
    for f in faelle:
        nach_ticker.setdefault(f["ticker"], []).append(f)
    for v in nach_ticker.values():
        v.sort(key=lambda x: x["i"])

    folge = []
    ko = 0
    for v in nach_ticker.values():
        for k in range(len(v) - 1):
            t = v[k]["tage_bis_bruch"].get(p)
            if t is not None and t <= QUARTAL:
                ko += 1
                naechstes = v[k + 1]
                if naechstes["i"] - v[k]["i"] <= KETTE_TAGE:
                    folge.append(naechstes)
    return {"ko": ko, "folge": len(folge),
            "quote": quote(folge, p),
            "anstieg": (float(np.median([x["anstieg_atr"] for x in folge]))
                        if folge else None)}


# ── Keine Positionsdaten ───────────────────────────────────────────
#
# Bewusst NICHT enthalten: die eigene Trade-Historie. Das Repository ist
# oeffentlich, und Kaufdaten, Stueckzahlen und Ergebnisse gehen niemanden
# etwas an. Die Trade-Nachbetrachtung, die frueher in rueckblick.py stand,
# gehoert in das Orderbuch - dort liegen die Daten ohnehin, vollstaendiger
# und ohne Umweg.
#
# Dieses Skript rechnet ausschliesslich mit oeffentlichen Kursdaten. Es
# kennt keine Position, keinen Schein und keinen Depotstand.

# ── Laden ──────────────────────────────────────────────────────────

def universum() -> list[str]:
    datei = BASE / "universe.json"
    if not datei.exists():
        return []
    roh = json.loads(datei.read_text(encoding="utf-8"))
    werte: list[str] = []
    for gruppe in roh.get("benchmarks", {}):
        werte += roh.get(gruppe, [])
    for gruppe in ("COMMODITIES", "CRYPTO"):
        werte += list(roh.get(gruppe, {}).keys())
    return sorted(set(werte))


def lade(tickers: list[str], jahre: int) -> dict[str, pd.DataFrame]:
    import yfinance as yf
    print(f"Lade {len(tickers)} Werte, {jahre} Jahre ...")
    daten: dict[str, pd.DataFrame] = {}
    for i in range(0, len(tickers), 40):
        teil = tickers[i:i + 40]
        try:
            roh = yf.download(teil, period=f"{jahre}y", interval="1d",
                              auto_adjust=True, group_by="ticker",
                              threads=True, progress=False)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! Abruf fehlgeschlagen ({teil[0]} ...): {exc}")
            continue
        for t in teil:
            try:
                d = roh[t] if isinstance(roh.columns, pd.MultiIndex) else roh
                d = d.dropna(subset=["High", "Low", "Close"])
                if len(d) > 120:
                    daten[t] = d
            except Exception:  # noqa: BLE001
                continue
    print(f"  {len(daten)} Werte geladen.")
    return daten


# ── Bericht ────────────────────────────────────────────────────────

def z(x, nk=0, einheit=""):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return f"{x:.{nk}f}{einheit}"


def block(titel: str, zeilen: list[dict], spalte: str = "Gruppe") -> list[str]:
    if not zeilen:
        return [f"### {titel}", "", "_Zu wenige Faelle._", ""]
    kopf = f"| {spalte} | Faelle | " + " | ".join(f"{p} ATR" for p in PUFFER) + " | Anstieg |"
    trenn = "|---" * (len(PUFFER) + 3) + "|"
    aus = [f"### {titel}", "", kopf, trenn]
    for r in zeilen:
        werte = " | ".join(z(r.get(f"p{p}"), 0, "%") for p in PUFFER)
        aus.append(f"| {r['gruppe']} | {r['faelle']} | {werte} | "
                   f"{z(r['anstieg_median'], 2)} ATR |")
    aus.append("")
    return aus


def bericht(alle: list[dict], daten: dict, jahre: int) -> str:
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    fest = [f for f in alle if not f["laufend"]]
    L = [
        "# Historie - Halteraten und Einstieg",
        "",
        f"_Erstellt {jetzt}. {jahre} Jahre, {len(daten)} Werte, "
        f"{len(fest)} auswertbare Tiefs aus abgeschlossenen Sequenzen "
        f"({len(alle) - len(fest)} aus laufenden ausgeschlossen)._",
        "",
        "_Tiefs nach der Umkehr-Regel aus `tiefs_regel.py`. Eine Abwaertsserie "
        "zaehlt nur neue Tiefststaende; sie endet erst, wenn ein hoeheres Tief "
        "kommt UND danach ein hoeheres Hoch ueber dem Hoch vor dem tiefsten "
        "Tief. HAELT heisst: der Puffer wurde ab dem Bestaetigungstag drei "
        "Monate lang nicht unterschritten. ANSTIEG ist der Median des "
        "hoechsten Punktes nach dem Einstieg, in ATR - die Ertragsseite._",
        "",
        "## Grundrate ueber alles",
        "",
    ]
    L += ["| Puffer | haelt 3 Monate | nie wieder durchbrochen | "
          "Median Tage bis Bruch |", "|---|---|---|---|"]
    for p_ in PUFFER:
        L.append(f"| {p_} ATR | {z(quote(fest, p_), 0, '%')} | "
                 f"{z(quote(fest, p_, None), 0, '%')} | "
                 f"{z(bruchtage(fest, p_), 0)} |")
    L += ["",
          "_Gemessen ab dem Bestaetigungstag bis zum Ende der Historie, ohne "
          "festes Fenster - der KO kann schlagen, solange die Position offen "
          "ist. HAELT 3 MONATE heisst: der Puffer wurde in den ersten 63 "
          "Handelstagen nie unterschritten. NIE WIEDER DURCHBROCHEN heisst: "
          "auch danach nicht. MEDIAN TAGE BIS BRUCH zaehlt nur die Faelle, "
          "die gebrochen wurden. Tiefs mit weniger als 63 Handelstagen "
          "Resthistorie sind ausgeschlossen, sonst wuerden sie als 'haelt' "
          "gezaehlt, ohne die Gelegenheit gehabt zu haben. Alle folgenden "
          "Tabellen nennen den Anteil, der drei Monate haelt._", ""]

    L += ["## Nach Position in der Serie", "",
          "_Die Leitfrage: haelt das erste Tief seltener als ein spaeteres? "
          "y ist die werttypische Anzahl Tiefs je Sequenz dieses Wertes._", ""]
    max_pos = max(f["position"] for f in fest)

    L += ["### Welchen Puffer haetten sie gebraucht?", "",
          "_Nicht die Frage 'hat es 1 ATR gehalten', sondern 'wie viel haette "
          "es gebraucht'. Null heisst: hielt ohne jeden Puffer. p90 heisst: "
          "dieser Puffer haette neun von zehn Tiefs dieser Position "
          "ueberstanden. Gemessen ueber drei Monate ab dem Bestaetigungstag._",
          "", "| Position | Faelle | ohne Puffer | p25 | Median | p75 | p80 | "
          "p85 | p90 | p95 | p99 | max |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    gruppen: dict = {}
    for f in fest:
        gruppen.setdefault(f["position"], []).append(f)
    for k in sorted(gruppen):
        g = gruppen[k]
        v = puffer_verteilung(g)
        L.append(f"| Tief {k} | {len(g)} | {z(v['ohne_puffer_pct'], 1, '%')} | "
                 + " | ".join(z(v[f"p{q}"], 2)
                              for q in (25, 50, 75, 80, 85, 90, 95, 99))
                 + f" | {z(v['max'], 2)} |")
    L += ["", "_Alle Angaben in ATR zum Zeitpunkt des Tiefs._", ""]

    L += ["### Wie weit traegt der Anstieg danach?", "",
          "_ANSTIEG ist die Bewegung vom Einstieg bis zum naechsten "
          "bestaetigten Hoch - die realistische Ertragsseite, weil dort nach "
          "der Strategie verkauft wird. MAXIMUM ist der hoechste Punkt bis "
          "zum Ende der Historie; die Zahl faellt in einem Aufwaertsmarkt "
          "zwangslaeufig gross aus und taugt nur zur Einordnung. ZIEL ist "
          "der werttypische Anstieg des Wertes mal "
          f"{ZIEL_ANTEIL:.0%}._", "",
          "| Position | Faelle | Anstieg p25 | Median | p75 | p90 | "
          "Maximum Median | Ziel Median |", "|---|---|---|---|---|---|---|---|"]
    for k in sorted(gruppen):
        g = gruppen[k]
        a = np.array([x["anstieg_pivot_atr"] for x in g
                      if np.isfinite(x["anstieg_pivot_atr"])])
        m = np.array([x["anstieg_atr"] for x in g
                      if np.isfinite(x["anstieg_atr"])])
        zz = [x["ziel_atr"] for x in g if x.get("ziel_atr")]
        if not len(a):
            continue
        L.append(f"| Tief {k} | {len(g)} | "
                 f"{z(float(np.percentile(a, 25)), 2)} | "
                 f"{z(float(np.median(a)), 2)} | "
                 f"{z(float(np.percentile(a, 75)), 2)} | "
                 f"{z(float(np.percentile(a, 90)), 2)} | "
                 f"{z(float(np.median(m)), 2) if len(m) else '-'} | "
                 f"{z(float(np.median(zz)), 2) if zz else '-'} |")
    L += ["", "_Alle Angaben in ATR zum Zeitpunkt des Tiefs._", ""]

    L += block("Dasselbe als Quote je Schwelle",
               tabelle(fest, position_absolut,
                       [f"Tief {i:02d}" for i in range(1, max_pos + 1)]),
               "Position")
    L += ["_Darunter dieselbe Frage relativ zur werttypischen Anzahl y "
          "dieses Wertes._", ""]
    L += block("Relativ zur werttypischen Anzahl",
               tabelle(fest, position_klasse,
                       ["1 (erstes)", "2 bis y", "y+1", "ueber y+1"]),
               "Position")

    L += ["_Nicht ausgewertet wird, ob es das LETZTE Tief der Serie war: "
          "eine Serie endet per Definition mit ihrem letzten Tief, also "
          "haelt dieses immer. Die Zahl waere 100 Prozent und sagte "
          "nichts - im Moment der Kaufentscheidung ist ohnehin nicht "
          "erkennbar, ob ein Tief das letzte sein wird._", ""]

    L += ["## Nach Abstand beim Einstieg", "",
          "_Wie weit hatte sich der Kurs am Bestaetigungstag schon vom Tief "
          "geloest? Die These: ein Tief, von dem der Kurs sich geloest hat, "
          "ist bestaetigt - ein frisches ist ein Kandidat._", ""]
    L += block("Abstand in ATR",
               tabelle(fest, lambda f: klasse(f["abstand_atr"], ABSTAND_KLASSEN),
                       [k[2] for k in ABSTAND_KLASSEN]), "Abstand")

    L += ["## Ziel gegen KO", "",
          f"_Ab dem Bestaetigungstag: was kommt zuerst? Ziel ist der "
          f"werttypische Anstieg mal {ZIEL_ANTEIL:.0%}, gemessen vom "
          f"Einstiegskurs. Werden Ziel und KO am selben Tag beruehrt, zaehlt "
          f"der KO - die vorsichtige Annahme. OFFEN heisst: bis zum Ende der "
          f"Historie weder noch._", "",
          "| Puffer | Faelle | Ziel zuerst | KO zuerst | offen | "
          "Tage bis Ziel | Tage bis KO |", "|---|---|---|---|---|---|---|"]
    for p_ in PUFFER:
        w = wettlauf(fest, p_)
        if not w:
            continue
        L.append(f"| {p_} ATR | {w['n']} | {z(w['ziel_pct'], 1, '%')} | "
                 f"{z(w['ko_pct'], 1, '%')} | {z(w['offen_pct'], 1, '%')} | "
                 f"{z(w['tage_ziel'], 0)} | {z(w['tage_ko'], 0)} |")
    L += ["", "### Ziel gegen KO, je Tiefsposition (Puffer 2 ATR)", "",
          "| Position | Faelle | Ziel zuerst | KO zuerst | offen | "
          "Tage bis Ziel |", "|---|---|---|---|---|---|"]
    gr: dict = {}
    for f in fest:
        gr.setdefault(f["position"], []).append(f)
    for k in sorted(gr):
        w = wettlauf(gr[k], 2.0)
        if not w:
            continue
        L.append(f"| Tief {k} | {w['n']} | {z(w['ziel_pct'], 1, '%')} | "
                 f"{z(w['ko_pct'], 1, '%')} | {z(w['offen_pct'], 1, '%')} | "
                 f"{z(w['tage_ziel'], 0)} |")
    L += ["", "## Nach Kalenderjahr", "",
          "_Der Markt hat sich veraendert. Diese Tabelle zeigt, ob eine "
          "Kennzahl stabil ist oder von einer einzelnen Phase getragen wird. "
          "2020 enthaelt den Corona-Absturz, 2022 die Zinswende._", ""]
    jahre_gr: dict = {}
    for f in fest:
        jahre_gr.setdefault(f["datum"][:4], []).append(f)
    L += ["| Jahr | Faelle | ohne Puffer | Median | p75 | p90 | p95 | "
          "Anstieg |", "|---|---|---|---|---|---|---|---|"]
    for j in sorted(jahre_gr):
        g = jahre_gr[j]
        v = puffer_verteilung(g)
        L.append(f"| {j} | {len(g)} | {z(v['ohne_puffer_pct'], 1, '%')} | "
                 f"{z(v['p50'], 2)} | {z(v['p75'], 2)} | {z(v['p90'], 2)} | "
                 f"{z(v['p95'], 2)} | "
                 f"{z(float(np.median([x['anstieg_atr'] for x in g])), 2)} ATR |")
    L += ["", "_Alle Angaben in ATR. Das laufende Jahr ist unvollstaendig: "
              "Tiefs der letzten drei Monate fehlen, weil ihnen die "
              "Resthistorie zum Urteil fehlt._", ""]

    k = korrelation(fest)
    L += ["## Nach RSI, relativ zum eigenen Median", "",
          f"_Korrelation zwischen Position in der Serie und relativem RSI: "
          f"{z(k, 2)}. Ist sie hoch, sagt der RSI nichts, was die Position "
          f"nicht schon sagt._", ""]
    L += block("RSI-Abstand zum eigenen Kauf-Median",
               tabelle(fest, lambda f: klasse(f["rsi_rel"], RSI_KLASSEN),
                       [k[2] for k in RSI_KLASSEN]), "RSI-Lage")

    L += ["## Nach einem Knock-out", "",
          "_Haelt das naechste Tief desselben Wertes besser als der "
          "Durchschnitt? Nur das entscheidet, ob ein KO eine Gelegenheit "
          "eroeffnet._", ""]
    for p in (1.0, 2.0):
        kt = kette(fest, p)
        if kt.get("ko"):
            grund = quote(fest, p)
            L.append(f"- Puffer {p} ATR: {kt['ko']} ausgeknockte Faelle, "
                     f"{kt['folge']} mit einem Folgetief binnen {KETTE_TAGE} "
                     f"Handelstagen. Davon hielten {z(kt['quote'], 0, '%')} "
                     f"gegen {z(grund, 0, '%')} im Durchschnitt, "
                     f"Anstieg {z(kt['anstieg'], 2)} ATR.")
    L += ["",
          "_Der Verlust aus dem ersten Trade zaehlt voll, unabhaengig davon, "
          "ob ein zweiter folgt. Liegt die Folgequote nicht deutlich ueber der "
          "Grundrate, rechtfertigt ein moeglicher Wiedereinstieg keinen "
          "engeren Puffer._", ""]

    nach_wert: dict = {}
    for f in fest:
        nach_wert.setdefault(f["ticker"], []).append(f)
    spalten = list(range(1, max_pos + 1))

    L += ["## Je Wert", "",
          "_Halterate bei 2 ATR Puffer, je Tiefsposition. Keine "
          "Sammelklassen: waren es zehn Tiefs, steht Tief 10 da. Ein Strich "
          "heisst, dass diese Position bei diesem Wert nicht vorkam. In "
          "Klammern die Fallzahl - eine Quote aus zwei Faellen ist keine "
          "Eigenschaft des Papiers, sondern Zufall. Alle Puffer stehen in "
          "`halteraten_werte.csv`._", "",
          "| Wert | Tiefs | alle | " +
          " | ".join(f"Tief {i}" for i in spalten) + " | Anstieg |",
          "|---" * (len(spalten) + 4) + "|"]
    for ticker in sorted(nach_wert):
        g_alle = nach_wert[ticker]
        gruppen: dict = {}
        for f in g_alle:
            gruppen.setdefault(position_wert(f), []).append(f)
        felder = []
        for k in spalten:
            g = gruppen.get(k, [])
            felder.append(f"{z(quote(g, 2.0), 0, '%')} ({len(g)})" if g else "-")
        L.append(f"| {ticker} | {len(g_alle)} | "
                 f"{z(quote(g_alle, 2.0), 0, '%')} | " + " | ".join(felder) +
                 f" | {z(float(np.median([x['anstieg_atr'] for x in g_alle])), 1)} ATR |")

    L += ["", "---", "",
          "_Keine Anlageberatung. Historische Kursverlaeufe, gemessen mit "
          "der Regel aus `tiefs_regel.py`._"]
    return "\n".join(L)


def csv_roh(fest: list[dict]) -> None:
    """Eine Zeile JE TIEF. Die Datei, aus der sich jede Frage neu
    beantworten laesst, ohne das Skript zu aendern.

    Aggregate sind immer eine Entscheidung darueber, was interessant ist -
    und die faellt hier nicht das Skript. Wer wissen will, wie sich Tief 7
    bei RSI-Abstand -13 und Einstieg 1,4 ATR verhalten hat, filtert das
    selbst heraus.
    """
    if not fest:
        return
    felder = ["ticker", "datum", "position", "serie_laenge", "typisch",
              "tief", "einstieg", "atr", "abstand_atr", "rsi", "rsi_rel",
              "benoetigt_atr", "benoetigt_ganz_atr", "anstieg_atr",
              "anstieg_pivot_atr", "typischer_anstieg_atr", "ziel_atr",
              "resthistorie"]
    DOCS.mkdir(exist_ok=True)
    with open(CSV_ROH, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(felder)
        for x in sorted(fest, key=lambda y: (y["ticker"], y["datum"])):
            w.writerow([
                x["ticker"], x["datum"], x["position"], x["serie_laenge"],
                x["typisch"],
                round(x["tief"], 4), round(x["einstieg"], 4),
                round(x["atr"], 4),
                round(x["abstand_atr"], 3),
                round(x["rsi"], 2) if x["rsi"] is not None else "",
                round(x["rsi_rel"], 2) if x["rsi_rel"] is not None else "",
                round(x["benoetigt_atr"], 3),
                round(x["benoetigt_ganz_atr"], 3),
                round(x["anstieg_atr"], 3),
                round(x["anstieg_pivot_atr"], 3),
                (round(x["typischer_anstieg_atr"], 3)
                 if x.get("typischer_anstieg_atr") else ""),
                round(x["ziel_atr"], 3) if x.get("ziel_atr") else "",
                x["resthistorie"],
            ])
    print(f"Geschrieben: {CSV_ROH} ({len(fest)} Zeilen)")


def csv_je_wert(fest: list[dict]) -> None:
    """Halteraten je Wert und Tiefsposition - die Datei fuer die Excel."""
    nach_wert: dict = {}
    for f in fest:
        nach_wert.setdefault(f["ticker"], []).append(f)

    zeilen = []
    for ticker in sorted(nach_wert):
        g_alle = nach_wert[ticker]
        # Grundwert des Papiers, ueber alle Positionen
        z0 = {"ticker": ticker, "position": "alle", "faelle": len(g_alle),
              "anstieg_median_atr": round(float(np.median(
                  [x["anstieg_atr"] for x in g_alle])), 2)}
        for p in PUFFER:
            z0[f"haelt_{p}_atr_pct"] = round(quote(g_alle, p), 1)
        z0.update({k: round(v, 2) for k, v in puffer_verteilung(g_alle).items()})
        av = [x["anstieg_pivot_atr"] for x in g_alle
              if np.isfinite(x["anstieg_pivot_atr"])]
        z0["anstieg_pivot_median_atr"] = round(float(np.median(av)), 3) if av else ""
        w = wettlauf(g_alle, 2.0)
        z0["ziel_zuerst_2atr_pct"] = round(w["ziel_pct"], 1) if w else ""
        zeilen.append(z0)

        gruppen: dict = {}
        for f in g_alle:
            gruppen.setdefault(position_wert(f), []).append(f)
        for k in sorted(gruppen):
            g = gruppen[k]
            z1 = {"ticker": ticker, "position": f"Tief {k}", "faelle": len(g),
                  "anstieg_median_atr": round(float(np.median(
                      [x["anstieg_atr"] for x in g])), 2)}
            for p in PUFFER:
                z1[f"haelt_{p}_atr_pct"] = round(quote(g, p), 1)
            z1.update({k: round(v, 2) for k, v in puffer_verteilung(g).items()})
            av = [x["anstieg_pivot_atr"] for x in g
                  if np.isfinite(x["anstieg_pivot_atr"])]
            z1["anstieg_pivot_median_atr"] = (round(float(np.median(av)), 3)
                                              if av else "")
            w = wettlauf(g, 2.0)
            z1["ziel_zuerst_2atr_pct"] = round(w["ziel_pct"], 1) if w else ""
            zeilen.append(z1)

    if not zeilen:
        return
    DOCS.mkdir(exist_ok=True)
    with open(CSV_WERT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_WERT} ({len(zeilen)} Zeilen)")


def csv_schreiben(fest: list[dict]) -> None:
    zeilen = []
    for name, schluessel, ordnung in (
        ("position_absolut", position_absolut,
         [f"Tief {i:02d}" for i in range(1, max(f["position"] for f in fest) + 1)]),
        ("position_relativ", position_klasse,
         ["1 (erstes)", "2 bis y", "y+1", "ueber y+1"]),
        ("abstand", lambda f: klasse(f["abstand_atr"], ABSTAND_KLASSEN),
         [k[2] for k in ABSTAND_KLASSEN]),
        ("rsi_rel", lambda f: klasse(f["rsi_rel"], RSI_KLASSEN),
         [k[2] for k in RSI_KLASSEN]),
    ):
        for r in tabelle(fest, schluessel, ordnung):
            z0 = {"dimension": name, "gruppe": r["gruppe"], "faelle": r["faelle"],
                  "anstieg_median_atr": round(r["anstieg_median"], 3)}
            for p in PUFFER:
                z0[f"haelt_{p}_atr_pct"] = (round(r[f"p{p}"], 1)
                                            if r[f"p{p}"] is not None else "")
            zeilen.append(z0)
    if not zeilen:
        return
    DOCS.mkdir(exist_ok=True)
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])

    # Diagnose: Wendepunkte eines Wertes zum Chartabgleich ausgeben und
    # sonst nichts tun. "python3 historie.py --pivots CDNS"
    if "--pivots" in sys.argv:
        t = sys.argv[sys.argv.index("--pivots") + 1]
        d = lade([t, "^NDX"], jahre)
        if t not in d:
            print(f"{t}: keine Kursdaten.")
            return 1
        tage = 120
        if "--tage" in sys.argv:
            tage = int(sys.argv[sys.argv.index("--tage") + 1])
        pivots_zeigen(t, d[t], tage)
        return 0

    tickers = universum()
    if not tickers:
        print("universe.json nicht gefunden oder leer.")
        return 1

    daten = lade(tickers, jahre)
    if len(daten) < 10:
        print("Zu wenige Kursdaten - Abbruch.")
        return 1

    alle: list[dict] = []
    for ticker, df in daten.items():
        try:
            alle += faelle_je_wert(ticker, df)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {ticker}: {exc}")
    print(f"  {len(alle)} Tiefs ausgewertet.")
    if not alle:
        print("Keine auswertbaren Tiefs - Abbruch.")
        return 1

    # Werttypischer Anstieg je Wert = Median des Anstiegs bis zum naechsten
    # Hoch. Daraus das Ziel fuer den Wettlauf.
    nach_wert: dict = {}
    for f in alle:
        nach_wert.setdefault(f["ticker"], []).append(f)
    for g in nach_wert.values():
        werte = [x["anstieg_pivot_atr"] for x in g
                 if np.isfinite(x["anstieg_pivot_atr"])]
        typ = float(np.median(werte)) if werte else None
        for x in g:
            x["typischer_anstieg_atr"] = typ
            x["ziel_atr"] = typ * ZIEL_ANTEIL if typ else None

    fest = [f for f in alle if not f["laufend"]]
    DOCS.mkdir(exist_ok=True)
    MD_AUS.write_text(bericht(alle, daten, jahre), encoding="utf-8")
    print(f"Geschrieben: {MD_AUS}")
    csv_schreiben(fest)
    csv_je_wert(fest)
    csv_roh(fest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
