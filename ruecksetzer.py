"""
ruecksetzer.py - Tagesverlauf INNERHALB jedes Ruecksetzers nach einem
bestaetigten Hoch. Ergaenzt hochs.py, das nur den Zustand AM Hoch kennt.

Laeuft auf Knopfdruck, nicht automatisch - siehe Begruendung unten.
Schreibt:
  docs/ruecksetzer_tage.csv.gz   eine Zeile JE TAG innerhalb eines
                                  laufenden Ruecksetzers

Entstanden aus der Frage vom 30.08.2026: "Steckt ein Wert gerade fest und
steht kurz vor einer groesseren Korrektur, oder pendelt er nur oben aus und
laeuft dann weiter?" hochs.py und puffer_je_hoch.csv kennen nur EINEN
Zustand je Hoch - RSI, EMA-Abstand, Volumen genau am Bestaetigungstag. Sie
sehen nicht, wie sich diese Werte waehrend des Ruecksetzers selbst
entwickeln. Genau das braucht ein Tages-Check wie "rote Kerze plus erhoehtes
Volumen an Tag 4 - was folgte historisch daraus".

WICHTIG: Volumen ist keine neue Datenquelle. kurse.py liefert es mit jedem
Kursabruf, marktdaten.py nutzt es laengst (vol_druck5, tiefX_volrel). Nur
hochs.py/historie.py schreiben pro Wendepunkt eine einzelne Zeile und lassen
den Verlauf dazwischen weg - dieses Skript ist der fehlende Tagesblick.

DEFINITION EINES TAGES

Ein Ruecksetzer beginnt am Bestaetigungstag eines Hochs (siehe
bestaetigungstag_hoch() in hochs.py - erster Tag, dessen Tief unter dem der
Hochkerze liegt) und laeuft, solange der Kurs nicht wieder nahe an das alte
Hoch herankommt. Fuer jeden Tag darin, bis zur Erholung oder bis zu
GRENZE_TAGE Handelstagen (63, wie QUARTAL in hochs.py):

  tag                Tage seit Bestaetigung (0 = Bestaetigungstag selbst)
  rueckstand_atr      staerkster bisher erreichter Ruecksetzer, kumuliert
                      bis EINSCHLIESSLICH diesem Tag, in ATR
  rsi                 RSI an diesem Tag
  vol_rel             Volumen dieses Tages / Mittel der vorangegangenen
                      20 Handelstage (dieselbe Definition wie
                      marktdaten.vol_rel)
  kerze               "rot" oder "gruen" (Schluss gegen Eroeffnung)
  ema200_atr           Abstand zur EMA(200) an diesem Tag, in ATR
  serie_laenge         Position des Hochs in seiner Serie (das bisher mit
                      Abstand staerkste Merkmal, siehe Notizen 30.08.2026 -
                      muss mitgefuehrt werden, sonst fehlt der wichtigste
                      Vergleichspunkt)

Sobald der Kurs an einem Tag wieder bis auf 0,25 ATR an das alte Hoch
herankommt, ist der Ruecksetzer beendet - dieser Tag wird noch mitgezaehlt
(er zeigt ja das Ende), danach folgen fuer diese Episode keine weiteren
Zeilen mehr.

ZIELGROESSE JE EPISODE, nicht je Tag

  zurueckfall_ganz_atr   wie tief der Ruecksetzer INSGESAMT ging, ueber die
                         volle Resthistorie (identische Definition wie in
                         hochs.py/puffer_je_hoch.csv). Das ist die
                         Zielgroesse: fuer jeden Tag innerhalb der Episode
                         gleich, weil es der Zustand am ENDE ist, den ein
                         Tages-Check vorhersagen soll. Rohdaten bleiben
                         fensterlos - ob ein Ruecksetzer als "gross" gilt,
                         entscheidet die Auswertung anhand einer
                         wertspezifischen Schwelle (etwa p75 wie in Notiz
                         zur Ausstiegs-Idee vom 30.08.2026), nicht dieses
                         Skript.
  erholt_tag             an welchem Tag die Erholung eintrat, falls
                         innerhalb GRENZE_TAGE - sonst leer. Leer heisst
                         nicht "nie", nur "nicht innerhalb dieses Fensters".

WARUM AUF KNOPFDRUCK, NICHT AUTOMATISCH

Anders als hochs.py und historie.py ist das hier eine EXPLORATIVE
Auswertung fuer eine offene Frage, kein etablierter Kennzahlen-Lieferant
fuer die Excel. Bis sich zeigt, ob ein Tages-Check ueberhaupt traegt, soll
das nicht jede Woche automatisch neu durchs ganze Universum laufen und
Rechenzeit binden. Zeigt sich ein brauchbares Muster, kann das nachtraeglich
in den woechentlichen Rhythmus wie hochs.py aufgenommen werden.

Das Repository ist oeffentlich. Dieses Skript rechnet ausschliesslich mit
oeffentlichen Kursdaten und kennt weder Positionen noch Trades noch den
Depotstand.

Aufruf:  python3 ruecksetzer.py
         python3 ruecksetzer.py --jahre 5
         python3 ruecksetzer.py --wert CDNS

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
import hochs
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
CSV_AUS = DOCS / "ruecksetzer_tage.csv.gz"
CSV_SCHWELLEN = DOCS / "ruecksetzer_schwellen.csv"

GRENZE_TAGE = 63        # wie QUARTAL in hochs.py
ERHOLT_SCHWELLE = 0.25  # ATR - ab hier gilt der Ruecksetzer als beendet
MINDESTLAUF = 21        # Hochs ohne so viel Resthistorie zaehlen nicht mit

# Fenster, in dem sich "rote Kerze + hohes Volumen" am 30.08.2026 als
# tragfaehig erwies (siehe Orderbuch, Blatt Notizen, Eintrag 6): Tag 0-3,
# oberstes Drittel der wertspezifischen Volumen-Verteilung an diesen
# fruehen Tagen. FRUEHFENSTER_TAGE und VOL_PERZENTIL duplizieren diesen
# Befund bewusst als Konstante hier, damit marktdaten.py nicht raten muss,
# was "hohes Volumen" heisst, sondern denselben Massstab wie die Auswertung
# selbst benutzt.
FRUEHFENSTER_TAGE = 3
VOL_PERZENTIL = 2 / 3
MINDESTFAELLE_SCHWELLE = 15  # darunter ist eine Schwelle nicht belastbar


def vol_rel(volumen: np.ndarray, bis: int, tage: int = 20) -> float | None:
    """Identische Definition wie marktdaten.vol_rel: Volumen dieses Tages
    geteilt durch das Mittel der VORANGEGANGENEN 20 Handelstage."""
    teil = volumen[max(0, bis - tage):bis]
    teil = teil[~np.isnan(teil)] if len(teil) else teil
    if len(teil) == 0 or np.mean(teil) == 0:
        return None
    v = volumen[bis]
    return None if np.isnan(v) else float(v) / float(np.mean(teil))


def ruecksetzer_tage_je_wert(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Eine Zeile je Tag innerhalb jedes laufenden Ruecksetzers."""
    seqs = regel.aufwaertssequenzen(df)
    if not seqs:
        return []

    a, r = hist.atr(df), hist.rsi(df)
    hoch_w, tief_w = df["High"].values, df["Low"].values
    open_w, close_w = df["Open"].values, df["Close"].values
    vol_w = (df["Volume"].values.astype(float) if "Volume" in df.columns
             else np.full(len(df), np.nan))
    ema_lang = (df["Close"].ewm(span=hist.EMA_LANG, adjust=False,
                                min_periods=hist.EMA_LANG).mean().values)
    daten = df.index

    ergebnis: list[dict] = []
    for s in seqs:
        for pos, i in enumerate(s["hochs"], start=1):
            atr_i = a[i]
            if not np.isfinite(atr_i) or atr_i <= 0:
                continue
            b = hochs.bestaetigungstag_hoch(df, i)
            if b is None or len(df) - b < MINDESTLAUF:
                continue

            hoch_preis = float(hoch_w[i])
            grenze = min(b + GRENZE_TAGE, len(df) - 1)
            zurueckfall_ganz = max(0.0, (hoch_preis - float(tief_w[b:].min())) / atr_i)

            schlimmster_bisher = 0.0
            for t in range(b, grenze + 1):
                schlimmster_bisher = max(schlimmster_bisher,
                                          (hoch_preis - float(tief_w[t])) / atr_i)
                e = ema_lang[t]
                ergebnis.append({
                    "ticker": ticker,
                    "hoch_datum": f"{daten[i]:%Y-%m-%d}",
                    "position": pos,
                    "serie_laenge": s["anzahl"],
                    "tag": t - b,
                    "rueckstand_atr": round(schlimmster_bisher, 3),
                    "rsi": round(float(r[t]), 2) if np.isfinite(r[t]) else None,
                    "vol_rel": (round(vr, 3) if (vr := vol_rel(vol_w, t)) is not None
                                else None),
                    "kerze": "rot" if close_w[t] < open_w[t] else "gruen",
                    "ema200_atr": (round((float(close_w[t]) - float(e)) / atr_i, 3)
                                   if np.isfinite(e) else None),
                    "zurueckfall_ganz_atr": round(zurueckfall_ganz, 3),
                })
                if float(hoch_w[t]) >= hoch_preis - ERHOLT_SCHWELLE * atr_i:
                    break  # erholt - dieser Tag zaehlt noch mit, dann Schluss
    return ergebnis


def csv_schreiben(alle: list[dict]) -> None:
    if not alle:
        return
    felder = ["ticker", "hoch_datum", "position", "serie_laenge", "tag",
              "rueckstand_atr", "rsi", "vol_rel", "kerze", "ema200_atr",
              "zurueckfall_ganz_atr"]
    DOCS.mkdir(exist_ok=True)
    with gzip.open(CSV_AUS, "wt", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder, restval="")
        w.writeheader()
        w.writerows(sorted(alle, key=lambda x: (x["ticker"], x["hoch_datum"], x["tag"])))
    print(f"Geschrieben: {CSV_AUS} ({len(alle)} Zeilen)")


def schwellen_schreiben(alle: list[dict]) -> None:
    """Je Wert: die Volumen-Schwelle (oberes Drittel), gemessen an den
    fruehen Tagen (0-3) aller Ruecksetzer dieses Werts. marktdaten.py
    liest diese Datei taeglich, um "hohes Volumen" nicht raten zu muessen,
    sondern am selben Massstab zu pruefen, der sich als tragfaehig
    erwiesen hat (Notiz 6, 30.08.2026)."""
    nach_wert: dict[str, list[float]] = {}
    for z in alle:
        if z["tag"] <= FRUEHFENSTER_TAGE and z["vol_rel"] is not None:
            nach_wert.setdefault(z["ticker"], []).append(z["vol_rel"])

    zeilen = []
    for ticker, werte in sorted(nach_wert.items()):
        if len(werte) < MINDESTFAELLE_SCHWELLE:
            continue
        arr = np.array(werte)
        zeilen.append({
            "ticker": ticker,
            "n": len(arr),
            "vol_rel_schwelle": round(float(np.quantile(arr, VOL_PERZENTIL)), 3),
        })
    if not zeilen:
        return
    DOCS.mkdir(exist_ok=True)
    with open(CSV_SCHWELLEN, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "n", "vol_rel_schwelle"])
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_SCHWELLEN} ({len(zeilen)} Werte)")


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
        zeilen = ruecksetzer_tage_je_wert(t, d[t])
        episoden = {(z["hoch_datum"]) for z in zeilen}
        print(f"{t}: {len(zeilen)} Tageszeilen ueber {len(episoden)} Ruecksetzer-Episoden.")
        for z in zeilen[-15:]:
            print(f"  {z['hoch_datum']} Tag {z['tag']:2d}  Rueckstand {z['rueckstand_atr']:5.2f} ATR  "
                  f"RSI {z['rsi']}  Vol {z['vol_rel']}  {z['kerze']}  Ziel {z['zurueckfall_ganz_atr']}")
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
            alle += ruecksetzer_tage_je_wert(t, df)
        except Exception as exc:  # noqa: BLE001
            fehler.append((t, str(exc)))
    if fehler:
        print(f"  {len(fehler)} Werte mit Fehler uebersprungen: "
              f"{', '.join(t for t, _ in fehler[:10])}"
              f"{' ...' if len(fehler) > 10 else ''}")

    print(f"{len(alle)} Tageszeilen ueber {len(daten)} Werte.")
    csv_schreiben(alle)
    schwellen_schreiben(alle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
