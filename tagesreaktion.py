"""
tagesreaktion.py - Was folgt auf einen harten Verlusttag, und wie weit
werden grosse Laeufe korrigiert?

Die Frage entstand am 24.08.2026: Micron verlor an einem Tag 7,3 Prozent,
weil der chinesische Wettbewerber CXMT an die Boerse ging. War das
uebertrieben? Statt zu schaetzen wird gezaehlt.

Gemessen wird je Wert und je Groessenklasse des Tagesverlusts:
  - wie oft der Schluss nach 5, 10, 20 und 60 Handelstagen hoeher lag
  - wie tief der Kurs in dieser Zeit vorher noch fiel (in ATR und Prozent)
  - wie weit er im besten Fall stieg

Der zweite Teil beantwortet die Montagsfrage: liegt der Schluss je
Wochentag ueber der Eroeffnung, und kommt das Tagestief vor dem Tageshoch?

Der dritte Teil beantwortet die Frage vom 24.08.2026: wie weit werden
grosse Laeufe in der Regel korrigiert? Ein Lauf ist die Strecke von einem
bestaetigten Tief bis zum naechsten Swing-Hoch, die Korrektur die Strecke
von dort bis zum naechsten Tief. Gemessen wird beides in ATR und die
Korrektur zusaetzlich als Anteil des Laufs. Gruppiert wird nach der
Laufhoehe in ATR - das ist die "aehnliche Situation": ein Lauf von 20 ATR
wird anders korrigiert als einer von 3 ATR.

KEINE Sammelklassen: der Tagesverlust wird in Schritten von 0,25 ATR
gefuehrt, die Fallzahl steht in jeder Zeile. Keine Pools ueber Werte
hinweg - die gepoolte Zeile steht daneben, ersetzt aber nichts.

Aufruf:  python3 tagesreaktion.py --jahre 7
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import kurse
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
MD_AUS = DOCS / "tagesreaktion.md"
CSV_AUS = DOCS / "tagesreaktion.csv"
CSV_WOCHENTAG = DOCS / "wochentage.csv"
CSV_LAEUFE = DOCS / "laeufe.csv"

JAHRE = 7
ATR_TAGE = 14
FRISTEN = (5, 10, 20, 60)
# Verlustklassen in ATR, Viertelschritte. Oben offen, damit der Ausreisser
# nicht in einer Sammelklasse verschwindet.
KLASSEN = tuple(round(0.25 * k, 2) for k in range(1, 25))
WOCHENTAGE = ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag")

# Laufklassen in ATR. Ein Schritt von 1 ATR bis 30, danach offen. Bewusst
# fein: zwischen 4 und 8 ATR liegt bei manchen Werten der Unterschied
# zwischen halber und ganzer Rueckgabe.
LAUF_KLASSEN = tuple(float(k) for k in range(1, 31))


def atr(df: pd.DataFrame, tage: int = ATR_TAGE) -> np.ndarray:
    h, t, c = df["High"], df["Low"], df["Close"]
    vor = c.shift(1)
    tr = pd.concat([h - t, (h - vor).abs(), (t - vor).abs()], axis=1).max(axis=1)
    return tr.rolling(tage).mean().values


def klasse(x: float) -> float | None:
    """Groesste Klassenschwelle, die der Verlust erreicht."""
    if x is None or not np.isfinite(x) or x <= 0:
        return None
    treffer = [k for k in KLASSEN if x >= k]
    return treffer[-1] if treffer else None


def faelle_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    a = atr(df)
    schluss = df["Close"].values
    tief = df["Low"].values
    hoch = df["High"].values
    daten = df.index
    aus = []
    for i in range(1, len(df) - max(FRISTEN)):
        if not np.isfinite(a[i]) or a[i] <= 0:
            continue
        verlust = schluss[i - 1] - schluss[i]
        if verlust <= 0:
            continue
        k = klasse(verlust / a[i])
        if k is None:
            continue
        z = {"ticker": ticker, "datum": f"{daten[i]:%Y-%m-%d}",
             "klasse_atr": k,
             "verlust_atr": verlust / a[i],
             "verlust_pct": 100.0 * verlust / schluss[i - 1],
             "atr": a[i], "schluss": schluss[i]}
        for f in FRISTEN:
            fenster_t = tief[i + 1:i + 1 + f]
            fenster_h = hoch[i + 1:i + 1 + f]
            z[f"hoeher_{f}"] = int(schluss[i + f] > schluss[i])
            z[f"schluss_{f}_pct"] = 100.0 * (schluss[i + f] / schluss[i] - 1)
            z[f"tiefer_{f}_atr"] = (schluss[i] - float(fenster_t.min())) / a[i]
            z[f"hoch_{f}_atr"] = (float(fenster_h.max()) - schluss[i]) / a[i]
        aus.append(z)
    return aus


def wochentage_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Zweiter Teil: haelt der Wochentag, was ihm nachgesagt wird?"""
    o, c = df["Open"].values, df["Close"].values
    h, t = df["High"].values, df["Low"].values
    aus = []
    for tag_nr, tag in enumerate(WOCHENTAGE):
        maske = df.index.dayofweek == tag_nr
        if not maske.any():
            continue
        idx = np.flatnonzero(maske)
        gruen = [c[i] > o[i] for i in idx]
        # Kam das Tagestief vor dem Tageshoch? Auf Tagesbasis nicht
        # entscheidbar - deshalb der Ersatz: lag das Tief naeher an der
        # Eroeffnung als das Hoch, spricht das fuer "erst runter".
        erst_runter = [abs(o[i] - t[i]) < abs(h[i] - o[i]) for i in idx]
        aus.append({"ticker": ticker, "wochentag": tag, "faelle": len(idx),
                    "schluss_ueber_eroeffnung_pct": round(100.0 * float(np.mean(gruen)), 1),
                    "erst_runter_pct": round(100.0 * float(np.mean(erst_runter)), 1),
                    "mittlere_tagesrendite_pct": round(
                        float(np.mean([100.0 * (c[i] / o[i] - 1) for i in idx])), 3)})
    return aus


def laeufe_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Lauf und anschliessende Korrektur, je Paar aus Tief-Hoch-Tief.

    Lauf     = vom bestaetigten Tief bis zum naechsten Swing-Hoch
    Korrektur= von diesem Hoch bis zum naechsten Swing-Tief

    Beides in ATR zum Zeitpunkt des jeweiligen Startpunkts. Die Korrektur
    zusaetzlich als Anteil des Laufs - das ist die Zahl, nach der gefragt
    wurde: wurde die Haelfte zurueckgegeben, ein Drittel, alles?

    Laeuft die letzte Strecke noch, faellt sie raus: ohne Ende laesst sich
    nicht sagen, wie weit korrigiert wurde.
    """
    a = atr(df)
    tief_w, hoch_w = df["Low"].values, df["High"].values
    daten = df.index
    punkte = regel.pivots(df)
    aus = []
    for n in range(len(punkte) - 2):
        art1, i = punkte[n]
        art2, j = punkte[n + 1]
        art3, k = punkte[n + 2]
        if not (art1 == "tief" and art2 == "hoch" and art3 == "tief"):
            continue
        if not np.isfinite(a[i]) or a[i] <= 0 or not np.isfinite(a[j]) or a[j] <= 0:
            continue
        lauf_punkte = float(hoch_w[j]) - float(tief_w[i])
        korr_punkte = float(hoch_w[j]) - float(tief_w[k])
        if lauf_punkte <= 0:
            continue
        lauf_atr = lauf_punkte / a[i]
        korr_atr = korr_punkte / a[j]
        aus.append({
            "ticker": ticker,
            "datum_tief": f"{daten[i]:%Y-%m-%d}",
            "datum_hoch": f"{daten[j]:%Y-%m-%d}",
            "datum_tief_danach": f"{daten[k]:%Y-%m-%d}",
            "lauf_atr": round(lauf_atr, 3),
            "lauf_pct": round(100.0 * lauf_punkte / float(tief_w[i]), 2),
            "lauf_tage": int(j - i),
            "korrektur_atr": round(korr_atr, 3),
            "korrektur_pct": round(100.0 * korr_punkte / float(hoch_w[j]), 2),
            "korrektur_tage": int(k - j),
            "anteil_pct": round(100.0 * korr_punkte / lauf_punkte, 1),
            "klasse_lauf_atr": max([c for c in LAUF_KLASSEN if lauf_atr >= c],
                                   default=None),
        })
    return [x for x in aus if x["klasse_lauf_atr"] is not None]


def zeile_lauf(g: list[dict]) -> dict:
    """Wie weit wurde zurueckgegeben - volle Spannweite, kein blosser Median."""
    anteil = np.array([x["anteil_pct"] for x in g], dtype=float)
    katr = np.array([x["korrektur_atr"] for x in g], dtype=float)
    tage = np.array([x["korrektur_tage"] for x in g], dtype=float)
    r = {"faelle": len(g),
         "lauf_atr_median": round(float(np.median([x["lauf_atr"] for x in g])), 2),
         "lauf_tage_median": round(float(np.median([x["lauf_tage"] for x in g])), 1),
         "anteil_niedrigster": round(float(anteil.min()), 1),
         "anteil_hoechster": round(float(anteil.max()), 1),
         "korrektur_atr_niedrigster": round(float(katr.min()), 2),
         "korrektur_atr_hoechster": round(float(katr.max()), 2),
         "korrektur_tage_median": round(float(np.median(tage)), 1),
         "ganz_zurueck_pct": round(100.0 * float((anteil >= 100).mean()), 1)}
    for q in (10, 25, 50, 75, 90, 95, 99):
        r[f"anteil_p{q}"] = round(float(np.percentile(anteil, q)), 1)
        r[f"korrektur_atr_p{q}"] = round(float(np.percentile(katr, q)), 2)
    return r


def universum() -> list[str]:
    datei = BASE / "universe.json"
    if not datei.exists():
        return []
    roh = json.loads(datei.read_text(encoding="utf-8"))
    werte: list[str] = []
    for gruppe in roh.get("benchmarks", {}):
        werte += roh.get(gruppe, [])
    return sorted(set(werte))


def lade(tickers: list[str], jahre: int) -> dict[str, pd.DataFrame]:
    """Kursdaten fuer viele Werte auf einmal - ueber kurse.kerzen_batch()
    statt eigenem yf.download() (30.08.2026, Frage 40). auto_adjust=True
    und die 200-Tage-Mindestschwelle bleiben erhalten - diese Schwelle war
    hier hoeher als bei historie.py/phasen.py (120), deshalb bewusst NICHT
    vereinheitlicht, nur die Abrufquelle geteilt.

    universum() darunter bleibt eine EIGENE Funktion, keine Kopie von
    historie.universum() - sie laesst COMMODITIES und CRYPTO bewusst oder
    versehentlich weg (beim Vergleich am 30.08.2026 aufgefallen, noch
    nicht geklaert, welches von beidem). Deshalb hier nicht angeglichen -
    das waere eine Verhaltensaenderung, keine reine Code-Zusammenlegung."""
    print(f"Lade {len(tickers)} Werte, {jahre} Jahre ...")
    roh = kurse.kerzen_batch(tickers, period=f"{jahre}y", auto_adjust=True)
    daten = {t: d for t, d in roh.items() if len(d) > 200}
    print(f"  {len(daten)} Werte geladen.")
    return daten


def z(x, nk=0, einheit=""):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return f"{x:.{nk}f}{einheit}"


def zeile(g: list[dict]) -> dict:
    r = {"faelle": len(g),
         "verlust_atr_median": round(float(np.median([x["verlust_atr"] for x in g])), 2),
         "verlust_pct_median": round(float(np.median([x["verlust_pct"] for x in g])), 2)}
    for f in FRISTEN:
        r[f"hoeher_nach_{f}_pct"] = round(100.0 * float(np.mean([x[f"hoeher_{f}"] for x in g])), 1)
        r[f"schluss_{f}_median_pct"] = round(float(np.median([x[f"schluss_{f}_pct"] for x in g])), 2)
        r[f"tiefer_{f}_median_atr"] = round(float(np.median([x[f"tiefer_{f}_atr"] for x in g])), 2)
        r[f"tiefer_{f}_p90_atr"] = round(float(np.percentile([x[f"tiefer_{f}_atr"] for x in g], 90)), 2)
        r[f"hoch_{f}_median_atr"] = round(float(np.median([x[f"hoch_{f}_atr"] for x in g])), 2)
    return r


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])
    nur = None
    if "--wert" in sys.argv:
        nur = sys.argv[sys.argv.index("--wert") + 1]

    tickers = universum()
    if not tickers:
        print("universe.json nicht gefunden oder leer.")
        return 1
    if nur and nur not in tickers:
        tickers.append(nur)
    daten = lade(tickers, jahre)
    if len(daten) < 5:
        print("Zu wenige Kursdaten - Abbruch.")
        return 1

    alle: list[dict] = []
    wtage: list[dict] = []
    laeufe: list[dict] = []
    for t, df in daten.items():
        try:
            alle += faelle_je_wert(t, df)
            wtage += wochentage_je_wert(t, df)
            laeufe += laeufe_je_wert(t, df)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {t}: {exc}")
    print(f"  {len(alle)} Verlusttage und {len(laeufe)} Laeufe ausgewertet.")

    DOCS.mkdir(exist_ok=True)

    # ── CSV je Wert und Klasse ────────────────────────────────────
    zeilen = []
    je_wert_klasse: dict = defaultdict(list)
    je_klasse: dict = defaultdict(list)
    for x in alle:
        je_wert_klasse[(x["ticker"], x["klasse_atr"])].append(x)
        je_klasse[x["klasse_atr"]].append(x)
    for (t, k), g in sorted(je_wert_klasse.items()):
        zeilen.append({"ticker": t, "klasse_atr": k, **zeile(g)})
    for k, g in sorted(je_klasse.items()):
        zeilen.append({"ticker": "ALLE", "klasse_atr": k, **zeile(g)})
    with CSV_AUS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
        w.writeheader(); w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")

    # ── CSV Laeufe: eine Zeile JE LAUF, dazu die Auswertung ──────
    if laeufe:
        with (DOCS / "laeufe_roh.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(laeufe[0].keys()))
            w.writeheader(); w.writerows(laeufe)
        print(f"Geschrieben: {DOCS / 'laeufe_roh.csv'} ({len(laeufe)} Zeilen)")
        lz = []
        je_wert_lauf: dict = defaultdict(list)
        je_lauf: dict = defaultdict(list)
        for x in laeufe:
            je_wert_lauf[(x["ticker"], x["klasse_lauf_atr"])].append(x)
            je_lauf[x["klasse_lauf_atr"]].append(x)
        for (t, k), g in sorted(je_wert_lauf.items()):
            lz.append({"ticker": t, "klasse_lauf_atr": k, **zeile_lauf(g)})
        for k, g in sorted(je_lauf.items()):
            lz.append({"ticker": "ALLE", "klasse_lauf_atr": k, **zeile_lauf(g)})
        with CSV_LAEUFE.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(lz[0].keys()))
            w.writeheader(); w.writerows(lz)
        print(f"Geschrieben: {CSV_LAEUFE} ({len(lz)} Zeilen)")

    with CSV_WOCHENTAG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(wtage[0].keys()))
        w.writeheader(); w.writerows(wtage)
    print(f"Geschrieben: {CSV_WOCHENTAG} ({len(wtage)} Zeilen)")

    # ── Bericht ───────────────────────────────────────────────────
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = ["# Tagesreaktion - was folgt auf einen harten Verlusttag?", "",
         f"_Erstellt {jetzt}. {jahre} Jahre, {len(daten)} Werte, "
         f"{len(alle)} Verlusttage._", "",
         "_HOEHER NACH X ist der Anteil der Faelle, in denen der Schluss nach "
         "X Handelstagen ueber dem Schluss des Verlusttags lag. TIEFER ist, wie "
         "weit der Kurs in dieser Zeit VORHER noch fiel - die Zahl, die "
         "entscheidet, ob ein Knock-out ueberlebt haette. Alles in ATR des "
         "Verlusttags._", "",
         "## Gepoolt ueber alle Werte", "",
         "| Verlust ab | Faelle | hoeher 5T | hoeher 10T | hoeher 20T | "
         "hoeher 60T | tiefer 20T Median | tiefer 20T p90 |",
         "|---|---|---|---|---|---|---|---|"]
    for k, g in sorted(je_klasse.items()):
        r = zeile(g)
        L.append(f"| {k} ATR | {r['faelle']} | {z(r['hoeher_nach_5_pct'],0,'%')} | "
                 f"{z(r['hoeher_nach_10_pct'],0,'%')} | {z(r['hoeher_nach_20_pct'],0,'%')} | "
                 f"{z(r['hoeher_nach_60_pct'],0,'%')} | {z(r['tiefer_20_median_atr'],2)} | "
                 f"{z(r['tiefer_20_p90_atr'],2)} |")
    L += ["", "_Je Wert einzeln steht alles in `docs/tagesreaktion.csv` - "
          "keine Sammelklassen, Fallzahl in jeder Zeile._", "",
          "## Wochentage", "",
          "_Schluss ueber Eroeffnung je Wochentag, gemittelt ueber alle Werte. "
          "ERST RUNTER ist ein Ersatzmass: lag das Tagestief naeher an der "
          "Eroeffnung als das Tageshoch. Auf Tagesbasis ist die echte "
          "Reihenfolge nicht entscheidbar._", "",
          "| Wochentag | Faelle | Schluss ueber Eroeffnung | erst runter | "
          "mittlere Tagesrendite |", "|---|---|---|---|---|"]
    je_tag: dict = defaultdict(list)
    for x in wtage:
        je_tag[x["wochentag"]].append(x)
    for tag in WOCHENTAGE:
        g = je_tag.get(tag, [])
        if not g:
            continue
        n = sum(x["faelle"] for x in g)
        L.append(f"| {tag} | {n} | "
                 f"{z(float(np.mean([x['schluss_ueber_eroeffnung_pct'] for x in g])),1,'%')} | "
                 f"{z(float(np.mean([x['erst_runter_pct'] for x in g])),1,'%')} | "
                 f"{z(float(np.mean([x['mittlere_tagesrendite_pct'] for x in g])),3,'%')} |")
    if laeufe:
        L += ["", "## Wie weit werden grosse Laeufe korrigiert?", "",
              "_Ein Lauf ist die Strecke von einem Tief bis zum naechsten "
              "Swing-Hoch, die Korrektur die Strecke von dort bis zum naechsten "
              "Tief. ANTEIL ist die Korrektur als Prozent des Laufs: 50 heisst, "
              "die Haelfte wurde zurueckgegeben, 100 heisst, der Lauf war ganz "
              "weg. GANZ ZURUECK zaehlt die Faelle mit 100 Prozent oder mehr._",
              "",
              "| Lauf ab | Faelle | Lauf Median | Anteil p10 | p25 | Median | "
              "p75 | p90 | ganz zurueck | Korrektur Tage |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for k, g in sorted(je_lauf.items()):
            r = zeile_lauf(g)
            L.append(f"| {k:.0f} ATR | {r['faelle']} | {z(r['lauf_atr_median'],1)} ATR | "
                     f"{z(r['anteil_p10'],0,'%')} | {z(r['anteil_p25'],0,'%')} | "
                     f"{z(r['anteil_p50'],0,'%')} | {z(r['anteil_p75'],0,'%')} | "
                     f"{z(r['anteil_p90'],0,'%')} | {z(r['ganz_zurueck_pct'],0,'%')} | "
                     f"{z(r['korrektur_tage_median'],0)} |")
        L += ["", "_Je Wert einzeln in `docs/laeufe.csv`, jeder einzelne Lauf "
              "mit Datum in `docs/laeufe_roh.csv`._", ""]

    L += ["", "---", "",
          "_Keine Anlageberatung. Gezaehlte historische Kursverlaeufe._"]
    MD_AUS.write_text("\n".join(L), encoding="utf-8")
    print(f"Geschrieben: {MD_AUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
