#!/usr/bin/env python3
"""
Phasen — wie laeuft eine Korrektur bei DIESEM Wert typischerweise ab?

Beantwortet drei Fragen je Basiswert, historisch gemessen:

  1. Wie viele Tiefs entstehen ueblicherweise, bis der naechste Anstieg
     startet? Also: wie oft laeuft die Treppe nach unten weiter, statt
     dass es dreht.
  2. Wie lange dauert die Korrektur, vom ersten bis zum letzten Tief?
  3. Wie lange dauert der Anstieg danach, und wie weit traegt er?

Grundlage sind die Tiefs nach der Umkehr-Regel, identisch zu
marktdaten.py: eine Abwaertsstrecke endet, sobald der Kurs das HOCH der
Tiefkerze ueberschreitet. Eine Aufwaertsstrecke endet, sobald der Kurs das
TIEF der Hoechstkerze unterschreitet.

Eine ABWAERTSSEQUENZ ist eine Folge von Tiefs, bei der jedes tiefer liegt
als das vorherige. Sie endet, sobald ein Tief hoeher liegt als sein
Vorgaenger - das ist der Beginn des Anstiegs. Der ANSTIEG laeuft von dort
bis zum letzten Hoch, bevor wieder ein tieferes Tief entsteht.

Alle Laengen in Handelstagen, alle Kursbewegungen in ATR(14) zum Zeitpunkt
des jeweiligen Tiefs - so sind Werte unterschiedlicher Groesse vergleichbar.

Ausgabe:
  docs/phasen.csv  -> eine Zeile je Wert, zum Einlesen ins Orderbuch
  docs/phasen.md   -> lesbare Uebersicht mit Gesamtverteilung

Aufruf:  python3 phasen.py
         python3 phasen.py --jahre 5

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

import kurse
import historie
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
CSV_AUS = DOCS / "phasen.csv"
MD_AUS = DOCS / "phasen.md"

JAHRE = 7  # 19.09.2026: gleiche Grundlage wie historie.py und die Fortsetzungskette
ATR_TAGE = 14


def atr(df: pd.DataFrame, tage: int = ATR_TAGE) -> pd.Series:
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vor = schluss.shift(1)
    spanne = pd.concat([hoch - tief, (hoch - vor).abs(), (tief - vor).abs()], axis=1).max(axis=1)
    return spanne.ewm(alpha=1 / tage, adjust=False).mean()


def pivots(df: pd.DataFrame) -> list[tuple[str, int]]:
    """Durchreiche auf tiefs_regel.pivots - eine Definition fuer alles."""
    return regel.pivots(df)


def rsi_reihe(df: pd.DataFrame, tage: int = 14) -> pd.Series:
    d = df["Close"].diff()
    g = d.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    v = (-d.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    return 100 - 100 / (1 + g / v.replace(0, np.nan))


def verkaufs_rsi(df: pd.DataFrame) -> dict:
    """Bei welchem RSI dreht DIESER Wert historisch nach unten?

    Die Verkaufsregel 'RSI ab 70' ist eine Zahl fuer alle Werte. Tatsaechlich
    dreht ein ruhiger Titel schon bei 62, ein Momentumwert erst bei 78. Wer
    ueberall 70 nimmt, verkauft die einen zu spaet und die anderen zu frueh.

    Gemessen wird der RSI an den bestaetigten HOCHS nach der Umkehr-Regel -
    also genau an den Punkten, an denen die Aufwaertsstrecke endete. Der
    Median ist der werttypische Verkaufsbereich, das 75-Prozent-Quantil die
    Zone, in der es meistens vorbei ist.
    """
    p = pivots(df)
    r = rsi_reihe(df).values
    werte = [r[i] for art, i in p if art == "hoch" and np.isfinite(r[i])]
    if len(werte) < 5:
        return {}
    a = np.array(werte)
    return {"vk_rsi_tiefster": float(a.min()),
            "vk_rsi_median": float(np.median(a)),
            "vk_rsi_hoechster": float(a.max()),
            "vk_rsi_p75": float(np.percentile(a, 75)),
            "vk_rsi_faelle": int(a.size)}


def kauf_rsi(df: pd.DataFrame) -> dict:
    """Bei welchem RSI dreht DIESER Wert historisch nach oben?

    Das Gegenstueck zu verkaufs_rsi. Die Kaufregel 'RSI unter 50' und die
    Punktschwelle 'unter 30' sind Zahlen fuer alle Werte - genauso falsch
    wie die 70 auf der Verkaufsseite. Gemessen wird der RSI an den
    bestaetigten TIEFS nach der Umkehr-Regel, also dort, wo die
    Abwaertsstrecke endete.

    Der Median ist der werttypische Kaufbereich, das 25-Prozent-Quantil die
    Zone, in der es bei diesem Papier wirklich ausverkauft war.
    """
    p = pivots(df)
    r = rsi_reihe(df).values
    werte = [r[i] for art, i in p if art == "tief" and np.isfinite(r[i])]
    if len(werte) < 5:
        return {}
    a = np.array(werte)
    return {"kauf_rsi_tiefster": float(a.min()),
            "kauf_rsi_median": float(np.median(a)),
            "kauf_rsi_hoechster": float(a.max()),
            "kauf_rsi_p25": float(np.percentile(a, 25)),
            "kauf_rsi_faelle": int(a.size)}


def puffer_bedarf(df: pd.DataFrame, fenster: int = 10) -> dict:
    """Wie tief unterschreitet DIESER Wert seine Tiefs?

    Die Regel '2 ATR Puffer' stammt aus dem Durchschnitt ueber alle Werte.
    Tatsaechlich haelt ein ruhiges Papier seine Tiefs enger als ein
    zerrissenes. Gemessen wird je bestaetigtem Tief, wie weit der Kurs in
    den naechsten Handelstagen darunter rutschte, in ATR zum Zeitpunkt des
    Tiefs.

    Ausgewiesen werden der Anteil der Tiefs, die vollstaendig hielten, und
    die Quantile - p90 heisst: dieser Puffer haette 90 Prozent der Faelle
    ueberstanden.
    """
    p = pivots(df)
    a = atr(df).values
    tief = df["Low"].values
    n = len(df)
    werte = []
    for art, i in p:
        if art != "tief" or i + fenster >= n:
            continue
        if not np.isfinite(a[i]) or a[i] <= 0:
            continue
        danach = tief[i + 1:i + 1 + fenster].min()
        werte.append(max(0.0, (tief[i] - danach) / a[i]))
    if len(werte) < 5:
        return {}
    x = np.array(werte)
    return {"puffer_haelt_pct": float((x <= 0.001).mean() * 100),
            "puffer_p75": float(np.percentile(x, 75)),
            "puffer_p90": float(np.percentile(x, 90)),
            "puffer_p95": float(np.percentile(x, 95))}


def phasen(df: pd.DataFrame) -> list[dict]:
    """Abwaertssequenzen und die jeweils folgenden Anstiege."""
    p = pivots(df)
    tiefe = [(i, float(df["Low"].values[i])) for art, i in p if art == "tief"]
    hochs = [(i, float(df["High"].values[i])) for art, i in p if art == "hoch"]
    if len(tiefe) < 3:
        return []

    a = atr(df).values
    ergebnis = []
    # Sequenzabgrenzung seit 22.08.2026 aus tiefs_regel: gezaehlt werden nur
    # neue Tiefststaende, ein hoeheres Zwischentief beendet die Strecke
    # nicht mehr. Die alte Schleife hier brach beim ersten hoeheren Tief ab
    # und lieferte deshalb kuerzere Sequenzen als die Chartablesung.
    for seq in regel.sequenzen(df):
        if seq["laufend"]:
            continue          # ohne Ende kein Anstieg zu messen
        letztes_i = seq["ende_i"]
        letztes_kurs = float(df["Low"].values[letztes_i])
        anzahl = seq["anzahl"]
        start_pos = seq["start_i"]

        atr_hier = a[letztes_i]
        if not np.isfinite(atr_hier) or atr_hier <= 0:
            continue

        # Die Korrektur beginnt beim letzten Hoch VOR dem ersten Tief der
        # Sequenz, nicht beim ersten Tief selbst - sonst waere die Dauer
        # null, sobald eine Sequenz nur aus einem Tief besteht.
        vorhoch = [(i, h) for i, h in hochs if i < start_pos]
        if vorhoch:
            start_i, start_kurs = vorhoch[-1]
        else:
            start_i, start_kurs = start_pos, float(df["Low"].values[start_pos])
        dauer_ab = letztes_i - start_i
        tiefe_ab = (start_kurs - letztes_kurs) / atr_hier

        # Anstieg, symmetrisch gemessen: bis zum NAECHSTEN bestaetigten Hoch.
        # Beide Strecken laufen damit von Pivot zu Pivot und sind direkt
        # vergleichbar. Die frueher benutzte Variante (hoechstes Hoch, bevor
        # ein tieferes Tief kommt) war unsymmetrisch: die Korrektur endete am
        # Tief, der Anstieg lief in einem Aufwaertsmarkt monatelang weiter.
        # Deshalb kam dort ein Verhaeltnis von 2,5 zu 1 heraus, das kein
        # Vorteil war, sondern ein Messfehler.
        naechstes_hoch = next(((i, h) for i, h in hochs if i > letztes_i), None)
        if naechstes_hoch:
            gipfel_i, gipfel_kurs = naechstes_hoch
            dauer_auf = gipfel_i - letztes_i
            hoehe_auf = (gipfel_kurs - letztes_kurs) / atr_hier
        else:
            dauer_auf = hoehe_auf = None

        # Zusaetzlich die weite Fassung: wie weit traegt es maximal, bevor
        # ein tieferes Tief kommt. Nur zur Einordnung, nicht fuer Vergleiche.
        naechstes_tieferes = next((i for i, kurs in tiefe
                                   if i > letztes_i and kurs < letztes_kurs), None)
        grenze = naechstes_tieferes if naechstes_tieferes is not None else len(df) - 1
        weit = [(i, h) for i, h in hochs if letztes_i < i <= grenze]
        if weit:
            w_i, w_kurs = max(weit, key=lambda x: x[1])
            dauer_weit = w_i - letztes_i
            hoehe_weit = (w_kurs - letztes_kurs) / atr_hier
        else:
            dauer_weit = hoehe_weit = None

        ergebnis.append({
            "tiefs": anzahl,
            "dauer_ab": dauer_ab,
            "tiefe_ab": tiefe_ab,
            "dauer_auf": dauer_auf,
            "hoehe_auf": hoehe_auf,
            "dauer_weit": dauer_weit,
            "hoehe_weit": hoehe_weit,
        })
    return ergebnis


def median(werte) -> float | None:
    sauber = [w for w in werte if w is not None and np.isfinite(w)]
    return float(np.median(sauber)) if sauber else None


def tiefster(werte) -> float | None:
    sauber = [w for w in werte if w is not None and np.isfinite(w)]
    return float(min(sauber)) if sauber else None


def hoechster(werte) -> float | None:
    sauber = [w for w in werte if w is not None and np.isfinite(w)]
    return float(max(sauber)) if sauber else None


def perzentil(werte, q: float) -> float | None:
    sauber = [w for w in werte if w is not None and np.isfinite(w)]
    return float(np.percentile(sauber, q)) if sauber else None


def spanne(name: str, werte) -> dict:
    """Je Kennzahl sechs Spalten: tiefster Wert, Median, p75, p90, p95,
    hoechster Wert.

    Beschlossen am 24.08.2026. Der Median bleibt der Median ueber ALLE
    Faelle - ein Vorhersagetest ueber 25.829 Faelle hat gezeigt, dass ein
    getrimmtes Mittel beim noetigen Puffer 9,9 Prozent und beim Anstieg
    19,2 Prozent schlechter trifft. Die Nachbarspalten zeigen nur die
    Verteilung und aendern die Kennzahl nicht.

    Perzentile ergaenzt am 17.09.2026. Grund: Die Kaufvorlage braucht
    Saetze der Form "neun von zehn Korrekturen blieben flacher als X ATR".
    Dafuer reichten tiefster/Median/hoechster nicht - der hoechste Wert
    ist ein Einzelfall und als Massstab unbrauchbar. Gemessen ueber 223
    Werte mit halbierter Historie weicht der hoechste Wert zwischen beiden
    Haelften im Mittel um 24,9 Prozent ab, p90 nur um 8,9 Prozent und der
    Median um 6,4 Prozent. Der hoechste Wert bleibt als Randnotiz in der
    Datei, taugt aber nicht als Entscheidungsgrundlage.
    """
    return {f"{name}_tiefster": tiefster(werte),
            name: median(werte),
            f"{name}_p75": perzentil(werte, 75),
            f"{name}_p90": perzentil(werte, 90),
            f"{name}_p95": perzentil(werte, 95),
            f"{name}_hoechster": hoechster(werte)}


def korr_je_tief(ph: list[dict]) -> str:
    """Korrekturtiefe AB HOCH, getrennt nach erreichter Tiefsposition.

    Ergaenzt 19.09.2026 (Peter, Costco): "Es muss immer der gleiche Bezug
    sein. Also ab Hoch." Die Kaufvorlage hatte zuvor die Tiefe ab Hoch aus
    dieser Datei mit dem Rest ab dem damaligen Tief (benoetigt_atr aus
    historie.py) addiert - zwei Bezuege, dazu zwei Zeitraeume. Ergebnis war
    der Widerspruch "19 von 20 enden nach 0,1 ATR, 13 von 15 nach 5,8".

    Je Position k zaehlen nur die Serien, die MINDESTENS k Tiefs erreicht
    haben - also die Faelle, die an derselben Stelle standen wie der Wert
    heute. Gemessen wird wie korrektur_atr: vom Hoch vor der Serie bis zum
    letzten Tief der Serie (Peters Wahl a, 19.09.2026). Derselbe Anker wie
    marktdaten.korrektur_ist(), die Ist-Tiefe ist also direkt vergleichbar.

    Format je Position "k:faelle:p90:p95:max", Positionen mit ";" getrennt.
    Eine Textspalte statt 5 x 4 Einzelspalten, damit phasen.csv nicht
    ausufert und neue Positionen ohne neue Spalten dazukommen.
    """
    teile = []
    for k in range(1, max((p["tiefs"] for p in ph), default=0) + 1):
        w = [p["tiefe_ab"] for p in ph
             if p["tiefs"] >= k and p["tiefe_ab"] is not None and np.isfinite(p["tiefe_ab"])]
        if not w:
            continue
        teile.append(f"{k}:{len(w)}:{np.percentile(w, 90):.2f}:"
                     f"{np.percentile(w, 95):.2f}:{max(w):.2f}")
    return ";".join(teile)


# lade() stand hier bis 30.08.2026 als wortwoertliche Kopie von
# historie.lade() - selbe Funktion, zweimal im Repo gepflegt. Jetzt einfach
# importiert (Frage 40, Fragen-Blatt).
lade = historie.lade


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])

    # Dieselbe Logik wie historie.universum() - stand hier bis 30.08.2026
    # noch einmal inline, jetzt ebenfalls importiert statt kopiert.
    tickers = historie.universum()
    if not tickers:
        print("universe.json nicht gefunden oder leer.")
        return 1

    daten = lade(tickers, jahre)
    if len(daten) < 10:
        print("Zu wenige Kursdaten - Abbruch.")
        return 1

    zeilen = []
    for t, df in sorted(daten.items()):
        ph = phasen(df)
        if len(ph) < 3:
            continue
        vk = verkaufs_rsi(df)
        ka = kauf_rsi(df)
        pb = puffer_bedarf(df)
        zeilen.append({
            "ticker": t,
            "sequenzen": len(ph),
            **spanne("tiefs_median", [p["tiefs"] for p in ph]),
            "tiefs_max": max(p["tiefs"] for p in ph),
            # Die letzten fuenf Sequenzen im Klartext - beantwortet die Frage
            # "wie viele Tiefs hatte die VORIGE Abwaertsstrecke", die ein
            # Median nicht beantworten kann.
            "tiefs_letzte": " ".join(str(p["tiefs"]) for p in ph[-5:]),
            **spanne("korrektur_tage", [p["dauer_ab"] for p in ph]),
            **spanne("korrektur_atr", [p["tiefe_ab"] for p in ph]),
            **spanne("anstieg_tage", [p["dauer_auf"] for p in ph]),
            **spanne("anstieg_atr", [p["hoehe_auf"] for p in ph]),
            **spanne("weit_tage", [p["dauer_weit"] for p in ph]),
            **spanne("weit_atr", [p["hoehe_weit"] for p in ph]),
            "korr_je_tief": korr_je_tief(ph),
            # Jede abgeschlossene Korrektur einzeln (Peter 25.09.2026): ersetzt
            # in der Kaufvorlage die Spalte "alle". Gezaehlt wird ab dem Hoch:
            # von allen Korrekturen, die mindestens so tief gingen wie die
            # heutige, wie viele blieben ueber dem KO. Format "tiefs:tiefe_ab"
            # je Korrektur, Leerzeichen getrennt, zeitlich geordnet.
            "korr_tiefen": " ".join(f"{p['tiefs']}:{p['tiefe_ab']:.2f}" for p in ph
                                    if p["tiefe_ab"] is not None and np.isfinite(p["tiefe_ab"])),
            **vk, **ka, **pb,
        })

    DOCS.mkdir(parents=True, exist_ok=True)
    # Feste Spaltenfolge statt der Schluessel der ERSTEN Zeile: Werte mit zu
    # kurzer Historie liefern die Zusatzkennzahlen nicht, und stand so ein
    # Wert an erster Stelle, fehlten die Spalten im Kopf - der Schreibvorgang
    # brach dann bei der ersten vollstaendigen Zeile ab.
    def drei(name: str) -> list[str]:
        """Sechs Spalten seit 17.09.2026 - Name aus Ruecksicht auf die
        Aufrufstellen beibehalten, siehe spanne()."""
        return [f"{name}_tiefster", name, f"{name}_p75", f"{name}_p90",
                f"{name}_p95", f"{name}_hoechster"]

    SPALTEN = (["ticker", "sequenzen"]
               + drei("tiefs_median") + ["tiefs_max"]
               + drei("korrektur_tage") + drei("korrektur_atr")
               + drei("anstieg_tage") + drei("anstieg_atr")
               + drei("weit_tage") + drei("weit_atr")
               + ["tiefs_letzte"]
               + ["vk_rsi_tiefster", "vk_rsi_median", "vk_rsi_hoechster",
                  "vk_rsi_p75", "vk_rsi_faelle"]
               + ["kauf_rsi_tiefster", "kauf_rsi_median", "kauf_rsi_hoechster",
                  "kauf_rsi_p25", "kauf_rsi_faelle"]
               + ["puffer_haelt_pct", "puffer_p75", "puffer_p90", "puffer_p95"]
               + ["korr_je_tief", "korr_tiefen"])
    with CSV_AUS.open("w", encoding="utf-8", newline="") as f:
        s = csv.DictWriter(f, fieldnames=SPALTEN, extrasaction="ignore")
        s.writeheader()
        for z in zeilen:
            s.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in z.items()})

    def spalte(name):
        return [z[name] for z in zeilen if z.get(name) is not None]

    def m0(name, nk=0, einheit=""):
        """Median einer Spalte als Text. Fehlt die Kennzahl bei allen Werten,
        steht ein Strich statt eines Formatierungsfehlers."""
        w = spalte(name)
        return f"{median(w):.{nk}f}{einheit}" if w else "-"

    L = ["# Phasen - Korrektur und Anstieg je Wert", "",
         f"_Erstellt {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC, {jahre} Jahre Historie, "
         f"{len(zeilen)} Werte. Tiefs nach der Umkehr-Regel. Eine Abwaertssequenz ist eine Folge "
         "von Tiefs, bei der jedes tiefer liegt als das vorherige; sie endet mit dem ersten "
         "hoeheren Tief. Alle Werte sind Mediane, Laengen in Handelstagen, Bewegungen in ATR(14)._", "",
         "## Gesamtbild", "",
         "| Kennzahl | Median ueber alle Werte |", "|---|---|",
         f"| Tiefs je Abwaertssequenz | {median(spalte('tiefs_median')):.1f} |",
         f"| Dauer der Korrektur | {median(spalte('korrektur_tage')):.1f} Handelstage |",
         f"| Tiefe der Korrektur | {median(spalte('korrektur_atr')):.2f} ATR |",
         f"| Dauer des Anstiegs (bis zum naechsten Hoch) | {median(spalte('anstieg_tage')):.1f} Handelstage |",
         f"| Hoehe des Anstiegs (bis zum naechsten Hoch) | {median(spalte('anstieg_atr')):.2f} ATR |",
         f"| Dauer der weiten Fassung | {median(spalte('weit_tage')):.1f} Handelstage |",
         f"| Hoehe der weiten Fassung | {median(spalte('weit_atr')):.2f} ATR |",
         f"| Verkaufs-RSI, Median ueber alle Werte | {m0('vk_rsi_median', 0, '')} |",
         f"| Verkaufs-RSI, 75-Prozent-Wert | {m0('vk_rsi_p75', 0, '')} |",
         f"| Kauf-RSI, Median ueber alle Werte | {m0('kauf_rsi_median', 0, '')} |",
         f"| Kauf-RSI, 25-Prozent-Wert | {m0('kauf_rsi_p25', 0, '')} |",
         f"| Anteil Tiefs, die vollstaendig halten | {m0('puffer_haelt_pct', 0, '%')} |",
         f"| Puffer fuer 90 Prozent der Faelle | {m0('puffer_p90', 2, ' ATR')} |", "",
         "_KAUF-RSI ist der RSI an den bestaetigten Tiefs dieses Wertes, VERKAUFS-RSI der an den "
         "Hochs. Beide ersetzen die pauschalen Schwellen 50 bzw. 70 durch das, was dieses Papier "
         "tatsaechlich tut. PUFFER 90% ist der Abstand, den die KO-Schwelle bei diesem Wert "
         "braucht, um neun von zehn Tiefunterschreitungen zu ueberstehen - der Ersatz fuer die "
         "pauschalen 2 ATR._", "",
         "_VERKAUFS-RSI ist der RSI an den bestaetigten Hochs dieses Wertes - dort, wo die "
         "Aufwaertsstrecke endete. Die pauschale Regel 'RSI ab 70' passt nur fuer Werte, deren "
         "Median dort liegt; bei den anderen verkauft sie zu frueh oder zu spaet._", "",
         "_'Anstieg' ist von Pivot zu Pivot gemessen und damit direkt mit der Korrektur "
         "vergleichbar. 'weit' misst dagegen bis zum hoechsten Punkt, bevor ein tieferes "
         "Tief kommt - diese Zahl faellt in einem Aufwaertsmarkt zwangslaeufig gross aus "
         "und taugt nur zur Einordnung, nicht zum Vergleich._", "",
         "## Je Wert", "",
         "| Ticker | Sequenzen | Tiefs Median | Tiefs max | letzte fuenf | Korrektur Tage | Korrektur ATR | "
         "Anstieg Tage | Anstieg ATR | Anstieg/Korrektur | weit Tage | weit ATR | "
         "Kauf-RSI Median | Kauf-RSI 25% | Verkaufs-RSI Median | Verkaufs-RSI 75% | "
         "Tief haelt | Puffer 90% |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def z(v, nk=1, einheit=""):
        """Zahl als Text, mit Strich fuer fehlende Werte. Die Einheit steht
        direkt dahinter - ohne sie brach der Bericht ab, sobald eine Zeile
        einen Prozentwert ausweisen sollte."""
        return "-" if v is None else f"{v:.{nk}f}{einheit}"

    for e in sorted(zeilen, key=lambda x: -((x["anstieg_atr"] or 0) / (x["korrektur_atr"] or 1))):
        v = (e["anstieg_atr"] / e["korrektur_atr"]
             if e["anstieg_atr"] and e["korrektur_atr"] else None)
        L.append(f"| {e['ticker']} | {e['sequenzen']} | {z(e['tiefs_median'])} | {e['tiefs_max']} | "
                 f"{e.get('tiefs_letzte','-')} | "
                 f"{z(e['korrektur_tage'])} | {z(e['korrektur_atr'], 2)} | "
                 f"{z(e['anstieg_tage'])} | {z(e['anstieg_atr'], 2)} | "
                 f"**{z(v, 2)}** | {z(e['weit_tage'])} | {z(e['weit_atr'], 2)} | "
                 f"**{z(e.get('kauf_rsi_median'), 0)}** | {z(e.get('kauf_rsi_p25'), 0)} | "
                 f"**{z(e.get('vk_rsi_median'), 0)}** | {z(e.get('vk_rsi_p75'), 0)} | "
                 f"{z(e.get('puffer_haelt_pct'), 0, '%')} | {z(e.get('puffer_p90'), 2)} ATR |")
    L += ["", "_Sortiert nach dem Verhaeltnis Anstieg zu Korrektur. Ein Wert mit vielen Tiefs je Sequenz braucht "
          "Geduld: dort folgen auf ein frisches Tief typischerweise noch weitere, bevor der "
          "Anstieg beginnt._"]

    MD_AUS.write_text("\n".join(L), encoding="utf-8")
    print(f"\nGeschrieben: {CSV_AUS} und {MD_AUS}")
    print("\n".join(L[:22]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
