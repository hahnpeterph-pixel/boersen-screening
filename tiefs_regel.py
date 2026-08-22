"""
tiefs_regel.py - die EINE Definition von Tiefs, Hochs und Abwaertsserien.

Alles, was Tiefs zaehlt, importiert aus dieser Datei. Vorher stand die Logik
dreimal im Repository: in marktdaten.py, in tiefs.py (noch mit der alten
3-links-3-rechts-Regel) und in phasen.py. Drei Staende, die sich nicht
widersprochen haben, aber auch nicht dasselbe meinten - "Tief 5 von 2" waere
sonst eine Zahl aus Skript A geteilt durch eine Zahl aus Skript C.

Die Regel (Stand 22.08.2026):

  1. Solange es abwaerts geht, gilt immer das TIEFSTE Tief der Strecke.
  2. Ein Tief zaehlt, sobald eine spaetere Kerze das HOCH der Tiefkerze
     ueberschreitet. Kein Kerzenmuster noetig, ein Tageshoch darueber reicht.
  3. Danach laeuft eine Aufwaertsstrecke, bis der Kurs das TIEF der
     Hoechstkerze unterschreitet. Ab dort wird das naechste Tief gesucht.
  4. Kommt ein tieferer Kurs, bevor die Umkehr belegt ist, rueckt der
     Kandidat nach unten - das alte Tief verschwindet ohne zu zaehlen.
  5. Keine Mindestbewegung. Jede Umkehr zaehlt.

Fuer die SERIE gilt zusaetzlich (das ist die Aenderung vom 22.08.2026):

  6. Gezaehlt werden nur NEUE Tiefststaende. Ein Tief ueber dem laufenden
     Tiefstand zaehlt nicht mit, die Serie laeuft weiter.
  7. Beendet ist die Abwaertsstrecke erst, wenn eine Erholung ein
     vorangegangenes Hoch ueberschreitet.

Zu Punkt 7 gibt es zwei Lesarten, beide werden gerechnet:

  "starthoch"        - Standard. Die Strecke endet erst ueber dem Hoch, an
                       dem sie begonnen hat.
  "vorheriges_hoch"  - Dow-Lesart. Die Strecke endet ueber dem unmittelbar
                       vorangegangenen Hoch.

Gemessen an der Cadence-Struktur vom 22.08.2026 (Tiefs 373,20 / 358,50 /
320,07 / 319,46 / 311,47, Zwischentief 333,00 zaehlt nicht) liefert
"starthoch" die 5, die im Chart abgelesen wurde; "vorheriges_hoch" kommt auf
2, weil eine kleine Erholung Anfang August die vorige ueberschreitet. Auf
dieser feinkoernigen Ebene gibt es auf der Hochseite genauso wenig eine
Mindestbewegung wie auf der Tiefseite - deshalb ist die Dow-Lesart hier
nicht anwendbar. Sie laeuft als Vergleichszahl mit, nicht als Kandidat.

Gerechnet wird auf abgeschlossenen Tageskerzen.
"""

from __future__ import annotations

import pandas as pd

VARIANTEN = ("dow", "starthoch", "vorheriges_hoch")
STANDARD = "dow"


def _leer(df) -> bool:
    """True, wenn mit diesem DataFrame nicht gerechnet werden kann.

    Ein Ticker ohne Daten ist der Normalfall, kein Sonderfall: XAUUSD=X
    liefert bei Yahoo seit Monaten nichts, delistete Werte hoeren von einem
    Tag auf den anderen auf. Alle Funktionen hier geben dann leer zurueck,
    statt den ganzen Lauf abzubrechen - das Aufrufskript entscheidet, ob es
    den Wert ueberspringt oder auf einen Ersatzticker ausweicht.
    """
    return df is None or len(df) < 2 or "Low" not in df.columns


def pivots(df: pd.DataFrame) -> list[tuple[str, int]]:
    """Abwechselnde Tiefs und Hochs nach der Umkehr-Regel, chronologisch.

    Rueckgabe: [("tief", i), ("hoch", j), ...] mit i als Zeilennummer in df.
    Das laufende, noch unbestaetigte Extrem ist NICHT enthalten - dafuer
    swing_tiefs(unbestaetigt=True).
    """
    if _leer(df):
        return []
    hoch, tief = df["High"].values, df["Low"].values
    punkte: list[tuple[str, int]] = []
    richtung = "ab"
    kandidat = gipfel = 0

    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i
            elif hoch[i] > hoch[kandidat]:
                punkte.append(("tief", kandidat))
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i
            elif tief[i] < tief[gipfel]:
                punkte.append(("hoch", gipfel))
                richtung, kandidat = "ab", i
    return punkte


def _laufendes_tief(df: pd.DataFrame) -> int | None:
    """Zeilennummer des juengsten, noch unbestaetigten Tiefs - oder None.

    Unbestaetigt heisst: das Hoch der Tiefkerze wurde noch nicht
    ueberschritten. Genau in diesen Tagen will man kaufen, deshalb wird es
    mitgegeben und mit best=0 markiert.
    """
    if _leer(df):
        return None
    hoch, tief = df["High"].values, df["Low"].values
    richtung = "ab"
    kandidat = gipfel = 0
    for i in range(1, len(df)):
        if richtung == "ab":
            if tief[i] < tief[kandidat]:
                kandidat = i
            elif hoch[i] > hoch[kandidat]:
                richtung, gipfel = "auf", i
        else:
            if hoch[i] > hoch[gipfel]:
                gipfel = i
            elif tief[i] < tief[gipfel]:
                richtung, kandidat = "ab", i
    return kandidat if richtung == "ab" else None


def swing_tiefs(df: pd.DataFrame, fenster_tage: int | None = None,
                unbestaetigt: bool = True) -> list[dict]:
    """Swing-Tiefs, juengstes zuerst.

    fenster_tage=None liefert die volle Historie. Das ist der Normalfall fuer
    die Serienzaehlung: eine Serie kann laenger sein als 90 Tage - bei
    Cadence reichte sie 78 Tage zurueck, bei einem traegen Wert faellt der
    Anfang sonst still heraus und die Serie wird zu kurz gezaehlt.
    """
    if _leer(df):
        return []
    tief = df["Low"].values
    daten = df.index
    vols = df["Volume"].values if "Volume" in df.columns else [None] * len(df)

    treffer = [{"i": i, "datum": daten[i], "tief": float(tief[i]),
                "vol": vols[i], "best": True}
               for art, i in pivots(df) if art == "tief"]

    if unbestaetigt:
        k = _laufendes_tief(df)
        if k is not None and not any(t["i"] == k for t in treffer):
            treffer.append({"i": k, "datum": daten[k], "tief": float(tief[k]),
                            "vol": vols[k], "best": False})

    if fenster_tage:
        grenze = daten[-1] - pd.Timedelta(days=fenster_tage)
        treffer = [t for t in treffer if t["datum"] >= grenze]
    treffer.sort(key=lambda t: t["datum"], reverse=True)
    return treffer


def swing_hochs(df: pd.DataFrame) -> list[dict]:
    """Bestaetigte Swing-Hochs, chronologisch."""
    if _leer(df):
        return []
    hoch = df["High"].values
    daten = df.index
    return [{"i": i, "datum": daten[i], "hoch": float(hoch[i])}
            for art, i in pivots(df) if art == "hoch"]


def sequenzen(df: pd.DataFrame, variante: str = STANDARD) -> list[dict]:
    """Alle Abwaertssequenzen der Historie, aelteste zuerst.

    Je Sequenz:
      tiefs        Zeilennummern der zaehlenden Tiefs (neue Tiefststaende)
      anzahl       wie viele davon
      start_i      Zeilennummer des ersten zaehlenden Tiefs
      start_hoch_i Zeilennummer des Hochs, an dem die Strecke begann
                   (None bei der ersten Sequenz der Historie)
      ende_i       Zeilennummer des letzten zaehlenden Tiefs
      tiefstand    tiefster Kurs der Sequenz
      laufend      True, wenn die Sequenz noch nicht beendet ist
    """
    if variante not in VARIANTEN:
        raise ValueError(f"Unbekannte Variante: {variante}")

    if _leer(df):
        return []
    hoch, tief = df["High"].values, df["Low"].values
    ergebnis: list[dict] = []

    def leer() -> dict:
        return {"tiefs": [], "start_hoch_i": None, "start_hoch": None,
                "tiefstand": None, "ref_hoch": None}

    seq = leer()
    letztes_hoch = None

    def schliessen(laufend: bool) -> None:
        if not seq["tiefs"]:
            return
        ergebnis.append({
            "tiefs": list(seq["tiefs"]),
            "anzahl": len(seq["tiefs"]),
            "start_i": seq["tiefs"][0],
            "start_hoch_i": seq["start_hoch_i"],
            "ende_i": seq["tiefs"][-1],
            "tiefstand": seq["tiefstand"],
            "laufend": laufend,
        })

    for art, i in pivots(df):
        if art == "hoch":
            h = float(hoch[i])
            if variante == "dow":
                # Dow: ein hoeheres Hoch beendet den Abwaertstrend nur, wenn
                # zuvor ein hoeheres Tief kam - und gemessen wird gegen das
                # Hoch VOR dem tiefsten Tief, nicht gegen ein beliebiges
                # Zwischenhoch. Diese Referenz wandert mit jedem neuen Tief
                # nach unten, der Trend zieht sich also selbst enger.
                #
                # Fehlt das Hoch davor - das ist am Anfang jeder Historie so,
                # weil das erste Tief vor dem ersten Hoch liegt -, dann dient
                # das erste Hoch DANACH als Referenz. Ohne diesen Rueckfall
                # bleibt grenze dauerhaft None und die Serie endet nie: im
                # Test lieferte ein Aufwaertstrend mit zehn Ruecksetzern eine
                # einzige Sequenz statt zehn, und Cadence kam auf 17 Tiefs in
                # drei Jahren statt der erwarteten 50 bis 60.
                # Ein Hoch ueber der Referenz beendet die Strecke sofort.
                #
                # Bis 22.08.2026 stand hier zusaetzlich die Bedingung, dass
                # VORHER ein hoeheres Tief gekommen sein muss. Diese
                # Reihenfolge war erfunden - Dow verlangt hoeheres Hoch UND
                # hoeheres Tief, aber nicht in dieser Folge. Die Wirkung war
                # gravierend: bei CDNS brach die Serie am 25.03.2025 nicht
                # (269,71 gegen Referenz 246,79), sondern erst am 02.04. am
                # kleineren Hoch 265,73 - und das Tief vom 31.03. bei 248,52
                # ging dabei zwischen zwei Sequenzen verloren. Es zaehlte
                # weder zur alten noch zur neuen Strecke.
                if seq["ref_hoch"] is None:
                    # Kein Hoch vor dem tiefsten Tief - das ist am Anfang
                    # jeder Historie so. Dann dient das erste Hoch DANACH als
                    # Referenz, sonst bleibt grenze dauerhaft None und die
                    # Serie endet nie.
                    seq["ref_hoch"] = h
                    grenze = None
                else:
                    grenze = seq["ref_hoch"]
            elif variante == "starthoch":
                grenze = seq["start_hoch"]
            else:
                grenze = letztes_hoch
            if grenze is not None and h > grenze:
                schliessen(False)
                seq = leer()
                seq["start_hoch_i"], seq["start_hoch"] = i, h
            elif seq["start_hoch"] is None:
                seq["start_hoch_i"], seq["start_hoch"] = i, h
            letztes_hoch = h
        else:
            t = float(tief[i])
            if seq["tiefstand"] is None or t < seq["tiefstand"]:
                seq["tiefs"].append(i)
                seq["tiefstand"] = t
                seq["ref_hoch"] = letztes_hoch

    schliessen(True)
    return ergebnis


def tiefserie(df: pd.DataFrame, variante: str = STANDARD) -> tuple:
    """Die LAUFENDE Abwaertsserie: (anzahl, startdatum, tiefstand).

    Leere Rueckgabe ("", "", ""), wenn keine laufende Serie erkennbar ist -
    etwa direkt nach einem Ausbruch nach oben.
    """
    seqs = sequenzen(df, variante)
    if not seqs or not seqs[-1]["laufend"]:
        return "", "", ""
    s = seqs[-1]
    return (s["anzahl"], f"{df.index[s['start_i']]:%Y-%m-%d}",
            round(s["tiefstand"], 4))
