#!/usr/bin/env python3
"""
Quellencheck - einmaliges Diagnoseskript, KEIN Teil des taeglichen Laufs.

Beantwortet zwei Fragen, die der Screener heute offen laesst:

TEST A - Lassen sich die Aggregat-Werte durch benannte Einzelratings
ersetzen? Yahoo fuehrt die namentliche Ratingtabelle (upgrades_downgrades)
offenbar nur fuer US-gehandelte Papiere. Fast jeder DAX-Wert hat aber eine
US-Notierung: Deutsche Bank und SAP direkt an der NYSE, der Rest als ADR.
Das Skript holt die Ratingtabelle fuer die US-Notierung und zaehlt, wie
viele Banken mit einer Einstufung juenger als CONSENSUS_MAX_AGE_DAYS
uebrigbleiben. Ergibt das genug, koennen diese Werte kuenftig ueber die
US-Notierung mit benannten, datierten Ratings versorgt werden - aus
derselben Quelle wie bisher, ohne neuen Anbieter.

TEST B - Bewegt sich Yahoos Aggregat ueberhaupt? Die Zaehlung kommt ohne
Datum und ohne Banknamen, ihr Alter ist aus den Daten nicht ablesbar.
Yahoo liefert sie aber je Monatsfenster (0m = laufender Monat, -1m, -2m,
-3m). Sind alle vier Fenster identisch, ist die Zahl eingefroren und als
Kaufkriterium unbrauchbar. Unterscheiden sie sich, aktualisiert Yahoo
wenigstens monatlich.

Ausgabe: docs/quellencheck.md

Aufruf:  python3 quellencheck.py
         python3 quellencheck.py --nur ADS.DE,SIE.DE     (Teilmenge testen)

KEINE Anlageberatung. Das Skript prueft Datenqualitaet, mehr nicht.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
DOCS_DIR = BASE / "docs"
ANALYSTEN_CSV = DOCS_DIR / "analysten.csv"
AUSGABE = DOCS_DIR / "quellencheck.md"

CONSENSUS_MAX_AGE_DAYS = 120   # gleiche Schwelle wie im Screener
PAUSE = 0.4                    # Sekunden zwischen Abrufen

# ---------------------------------------------------------------------------
# US-Notierung je deutschem Ticker.
#
# WICHTIG: Diese Zuordnung ist von Hand zusammengestellt und NICHT geprueft.
# Ein ADR-Kuerzel kann falsch, veraltet oder ein unsponsored Papier ohne
# Analystenabdeckung sein. Deshalb gibt das Skript zu jedem Kandidaten den
# Firmennamen aus, den Yahoo dazu liefert - Namen gegenpruefen, bevor
# irgendetwas davon in den Screener wandert.
#
# Mehrere Kandidaten je Wert sind erlaubt: das Skript nimmt den ersten, der
# eine gefuellte Ratingtabelle liefert.
# ---------------------------------------------------------------------------
ALT_NOTIERUNG: dict[str, list[str]] = {
    "ADS.DE":  ["ADDYY"],            # Adidas
    "AIR.DE":  ["EADSY", "EADSF"],   # Airbus
    "ALV.DE":  ["ALIZY"],            # Allianz
    "BAS.DE":  ["BASFY"],            # BASF
    "BAYN.DE": ["BAYRY"],            # Bayer
    "BEI.DE":  ["BDRFY"],            # Beiersdorf
    "BMW.DE":  ["BMWYY"],            # BMW
    "BNR.DE":  ["BNTGY"],            # Brenntag
    "CBK.DE":  ["CRZBY"],            # Commerzbank
    "CON.DE":  ["CTTAY"],            # Continental
    "DB1.DE":  ["DBOEY"],            # Deutsche Boerse
    "DBK.DE":  ["DB"],               # Deutsche Bank, echte NYSE-Notierung
    "DHL.DE":  ["DHLGY"],            # DHL Group
    "DTE.DE":  ["DTEGY"],            # Deutsche Telekom
    "DTG.DE":  ["DTRUY"],            # Daimler Truck
    "ENR.DE":  ["SMNEY"],            # Siemens Energy
    "EOAN.DE": ["EONGY"],            # E.ON
    "FRE.DE":  ["FSNUY"],            # Fresenius
    "HEI.DE":  ["HDELY"],            # Heidelberg Materials
    "HEN3.DE": ["HENKY"],            # Henkel Vorzug
    "HNR1.DE": ["HVRRY"],            # Hannover Rueck
    "IFX.DE":  ["IFNNY"],            # Infineon
    "MBG.DE":  ["MBGYY"],            # Mercedes-Benz
    "MRK.DE":  ["MKKGY"],            # Merck KGaA
    "MTX.DE":  ["MTUAY"],            # MTU Aero Engines
    "MUV2.DE": ["MURGY"],            # Muenchener Rueck
    "P911.DE": ["DRPRY"],            # Porsche AG
    "PAH3.DE": ["POAHY"],            # Porsche SE
    "RHM.DE":  ["RNMBY"],            # Rheinmetall
    "RWE.DE":  ["RWEOY"],            # RWE
    "SAP.DE":  ["SAP"],              # SAP, echte NYSE-Notierung
    "SHL.DE":  ["SMMNY"],            # Siemens Healthineers
    "SIE.DE":  ["SIEGY"],            # Siemens
    "SRT3.DE": ["SUVPF", "SARTF"],   # Sartorius Vorzug
    "SY1.DE":  ["SYIEY"],            # Symrise
    "VNA.DE":  ["VONOY", "VNNVF"],   # Vonovia
    "VOW3.DE": ["VWAGY"],            # Volkswagen Vorzug
    "ZAL.DE":  ["ZLNDY"],            # Zalando

    # ── Andere Richtung: US-Notierung -> Heimatnotierung ───────────────
    # Am 24.08.2026 ergaenzt fuer Frage 53. Der Report rechnet bei diesen
    # vier Werten auf der US-Notierung, die Knock-out-Scheine bei Trade
    # Republic beziehen sich aber auf die Heimatboerse in EUR bzw. GBP.
    # Solange beide auf verschiedenen Boersen rechnen, ist der ausgewiesene
    # Puffer falsch - bei ASML war er sechsmal zu gross.
    #
    # Vor der Umstellung muss feststehen, ob Yahoo fuer die Heimatnotierung
    # ueberhaupt Analystendaten liefert. Ohne Kursziel gibt es kein
    # Verkaufsziel, dann waere ein Fehler gegen den anderen getauscht.
    #
    # Kandidaten kamen aus der Regel: US-Boerse UND Domizil ungleich
    # United States. Die uebrigen sechs Treffer (ARM, PDD, MELI, LULU,
    # TEAM, dazu CCEP mit Einschraenkung) notieren nur in den USA - reine
    # Domizilfaelle ohne Zweitnotierung.
    "ASML": ["ASML.AS"],             # Amsterdam, EUR
    "NXPI": ["NXPI.AS"],             # Amsterdam, EUR
    "AZN":  ["AZN.L"],               # London, GBp - Achtung: Pence
    "CCEP": ["CCEP.AS"],             # Amsterdam, EUR
}


# ---------------------------------------------------------------------------
# Auswahl der zu pruefenden Werte
# ---------------------------------------------------------------------------

def zu_pruefende_ticker() -> list[tuple[str, str, str]]:
    """Alle Werte aus analysten.csv, deren Konsens NICHT aus benannten
    Einzelratings stammt. Gibt (ticker, name, quelle) zurueck."""
    if not ANALYSTEN_CSV.exists():
        print(f"! {ANALYSTEN_CSV} nicht gefunden - erst den Screener laufen lassen.")
        return []
    import csv
    treffer = []
    with ANALYSTEN_CSV.open(encoding="utf-8") as f:
        for z in csv.DictReader(f):
            if (z.get("quelle") or "").strip() in ("Aggregat", "keine", ""):
                treffer.append((z["ticker"], z.get("name", ""), z.get("quelle", "")))
    return sorted(treffer)


# ---------------------------------------------------------------------------
# TEST A: benannte Ratings ueber die US-Notierung
# ---------------------------------------------------------------------------

def ratings_der_us_notierung(kandidat: str, stichtag) -> dict:
    """Ratingtabelle eines US-Papiers auswerten: wie viele Banken haben eine
    Einstufung juenger als der Stichtag, und welche."""
    import yfinance as yf

    ergebnis = {
        "kandidat": kandidat, "name": None, "gefunden": False,
        "zeilen_gesamt": 0, "banken_frisch": 0, "juengstes": None,
        "beispiele": [], "fehler": None,
    }
    try:
        tk = yf.Ticker(kandidat)
        try:
            ergebnis["name"] = (tk.info or {}).get("shortName")
        except Exception:  # noqa: BLE001
            pass

        ud = tk.upgrades_downgrades
        if ud is None or ud.empty:
            return ergebnis

        ud = ud.reset_index()
        spalte = "GradeDate" if "GradeDate" in ud.columns else ud.columns[0]
        ud[spalte] = pd.to_datetime(ud[spalte], utc=True, errors="coerce")
        ud = ud.dropna(subset=[spalte])
        ergebnis["gefunden"] = True
        ergebnis["zeilen_gesamt"] = int(len(ud))
        if len(ud):
            ergebnis["juengstes"] = str(ud[spalte].max().date())

        frisch = ud[ud[spalte] >= stichtag]
        if frisch.empty or "Firm" not in frisch.columns:
            return ergebnis

        # Wie im Screener: pro Bank nur die juengste Einstufung
        je_bank = frisch.sort_values(spalte).groupby("Firm", as_index=False).last()
        ergebnis["banken_frisch"] = int(len(je_bank))
        for _, r in je_bank.sort_values(spalte, ascending=False).head(4).iterrows():
            ergebnis["beispiele"].append(
                f"{r[spalte].date()} {r.get('Firm')}: {r.get('ToGrade') or '-'}"
            )
    except Exception as exc:  # noqa: BLE001
        ergebnis["fehler"] = str(exc)[:120]
    return ergebnis


def test_a(werte: list) -> list[dict]:
    stichtag = datetime.now(timezone.utc) - pd.Timedelta(days=CONSENSUS_MAX_AGE_DAYS)
    zeilen = []
    print(f"\nTEST A - benannte Ratings ueber die US-Notierung "
          f"({len(werte)} Werte, Stichtag {stichtag.date()})")

    for n, (ticker, name, quelle) in enumerate(werte, 1):
        kandidaten = ALT_NOTIERUNG.get(ticker, [])
        zeile = {"ticker": ticker, "name": name, "quelle": quelle,
                 "kandidaten": kandidaten, "treffer": None, "versuche": []}

        if not kandidaten:
            # Kein ADR hinterlegt. Bei US-Werten (META, CAT, AZN, FANG) ist
            # das kein Fehler: die Aktie IST bereits US-notiert, es gibt
            # nichts zu ersetzen - dort fehlt die Ratingtabelle bei Yahoo
            # schlicht, das ist der eigentliche Befund.
            zeile["hinweis"] = ("bereits US-notiert" if "." not in ticker
                                else "keine US-Notierung hinterlegt")
            zeilen.append(zeile)
            print(f"  {n:>3}/{len(werte)} {ticker:<8} uebersprungen ({zeile['hinweis']})")
            continue

        for kandidat in kandidaten:
            res = ratings_der_us_notierung(kandidat, stichtag)
            zeile["versuche"].append(res)
            time.sleep(PAUSE)
            if res["banken_frisch"] > 0:
                zeile["treffer"] = res
                break
        best = zeile["treffer"] or (zeile["versuche"][0] if zeile["versuche"] else None)
        anz = best["banken_frisch"] if best else 0
        kand = best["kandidat"] if best else "-"
        print(f"  {n:>3}/{len(werte)} {ticker:<8} via {kand:<7} -> {anz} Banken frisch")
        zeilen.append(zeile)
    return zeilen


# ---------------------------------------------------------------------------
# TEST B: bewegt sich das Aggregat?
# ---------------------------------------------------------------------------

def test_b(werte: list) -> list[dict]:
    """Yahoos Empfehlungszaehlung je Monatsfenster abholen und vergleichen.
    Sind alle Fenster identisch, ist die Zahl eingefroren."""
    import yfinance as yf

    zeilen = []
    print(f"\nTEST B - bewegt sich das Aggregat? ({len(werte)} Werte)")
    for n, (ticker, name, quelle) in enumerate(werte, 1):
        zeile = {"ticker": ticker, "name": name, "fenster": {}, "urteil": "keine Daten"}
        try:
            rec = yf.Ticker(ticker).recommendations
            if rec is not None and not getattr(rec, "empty", True):
                rec = rec.reset_index()
                for _, r in rec.iterrows():
                    p = str(r.get("period", "")).strip()
                    if p not in ("0m", "-1m", "-2m", "-3m"):
                        continue

                    def z(spalte):
                        w = r.get(spalte)
                        try:
                            return int(w) if w is not None and not pd.isna(w) else 0
                        except Exception:  # noqa: BLE001
                            return 0

                    kaufen = z("strongBuy") + z("buy")
                    halten = z("hold")
                    verkaufen = z("sell") + z("strongSell")
                    zeile["fenster"][p] = (kaufen, halten, verkaufen)

                vorhandene = [zeile["fenster"][p] for p in ("0m", "-1m", "-2m", "-3m")
                              if p in zeile["fenster"]]
                if len(vorhandene) < 2:
                    zeile["urteil"] = "nur ein Fenster - nicht pruefbar"
                elif len(set(vorhandene)) == 1:
                    zeile["urteil"] = "EINGEFROREN (alle Fenster gleich)"
                else:
                    zeile["urteil"] = "bewegt sich"
        except Exception as exc:  # noqa: BLE001
            zeile["urteil"] = f"Fehler: {str(exc)[:60]}"
        print(f"  {n:>3}/{len(werte)} {ticker:<8} {zeile['urteil']}")
        zeilen.append(zeile)
        time.sleep(PAUSE)
    return zeilen


# ---------------------------------------------------------------------------
# Bericht
# ---------------------------------------------------------------------------

def baue_bericht(a_zeilen: list, b_zeilen: list) -> str:
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    L = ["# Quellencheck - Ersatz fuer die Aggregat-Werte", "",
         f"_Erstellt {jetzt} UTC. Einmalige Diagnose, kein Teil des taeglichen Laufs._", ""]

    # --- Zusammenfassung ---
    mit_treffer = [z for z in a_zeilen if z.get("treffer")]
    genug = [z for z in mit_treffer if z["treffer"]["banken_frisch"] >= 3]
    eingefroren = [z for z in b_zeilen if z["urteil"].startswith("EINGEFROREN")]
    bewegt = [z for z in b_zeilen if z["urteil"] == "bewegt sich"]

    L += ["## Kurzfassung", "",
          f"- **Test A:** {len(mit_treffer)} von {len(a_zeilen)} Werten liefern ueber die "
          f"US-Notierung ueberhaupt benannte Ratings juenger als {CONSENSUS_MAX_AGE_DAYS} Tage. "
          f"Davon **{len(genug)} mit mindestens 3 Banken** - nur die sind ein brauchbarer Ersatz.",
          f"- **Test B:** {len(eingefroren)} Werte haben ueber alle vier Monatsfenster "
          f"identische Zahlen (Aggregat eingefroren), {len(bewegt)} bewegen sich.", "",
          "Lesehilfe: Ein Wert taugt als Ersatz, wenn Test A genug Banken liefert UND der "
          "Firmenname der US-Notierung tatsaechlich zur deutschen Aktie passt. Der Name kommt "
          "ungeprueft von Yahoo - bitte durchsehen, bevor etwas davon in den Screener wandert.", ""]

    # --- Test A ---
    L += ["## Test A - benannte Ratings ueber die US-Notierung", "",
          "| Ticker | Name | bisher | US-Papier | Name laut Yahoo | Banken frisch | "
          "Zeilen gesamt | juengstes Rating | Beispiele |",
          "|---|---|---|---|---|---|---|---|---|"]
    for z in sorted(a_zeilen, key=lambda x: -(x["treffer"]["banken_frisch"] if x.get("treffer") else -1)):
        best = z.get("treffer") or (z["versuche"][0] if z.get("versuche") else None)
        if best is None:
            L.append(f"| {z['ticker']} | {z['name']} | {z['quelle']} | - | - | - | - | - | "
                     f"{z.get('hinweis', '-')} |")
            continue
        beisp = "<br>".join(best["beispiele"]) if best["beispiele"] else "-"
        L.append(f"| {z['ticker']} | {z['name']} | {z['quelle']} | {best['kandidat']} | "
                 f"{best['name'] or '?'} | **{best['banken_frisch']}** | "
                 f"{best['zeilen_gesamt']} | {best['juengstes'] or '-'} | {beisp} |")
    L.append("")

    # --- Test B ---
    L += ["## Test B - bewegt sich Yahoos Aggregat?", "",
          "_Kaufen/Halten/Verkaufen je Monatsfenster. `0m` ist der laufende Monat. "
          "Identische Zahlen ueber alle Fenster heissen: die Zaehlung wird nicht "
          "fortgeschrieben und ist als Kaufkriterium wertlos._", "",
          "| Ticker | Name | 0m | -1m | -2m | -3m | Urteil |",
          "|---|---|---|---|---|---|---|"]
    for z in b_zeilen:
        def f(p):
            w = z["fenster"].get(p)
            return f"{w[0]}/{w[1]}/{w[2]}" if w else "-"
        L.append(f"| {z['ticker']} | {z['name']} | {f('0m')} | {f('-1m')} | "
                 f"{f('-2m')} | {f('-3m')} | {z['urteil']} |")
    L.append("")

    # --- Vorschlag fuer analysten_extern.csv ---
    L += ["## Fertige Zeilen fuer analysten_extern.csv", "",
          "_Nur Werte aus Test A mit mindestens 3 frischen Banken. Kopiervorlage - "
          "erst uebernehmen, wenn der Firmenname oben stimmt. Die Kursziele fehlen "
          "bewusst: sie stuenden in USD und wuerden gegen die Euro-Kurse gerechnet "
          "Unsinn ergeben._", "", "```",
          "ticker,bank,datum,einstufung,kursziel,quelle"]
    if genug:
        for z in genug:
            best = z["treffer"]
            for b in best["beispiele"]:
                datum, rest = b.split(" ", 1)
                bank, grade = rest.rsplit(": ", 1)
                L.append(f"{z['ticker']},{bank},{datum},{grade},,Yahoo/{best['kandidat']}")
    else:
        L.append("# kein Wert erreicht 3 frische Banken")
    L += ["```", "",
          "_Achtung: oben stehen nur die vier juengsten Banken je Wert. Wenn ein Wert "
          "als Ersatz taugt, gehoert die Abfrage in den Screener statt in eine "
          "Handdatei - dann kommen alle Banken automatisch mit._", ""]
    return "\n".join(L)


def alle_ticker() -> dict[str, tuple[str, str, str]]:
    """Jede Zeile aus analysten.csv, unabhaengig von der Quelle."""
    if not ANALYSTEN_CSV.exists():
        return {}
    import csv
    with ANALYSTEN_CSV.open(encoding="utf-8") as f:
        return {z["ticker"].upper(): (z["ticker"], z.get("name", ""),
                                      z.get("quelle", ""))
                for z in csv.DictReader(f)}


def main() -> int:
    werte = zu_pruefende_ticker()

    if "--nur" in sys.argv:
        wunsch = {t.strip().upper() for t in sys.argv[sys.argv.index("--nur") + 1].split(",")}
        werte = [w for w in werte if w[0].upper() in wunsch]
        # Ein ausdruecklich genannter Ticker wird geprueft, auch wenn sein
        # Konsens schon aus benannten Einzelratings stammt. Sonst liesse
        # sich eine Zweitnotierung nie gegen die vorhandene Quelle testen -
        # genau das war am 24.08.2026 der Fall: ASML fiel aus der Auswahl,
        # der Lauf prueft dann einen einzigen Wert und beantwortet nichts.
        alle = alle_ticker()
        vorhanden = {w[0].upper() for w in werte}
        for t in sorted(wunsch - vorhanden):
            if t in alle:
                werte.append(alle[t])
                print(f"  {t} zusaetzlich aufgenommen "
                      f"(Quelle bisher: {alle[t][2] or 'keine'}).")
            else:
                print(f"  ! {t} steht nicht in analysten.csv - uebersprungen.")
        print(f"Eingeschraenkt auf {len(werte)} Werte.")

    if not werte:
        print("Nichts zu pruefen.")
        return 1

    print(f"Quellencheck fuer {len(werte)} Werte.")
    a_zeilen = test_a(werte)
    b_zeilen = test_b(werte)

    bericht = baue_bericht(a_zeilen, b_zeilen)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    AUSGABE.write_text(bericht, encoding="utf-8")
    (DOCS_DIR / "quellencheck.json").write_text(
        json.dumps({"erstellt": datetime.now(timezone.utc).isoformat(),
                    "test_a": a_zeilen, "test_b": b_zeilen},
                   indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nGeschrieben: {AUSGABE}")
    print("\n" + bericht[:1200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
