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
import stand
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


def stimmigkeit(tag: pd.DataFrame, tages: pd.DataFrame,
                a: float | None) -> tuple[str, float]:
    """Passen Stundenreihe und Tagesreihe ueberhaupt zusammen?

    Beide Reihen kommen von Yahoo, aber aus verschiedenen Endpunkten. Rund
    um Splits und andere Kapitalmassnahmen rechnet der eine Endpunkt die
    Historie schon zurueck und der andere noch nicht - dann stehen die
    Marken aus der Tagesreihe auf einer anderen Skala als der laufende
    Kurs aus der Stundenreihe.

    Beobachtet am 25.08.2026 im ersten Lauf: MRNA hatte Tagesmarken bei
    62-65 und einen Stundenkurs von 159 (Faktor 2,43), MRK Marken bei
    127-131 gegen 155 (Faktor 1,19). Beides wurde als "Swing-Hoch
    ueberwunden" mit 5,2 bzw. 5,3 ATR gemeldet - eine Zahl, die wie ein
    starkes Signal aussieht und in Wahrheit ein Skalenfehler war. Die
    uebrigen 156 Werte lagen zwischen 0,80 und 1,03.

    Lieber "unklar" ausweisen als eine erfundene Zahl. Geprueft wird gegen
    den letzten Tagesschluss; ein echter Kurssprung faellt damit auch auf,
    was in Ordnung ist - dann steht der Wert zur Ansicht statt zum Urteil.
    """
    letzter_tagesschluss = float(tages["Close"].iloc[-1])
    jetzt = float(tag["Close"].iloc[-1])
    if letzter_tagesschluss <= 0:
        return "unklar", 0.0
    abweichung = abs(jetzt - letzter_tagesschluss) / letzter_tagesschluss
    in_atr = abs(jetzt - letzter_tagesschluss) / a if a else 0.0
    # Beide Huerden muessen fallen: prozentual gross UND in ATR gross.
    # Ein volatiler Wert darf sich bewegen, ohne gleich als unstimmig zu
    # gelten.
    if abweichung > 0.15 and in_atr > 3.0:
        return "unstimmig", round(abweichung, 4)
    return "ok", round(abweichung, 4)


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
    lage, abw = stimmigkeit(tag, tages, a)
    if lage == "unstimmig":
        u_tief["art"] = "unklar"

    zeile = {
        "ticker": ticker,
        "datum": tag.index[-1].date().isoformat(),
        "stunden_erfasst": len(tag),
        "reihen_lage": lage,
        "reihen_abweichung": abw,
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
        if lage == "unstimmig":
            u_hoch["art"] = "unklar"
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


FELDER = ["ticker", "datum", "stunden_erfasst", "reihen_lage",
          "reihen_abweichung", "tages_offen", "tages_hoch",
          "tages_tief", "tages_schluss", "atr",
          "tief_marke", "tief_datum", "tief_bestaetigt", "tief_urteil",
          "tief_stunden_drunter", "tief_abstand_atr", "tief_tiefster_punkt_atr",
          "hoch_marke", "hoch_datum", "hoch_urteil", "hoch_stunden_drueber",
          "hoch_abstand_atr"]


def csv_schreiben(zeilen: list[dict]) -> None:
    DOCS.mkdir(exist_ok=True)
    felder = FELDER + ["stand_gehalten"]
    with open(CSV_AUS, "w", newline="", encoding="utf-8") as f:
        s = csv.writer(f)
        s.writerow(felder)
        for z in sorted(zeilen, key=lambda x: x["ticker"]):
            s.writerow([z.get(k, "") for k in felder])
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")


def md_schreiben(zeilen: list[dict]) -> None:
    """Nur was auffaellt. An einem ruhigen Tag ist die Datei fast leer -
    das ist der Zweck, nicht ein Fehler."""
    gebrochen = [z for z in zeilen if z["tief_urteil"] == "gebrochen"]
    erobert = [z for z in zeilen if z["tief_urteil"] == "zurueckerobert"]
    getestet = [z for z in zeilen if z["tief_urteil"] == "angetestet"]
    ueber_hoch = [z for z in zeilen if z.get("hoch_urteil") == "gebrochen"]
    unstimmig = [z for z in zeilen if z["reihen_lage"] == "unstimmig"]

    # Wie weit ist der Handelstag? Ein voller US-Tag hat 7 Stundenkerzen,
    # ein DAX-Tag 9. Weniger heisst: der Lauf faellt mitten in die Sitzung,
    # und "Schluss" ist in Wahrheit der Stand im Moment des Abrufs. Im
    # ersten Lauf am 25.08.2026 um 17:40 UTC hatten die US-Werte erst 5 von
    # 7 Kerzen - die Marktdaten waren also noch nicht endgueltig.
    stunden = sorted({z["stunden_erfasst"] for z in zeilen})
    voll = max(stunden) if stunden else 0
    teilweise = [z for z in zeilen if z["stunden_erfasst"] < 7]

    L = ["# Stundenwache", "",
         f"Stand: {zeilen[0]['datum'] if zeilen else '-'} · "
         f"{len(zeilen)} Werte mit Stundendaten · "
         f"erstellt {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC", ""]

    if teilweise:
        L += [f"> **Sitzung noch nicht abgeschlossen.** {len(teilweise)} Werte "
              f"haben weniger als 7 Stundenkerzen (erfasste Stunden: "
              f"{', '.join(str(s) for s in stunden)}). Bei diesen ist "
              f"\"Schluss\" der Stand im Moment des Abrufs, nicht der "
              f"Tagesschluss - die Urteile koennen sich bis Handelsende noch "
              f"drehen.", ""]

    L += ["Marken sind das juengste Swing-Tief und das juengste Swing-Hoch aus "
          "`tiefs_regel.py`, also dieselben wie im Tagesbericht. Geprueft wird "
          "nur, was der letzte Handelstag auf Stundenbasis damit gemacht hat.",
          "", "Lesart der Urteile:", "",
          "- **gebrochen** - eine Stundenkerze hat jenseits der Marke geschlossen",
          "- **zurueckerobert** - im Tagesverlauf drunter gewesen, am Ende darueber "
          "geschlossen. Auf der Tageskerze nicht erkennbar.",
          "- **angetestet** - nur mit dem Docht beruehrt, kein Schluss dahinter",
          "- **unklar** - Stunden- und Tagesreihe passen nicht zusammen, siehe unten",
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

    L.append(f"## Reihen unstimmig - kein Urteil ({len(unstimmig)})")
    L.append("")
    if unstimmig:
        L.append("Stundenkurs und Tagesreihe stehen auf verschiedenen Skalen - "
                 "typisch rund um Splits, wenn die beiden Yahoo-Endpunkte die "
                 "Historie unterschiedlich zurueckrechnen. Die Marken aus der "
                 "Tagesreihe sind hier nicht mit dem laufenden Kurs "
                 "vergleichbar, deshalb steht kein Urteil. Von Hand im Chart "
                 "nachsehen.")
        L.append("")
        L.append("| Wert | Tief-Marke | Hoch-Marke | Stundenkurs | Abweichung |")
        L.append("|---|---|---|---|---|")
        for z in sorted(unstimmig, key=lambda x: -x["reihen_abweichung"]):
            L.append(f"| {z['ticker']} | {z['tief_marke']} | "
                     f"{z.get('hoch_marke', '')} | {z['tages_schluss']} | "
                     f"{z['reihen_abweichung']:.0%} |")
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

    # Gleiche Schutzregel wie in marktdaten.py: der Abendlauf darf den
    # abgeschlossenen europaeischen Handelstag aus dem Nachmittagslauf
    # nicht mit einem zurueckgefallenen Abruf ueberschreiben.
    zeilen, _gehalten = stand.zusammenfuehren(zeilen, str(CSV_AUS))

    csv_schreiben(zeilen)
    md_schreiben(zeilen)
    if ohne:
        print(f"Ohne Stundendaten ({len(ohne)}): {' '.join(ohne)}")


if __name__ == "__main__":
    main()
