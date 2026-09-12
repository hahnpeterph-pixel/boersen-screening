"""Lange Kurshistorie fuer Marktphasen-Auswertungen.

Warum es dieses Skript ueberhaupt gibt: kursverlauf.py schneidet auf 140
Kerzen ab. Das reicht fuer wertspezifische Aussagen an den Tiefs - dafuer
liefert puffer_je_tief.csv.gz rund 40.000 Faelle - aber nicht fuer Aussagen
ueber Marktphasen. Am 10.09.2026 sollte beantwortet werden, was nach einem
Tag folgt, an dem 81 Prozent aller Werte fallen. In 126 auswertbaren Tagen
gab es SIEBEN vergleichbare Faelle; die Folgequoten sprangen zwischen 33 und
67 Prozent hin und her. Das ist Rauschen, keine Erwartung.

Das Skript laeuft deshalb NICHT taeglich mit, sondern nur auf Zuruf
(workflow_dispatch). Es zieht sieben Jahre Tagesschluesse fuer das gesamte
Universum, legt sie gepackt ab und rechnet daraus die Marktbreite-Statistik.

Laufzeit rund 10 bis 20 Minuten, Ausgabe etwa 3 bis 6 MB gepackt.
"""

import gzip
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import kurse

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
CSV_AUS = os.path.join(DOCS, "markthistorie.csv.gz")
MD_AUS = os.path.join(DOCS, "marktbreite.md")

# Sieben Jahre. Yahoo liefert Tagesdaten deutlich weiter zurueck, aber
# alles vor 2019 hilft kaum: Indexzusammensetzung und Handelsverhalten
# haben sich zu stark veraendert, und die Corona-Verwerfungen 2020 wuerden
# als Ausreisser jede Verteilung dominieren, wenn der Zeitraum zu kurz ist,
# um sie einzuordnen. Sieben Jahre enthalten sie MIT genug Umfeld.
ZEITRAUM = "7y"

# Schwellen fuer die Breite-Auswertung, in Prozent gefallener Werte.
SCHWELLEN = [60, 65, 70, 75, 80, 85]

# Horizonte in Handelstagen.
HORIZONTE = [1, 2, 3, 4, 5, 6, 10, 20]


def universum() -> list[str]:
    """Dieselbe Liste wie kursverlauf.py, aus universe.json.

    Bewusst aus der Datei statt aus einem Import: markthistorie.py soll
    unabhaengig laufen koennen, auch wenn kursverlauf.py gerade umgebaut
    wird. Rohstoffe und Devisen bleiben draussen - sie handeln
    durchgehend und wuerden die Marktbreite verfaelschen.
    """
    pfad = os.path.join(HIER, "universe.json")
    with open(pfad, encoding="utf-8") as f:
        u = json.load(f)
    # universe.json ist uneinheitlich aufgebaut: DOW, NASDAQ, SP100, DAX und
    # Watchlist sind LISTEN von Tickern, COMMODITIES, CRYPTO und benchmarks
    # dagegen Dictionaries mit Ticker als Schluessel. Die erste Fassung rief
    # blind .keys() auf und brach am 10.09.2026 mit "'list' object has no
    # attribute 'keys'" ab. Beide Formen werden jetzt akzeptiert; die Gruppen
    # COMMODITIES, CRYPTO und benchmarks bleiben ohnehin draussen.
    tickers = []
    for gruppe in ("DOW", "NASDAQ", "SP100", "DAX", "Watchlist"):
        eintrag = u.get(gruppe)
        if isinstance(eintrag, dict):
            tickers += list(eintrag.keys())
        elif isinstance(eintrag, list):
            tickers += [str(x) for x in eintrag]
        elif eintrag is not None:
            print(f"  Gruppe {gruppe}: unerwarteter Typ "
                  f"{type(eintrag).__name__} - uebersprungen")
    if not tickers:
        sys.exit("universe.json lieferte keine Ticker - Abbruch.")
    raus = [t for t in tickers if t.endswith("=F") or t.endswith("=X")]
    if raus:
        print(f"  {len(raus)} Rohstoffe/Devisen ausgeschlossen")
    return list(dict.fromkeys(t for t in tickers if t not in raus))


def historie(tickers: list[str]) -> pd.DataFrame:
    """Tagesschluesse als DataFrame, Zeilen Ticker, Spalten Datum."""
    je_wert = {}
    fehlt = []
    for n, t in enumerate(tickers, 1):
        if n % 25 == 0:
            print(f"  {n}/{len(tickers)} ...")
        df = kurse.kerzen(t, period=ZEITRAUM)
        if df is None or df.empty or "Close" not in df.columns:
            fehlt.append(t)
            continue
        je_wert[t] = {str(d.date()): round(float(v), 4)
                      for d, v in zip(df.index, df["Close"])
                      if pd.notna(v)}
    if fehlt:
        # Sichtbar machen, nicht verschweigen: eine Marktbreite ueber ein
        # unvollstaendiges Universum ist eine andere Groesse als eine ueber
        # das ganze.
        print(f"  KEINE DATEN ({len(fehlt)}): " + ", ".join(sorted(fehlt)))
    alle_tage = sorted({d for w in je_wert.values() for d in w})
    print(f"  {len(je_wert)} Werte, {len(alle_tage)} Handelstage "
          f"({alle_tage[0]} bis {alle_tage[-1]})")
    return pd.DataFrame(
        [[je_wert[t].get(d) for d in alle_tage] for t in je_wert],
        index=list(je_wert), columns=alle_tage,
    )


def breite_auswertung(k: pd.DataFrame) -> str:
    """Was folgt auf Tage mit hohem Anteil gefallener Werte?

    Gerechnet wird auf dem gleichgewichteten Mittel aller Werte, nicht auf
    einem Index - das Universum ist keine Indexnachbildung, und ein
    kapitalgewichteter Durchschnitt haette bei 218 Werten die groessten
    fuenf zu stark gewichtet.

    MINDESTBESETZUNG: Ein Tag zaehlt nur, wenn mindestens die Haelfte der
    Werte an ihm UND am Vortag einen Kurs hat. Sonst wuerden fruehe Jahre,
    in denen viele Werte noch nicht notierten, die Breite verzerren.
    """
    tage = list(k.columns)
    ver = k.pct_change(axis=1) * 100
    besetzt = ver.notna().sum()
    gueltig = [t for t in tage[1:] if besetzt[t] >= len(k) * 0.5]
    breite = ((ver < 0).sum() / besetzt * 100)[gueltig]

    zeilen = [
        "# Marktbreite und was danach folgt",
        "",
        f"Stand {datetime.now(timezone.utc):%d.%m.%Y %H:%M} UTC. "
        f"{len(k)} Werte, {len(gueltig)} auswertbare Handelstage "
        f"({gueltig[0]} bis {gueltig[-1]}).",
        "",
        "Grundlage ist das gleichgewichtete Mittel aller Werte. Ein Tag "
        "zaehlt nur, wenn mindestens die Haelfte der Werte an ihm und am "
        "Vortag einen Kurs hat.",
        "",
        f"Breite im Mittel: Median {breite.median():.0f} Prozent gefallene "
        f"Werte, p25 {breite.quantile(.25):.0f}, p75 "
        f"{breite.quantile(.75):.0f}, p95 {breite.quantile(.95):.0f}.",
        "",
    ]

    def folge(auswahl, n):
        werte = []
        for t in auswahl:
            i = tage.index(t)
            if i + n >= len(tage):
                continue
            v = (k[tage[i + n]] / k[t] - 1) * 100
            m = v.mean()
            if not np.isnan(m):
                werte.append(m)
        return np.array(werte)

    basis = {n: folge(gueltig, n) for n in HORIZONTE}
    zeilen += ["## Basisrate ueber alle Tage", "",
               "| nach | Faelle | Median | positiv | p25 | p75 |",
               "|---|---|---|---|---|---|"]
    for n in HORIZONTE:
        a = basis[n]
        zeilen.append(
            f"| {n} T | {len(a)} | {np.median(a):+.2f} % | "
            f"{(a > 0).mean() * 100:.0f} % | {np.percentile(a, 25):+.2f} % | "
            f"{np.percentile(a, 75):+.2f} % |")
    zeilen.append("")

    for s in SCHWELLEN:
        auswahl = [t for t in gueltig if breite[t] >= s]
        zeilen += [f"## Tage mit mindestens {s} Prozent gefallenen Werten",
                   "",
                   f"{len(auswahl)} von {len(gueltig)} Tagen "
                   f"({len(auswahl) / len(gueltig) * 100:.1f} Prozent).",
                   ""]
        if len(auswahl) < 20:
            zeilen += ["Zu wenig Faelle fuer eine belastbare Aussage.", ""]
            continue
        zeilen += ["| nach | Faelle | Median | positiv | Basis positiv | Unterschied |",
                   "|---|---|---|---|---|---|"]
        for n in HORIZONTE:
            f_ = folge(auswahl, n)
            b_ = basis[n]
            if len(f_) < 20:
                continue
            q, qb = (f_ > 0).mean() * 100, (b_ > 0).mean() * 100
            zeilen.append(
                f"| {n} T | {len(f_)} | {np.median(f_):+.2f} % | {q:.0f} % | "
                f"{qb:.0f} % | {q - qb:+.0f} Punkte |")
        zeilen.append("")

    zeilen += ["## Lesehinweis", "",
               "Die Spalte 'Unterschied' ist die einzige, die zaehlt. Eine "
               "positiv-Quote von 60 Prozent sagt nichts, wenn die Basisrate "
               "ebenfalls bei 60 liegt. Erst ein Abstand von mehreren Punkten "
               "bei ausreichend Faellen ist ein Befund.", ""]
    return "\n".join(zeilen)


def main() -> None:
    tickers = universum()
    print(f"Markthistorie fuer {len(tickers)} Werte, Zeitraum {ZEITRAUM}")
    k = historie(tickers)
    if k.empty:
        sys.exit("Keine Daten geladen - Abbruch.")

    os.makedirs(DOCS, exist_ok=True)
    with gzip.open(CSV_AUS, "wt", encoding="utf-8", newline="") as f:
        k.to_csv(f, index_label="ticker")
    groesse = os.path.getsize(CSV_AUS) / 1024 / 1024
    print(f"Geschrieben: {CSV_AUS} ({groesse:.1f} MB)")

    bericht = breite_auswertung(k)
    with open(MD_AUS, "w", encoding="utf-8") as f:
        f.write(bericht)
    print(f"Geschrieben: {MD_AUS}")


if __name__ == "__main__":
    main()
