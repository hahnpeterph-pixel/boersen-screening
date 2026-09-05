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
"""

from __future__ import annotations

import csv
import gzip
import os

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


def block1_treffer(markt: pd.DataFrame, analysten: pd.DataFrame) -> list[str]:
    """Dieselbe Bedingung wie in Report-Spalte AJ: AF & AG & AZ & (AH | DG).

    AF = Kurs < EMA50, AG = gruene Kerze, AH = Tief1 bestaetigt,
    DG = kein neues Tief, AZ = Kaufanteil >= 75%. RSI ist seit
    Entscheidung 79/03.09.2026 bewusst KEIN Gate mehr.
    """
    treffer = []
    for ticker in markt.index:
        if ticker not in analysten.index:
            continue
        z = markt.loc[ticker]
        a = analysten.loc[ticker]
        af = pd.notna(z.ema50) and z.kurs < z.ema50
        ag = z.kurs > z.open
        ah = z.tief1_best == 1
        dg = z.kein_neues_tief == 1
        az = pd.notna(a.kaufen_pct) and (a.kaufen_pct / 100) >= 0.75
        if af and ag and az and (ah or dg):
            treffer.append(ticker)
    return treffer


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
        if ziel not in kette:
            continue
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


def main() -> None:
    markt = pd.read_csv(os.path.join(DOCS, "marktdaten.csv")).set_index("ticker")
    analysten = pd.read_csv(os.path.join(DOCS, "analysten.csv")).set_index("ticker")
    phasen = pd.read_csv(os.path.join(DOCS, "phasen.csv")).set_index("ticker")
    rsi_schwellen = pd.read_csv(os.path.join(DOCS, "rsi_schwellen.csv"))
    luecken = pd.read_csv(os.path.join(DOCS, "luecken.csv"))
    with gzip.open(os.path.join(DOCS, "puffer_je_tief.csv.gz")) as f:
        puffer = pd.read_csv(f)

    puffer = puffer.sort_values(["ticker", "datum"])
    puffer["serie"] = (puffer["position"] == 1).cumsum()
    serientiefe = (
        puffer.groupby(["ticker", "serie"])
        .agg(n=("position", "max"), t1=("tief", "first"), tl=("tief", "last"), atr1=("atr", "first"))
        .reset_index()
    )
    serientiefe = serientiefe[serientiefe.n >= 2]
    serientiefe["tiefe_atr"] = (serientiefe.t1 - serientiefe.tl) / serientiefe.atr1
    serientiefe_je_wert = {
        t: g["tiefe_atr"].to_numpy() for t, g in serientiefe.groupby("ticker")
    }

    ketten_je_wert: dict[str, dict[int, tuple]] = {}
    for t, gruppe in rsi_schwellen.groupby("ticker"):
        ketten_je_wert[t] = {
            int(r.position): (int(r.faelle), r.rsi_p75, r.rsi_min, r.rsi_max, r.anteil_serien)
            for r in gruppe.itertuples()
        }

    treffer = block1_treffer(markt, analysten)
    print(f"Block-1-Treffer heute: {len(treffer)}")

    zeilen = []
    for t in treffer:
        z = markt.loc[t]
        a = analysten.loc[t]
        kurs, atr, tief = float(z.kurs), float(z.atr14), float(z.tief1)
        position = z.tiefs_serie
        ziel = float(a.kursziel) if pd.notna(a.kursziel) else None
        eigen = ziel - 0.10 * kurs if ziel is not None else None

        kette_wert = ketten_je_wert.get(t, {})
        kette_roh = {
            p: (v[0], kette_wert[p + 1][0])
            for p, v in kette_wert.items()
            if (p + 1) in kette_wert
        }
        schwelle = kette_wert.get(int(position)) if position == position and position else None

        ueblich = phasen.loc[t, "korrektur_atr"] if t in phasen.index else None
        luecken_wert = luecken[luecken.ticker == t]
        arr_serientiefe = serientiefe_je_wert.get(t)

        teil_puffer = puffer[puffer.ticker == t]
        teil_position = (
            teil_puffer[teil_puffer.position == position] if position == position else teil_puffer.iloc[0:0]
        )

        zeile = {
            "ticker": t,
            "name": a.get("name", t),
            "boerse": a.get("index", ""),
            "branche": a.get("sektor", ""),
            "kurs": kurs,
            "atr14": atr,
            "bezugstief": tief,
            "bezugstief_datum": z.tief1_datum,
            "bezugstief_bestaetigt": int(z.tief1_best) if pd.notna(z.tief1_best) else 0,
            "position": position,
            "fortsetzungskette": fortsetzungskette(kette_roh, position),
            "rsi_heute": z.rsi14,
            "rsi_min": schwelle[2] if schwelle else None,
            "rsi_max": schwelle[3] if schwelle else None,
            "rsi_schwelle": schwelle[1] if schwelle else None,
            "rsi_schwelle_faelle": schwelle[0] if schwelle else None,
            "rsi_schwelle_anteil_serien": schwelle[4] if schwelle else None,
            "kaufanteil_pct": a.kaufen_pct,
            "banken": a.banken,
            "kursziel": ziel,
            "eigenes_ziel": eigen,
            "korrektur_atr": z.korr_ist_atr,
            "korrektur_tage": z.korr_ist_tage,
            "korrektur_ueblich_atr": ueblich,
            "long_anteil_tr": "nicht erfasst - bitte Screenshot",
            "luecken": luecken_zeile(luecken_wert, kurs) if len(luecken_wert) else "keine Daten",
        }

        for puf in [1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00]:
            ko = tief - puf * atr
            haelt_position, n_position = _haelt(teil_position, puf)
            haelt_alle, n_alle = _haelt(teil_puffer, puf)
            ko_haelt = (
                (arr_serientiefe < puf).mean() * 100
                if arr_serientiefe is not None and len(arr_serientiefe)
                else None
            )
            hoehe = kurs - ko
            zeile[f"p{puf:g}_ko"] = ko
            zeile[f"p{puf:g}_abstand_pct"] = (kurs - ko) / kurs * 100 if kurs else None
            zeile[f"p{puf:g}_einsatz"] = 50 + 50 * puf
            zeile[f"p{puf:g}_haelt63_position_pct"] = haelt_position
            zeile[f"p{puf:g}_haelt63_position_n"] = n_position
            zeile[f"p{puf:g}_haelt63_alle_pct"] = haelt_alle
            zeile[f"p{puf:g}_haelt63_alle_n"] = n_alle
            zeile[f"p{puf:g}_ko_haelt_pct"] = ko_haelt
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

    os.makedirs(DOCS, exist_ok=True)
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")


if __name__ == "__main__":
    main()