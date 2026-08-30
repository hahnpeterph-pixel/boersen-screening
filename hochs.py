"""
hochs.py - Auswertungen ueber die AUSSTIEGSSEITE. Spiegel von historie.py.

Laeuft auf Knopfdruck, nicht nachts. Schreibt:
  docs/puffer_je_hoch.csv.gz   eine Zeile JE HOCH - die Rohdaten (gepackt)
  docs/halteraten_hoch_werte.csv  je Wert und Hochposition, geht in die Excel

Entstanden aus der Frage vom 29.08.2026: "Wenn ein Anstieg eine bestimmte
Strecke gelaufen ist, sollte man dann verkaufen und spaeter tiefer wieder
einsteigen?" Die einfache Lesart (Ausstieg nach X ATR, Wiedereinstieg unter
dem alten Tief) wurde bereits an diesem Tag lokal aus puffer_je_tief.csv
rekonstruiert und verworfen: in 64 bis 84 Prozent der Faelle kam der Kurs nie
wieder unter das alte Tief, und genau diese Faelle liefen im Median 6 bis 22
ATR weiter (siehe Orderbuch, Blatt Notizen, Eintrag 2).

Was diese Datei zusaetzlich liefert und aus puffer_je_tief.csv NICHT
rekonstruierbar war: Ruecksetzer INNERHALB eines laufenden Anstiegs, die
nicht bis unter den alten Tiefpunkt reichen. tage_ko_X in puffer_je_tief.csv
misst nur Staende unterhalb des EINSTIEGSTIEFS - ein Ruecksetzer von +5 ATR
auf +2 ATR taucht dort nirgends auf, weil er den Ausgangspunkt nicht
unterschreitet. Hier wird stattdessen JE HOCH gemessen, nicht je Tief.

DEFINITION "HOCH" UND "SERIE"

Strenge Spiegelung der Tiefsregel aus tiefs_regel.py, siehe dort
aufwaertssequenzen(): eine Serie zaehlender NEUER Hoechststaende innerhalb
einer Aufwaertsstrecke, beendet durch ein Tief unter der wandernden
Referenz. Bestaetigt ist ein Hoch, sobald eine spaetere Kerze das TIEF der
Hochkerze unterschreitet - das Spiegelbild von bestaetigungstag() in
historie.py, dort ueberschreitet eine spaetere Kerze das HOCH der Tiefkerze.

GEMESSEN WIRD, JE HOCH:

  tage_rueck_X   nach wie vielen Handelstagen (ab Bestaetigung) fiel der
                 Kurs erstmals X ATR UNTER dieses Hoch. Das Gegenstueck zu
                 tage_ko_X: dort "wie tief faellt er, bevor der KO reisst",
                 hier "wie tief faellt er, bevor die Position im Verlust
                 waere, haette man am Hoch verkauft und wollte guenstiger
                 zurueck". Leer heisst: in der beobachteten Zeit nie.

  tage_weiter_X  nach wie vielen Handelstagen stieg der Kurs erstmals X ATR
                 UEBER dieses Hoch - die Fortsetzung nach oben, gemessen ab
                 dem Hoch selbst statt ab einem Einstiegstief. Das
                 Gegenstueck zu tage_ziel_X in puffer_je_tief.csv, nur mit
                 anderem Nullpunkt.

  zurueckfall_atr   wie tief der Kurs INNERHALB von QUARTAL Handelstagen ab
                    der Bestaetigung mindestens fiel, in ATR. Das
                    Gegenstueck zu benoetigt_atr auf der Tiefsseite: dort
                    "wie viel Puffer haette das Tief gebraucht, um nicht zu
                    reissen", hier "wie tief fiel der Rueckschlag nach
                    diesem Hoch tatsaechlich".
  zurueckfall_ganz_atr  dieselbe Groesse ohne Fenster, ueber die volle
                        Resthistorie.

Genau wie in historie.py: kein Fenster in den Rohdaten. Ein Ruecksetzer kann
kommen, solange die Position offen ist, das Fenster gehoert in die
Auswertung, nicht in die Messung.

FENSTER DER AUSWERTUNG

Festgelegt am 29.08.2026, gilt fuer Tiefs- UND Hochauswertung gleichermassen:
21 / 42 / 63 / 84 / 126 / 189 / 252 Handelstage. Begruendung: ein
gleichmaessiges statt eines groben Rasters, siehe Orderbuch Blatt Notizen,
Eintrag 3. Die Aufteilung 63/252 (alt: "3M"/"12M") ist damit ueberholt.

Das Repository ist oeffentlich. Dieses Skript rechnet ausschliesslich mit
oeffentlichen Kursdaten und kennt weder Positionen noch Trades noch den
Depotstand.

Aufruf:  python3 hochs.py
         python3 hochs.py --jahre 5
         python3 hochs.py --wert CDNS

KEINE Anlageberatung. Das Skript misst historische Kursverlaeufe.
"""

from __future__ import annotations

import csv
import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import historie as hist
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
CSV_ROH = DOCS / "puffer_je_hoch.csv.gz"
CSV_WERT = DOCS / "halteraten_hoch_werte.csv"

# Dieselben Konstanten wie historie.py, von dort importiert statt
# dupliziert: ATR_TAGE, RSI_TAGE, EMA_LANG, EMA_KURZ, NEIGUNG_TAGE,
# NEIGUNG_TAGE_KURZ, JAHRE. Eine zweite Kopie widerspraeche genau dem
# Grund, aus dem tiefs_regel.py entstanden ist - drei Staende, die
# irgendwann auseinanderlaufen.

# Ruecksetzer- und Fortsetzungsstufen in Viertelschritten, wie PUFFER und
# ZIELE in historie.py. Ruecksetzer nur bis 16 ATR (wie PUFFER dort) - ein
# Ruecksetzer, der tiefer geht als das ganze bisherige Muster ueblich ist,
# ist ohnehin kein Ruecksetzer mehr, sondern ein neuer Abwaertstrend, den
# tiefs_regel.py als eigene Tiefsserie erfasst.
RUECK = tuple(round(0.25 * k, 2) for k in range(1, 65))
WEITER = tuple(round(0.25 * k, 2) for k in range(1, 121))

QUARTAL = 63          # Fenster fuer zurueckfall_atr, wie in historie.py
MINDESTLAUF = 63      # Hochs ohne so viel Resthistorie zaehlen nicht mit

# Fenster der Auswertung, Entscheidung vom 29.08.2026.
FENSTER = (21, 42, 63, 84, 126, 189, 252)


def bestaetigungstag_hoch(df: pd.DataFrame, i: int) -> int | None:
    """Erster Tag nach dem Hoch, dessen Tief UNTER dem Tief der Hochkerze
    liegt. Spiegel von bestaetigungstag() in historie.py. Vorher ist nicht
    entscheidbar, dass dies wirklich ein Wendepunkt nach unten war."""
    tief = df["Low"].values
    for j in range(i + 1, len(df)):
        if tief[j] < tief[i]:
            return j
    return None


def hoch_faelle_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Ein Eintrag je zaehlendem Hoch einer abgeschlossenen Aufwaertsserie."""
    seqs = regel.aufwaertssequenzen(df)
    if not seqs:
        return []
    tiefs = regel.swing_tiefs(df, unbestaetigt=False)
    tiefs_chrono = sorted(tiefs, key=lambda t: t["i"])
    a, r = hist.atr(df), hist.rsi(df)
    tief_w, hoch_w = df["Low"].values, df["High"].values
    daten = df.index

    ema_lang = (df["Close"].ewm(span=hist.EMA_LANG, adjust=False,
                                min_periods=hist.EMA_LANG).mean().values)
    ema_kurz = (df["Close"].ewm(span=hist.EMA_KURZ, adjust=False,
                                min_periods=hist.EMA_KURZ).mean().values)

    abgeschlossen = [s for s in seqs if not s["laufend"]]
    typisch = (float(np.median([s["anzahl"] for s in abgeschlossen]))
               if abgeschlossen else None)
    rsi_an_hochs = [r[i] for s in seqs for i in s["hochs"] if np.isfinite(r[i])]
    rsi_median = float(np.median(rsi_an_hochs)) if rsi_an_hochs else None

    ergebnis = []
    for s in seqs:
        for pos, i in enumerate(s["hochs"], start=1):
            atr_i = a[i]
            if not np.isfinite(atr_i) or atr_i <= 0:
                continue
            b = bestaetigungstag_hoch(df, i)
            if b is None:
                continue
            # Ende der Abwaertsstrecke, die diesem Hoch folgt: das naechste
            # bestaetigte Swing-Tief nach b. Spiegel von "ende" in
            # faelle_je_wert() (dort: naechstes Hoch nach dem Tief).
            ende = next((t["i"] for t in tiefs_chrono if t["i"] > b), None)
            if ende is None:
                continue  # Abwaertsstrecke laeuft noch, kein Urteil

            if len(df) - b < MINDESTLAUF:
                continue

            nach_tief = tief_w[b:]
            nach_hoch = hoch_w[b:]
            fenster_t = nach_tief[:QUARTAL + 1]
            zurueckfall = max(0.0, (float(hoch_w[i]) - float(fenster_t.min())) / atr_i)
            zurueckfall_ganz = max(0.0, (float(hoch_w[i]) - float(nach_tief.min())) / atr_i)

            tage_rueck = {}
            for pp in RUECK:
                schwelle = float(hoch_w[i]) - pp * atr_i
                treffer = np.flatnonzero(nach_tief < schwelle)
                tage_rueck[pp] = int(treffer[0]) if len(treffer) else None

            ausgang = float(df["Close"].values[b])
            tage_weiter = {}
            for zz in WEITER:
                marke = float(hoch_w[i]) + zz * atr_i
                treffer = np.flatnonzero(nach_hoch >= marke)
                tage_weiter[zz] = int(treffer[0]) if len(treffer) else None

            tal = float(tief_w[b:].min())
            rueckschlag_pivot = (float(hoch_w[i]) - float(tief_w[ende])) / atr_i

            e_b = ema_lang[b]
            ema200_atr = (None if not np.isfinite(e_b)
                          else (ausgang - float(e_b)) / atr_i)
            j = b - hist.NEIGUNG_TAGE
            e_j = ema_lang[j] if j >= 0 else np.nan
            ema200_neigung_atr = (
                None if not (np.isfinite(e_b) and np.isfinite(e_j))
                else (float(e_b) - float(e_j)) / atr_i)

            ek_b = ema_kurz[b]
            ema50_atr = (None if not np.isfinite(ek_b)
                         else (ausgang - float(ek_b)) / atr_i)
            jk = b - hist.NEIGUNG_TAGE_KURZ
            ek_j = ema_kurz[jk] if jk >= 0 else np.nan
            ema50_neigung_atr = (
                None if not (np.isfinite(ek_b) and np.isfinite(ek_j))
                else (float(ek_b) - float(ek_j)) / atr_i)

            ergebnis.append({
                "ticker": ticker,
                "datum": f"{daten[i]:%Y-%m-%d}",
                "position": pos,
                "serie_laenge": s["anzahl"],
                "typisch": typisch,
                "laufend": s["laufend"],
                "hoch": float(hoch_w[i]),
                "ausgang": ausgang,
                "atr": atr_i,
                "rsi": float(r[i]) if np.isfinite(r[i]) else None,
                "rsi_rel": (float(r[i]) - rsi_median
                            if (rsi_median is not None and np.isfinite(r[i]))
                            else None),
                "ema200_atr": ema200_atr,
                "ema200_neigung_atr": ema200_neigung_atr,
                "ema50_atr": ema50_atr,
                "ema50_neigung_atr": ema50_neigung_atr,
                "zurueckfall_atr": zurueckfall,
                "zurueckfall_ganz_atr": zurueckfall_ganz,
                "rueckschlag_pivot_atr": rueckschlag_pivot,
                "resthistorie": len(df) - b,
                "beobachtet": len(nach_tief) - 1,
                "tage_rueck": tage_rueck,
                "tage_weiter": tage_weiter,
                "i": i, "b": b, "ende": ende,
            })
    return ergebnis


def csv_roh(fest: list[dict]) -> None:
    """Eine Zeile JE HOCH, ohne Fenster. Spiegel von csv_roh() in
    historie.py."""
    if not fest:
        return
    felder = ["ticker", "datum", "position", "serie_laenge", "typisch",
              "hoch", "ausgang", "atr", "rsi", "rsi_rel",
              "ema200_atr", "ema200_neigung_atr", "ema50_atr",
              "ema50_neigung_atr", "zurueckfall_atr", "zurueckfall_ganz_atr",
              "rueckschlag_pivot_atr", "resthistorie", "beobachtet"]
    felder += [f"tage_rueck_{p:g}" for p in RUECK]
    felder += [f"tage_weiter_{z:g}" for z in WEITER]
    DOCS.mkdir(exist_ok=True)
    with gzip.open(CSV_ROH, "wt", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(felder)
        for x in sorted(fest, key=lambda y: (y["ticker"], y["datum"])):
            w.writerow([
                x["ticker"], x["datum"], x["position"], x["serie_laenge"],
                x["typisch"],
                round(x["hoch"], 4), round(x["ausgang"], 4),
                round(x["atr"], 4),
                round(x["rsi"], 2) if x["rsi"] is not None else "",
                round(x["rsi_rel"], 2) if x["rsi_rel"] is not None else "",
                (round(x["ema200_atr"], 3)
                 if x.get("ema200_atr") is not None else ""),
                (round(x["ema200_neigung_atr"], 3)
                 if x.get("ema200_neigung_atr") is not None else ""),
                (round(x["ema50_atr"], 3)
                 if x.get("ema50_atr") is not None else ""),
                (round(x["ema50_neigung_atr"], 3)
                 if x.get("ema50_neigung_atr") is not None else ""),
                round(x["zurueckfall_atr"], 3),
                round(x["zurueckfall_ganz_atr"], 3),
                round(x["rueckschlag_pivot_atr"], 3),
                x["resthistorie"], x.get("beobachtet", ""),
            ] + [
                ("" if x["tage_rueck"].get(p) is None else x["tage_rueck"][p])
                for p in RUECK
            ] + [
                ("" if x["tage_weiter"].get(z) is None else x["tage_weiter"][z])
                for z in WEITER
            ])
    print(f"Geschrieben: {CSV_ROH} ({len(fest)} Zeilen)")


def _perzentile(werte: list[float]) -> dict:
    if not werte:
        return {}
    a = np.array(werte)
    return {"min": float(a.min()), "p25": float(np.percentile(a, 25)),
            "median": float(np.median(a)), "p75": float(np.percentile(a, 75)),
            "p90": float(np.percentile(a, 90)), "p95": float(np.percentile(a, 95)),
            "max": float(a.max())}


def zeile_je_gruppe(ticker: str, position, g: list[dict]) -> dict:
    """Je Wert und Hochposition (oder 'alle'): Ruecksetzertiefe und
    Ueberschreitungsquote ueber die sieben Fenster. Spiegel der
    entsprechenden Stelle in historie.py, aber mit dem am 29.08.2026
    festgelegten Fensterraster statt der alten 63/252-Aufteilung."""
    z: dict = {"ticker": ticker, "position": position, "faelle": len(g)}
    z.update({f"zurueckfall_atr_{k}": v for k, v in
              _perzentile([f["zurueckfall_atr"] for f in g]).items()})

    for fen in FENSTER:
        gg = [f for f in g if f["beobachtet"] >= fen]
        z[f"n_{fen}t"] = len(gg)
        if not gg:
            continue
        # haelt = das Hoch wurde INNERHALB des Fensters nicht mehr um mehr
        # als eine Bagatellstufe (0.25 ATR) ueberschritten.
        haelt = [1 for f in gg if f["tage_weiter"].get(0.25) is None
                 or f["tage_weiter"][0.25] > fen]
        z[f"haelt_{fen}t_pct"] = round(100 * len(haelt) / len(gg), 1)
        rueck_min = []
        for f in gg:
            arr = [pp for pp in RUECK if (f["tage_rueck"].get(pp) is not None
                                           and f["tage_rueck"][pp] <= fen)]
            rueck_min.append(max(arr) if arr else 0.0)
        p = _perzentile(rueck_min)
        z[f"ruecksetzer_{fen}t_median"] = round(p.get("median", 0.0), 2)
        z[f"ruecksetzer_{fen}t_p75"] = round(p.get("p75", 0.0), 2)
        z[f"ruecksetzer_{fen}t_p90"] = round(p.get("p90", 0.0), 2)
    return z


def csv_je_wert(fest: list[dict]) -> None:
    nach_wert: dict = {}
    for f in fest:
        nach_wert.setdefault(f["ticker"], []).append(f)

    zeilen = []
    for ticker in sorted(nach_wert):
        g_alle = nach_wert[ticker]
        zeilen.append(zeile_je_gruppe(ticker, "alle", g_alle))
        gruppen: dict = {}
        for f in g_alle:
            gruppen.setdefault(f["position"], []).append(f)
        for k in sorted(gruppen):
            zeilen.append(zeile_je_gruppe(ticker, f"Hoch {k}", gruppen[k]))

    if not zeilen:
        return
    DOCS.mkdir(exist_ok=True)
    felder: list[str] = []
    for z0 in zeilen:
        for k in z0:
            if k not in felder:
                felder.append(k)
    with open(CSV_WERT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder, restval="")
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_WERT} ({len(zeilen)} Zeilen)")


def main() -> int:
    jahre = hist.JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])

    if "--wert" in sys.argv:
        t = sys.argv[sys.argv.index("--wert") + 1]
        d = hist.lade(sorted(set(hist.universum() + [t])), jahre)
        if t not in d:
            print(f"{t}: keine Kursdaten.")
            return 1
        fest = hoch_faelle_je_wert(t, d[t])
        print(f"{t}: {len(fest)} zaehlende Hochs.")
        for f in fest[-10:]:
            print(f"  Pos {f['position']:2d} {f['datum']} Hoch {f['hoch']:.2f} "
                  f"Ruecksetzer(63T) {f['zurueckfall_atr']:.2f} ATR "
                  f"RSI {f['rsi']}")
        return 0

    tickers = hist.universum()
    if not tickers:
        print("universe.json nicht gefunden oder leer.")
        return 1
    daten = hist.lade(tickers, jahre)

    alle: list[dict] = []
    fehler = []
    for t, df in daten.items():
        try:
            alle += hoch_faelle_je_wert(t, df)
        except Exception as exc:  # noqa: BLE001
            fehler.append((t, str(exc)))
    if fehler:
        print(f"  {len(fehler)} Werte mit Fehler uebersprungen: "
              f"{', '.join(t for t, _ in fehler[:10])}"
              f"{' ...' if len(fehler) > 10 else ''}")

    print(f"{len(alle)} zaehlende Hochs ueber {len(daten)} Werte.")
    csv_roh(alle)
    csv_je_wert(alle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
