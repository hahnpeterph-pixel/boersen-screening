"""
stundenwache.py - was ist an den Marken passiert, die ohnehin schon feststehen.

Kein zweites Screening. Das Skript sucht KEINE eigenen Tiefs und stellt
keine eigenen Regeln auf. Es nimmt die Marken, die tiefs_regel.py auf
Tagesbasis ohnehin liefert - juengstes Swing-Tief und juengstes
Swing-Hoch - und schaut auf Stundenkerzen nach, was der laufende Tag mit
ihnen gemacht hat.

Warum ueberhaupt:
Auf der Tageskerze ist ein Bruch nicht von einem kurzen Unterschreiten zu
unterscheiden, wenn der Wert am Ende darueber schliesst. Genau dieser
Fall - intraday drunter, Schluss drueber - ist die interessante Information
und auf Tagesbasis unsichtbar. Umgekehrt sagt "fuenf Stunden unter der
Marke" etwas anderes als "eine Stunde".

Warum die Stundenreihe NICHT weiterverwendet wird:
Yahoo liefert 1h nur rund zwei Jahre zurueck. Fuer Halteraten, Puffer-
Verteilungen oder RSI-Schwellen je Wert reicht das nicht - dort haetten
einzelne Tiefspositionen null bis zwei Faelle. Diese Auswertungen bleiben
auf der Tagesreihe in historie.py. Hier geht es ausschliesslich um den
laufenden Tag.

Was NICHT hier steht:
Der Abstand zum eigenen Knock-out. Positionsdaten gehoeren nicht ins
oeffentliche Repo (Entscheidung 58). Die Verknuepfung "Marke gefallen UND
mein KO ist nah" passiert in der Excel-Mappe.

Schreibt:
  docs/stundenwache.csv  eine Zeile je Wert, alle Rohwerte einzeln
  docs/stundenwache.md   nur die Werte, bei denen etwas passiert ist
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import kurse
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
CSV_AUS = DOCS / "stundenwache.csv"
MD_AUS = DOCS / "stundenwache.md"

ATR_TAGE = 14

# Universum wie in marktdaten.py. Bewusst dieselbe Liste und bewusst
# dupliziert statt importiert: marktdaten.py baut UNIVERSUM auf Modulebene
# mit Rohstoffen und Waehrung zusammen, die hier nichts zu suchen haben -
# Gold und EUR/USD haben keine Swing-Tief-Logik im Sinne der Kaufregel.
US = """AAPL ABNB ADBE ADI ADP ADSK AEP AMAT AMD AMGN AMZN ARM ASML AVGO
AXP AZN BA BIIB BKNG BKR CAT CDNS CDW CEG CHTR CMCSA COST CPRT CRM CRWD CSCO
CSGP CSX CTAS CTSH DASH DDOG DIS DXCM EXC FANG FAST FTNT GEHC GILD
GOOGL GS HD HON IBM IDXX ILMN INTC INTU ISRG JNJ JPM KDP KHC KLAC KO LIN LRCX
LULU MAR MCD MCHP MDB MDLZ MELI META MMM MNST MRK MRNA MRVL MSFT MU NFLX NKE
NVDA NXPI ODFL ON ORCL ORLY PANW PAYX PCAR PDD PEP PG PLTR PYPL QCOM REGN ROP
ROST SBUX SHW SNPS SPGI TEAM TMUS TRV TSLA TTD TTWO TXN UNH V VRSK VRTX VZ
WBD WDAY WMT XEL ZS""".split()

DAX = """ADS.DE AIR.DE ALV.DE BAS.DE BAYN.DE BEI.DE BMW.DE BNR.DE CBK.DE CON.DE
DTG.DE DBK.DE DB1.DE DHL.DE DTE.DE EOAN.DE FRE.DE HNR1.DE HEI.DE HEN3.DE
IFX.DE MBG.DE MRK.DE MTX.DE MUV2.DE P911.DE PAH3.DE QIA.DE RHM.DE RWE.DE SAP.DE
SRT3.DE SIE.DE ENR.DE SHL.DE SY1.DE VOW3.DE VNA.DE ZAL.DE""".split()

UNIVERSUM = list(dict.fromkeys(US + DAX))


def atr(df: pd.DataFrame, tage: int = ATR_TAGE) -> float | None:
    """Wie in marktdaten.py - gleiche Formel, damit die ATR-Angaben
    zwischen den Berichten vergleichbar bleiben."""
    h, t, c = df["High"], df["Low"], df["Close"]
    v = c.shift(1)
    tr = pd.concat([h - t, (h - v).abs(), (t - v).abs()], axis=1).max(axis=1)
    w = tr.tail(tage).mean()
    return None if pd.isna(w) else float(w)


def letzter_tag(std: pd.DataFrame) -> pd.DataFrame:
    """Nur die Kerzen des juengsten Handelstags der Stundenreihe."""
    tage = std.index.normalize()
    return std[tage == tage[-1]]


def urteil(tag: pd.DataFrame, marke: float, richtung: str) -> dict:
    """Was der Tag mit einer Marke gemacht hat.

    richtung "unten": Marke ist eine Unterstuetzung (Swing-Tief).
    richtung "oben":  Marke ist ein Widerstand (Swing-Hoch).

    Unterschieden wird bewusst zwischen beruehrt (Docht) und geschlossen
    (Kerzenkoerper). Ein Docht unter dem Tief ist kein Bruch - eine
    Stundenkerze, die darunter schliesst, ist einer.
    """
    if richtung == "unten":
        beruehrt = bool((tag["Low"] < marke).any())
        stunden = int((tag["Close"] < marke).sum())
        schluss_drunter = bool(tag["Close"].iloc[-1] < marke)
        extrem = float(tag["Low"].min())
    else:
        beruehrt = bool((tag["High"] > marke).any())
        stunden = int((tag["Close"] > marke).sum())
        schluss_drunter = bool(tag["Close"].iloc[-1] > marke)
        extrem = float(tag["High"].max())

    # Der eigentliche Grund fuer dieses Skript: auf der Tageskerze sind
    # diese beiden Faelle nicht auseinanderzuhalten.
    #
    # Reihenfolge ist wichtig. "Zurueckerobert" setzt voraus, dass eine
    # Stundenkerze tatsaechlich jenseits der Marke GESCHLOSSEN hat und der
    # Wert danach zurueckkam. Ein blosser Docht ohne Schluss dahinter ist
    # nur ein Antesten - wird das nicht getrennt geprueft, meldet jeder
    # Docht faelschlich eine Rueckeroberung.
    if schluss_drunter:
        art = "gebrochen"
    elif stunden > 0:
        art = "zurueckerobert"
    elif beruehrt:
        art = "angetestet"
    else:
        art = "unberuehrt"

    return {"art": art, "stunden": stunden, "extrem": extrem}


def je_wert(ticker: str) -> dict | None:
    tages = kurse.kerzen(ticker, period="400d")
    if tages is None:
        return None
    std = kurse.stundenkerzen(ticker, period="5d")
    if std is None:
        return None

    tag = letzter_tag(std)
    if tag.empty:
        return None

    a = atr(tages)
    tiefs = regel.swing_tiefs(tages, unbestaetigt=True)
    hochs = regel.swing_hochs(tages)
    if not tiefs:
        return None

    t = tiefs[0]
    u_tief = urteil(tag, t["tief"], "unten")

    zeile = {
        "ticker": ticker,
        "datum": tag.index[-1].date().isoformat(),
        "stunden_erfasst": len(tag),
        "tages_offen": round(float(tag["Open"].iloc[0]), 4),
        "tages_hoch": round(float(tag["High"].max()), 4),
        "tages_tief": round(float(tag["Low"].min()), 4),
        "tages_schluss": round(float(tag["Close"].iloc[-1]), 4),
        "atr": round(a, 4) if a else "",
        "tief_marke": round(t["tief"], 4),
        "tief_datum": pd.Timestamp(t["datum"]).date().isoformat(),
        "tief_bestaetigt": int(bool(t["best"])),
        "tief_urteil": u_tief["art"],
        "tief_stunden_drunter": u_tief["stunden"],
        # Abstand in ATR: negativ heisst unter der Marke. In ATR statt in
        # Prozent, damit die Zahl ueber Werte hinweg vergleichbar ist -
        # dieselbe Ueberlegung wie beim Puffer (Transaktionen Zeile 48).
        "tief_abstand_atr": (round((float(tag["Close"].iloc[-1]) - t["tief"]) / a, 3)
                             if a else ""),
        "tief_tiefster_punkt_atr": (round((u_tief["extrem"] - t["tief"]) / a, 3)
                                    if a else ""),
    }

    if hochs:
        h = hochs[-1]
        u_hoch = urteil(tag, h["hoch"], "oben")
        zeile.update({
            "hoch_marke": round(h["hoch"], 4),
            "hoch_datum": pd.Timestamp(h["datum"]).date().isoformat(),
            "hoch_urteil": u_hoch["art"],
            "hoch_stunden_drueber": u_hoch["stunden"],
            "hoch_abstand_atr": (round((float(tag["Close"].iloc[-1]) - h["hoch"]) / a, 3)
                                 if a else ""),
        })
    else:
        zeile.update({"hoch_marke": "", "hoch_datum": "", "hoch_urteil": "",
                      "hoch_stunden_drueber": "", "hoch_abstand_atr": ""})
    return zeile


FELDER = ["ticker", "datum", "stunden_erfasst", "tages_offen", "tages_hoch",
          "tages_tief", "tages_schluss", "atr",
          "tief_marke", "tief_datum", "tief_bestaetigt", "tief_urteil",
          "tief_stunden_drunter", "tief_abstand_atr", "tief_tiefster_punkt_atr",
          "hoch_marke", "hoch_datum", "hoch_urteil", "hoch_stunden_drueber",
          "hoch_abstand_atr"]


def csv_schreiben(zeilen: list[dict]) -> None:
    DOCS.mkdir(exist_ok=True)
    with open(CSV_AUS, "w", newline="", encoding="utf-8") as f:
        s = csv.writer(f)
        s.writerow(FELDER)
        for z in sorted(zeilen, key=lambda x: x["ticker"]):
            s.writerow([z.get(k, "") for k in FELDER])
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")


def md_schreiben(zeilen: list[dict]) -> None:
    """Nur was auffaellt. An einem ruhigen Tag ist die Datei fast leer -
    das ist der Zweck, nicht ein Fehler."""
    gebrochen = [z for z in zeilen if z["tief_urteil"] == "gebrochen"]
    erobert = [z for z in zeilen if z["tief_urteil"] == "zurueckerobert"]
    getestet = [z for z in zeilen if z["tief_urteil"] == "angetestet"]
    ueber_hoch = [z for z in zeilen if z.get("hoch_urteil") == "gebrochen"]

    L = ["# Stundenwache", "",
         f"Stand: {zeilen[0]['datum'] if zeilen else '-'} · "
         f"{len(zeilen)} Werte mit Stundendaten · "
         f"erstellt {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC", "",
         "Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus "
         "`tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird "
         "nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.",
         "", "Lesart der Urteile:", "",
         "- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen",
         "- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber "
         "geschlossen. Auf der Tageskerze nicht erkennbar.",
         "- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter",
         ""]

    def block(titel: str, liste: list[dict], schluessel: str,
              erklaerung: str) -> None:
        L.append(f"## {titel} ({len(liste)})")
        L.append("")
        if not liste:
            L.append("Keine.")
            L.append("")
            return
        L.append(erklaerung)
        L.append("")
        L.append("| Wert | Marke | Schluss | Abstand (ATR) | Stunden dahinter |")
        L.append("|---|---|---|---|---|")
        for z in sorted(liste, key=lambda x: x.get("tief_abstand_atr") or 0):
            L.append(f"| {z['ticker']} | {z[schluessel]} | {z['tages_schluss']} "
                     f"| {z.get('tief_abstand_atr', '')} "
                     f"| {z.get('tief_stunden_drunter', '')} |")
        L.append("")

    block("Tief gebrochen", gebrochen, "tief_marke",
          "Schluss unter dem juengsten Swing-Tief. Die Sequenz ist gerissen.")
    block("Tief zurueckerobert", erobert, "tief_marke",
          "Im Tagesverlauf unter der Marke, am Ende darueber. Das ist der Fall, "
          "den die Tageskerze verschluckt.")
    block("Tief angetestet", getestet, "tief_marke",
          "Docht bis unter die Marke, kein Stundenschluss darunter.")

    L.append(f"## Swing-Hoch ueberwunden ({len(ueber_hoch)})")
    L.append("")
    if ueber_hoch:
        L.append("| Wert | Hoch | Schluss | Abstand (ATR) | Stunden darueber |")
        L.append("|---|---|---|---|---|")
        for z in sorted(ueber_hoch,
                        key=lambda x: -(x.get("hoch_abstand_atr") or 0)):
            L.append(f"| {z['ticker']} | {z['hoch_marke']} | {z['tages_schluss']} "
                     f"| {z.get('hoch_abstand_atr', '')} "
                     f"| {z.get('hoch_stunden_drueber', '')} |")
        L.append("")
    else:
        L.append("Keine.")
        L.append("")

    L.append("---")
    L.append("")
    L.append("Alle Werte einzeln mit allen Rohzahlen: `stundenwache.csv`. "
             "Der Abstand zum eigenen Knock-out steht bewusst nicht hier - "
             "Positionsdaten bleiben ausserhalb des Repos.")

    DOCS.mkdir(exist_ok=True)
    MD_AUS.write_text("\n".join(L), encoding="utf-8")
    print(f"Geschrieben: {MD_AUS}")


def main() -> None:
    kurse.aufraeumen()
    zeilen, ohne = [], []
    for i, t in enumerate(UNIVERSUM, 1):
        z = je_wert(t)
        if z:
            zeilen.append(z)
        else:
            ohne.append(t)
        if i % 25 == 0:
            print(f"  {i}/{len(UNIVERSUM)} ...")

    if not zeilen:
        print("Keine Stundendaten erhalten - nichts geschrieben.")
        return

    csv_schreiben(zeilen)
    md_schreiben(zeilen)
    if ohne:
        print(f"Ohne Stundendaten ({len(ohne)}): {' '.join(ohne)}")


if __name__ == "__main__":
    main()
