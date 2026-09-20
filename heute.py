#!/usr/bin/env python3
"""heute.py - komplette Block-1-Auswertung fuer die taegliche Kaufvorlage.

Entstanden am 05.09.2026, weil bis dahin JEDE einzelne Zahl in jeder
Kaufvorlage von Hand aus den Rohdaten zusammengebaut wurde - Fortsetzungs-
kette, Luecken-Fenster, RSI-Schwelle, alles neu pro Wert pro Tag. Das war
nicht nur Zeitaufwand, sondern auch die Fehlerquelle: an diesem Tag fiel
"Long-Anteil TR" bei allen 17 Kandidaten aus der Vorlage, weil niemand
gegen eine feste Zeilenliste geprueft hat, und mehrere Kandidaten liefen
noch mit einer laengst verworfenen Luecken-Formel, weil die Korrektur nicht
rueckwirkend auf schon berechnete Werte angewendet wurde.

WICHTIG: Dieses Skript schreibt NICHT in die Excel-Mappe. Die Mappe
(Orderbuch_Derivate.xlsx) existiert nur lokal bei Claude, nie im Repo -
requirements.txt enthaelt nicht einmal openpyxl. Dieses Skript liefert
stattdessen eine fertige Tabelle (docs/heute.csv), aus der die Kaufvorlage
nur noch in Prosa gegossen werden muss, statt jede Zahl neu herzuleiten.

Ausgabe: docs/heute.csv, eine Zeile je Block-1-Treffer, EU vor USA sortiert.

STAND 18.09.2026 - zwei Aenderungen gegenueber der Fassung vom 10.09.2026:

1. BEZUGSTIEF: Das Tagestief gilt nur noch dann als Bezugstief, wenn an
   diesem Tag auch wirklich ein neues Tief entstanden ist. Sonst gilt das
   juengste bestaetigte Serientief. Details am Codeort weiter unten.

2. SICHERHEITSMARKEN: Neue Spalten marke_9von10_* und marke_19von20_* je
   Wert sowie p<puffer>_reserve_atr je Pufferstufe. Dafuer ist die Spalte
   p<puffer>_ko_haelt_pct entfallen. Hintergrund: Die Kaufvorlage zeigte
   bisher nur, wie sicher der KO innerhalb des Ankerfensters ist, das
   spaetestens bei 4,00 ATR endet - die wirklich sicheren Stufen liegen
   regelmaessig darueber und waren nirgends sichtbar.
"""

from __future__ import annotations

import csv
import gzip
import os
import re

import tiefs_regel as regel
import numpy as np
import pandas as pd

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CSV_AUS = os.path.join(DOCS, "heute.csv")

# Perzentil-Fenster fuer die Luecken-Schliesswahrscheinlichkeit. p90 statt
# eines pauschalen Fensters (frueher 63 Tage) - Peters Einwand vom
# 05.09.2026: 63 Tage sagt wenig aus, wenn eine Luecke bei diesem Wert und
# dieser Richtung typischerweise in 6 oder 13 Tagen schliesst. Das Fenster
# wird deshalb je Wert UND Richtung eigens aus den geschlossenen Luecken
# hergeleitet, nicht global vorgegeben.
LUECKEN_PERZENTIL = 90

# Mindestbeobachtungszeit fuer die Halteraten-Spalten (Haelt63T) - deckungs-
# gleich mit dem Rest des Projekts (QUARTAL = 63 Handelstage in historie.py).
HALTE_FENSTER = 63


def de(x, nachkomma=0):
    """Deutsche Zahlschreibweise, ohne pandas/numpy-Typen zu verlieren."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    text = f"{x:,.{nachkomma}f}"
    return text.replace(",", "\ufffd").replace(".", ",").replace("\ufffd", ".")


def ist_rohstoff_oder_fx(ticker: str) -> bool:
    """Yahoo-Tickerendungen fuer Futures (=F) und Devisenpaare (=X).

    Bewusst am Tickernamen erkannt, nicht ueber eine weitere Ticker-Liste:
    marktdaten.py, kursverlauf.py und universe.json fuehren bereits DREI
    verschiedene, nicht deckungsgleiche Rohstoff-/FX-Listen (Fund vom
    05.09.2026 - universe.json kennt nur 4 von 11 Rohstoff-Tickern aus
    marktdaten.py). Eine vierte waere genau der Fehler, der diese Woche
    schon zweimal Bugs verursacht hat (kursverlauf.py, luecken.py).
    """
    return ticker.endswith("=F") or ticker.endswith("=X")


# Rohstoffe, auf die es bei Trade Republic KO-Zertifikate gibt. Alles
# andere hat in Block 1 nichts verloren - ein Kaufkandidat, den Peter gar
# nicht kaufen kann, ist keiner.
#
# Stand 05.09.2026, von Peter per Screenshot in der TR-Suche geprueft.
# WICHTIG fuer kuenftige Pruefungen: TR fuehrt Rohstoffe unter ENGLISCHEN
# Namen. Unter "Zucker" oder "Erdgas" findet man nichts, unter "Sugar" bzw.
# "Natural Gas" schon. Suchbegriffe: Sugar, Natural Gas (dort "Henry Hub
# Natural Gas"), Cocoa, Wheat, Corn, Platinum, Palladium.
#
# MAIS bleibt draussen: unter "Corn" erschienen nur Aktien-Derivate
# (Coinbase, CoreWeave, Core MSCI World), kein Mais-Basiswert.
# EUR/USD ist nicht geprueft und bleibt vorerst draussen.
HANDELBARE_ROHSTOFFE = {
    "GC=F",   # Gold
    "SI=F",   # Silber
    "HG=F",   # Kupfer
    "CL=F",   # WTI Oel
    "BZ=F",   # Brent Oel
    "NG=F",   # Erdgas -> TR "Henry Hub Natural Gas", KO-Scheine Vontobel
    "SB=F",   # Zucker -> TR "Sugar Future" (ICE), KO Vontobel/Soc.Gen.
    "CC=F",   # Kakao  -> TR "Cocoa" (ICE)
    "ZW=F",   # Weizen -> TR "Wheat Soft Red Future"
    "PL=F",   # Platin -> TR "Platin"/"Platinum"
    "PA=F",   # Palladium -> TR "Palladium"
}

# Handelsplatz je Rohstoff - Peter will bei jedem besprochenen Wert die
# Boerse genannt haben (Merkregel 9). Vorher stand hier pauschal
# "Rohstoff/FX", was diese Regel verletzte.
ROHSTOFF_BOERSE = {
    "GC=F": "COMEX", "SI=F": "COMEX", "HG=F": "COMEX",
    "PL=F": "NYMEX", "PA=F": "NYMEX", "NG=F": "NYMEX", "CL=F": "NYMEX",
    "BZ=F": "ICE", "SB=F": "ICE", "CC=F": "ICE",
    "ZW=F": "CBOT",
}

# Branche je Rohstoff, analog zur Sektorspalte bei Aktien.
ROHSTOFF_BRANCHE = {
    "GC=F": "Edelmetall", "SI=F": "Edelmetall",
    "PL=F": "Edelmetall", "PA=F": "Edelmetall",
    "HG=F": "Industriemetall",
    "CL=F": "Energie", "BZ=F": "Energie", "NG=F": "Energie",
    "ZW=F": "Agrar", "CC=F": "Agrar", "SB=F": "Agrar",
}

# ACHTUNG EINHEITEN (Fund 05.09.2026): Bei einigen Rohstoffen notiert
# Yahoo in einer anderen Einheit als Trade Republic. Zucker steht in
# marktdaten.csv bei 18,07 (US-Cent je Pfund), die TR-Knock-Outs liegen bei
# 0,1545-0,1785 US-Dollar - Faktor 100. Fuer die Block-1-Rechnung ist das
# egal (Puffer in ATR, alles in derselben Einheit), ABER beim Vergleich
# eines konkreten Scheins gegen unser Bezugstief muss umgerechnet werden.
# Erdgas und die Metalle stimmen dagegen direkt ueberein.


def gruen_nach_rot(z) -> bool:
    """Heutige Kerze gruen, die davor rot (Peters Kriterium vom 05.09.2026).

    Liest nur zwei Spalten aus marktdaten.csv - KEIN eigener Kursabruf.
    marktdaten.py hat die Kursreihe ohnehin in der Hand und schreibt beide
    Flags mit; ein zweiter Abruf hier waere nicht nur Doppelarbeit, sondern
    eine zusaetzliche Ausfallquelle, die Rohstoffe stillschweigend aus
    Block 1 fallen lassen koennte.

    Rot-Definition identisch zu rote_kerze() in marktdaten.py: Schluss unter
    Eroeffnung, sonst nichts. Bewusst KEIN EMA-Filter - Peter hat den
    Trendfilter-Vorschlag (Kurs ueber EMA200, wie in der Momentum-Literatur
    ueblich) ausdruecklich verworfen. Das Setup ist die Umkehr selbst, nicht
    die Lage im uebergeordneten Trend.

    Ersetzt bei Rohstoffen/FX die Rolle, die bei Aktien der Analysten-
    Kaufanteil spielt: eine zweite, vom Ruecksetzer-Setup unabhaengige
    Bestaetigung, dass gerade tatsaechlich gedreht wird.
    """
    heute_gruen = z.kurs > z.open
    vortag_rot = pd.notna(z.get("rote_kerze_vortag")) and z.get("rote_kerze_vortag") == 1
    return bool(heute_gruen and vortag_rot)


def block1_treffer(markt: pd.DataFrame, analysten: pd.DataFrame,
                   tiefe: pd.DataFrame | None = None) -> list[str]:
    """Block-1-Grundbedingungen nach Entscheidung 154 (Stand 10.09.2026).

    Ersetzt die alte Bedingung AF & AG & AZ & (AH | DG) vollstaendig.

    NEU sind drei Dinge:

    1. KEIN EMA MEHR. Die Bedingung AF "Kurs unter EMA50" ist mit
       Entscheidung 149 ersatzlos gestrichen - fuer Aktien wie fuer alles
       andere. Auswertung ueber 39.040 reife Tiefs: Die Korrelation zwischen
       RSI-Abstand zur Schwelle und EMA50-Abstand betraegt 0,885, beide
       sagen in 84,6 Prozent der Faelle dasselbe. Bei bekanntem RSI traegt
       die EMA-Lage keine eigene Information (Halterate 63 Tage bei 2,00
       ATR: 51,1 gegen 52,0 Prozent unter bzw. ueber dem EMA50). Zusaetzlich
       selektiert AF auf die SCHWAECHERE Folgebewegung: Median-Anstieg
       25,95 ATR unter dem EMA50 gegen 32,23 ATR darueber.

    2. UMKEHR STATT BESTAETIGUNG. Statt "Tief bestaetigt ODER kein neues
       Tief" (AH | DG) zaehlt jetzt eines von drei Umkehrzeichen:
         a) frisches Tief UND gruene Kerze,
         b) hoeheres Hoch als am Vortag UND rote Vortageskerze,
         c) Hammer.
       Die alte Bedingung liess 91,6 Prozent aller Tage durch und war damit
       praktisch kein Filter. Entscheidend ist nicht die Durchlassquote,
       sondern der Einstiegspunkt: Unter der alten Bedingung stand der Kurs
       im Median 2,94 ATR ueber dem massgeblichen Tief, unter der neuen
       0,64 ATR. Da der KO am Tief verankert wird, entscheidet dieser
       Abstand ueber die gesamte Rendite.

    3. RSI IST WIEDER GATE, aber absolut. RSI unter 50, nicht die
       wertspezifische Schwelle. Hebt insoweit Entscheidung 79 auf; die
       wertspezifische Schwelle bleibt als Kontextangabe in der Vorlage.

    AUSDRUECKLICH NICHT VERWENDET: das Flag umkehrkerze. Es ist laut
    eigener Docstring in marktdaten.py ein BEARISCHES Warnsignal ("Schluss
    unter Eroeffnung UND unter Vortageshoch UND unter Vortagestief"). Eine
    erste Fassung dieser Bedingung fuehrte es faelschlich als viertes
    Umkehrzeichen. Folge am 10.09.2026: 13 Kandidaten, von denen nur zwei
    eine gruene Kerze hatten - Schlusslagen bei 0, 2, 4, 12, 15, 21, 23 und
    28 Prozent der Tagesspanne. Peter fiel es bei Capital One auf, dessen
    Schluss exakt auf dem Tagestief lag.

    FRISCHES TIEF wird aus kursverlauf_tief.csv gerechnet, NICHT aus der
    Spalte vortagestief_verletzt in marktdaten.csv. Die stand am 09.09.2026
    bei O Reilly Automotive, Cadence, Marriott und JPMorgan auf 0, obwohl
    das Tagestief eindeutig unter dem Vortagestief lag (84,845 gegen 85,55 /
    281,65 gegen 282,68 / 320,91 gegen 328,24 / 348,69 gegen 353,23).

    TIEF 1 wird in auswertung() ausgeschlossen, nicht hier - dort liegt die
    Tiefsposition ohnehin vor.

    ROHSTOFFE/FX sind seit dem 09.09.2026 komplett aus dem Screening
    genommen (Peters Festlegung). Die Sonderbehandlung "gruene Kerze nach
    roter Kerze" entfaellt damit.
    """
    # VERALTETE WERTE KOMMEN NICHT IN BLOCK 1 (Peters Festlegung vom
    # 15.09.2026).
    #
    # Anlass: Am 14.09.2026 lieferte Yahoo fuer 39 DAX-Werte plus ASML und
    # KHC keinen Montag. Beide Zweitquellen halfen nicht - Stooq antwortet
    # seit dem 09.09.2026 mit einer JavaScript-Browserpruefung statt einer
    # CSV, und der Twelve-Data-Basistarif deckt XETRA nicht ab (404 fuer
    # jedes deutsche Symbol ausser dem Trial-Symbol VOW3). Ein Tarif mit
    # europaeischer Abdeckung kostet 79 USD im Monat - das ist es nicht
    # wert.
    #
    # Ohne diese Pruefung waeren die veralteten Werte trotzdem als
    # Kandidaten aufgetaucht: Das "frische Tief" haette sich aus den
    # letzten beiden VORHANDENEN Tagen ergeben, also aus dem 10. und 11.09.
    # Eine Kaufvorlage auf Basis eines zwei Tage alten Tiefs ist schlimmer
    # als gar keine.
    #
    # Massstab ist der neueste Handelstag im gesamten Universum. An einem
    # Feiertag EINER Boerse faellt deren Gruppe damit fuer einen Tag aus
    # Block 1 - gewollt und harmlos: Die Werte melden sich am naechsten
    # Handelstag von selbst zurueck.
    neuester = str(markt["datum"].max())
    veraltet = []

    treffer = []
    for ticker in markt.index:
        if ist_rohstoff_oder_fx(ticker):
            continue
        if ticker not in analysten.index:
            continue
        z = markt.loc[ticker]
        a = analysten.loc[ticker]

        if str(z.datum) != neuester:
            veraltet.append(ticker)
            continue

        # Umkehrzeichen, eines von dreien.
        vortagestief = None
        if tiefe is not None and ticker in tiefe.index:
            vortagestief = tiefe.loc[ticker]
        frisches_tief = (vortagestief is not None and pd.notna(z.low)
                         and z.low < vortagestief)
        zweig_a = frisches_tief and z.kurs > z.open
        zweig_b = z.hoeheres_hoch == 1 and z.rote_kerze_vortag == 1
        zweig_c = z.hammer == 1
        if not (zweig_a or zweig_b or zweig_c):
            continue

        if not (pd.notna(a.kaufen_pct) and (a.kaufen_pct / 100) >= 0.75):
            continue
        if pd.isna(z.rsi14) or z.rsi14 >= 50:
            continue
        treffer.append(ticker)

    if veraltet:
        print(f"  {len(veraltet)} Werte nicht aktuell (Stand ungleich "
              f"{neuester}) und deshalb NICHT in Block 1:")
        print("    " + ", ".join(sorted(veraltet)))
    return treffer


def vortagestiefs() -> pd.Series:
    """Tagestief des VORLETZTEN erfassten Handelstages je Ticker.

    Aus kursverlauf_tief.csv, weil die Spalte vortagestief_verletzt in
    marktdaten.csv nachweislich falsche Werte liefert (siehe
    block1_treffer). Die letzte Spalte der Datei ist der aktuelle Tag, die
    vorletzte der Vortag - je Ticker einzeln bestimmt, damit ein Wert mit
    Datenluecke nicht versehentlich gegen einen zu alten Tag verglichen
    wird.
    """
    pfad = os.path.join(DOCS, "kursverlauf_tief.csv")
    if not os.path.exists(pfad):
        print("  kursverlauf_tief.csv fehlt - frisches Tief nicht pruefbar")
        return pd.Series(dtype=float)
    df = pd.read_csv(pfad).set_index("ticker")
    tage = [c for c in df.columns if re.match(r"\d{4}-\d{2}-\d{2}$", c)]
    werte = {}
    for ticker, zeile in df[tage].iterrows():
        gefuellt = zeile.dropna()
        if len(gefuellt) >= 2:
            werte[ticker] = float(gefuellt.iloc[-2])
    return pd.Series(werte, dtype=float)



def fortsetzungskette(kette: dict[int, tuple], position: float) -> str:
    """Baut die Kettenzeile inkl. Markierung und Kumulierung.

    Regel (Peter, mehrfach bestaetigt zuletzt 05.09.2026):
    - Schritte VOR der aktuellen Position: unveraenderte Einzel-
      wahrscheinlichkeit.
    - Der Schritt AB der aktuellen Position (abgehend): eigene Einzel-
      wahrscheinlichkeit, mit »« markiert.
    - Jeder Schritt DANACH: mit dem vorherigen kumulierten Wert
      aufmultipliziert, OHNE eigene Markierung.
    - Gibt es keinen abgehenden Schritt (aktuelle Position ist die
      tiefste je erreichte, z.B. Walmart am 04.09.2026 bei Tief 4 ohne
      Tief 5), wird stattdessen der ANKOMMENDE Schritt markiert - sonst
      steht ein Wert ganz ohne »« da, was am 04.09.2026 uebersehen wurde.
    """
    if not kette:
        return "keine Daten"
    hat_position = position == position and position  # nicht NaN, nicht 0
    teile = []
    kumuliert = 1.0
    markiert = False
    for stufe in sorted(kette):
        ziel = stufe + 1
        # KORREKTUR 19.09.2026: Hier stand "if ziel not in kette: continue".
        # kette enthaelt aber bereits nur Stufen, deren Uebergang existiert
        # (kette_roh in main). Die Pruefung verlangte zusaetzlich, dass auch
        # die ZIELstufe noch einen Nachfolger hat - dadurch fiel bei JEDEM
        # Wert der letzte Uebergang der Kette weg. Aufgefallen bei Applied
        # Materials: 1 von 4 Serien erreichte Tief 6, die Kette zeigte aber
        # keinen Schritt Tief5->6 und markierte deshalb den ankommenden.
        faelle_ab, faelle_bis = kette[stufe]
        anteil = faelle_bis / faelle_ab if faelle_ab else 0.0
        stueck = f"Tief{stufe}\u2192{ziel}: {faelle_bis}/{faelle_ab}"
        if hat_position and stufe == int(position):
            kumuliert = anteil
            teile.append(f"\u00bb{stueck} ({de(anteil * 100)} %)\u00ab")
            markiert = True
        elif hat_position and stufe > int(position):
            kumuliert *= anteil
            teile.append(
                f"{stueck} ({de(kumuliert * 100)} % kum. ab Tief{int(position)})"
            )
        else:
            teile.append(f"{stueck} ({de(anteil * 100)} %)")
    if hat_position and not markiert and teile:
        # Ankommenden Schritt (letzter in der Liste) nachtraeglich markieren.
        letzter = teile[-1]
        teile[-1] = f"\u00bb{letzter}\u00ab"
    return " \u00b7 ".join(teile) if teile else "keine Daten"


def luecken_zeile(luecken_wert: pd.DataFrame, kurs: float) -> str:
    """Peters finale Fassung vom 05.09.2026: p90-Fenster je Richtung,
    Erfolgsquote in genau diesem (nicht mehr pauschalen 63-Tage-)Fenster.
    """
    reif = luecken_wert[luecken_wert.reif == 1]
    geschlossen = reif[reif.geschlossen == 1]
    if len(reif) == 0:
        return "keine Daten"
    quote = len(geschlossen) / len(reif) * 100
    median = geschlossen.tage_bis_schluss.median() if len(geschlossen) else None
    offen = luecken_wert[luecken_wert.geschlossen == 0].sort_values("alter_tage")
    kopf = f"Quote {de(quote)} % ({len(geschlossen)}/{len(reif)}), Median {de(median)} Tag. {len(offen)} offen"
    if len(offen) == 0:
        return kopf

    def fenster(richtung: str):
        teil = geschlossen[geschlossen.richtung == richtung]
        if len(teil) == 0:
            return None
        return int(round(np.percentile(teil.tage_bis_schluss, LUECKEN_PERZENTIL)))

    def schliesst_binnen(richtung: str, alter: float, fenster_tage: int):
        hist = reif[reif.richtung == richtung]
        kohorte = hist[(hist.geschlossen == 0) | (hist.tage_bis_schluss >= alter)]
        basis = kohorte[
            (kohorte.alter_tage >= alter + fenster_tage)
            | ((kohorte.geschlossen == 1) & (kohorte.tage_bis_schluss < alter + fenster_tage))
        ]
        if len(basis) == 0:
            return None, 0
        erfolg = (basis.geschlossen == 1) & (basis.tage_bis_schluss < alter + fenster_tage)
        return erfolg.sum() / len(basis) * 100, len(basis)

    saetze = []
    for richtung, label in (("abwaerts", "abw\u00e4rts"), ("aufwaerts", "aufw\u00e4rts")):
        gruppe = offen[offen.richtung == richtung]
        if len(gruppe) == 0:
            continue
        fenster_tage = fenster(richtung)
        einzelteile = []
        for zeile in gruppe.itertuples():
            lage = "\u00fcber" if zeile.kante > kurs else "unter"
            if fenster_tage is None:
                einzelteile.append(
                    f"{int(zeile.alter_tage)} Tage alt ({lage} Kurs), keine F\u00e4lle"
                )
                continue
            wahrsch, n = schliesst_binnen(richtung, zeile.alter_tage, fenster_tage)
            if wahrsch is None:
                einzelteile.append(
                    f"{int(zeile.alter_tage)} Tage alt ({lage} Kurs), binnen {fenster_tage} Tagen ohne F\u00e4lle"
                )
            else:
                einzelteile.append(
                    f"{int(zeile.alter_tage)} Tage alt ({lage} Kurs), binnen {fenster_tage} Tagen zu {de(wahrsch)} %"
                )
        saetze.append(f"{label}: " + "; ".join(einzelteile))
    return kopf + " \u2014 " + ". ".join(saetze) + "."


def _haelt(teilmenge: pd.DataFrame, puffer_atr: float):
    """Anteil der Faelle, die diesen Puffer mindestens HALTE_FENSTER Tage
    hielten (kein KO innerhalb dieses Fensters)."""
    beobachtet_genug = teilmenge[teilmenge["beobachtet"] >= HALTE_FENSTER]
    if len(beobachtet_genug) == 0:
        return None, 0
    spalte = f"tage_ko_{puffer_atr:g}"
    tage_bis_ko = beobachtet_genug[spalte]
    haelt = (tage_bis_ko.isna()) | (tage_bis_ko > HALTE_FENSTER)
    return haelt.mean() * 100, len(beobachtet_genug)


def _haelt_flex(teilmenge: pd.DataFrame, puffer_atr: float):
    """Wie _haelt(), aber fuer JEDEN Puffer (19.09.2026, Peter: "Die
    Spanne 0,25-4 ATR kann entfallen").

    Bis 4,00 ATR stehen fertige Spalten tage_ko_* in der Rohdatei - dann
    wird genau wie bisher gerechnet, keine Zahl aendert sich. Darueber
    gibt es keine Spalte; dann entscheidet benoetigt_atr (Tiefe unter dem
    Tief binnen 63 Tagen): gehalten, wenn benoetigt <= Puffer. Beide Wege
    sind gleichwertig - nachgeprueft auf allen 638.832 Faellen der Stufen
    0,25 bis 4,00: 37 Abweichungen, alle exakt auf der Stufe, weil
    benoetigt_atr in der Datei auf drei Stellen gerundet ist.
    """
    if f"tage_ko_{puffer_atr:g}" in teilmenge.columns:
        return _haelt(teilmenge, puffer_atr)
    genug = teilmenge[teilmenge["beobachtet"] >= HALTE_FENSTER]
    werte = genug["benoetigt_atr"].dropna().to_numpy(dtype=float)
    if len(werte) == 0:
        return None, 0
    return float((werte <= puffer_atr + 1e-9).mean() * 100), int(len(werte))


def _benoetigt(teilmenge: pd.DataFrame) -> np.ndarray:
    """Benoetigter Puffer je Tief, in ATR - also wie viel Abstand unter dem
    Tief noetig gewesen waere, damit der KO nicht faellt. Gleiche Grund-
    gesamtheit wie _haelt(), damit Prozentwerte und Marken denselben
    Nenner haben."""
    if len(teilmenge) == 0:
        return np.array([], dtype=float)
    genug = teilmenge[teilmenge["beobachtet"] >= HALTE_FENSTER]
    werte = genug["benoetigt_atr"].to_numpy(dtype=float)
    return werte[~np.isnan(werte)]


def _marke(werte: np.ndarray, anteil: float):
    """Kleinster Puffer, bei dem mindestens <anteil> aller Ruecksetzer den
    KO nie gerissen haetten.

    AUSGEZAEHLT, nicht zwischen Perzentilen interpoliert - Peters
    ausdrueckliche Vorgabe. Der Index laeuft ueber die sortierte Reihe der
    benoetigten Puffer: bei 195 Faellen und 90 Prozent ist das der
    176. Wert, also genau die Stufe, ab der 176 von 195 gehalten haetten.

    Hintergrund (18.09.2026): Ein reissender KO reisst praktisch immer
    innerhalb der ersten 63 Handelstage. Nachgemessen an Broadcom stimmt
    "haelt 63 Tage" auf jeder einzelnen Pufferstufe exakt mit "reisst nie"
    ueberein. Die Marken hier und die Halteraten-Spalten messen deshalb
    dasselbe und sind untereinander vergleichbar."""
    if len(werte) == 0:
        return None
    sortiert = np.sort(werte)
    index = int(np.ceil(anteil * len(sortiert))) - 1
    index = min(max(index, 0), len(sortiert) - 1)
    return float(sortiert[index])


def _haelt_bei(werte: np.ndarray, puffer_atr: float):
    """Halteanteil bei einem beliebigen Puffer - auch ausserhalb der 16
    festen tage_ko-Stufen, die nur bis 4,00 ATR reichen. Die Sicherheits-
    marken liegen regelmaessig darueber (Broadcom 5,32, Sherwin-Williams
    6,77 ATR), deshalb kann _haelt() sie nicht liefern."""
    if len(werte) == 0:
        return None, 0
    return float((werte <= puffer_atr).mean() * 100), int(len(werte))


def vp_leiste(txt, ko, kurs, atr) -> str:
    """Volumenspitzen unter dem Kurs, naechste zuerst, mit dem Anker-KO an
    seiner Stelle einsortiert (20.09.2026). Peter: "Einfach nur eine
    Kennzahl" - eine Zeile, z. B. "205 · KO 187 · 183 (0,8 ATR)".
    Lesart: jede Spitze ist eine Unterstuetzung; bricht die erste, ist die
    naechste darunter das Ziel. Steht der KO VOR einer Spitze, reisst er,
    bevor der Kurs diese Unterstuetzung erreicht. Die ATR-Zahl ist der
    Abstand vom KO bis zur naechsten Spitze darunter."""
    if not isinstance(txt, str) or not txt or atr in (None, 0):
        return ""
    fmt = lambda x: f"{x:.0f}" if x >= 100 else f"{x:.1f}".replace(".", ",")
    spitzen = sorted((float(t.split(":")[0]) for t in txt.split(";") if t), reverse=True)
    unten = [s for s in spitzen if s < kurs][:4]
    teile, ko_drin = [], False
    for s in unten:
        if not ko_drin and ko > s:
            teile.append(f"KO {fmt(ko)}")
            ko_drin = True
            teile.append(f"{fmt(s)} ({(ko - s) / atr:.1f} ATR)".replace(".", ","))
        else:
            teile.append(fmt(s))
    if not ko_drin:
        teile.append(f"KO {fmt(ko)} (keine Spitze darunter)")
    return " · ".join(teile)


def korr_an_position(puffer: pd.DataFrame, phasen: pd.DataFrame, t: str,
                     position) -> tuple:
    """Korrektur AB HOCH bis zum Serienende fuer alle abgeschlossenen
    Serien dieses Werts, die die heutige Tiefsposition erreicht haben.
    Rueckgabe: Faelle, 9 von 10, 19 von 20, tiefste.

    QUELLE seit 19.09.2026: puffer_je_tief.csv.gz, Spalte korr_serie_atr
    (historie.py). Damit zaehlt die Korrektur-Tabelle dieselben Faelle wie
    die Fortsetzungskette. Die Zwischenloesung ueber phasen.korr_je_tief
    zaehlte anders (Costco 17 statt 15) und bleibt nur Rueckfall, solange
    die Rohdatei die neue Spalte noch nicht hat.

    AUSGEZAEHLT, nicht interpoliert - wie die Sicherheitsmarken: "9 von
    10" ist der Wert, unter dem mindestens 90 Prozent der Faelle liegen
    (der k-te sortierte Wert mit k = aufgerundet 0,9 * n).
    """
    leer = (None, None, None, None)
    if position != position or not position:
        return leer
    if "korr_serie_atr" in puffer.columns:
        w = puffer[(puffer.ticker == t) & (puffer.position == int(position))]
        w = np.sort(w["korr_serie_atr"].dropna().to_numpy(dtype=float))
        if len(w) == 0:
            return leer
        n = len(w)
        marke = lambda q: float(w[min(n, int(np.ceil(q * n))) - 1])
        return n, marke(0.90), marke(0.95), float(w[-1])
    # Rueckfall: alte Rohdatei ohne korr_serie_atr.
    if t not in phasen.index or "korr_je_tief" not in phasen.columns:
        return leer
    roh = phasen.loc[t, "korr_je_tief"]
    if not isinstance(roh, str):
        return leer
    for teil in roh.split(";"):
        k, n, p90, p95, mx = teil.split(":")
        if int(k) == int(position):
            return int(n), float(p90), float(p95), float(mx)
    return leer


def main() -> None:
    markt = pd.read_csv(os.path.join(DOCS, "marktdaten.csv")).set_index("ticker")
    analysten = pd.read_csv(os.path.join(DOCS, "analysten.csv")).set_index("ticker")
    phasen = pd.read_csv(os.path.join(DOCS, "phasen.csv")).set_index("ticker")
    rsi_schwellen = pd.read_csv(os.path.join(DOCS, "rsi_schwellen.csv"))
    luecken = pd.read_csv(os.path.join(DOCS, "luecken.csv"))
    # DATENLUECKEN (19.09.2026, harte Sperre nach Peters Entscheidung):
    # "Wenn keine vollstaendigen Daten vorliegen, kann man das Tief nicht
    # richtig bestimmen" - ein Wert mit fehlendem Handelstag in den letzten
    # kurse.PRUEF_TAGE faellt aus Block 1. Geschrieben von kursverlauf.py,
    # NACHDEM kurse.py versucht hat, die Loecher zu fuellen. Fehlt die
    # Datei, laut melden und ohne Sperre weiter - ein fehlender Bericht
    # darf nicht still als "alles vollstaendig" durchgehen.
    datenluecken_pfad = os.path.join(DOCS, "datenluecken.csv")
    if os.path.exists(datenluecken_pfad):
        datenluecken = pd.read_csv(datenluecken_pfad, dtype=str).fillna("").set_index("ticker")
    else:
        datenluecken = None
        print("WARNUNG: docs/datenluecken.csv fehlt - Vollstaendigkeit der "
              "Kursreihen NICHT geprueft, Sperre wirkt heute nicht.")
    with gzip.open(os.path.join(DOCS, "puffer_je_tief.csv.gz")) as f:
        puffer = pd.read_csv(f)

    puffer = puffer.sort_values(["ticker", "datum"])
    # Die Serientiefe-Aggregation ist am 18.09.2026 entfallen, zusammen mit
    # der Spalte ko_haelt_pct, die als einzige daraus gespeist wurde. Die
    # Serientiefe selbst bleibt unveraendert bestehen - sie wird von
    # historie.py gerechnet und im Excel-Blatt "Serientiefe" gefuehrt
    # (Entscheidung 100). Was hier wegfaellt, ist nur die zweite, kleinere
    # Sicherheitsspalte in der Kaufvorlage.

    ketten_je_wert: dict[str, dict[int, tuple]] = {}
    for t, gruppe in rsi_schwellen.groupby("ticker"):
        ketten_je_wert[t] = {
            int(r.position): (int(r.faelle), r.rsi_p75, r.rsi_min, r.rsi_max, r.anteil_serien)
            for r in gruppe.itertuples()
        }

    # Fehlt die Spalte, laeuft marktdaten.py noch in der alten Fassung -
    # dann koennen Rohstoffe nicht in Block 1 auftauchen. Das muss laut
    # werden, nicht stillschweigend passieren: genau solche unsichtbaren
    # Ausfaelle waren der Grund, warum die Rohstoff-Luecke ueberhaupt
    # monatelang unbemerkt blieb.
    if "rote_kerze_vortag" not in markt.columns:
        print("WARNUNG: Spalte 'rote_kerze_vortag' fehlt in marktdaten.csv - "
              "marktdaten.py ist nicht auf dem Stand vom 05.09.2026. "
              "Rohstoffe/FX koennen heute NICHT in Block 1 auftauchen.")

    treffer = block1_treffer(markt, analysten, vortagestiefs())
    print(f"Block-1-Treffer heute: {len(treffer)}")

    zeilen = []
    for t in treffer:
        z = markt.loc[t]
        rohstoff = ist_rohstoff_oder_fx(t)
        a = analysten.loc[t] if t in analysten.index else None
        kurs, atr = float(z.kurs), float(z.atr14)
        position = z.tiefs_serie

        # TIEF 1 AUSGESCHLOSSEN (Entscheidung 154). Begruendung: Bei Tief 1
        # ist die Wahrscheinlichkeit weiterer Tiefs am hoechsten, und nach
        # dem Umbau der Umkehrbedingung waeren sonst 19 bis 25 Kandidaten
        # taeglich zu pruefen - zu viel fuer eine Morgenrunde. Datenlage:
        # Tief 1 haelt ueber 63 Tage bei 2,00 ATR nur zu 47,7 Prozent,
        # Tief 2 zu 49,0, Tief 3 zu 51,5, Tief 4 zu 54,8. Bewusst
        # aufgegeben wird dabei, dass Tief 1 mit 31,8 ATR den hoechsten
        # Median-Anstieg der ganzen Reihe hat.
        # (Tief-1-Ausschluss steht seit 19.09.2026 weiter unten, NACH der
        # Positionskorrektur - siehe dort.)

        # BEZUGSTIEF ist ab Entscheidung 154 das TAGESTIEF dieses Tages -
        # aber nur dann, wenn an diesem Tag auch tatsaechlich ein neues
        # Tief entstanden ist, das Tagestief also UNTER dem juengsten
        # bestaetigten Serientief liegt. Sonst gilt dieses Serientief.
        #
        # KORREKTUR vom 18.09.2026: Die alte Fassung nahm bedingungslos
        # z.low. An jedem Tag ohne neues Tief erklaerte sie damit das
        # Tagestief einer AUFWAERTSkerze zum Bezugstief - einen Wert, der
        # nie ein Tief war. Am 17.09.2026 betraf das alle drei Kandidaten:
        # Broadcom 345,31 statt 335,82 (9,50 zu hoch), Sherwin-Williams
        # 320,64 statt 315,42 (5,22 zu hoch), UnitedHealth 374,20 statt
        # 373,63 (0,57 zu hoch). Folge: KO zu hoch verankert, Puffer zu
        # klein, Rendite zu gross ausgewiesen. Bei Sherwin-Williams
        # reichte der Fehler, um die Renditehuerde faelschlich zu nehmen -
        # 180,1 Prozent ausgewiesen, tatsaechlich 148,6. Der Wert waere
        # gar nicht in Block 1 gelandet. Aufgefallen durch Peters
        # stock3-Charts, nicht durch das Skript.
        #
        # Entscheidung 154 bleibt damit unveraendert gueltig - sie war nur
        # falsch umgesetzt. Das ist eine Fehlerkorrektur, keine
        # Regelaenderung; die Stoppregel vom 17.09.2026 greift hier nicht.
        tagestief = float(z.low) if pd.notna(z.low) else None
        serientief = float(z.tief1) if pd.notna(z.tief1) else None
        if tagestief is not None and serientief is not None:
            if tagestief < serientief:
                tief, tief_datum = tagestief, z.datum
            else:
                tief, tief_datum = serientief, z.tief1_datum
        elif tagestief is not None:
            tief, tief_datum = tagestief, z.datum
        elif serientief is not None:
            tief, tief_datum = serientief, z.tief1_datum
        else:
            print(f"WARNUNG: {t} hat weder Tagestief noch Serientief - uebersprungen.")
            continue

        # POSITIONSKORREKTUR (19.09.2026, gefunden bei der Detailpruefung).
        # tiefs_serie zaehlt nur BESTAETIGTE Tiefs. Liegt das Bezugstief
        # aber UNTER dem tiefsten bestaetigten Tief der Serie, ist es ein
        # weiteres, noch unbestaetigtes Tief - also Position + 1. Genau so
        # zaehlt Peter im Chart. Vorher wurde es mit der Position des
        # VORIGEN Tiefs gefuehrt: Mastercard lief als Tief 3, obwohl nach
        # 27.08./01.09./10.09. das Tief vom 18.09. das vierte ist; ebenso
        # GE Aerospace (2 statt 3), Linde (6 statt 7), Sherwin-Williams
        # (3 statt 4), UnitedHealth (5 statt 6). Kette, RSI-Vergleich,
        # Halteraten, Anker und Korrektur-Tabelle hingen alle an der
        # falschen Position. Beginnt mit dem Bezugstief eine neue Serie
        # (keine laufende), ist es Tief 1.
        serie_tief = (float(z.tiefs_serie_tief)
                      if pd.notna(z.tiefs_serie_tief) and str(z.tiefs_serie_tief) != ""
                      else None)
        if position == position and position and serie_tief is not None:
            if regel._unter(tief, serie_tief):
                position = int(position) + 1
        elif position != position or not position:
            position = 1 if tief is not None else position

        # TIEF 1 AUSGESCHLOSSEN (Entscheidung 154), Begruendung oben.
        if position != position or not position or int(position) == 1:
            continue
        # Kein Analystenziel fuer Rohstoffe/FX moeglich - "Kursziel" und
        # "Eigenes Ziel" bleiben leer statt einer erfundenen Zahl. Peters
        # Regel "grobe Naeherungen sind kein akzeptables Ergebnis" gilt
        # auch hier: lieber leer als falsch.
        ziel = float(a.kursziel) if a is not None and pd.notna(a.kursziel) else None
        eigen = ziel - 0.10 * kurs if ziel is not None else None

        kette_wert = ketten_je_wert.get(t, {})
        kette_roh = {
            p: (v[0], kette_wert[p + 1][0])
            for p, v in kette_wert.items()
            if (p + 1) in kette_wert
        }
        schwelle = kette_wert.get(int(position)) if position == position and position else None

        ueblich = phasen.loc[t, "korrektur_atr"] if t in phasen.index else None
        korr_tief = korr_an_position(puffer, phasen, t, position)
        luecken_wert = luecken[luecken.ticker == t]

        teil_puffer = puffer[puffer.ticker == t]
        teil_position = (
            teil_puffer[teil_puffer.position == position] if position == position else teil_puffer.iloc[0:0]
        )

        zeile = {
            "ticker": t,
            "name": (a.get("name", t) if a is not None else z.get("name", t)),
            "boerse": (a.get("index", "") if a is not None
                       else ROHSTOFF_BOERSE.get(t, "Rohstoff/FX")),
            "branche": (a.get("sektor", "") if a is not None
                        else ROHSTOFF_BRANCHE.get(t, "Rohstoff/FX")),
            "kurs": kurs,
            "atr14": atr,
            "bezugstief": tief,
            "bezugstief_datum": tief_datum,
            # 19.09.2026: stand fest auf 0 - Costco wurde dadurch als
            # "unbestaetigt" gefuehrt, obwohl tief1_best=1 (das Hoch vom
            # 18.09. lag ueber dem Hoch der Tiefkerze vom 17.09.). Ein
            # Tagestief von heute ist nie bestaetigt; ein Serientief traegt
            # die Bestaetigung aus marktdaten.csv.
            "bezugstief_bestaetigt": (int(z.tief1_best) if tief_datum == z.tief1_datum
                                      and pd.notna(z.tief1_best) and str(z.tief1_best) != ""
                                      else 0),
            "position": position,
            "fortsetzungskette": fortsetzungskette(kette_roh, position),
            "rsi_heute": z.rsi14,
            "rsi_min": schwelle[2] if schwelle else None,
            "rsi_max": schwelle[3] if schwelle else None,
            "rsi_schwelle": schwelle[1] if schwelle else None,
            "rsi_schwelle_faelle": schwelle[0] if schwelle else None,
            "rsi_schwelle_anteil_serien": schwelle[4] if schwelle else None,
            "kaufanteil_pct": (a.kaufen_pct if a is not None else None),
            "banken": (a.banken if a is not None else None),
            "kursziel": ziel,
            "eigenes_ziel": eigen,
            "korrektur_atr": z.korr_ist_atr,
            "korrektur_tage": z.korr_ist_tage,
            "korrektur_ueblich_atr": ueblich,
            # Volumenprofil aus marktdaten.csv (19.09.2026), 1 Jahr Tageskerzen.
            "vp_poc": z.get("vp_poc", ""),
            "vp_spitzen": z.get("vp_spitzen", ""),
            # Ab Hoch, nur Serien mit mindestens so vielen Tiefs wie heute
            # (phasen.korr_je_tief, 19.09.2026). Rest = Marke minus Ist.
            "korr_tief_faelle": korr_tief[0],
            "korr_tief_p90": korr_tief[1],
            "korr_tief_p95": korr_tief[2],
            "korr_tief_max": korr_tief[3],
            "long_anteil_tr": "nicht erfasst - bitte Screenshot",
            "luecken": luecken_zeile(luecken_wert, kurs) if len(luecken_wert) else "keine Daten",
        }
        dl = (datenluecken.loc[t] if datenluecken is not None and t in datenluecken.index
              else None)
        zeile["daten_fehlend"] = dl["fehlend"] if dl is not None else ""
        zeile["daten_gefuellt"] = dl["gefuellt"] if dl is not None else ""
        zeile["daten_wochenkontrolle"] = dl["wochenkontrolle"] if dl is not None else ""

        # ANKERZEILE UND PUFFERFENSTER (Entscheidung 149, Fassung vom
        # 19.09.2026).
        #
        # Die Ankerzeile ist die NIEDRIGSTE Pufferzeile, in der BEIDE
        # 63-Tage-Halteraten mindestens 60 Prozent erreichen - die fuer
        # diese Tiefsposition und die ueber alle Tiefs. Die niedrigste wird
        # genommen, weil die Rendite mit sinkendem Puffer steigt.
        #
        # AENDERUNG 19.09.2026 (Peter): "Die Spanne 0,25-4 ATR kann
        # entfallen. Wichtig ist die Rendite bei Haltewahrscheinlichkeiten."
        # Bisher war bei 4,00 ATR Schluss - ein Wert, der 60/60 erst bei
        # 4,25 schafft, flog mit "60/60 nie erreicht" raus, obwohl die
        # Rendite dort noch reichen kann. Jetzt wird in Viertelschritten
        # weitergesucht, bis beide Raten stehen oder kein Fall mehr tiefer
        # fiel. Ob sich der Puffer lohnt, entscheidet allein die
        # Renditepruefung darunter. 0,25 bleibt der kleinste Schritt - ein
        # KO direkt auf dem Tief ist keiner.
        #
        # Ausgegeben wird ein FENSTER um den Anker: vier Viertelschritte
        # darunter und vier darueber, unten bei 0,25 gekappt. Ein festes
        # Raster wurde am 08.09.2026 erprobt und wieder verworfen, weil es
        # die Ankerzeile auf den naechsthoeheren Puffer schob und dadurch
        # Rendite kostete.
        tiefste_faelle = _benoetigt(teil_puffer)
        suchende = (float(tiefste_faelle.max()) + 0.25) if len(tiefste_faelle) else 4.0
        anker = None
        puf = 0.25
        while puf <= max(suchende, 0.25) + 1e-9:
            hp, _ = _haelt_flex(teil_position, puf)
            ha, _ = _haelt_flex(teil_puffer, puf)
            if hp is not None and ha is not None and hp >= 60 and ha >= 60:
                anker = puf
                break
            puf = round(puf + 0.25, 2)

        zeile["anker_atr"] = anker
        if anker is None:
            # Kein Puffer erreicht 60/60 (kommt nur bei zu wenigen
            # Faellen vor) - der Wert faellt nach Entscheidung 149 raus.
            zeile["filter_ergebnis"] = "raus - 60/60 nie erreicht"
            zeile["filter_variante"] = None
            zeilen.append(zeile)
            continue

        ko_anker = tief - anker * atr
        zeile["vp_leiste"] = vp_leiste(z.get("vp_spitzen", ""), ko_anker, kurs, atr)
        hoehe_anker = kurs - ko_anker
        r_eigen = ((eigen - kurs) / hoehe_anker * 100
                   if eigen is not None and hoehe_anker else None)
        r_analyst = ((ziel - kurs) / hoehe_anker * 100
                     if ziel is not None and hoehe_anker else None)
        zeile["anker_rendite_eigen_pct"] = r_eigen
        zeile["anker_rendite_analyst_pct"] = r_analyst

        # RENDITEPRUEFUNG in genau dieser Zeile. Hauptregel: mindestens
        # 150 Prozent auf das eigene Ziel. Zusatzvariante fuer knappe
        # Faelle: zwischen 120 und unter 150 Prozent bleibt der Wert drin,
        # wenn das Analystenziel in derselben Zeile mindestens 200 Prozent
        # bringt. Hintergrund der Zusatzvariante: eigene und
        # Analystenrendite sind nicht unabhaengig - das eigene Ziel ist
        # definitionsgemaess das Analystenziel minus 10 Prozent des
        # Kurses. Die Variante belohnt damit faktisch einen engen KO, also
        # hohen Hebel. Das ist gewollt, sollte aber bekannt sein.
        if r_eigen is None:
            zeile["filter_ergebnis"] = "raus - kein eigenes Ziel"
            zeile["filter_variante"] = None
        elif r_eigen >= 150:
            zeile["filter_ergebnis"] = "drin"
            zeile["filter_variante"] = "Hauptregel"
        elif r_eigen >= 120 and r_analyst is not None and r_analyst >= 200:
            zeile["filter_ergebnis"] = "drin"
            zeile["filter_variante"] = "Zusatzvariante"
        else:
            zeile["filter_ergebnis"] = f"raus - Rendite {r_eigen:.0f} %"
            zeile["filter_variante"] = None

        # HARTE SPERRE bei unvollstaendigen Daten (19.09.2026). Steht NACH
        # der Renditepruefung, damit Anker, Renditen und Marken trotzdem
        # gerechnet und sichtbar bleiben - man sieht, was der Wert waere,
        # kann ihn aber nicht kaufen.
        if zeile["daten_fehlend"]:
            tage_txt = ", ".join(pd.Timestamp(d).strftime("%d.%m.")
                                 for d in zeile["daten_fehlend"].split())
            zeile["filter_ergebnis"] = f"raus - Daten unvollstaendig ({tage_txt})"

        # SICHERHEITSMARKEN (neu am 18.09.2026, auf Peters Vorgabe). Die
        # Pufferstufen zeigen bisher nur, wie sicher der KO IN DIESEM
        # Fenster ist - das Fenster endet aber spaetestens bei 4,00 ATR,
        # und die wirklich sicheren Stufen liegen regelmaessig darueber.
        # Gefragt war: "der Wert, wo es rein stochastisch fast
        # ausgeschlossen ist, dass der KO gerissen wird" - und der Abstand
        # dorthin, damit man sieht, ob die naechste Sicherheitsstufe
        # billig zu haben ist oder teuer.
        benoetigt_alle = _benoetigt(teil_puffer)
        benoetigt_position = _benoetigt(teil_position)
        marke90 = _marke(benoetigt_alle, 0.90)
        marke95 = _marke(benoetigt_alle, 0.95)

        for feld, quote in (("9von10", 0.90), ("19von20", 0.95)):
            m = marke90 if feld == "9von10" else marke95
            zeile[f"marke_{feld}_atr"] = m
            if m is None:
                continue
            ko_m = tief - m * atr
            hoehe_m = kurs - ko_m
            hp_m, hpn_m = _haelt_bei(benoetigt_position, m)
            ha_m, han_m = _haelt_bei(benoetigt_alle, m)
            zeile[f"marke_{feld}_ko"] = ko_m
            zeile[f"marke_{feld}_abstand_pct"] = (kurs - ko_m) / kurs * 100 if kurs else None
            zeile[f"marke_{feld}_einsatz"] = 50 + 50 * m
            zeile[f"marke_{feld}_haelt_position_pct"] = hp_m
            zeile[f"marke_{feld}_haelt_position_n"] = hpn_m
            zeile[f"marke_{feld}_haelt_alle_pct"] = ha_m
            zeile[f"marke_{feld}_haelt_alle_n"] = han_m
            if eigen is not None and hoehe_m:
                zeile[f"marke_{feld}_rendite_eigen_pct"] = (eigen - kurs) / hoehe_m * 100
            if ziel is not None and hoehe_m:
                zeile[f"marke_{feld}_rendite_analyst_pct"] = (ziel - kurs) / hoehe_m * 100

        untergrenze = max(0.25, round(anker - 1.00, 2))
        fenster = [round(untergrenze + 0.25 * i, 2) for i in range(9)]
        fenster = [p for p in fenster if p >= 0.25]

        for puf in fenster:
            ko = tief - puf * atr
            haelt_position, n_position = _haelt_flex(teil_position, puf)
            haelt_alle, n_alle = _haelt_flex(teil_puffer, puf)
            hoehe = kurs - ko
            zeile[f"p{puf:g}_ko"] = ko
            zeile[f"p{puf:g}_abstand_pct"] = (kurs - ko) / kurs * 100 if kurs else None
            zeile[f"p{puf:g}_einsatz"] = 50 + 50 * puf
            zeile[f"p{puf:g}_haelt63_position_pct"] = haelt_position
            zeile[f"p{puf:g}_haelt63_position_n"] = n_position
            zeile[f"p{puf:g}_haelt63_alle_pct"] = haelt_alle
            zeile[f"p{puf:g}_haelt63_alle_n"] = n_alle
            # RESERVE: wie viele ATR von dieser Stufe bis zu der Stufe
            # fehlen, ab der neun von zehn Ruecksetzer gehalten haetten.
            # Ersetzt die Spalte ko_haelt_pct, die am 18.09.2026 gestrichen
            # wurde: Sie mass dasselbe wie haelt63_alle_pct, nur auf der
            # kleineren Grundgesamtheit der Serien (46 statt 195 Faellen
            # bei Broadcom), und ihr Nenner stand nirgends in der Ausgabe.
            # Zwei Sicherheitsspalten mit verschiedenen Nennern nebenein-
            # ander waren der Grund, warum die Tabelle unklar wirkte.
            zeile[f"p{puf:g}_reserve_atr"] = (
                round(marke90 - puf, 2) if marke90 is not None else None
            )
            zeile[f"p{puf:g}_ist_anker"] = 1 if puf == anker else 0
            if eigen is not None and hoehe:
                zeile[f"p{puf:g}_rendite_eigen_pct"] = (eigen - kurs) / hoehe * 100
            if ziel is not None and hoehe:
                zeile[f"p{puf:g}_rendite_analyst_pct"] = (ziel - kurs) / hoehe * 100

        zeilen.append(zeile)

    # EU vor USA: Ticker mit .DE-Endung zuerst, dann Rest alphabetisch.
    zeilen.sort(key=lambda z: (0 if str(z["ticker"]).endswith(".DE") else 1, z["ticker"]))

    if not zeilen:
        print("Keine Block-1-Treffer, nichts zu schreiben.")
        return

    # Spaltenmenge aus ALLEN Zeilen, nicht nur aus der ersten. Seit das
    # Pufferfenster um die Ankerzeile wandert (Entscheidung 149), hat jeder
    # Wert andere p-Spalten: ein Anker bei 2,00 ATR liefert p1 bis p3, einer
    # bei 3,75 liefert p2.75 bis p4. Die alte Fassung nahm die Spalten der
    # ersten Zeile und brach mit "dict contains fields not in fieldnames" ab.
    # Reihenfolge: erst die festen Spalten in der Reihenfolge ihres
    # Auftretens, dann die Pufferspalten aufsteigend nach Puffer.
    fest, puffer_spalten = [], set()
    for z in zeilen:
        for k in z:
            if re.match(r"^p\d", str(k)):
                puffer_spalten.add(k)
            elif k not in fest:
                fest.append(k)

    def _sortier(spalte: str):
        m_ = re.match(r"^p([\d.]+)_(.*)$", spalte)
        return (float(m_.group(1)), m_.group(2)) if m_ else (99.0, spalte)

    feldnamen = fest + sorted(puffer_spalten, key=_sortier)

    os.makedirs(DOCS, exist_ok=True)
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=feldnamen)
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")


if __name__ == "__main__":
    main()