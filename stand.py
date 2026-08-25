"""
stand.py - eine Regel, die verhindert, dass ein guter Stand von einem
schlechteren ueberschrieben wird.

Das Problem, das dieses Modul loest:
Seit dem 26.08.2026 laufen zwei Screenings am Tag - 18:00 UTC fuer die
europaeischen Boersen (XETRA schliesst 15:30 UTC im Sommer, 16:30 UTC im
Winter) und 22:15 UTC fuer die US-Boersen. Jeder Lauf schreibt die CSV
KOMPLETT neu, fuer alle Werte. Faellt Yahoo bis 22:15 bei den DAX-Werten
schon auf den Vortag zurueck - genau das ist am 25.08.2026 passiert, dort
standen um 02:17 UTC alle 39 DAX-Werte und ASML auf dem Freitagsschluss -,
dann wuerde der Abendlauf die guten Daten des Nachmittagslaufs mit
schlechteren ueberschreiben.

Die Regel:
  Ist der frische Abruf fuer einen Wert AELTER als der schon gespeicherte
  Stand, bleibt der gespeicherte stehen. Bei gleichem Datum gewinnt der
  frische Abruf - so bekommen die US-Werte um 22:15 ihre vollstaendige
  Tageskerze, waehrend die europaeischen vom 18:00-Lauf geschuetzt bleiben.

Was die Regel NICHT kann:
Sie rettet nur, was schon einmal berechnet und gespeichert wurde. Skripte,
die ihre Ausgabe bei jedem Lauf komplett aus den Kerzen neu berechnen und
kein Zwischenergebnis je Wert ablegen - tiefs.py schreibt nur Markdown -
koennen einen verlorenen Handelstag nicht zurueckholen. Fuer die gibt es
`vergleichsstaende()`: sie merken wenigstens, dass sie aelter sind als
marktdaten.csv, und koennen es melden, statt still abzuweichen.

Bewusst KEIN Zeitstempel als Kriterium, sondern das Handelsdatum der
letzten Kerze. Ein spaeterer Lauf ist nicht automatisch der bessere -
darum geht es hier ja gerade.
"""

from __future__ import annotations

import csv
import os


def _zahl(wert):
    """Text aus der CSV zurueck in Zahl, wenn es eine war.

    Wichtig, nicht kosmetisch: aus einer CSV kommt alles als Text zurueck,
    und in Python ist der String "0" WAHR. Ohne diese Umwandlung haette
    eine zurueckgehaltene Zeile in marktdaten.py jeden Wert als
    Hammer-Signal gemeldet (`if r["hammer"] or r["umkehrkerze"]`), und in
    stundenwache.py haette das Sortieren von Text gegen Zahl den Lauf
    abgebrochen. Beides beim Test am 26.08.2026 aufgefallen.

    Datumsangaben und andere Texte bleiben unangetastet.
    """
    if not isinstance(wert, str) or wert == "":
        return wert
    try:
        return int(wert)
    except ValueError:
        pass
    try:
        return float(wert)
    except ValueError:
        return wert


def gespeicherte_staende(pfad, schluessel: str = "ticker",
                         datum_feld: str = "datum") -> dict[str, str]:
    """Handelsdatum je Wert aus einer vorhandenen CSV. Leer, wenn keine da.

    Fehler werden geschluckt und als "nichts bekannt" behandelt: eine
    unlesbare Altdatei darf den Lauf nicht kippen, sie kostet dann nur
    den Schutz fuer diesen einen Durchgang.
    """
    if not os.path.exists(pfad):
        return {}
    try:
        with open(pfad, encoding="utf-8", newline="") as f:
            return {r[schluessel]: (r.get(datum_feld) or "")
                    for r in csv.DictReader(f)
                    if r.get(schluessel)}
    except Exception as e:
        print(f"  Stand: {pfad} nicht lesbar ({e}) - ohne Schutz weiter.")
        return {}


def zusammenfuehren(neue: list[dict], pfad, schluessel: str = "ticker",
                    datum_feld: str = "datum",
                    markierung: str = "stand_gehalten") -> tuple[list[dict], list[dict]]:
    """Frische Zeilen mit der vorhandenen CSV verschmelzen.

    Rueckgabe: (zeilen, gehalten). `zeilen` enthaelt je Wert die bessere
    der beiden Fassungen, `gehalten` nur die, bei denen die alte gewonnen
    hat - fuer die Meldung im Lauf.

    Jede Zeile bekommt die Spalte `stand_gehalten`: 1 heisst, hier steht
    nicht der Abruf von eben, sondern ein aelterer, aber juengerer Stand.
    Sichtbar statt still.
    """
    if not neue:
        return neue, []

    alt_datum = gespeicherte_staende(pfad, schluessel, datum_feld)
    alt_zeilen: dict[str, dict] = {}
    if alt_datum and os.path.exists(pfad):
        try:
            with open(pfad, encoding="utf-8", newline="") as f:
                alt_zeilen = {r[schluessel]: r for r in csv.DictReader(f)
                              if r.get(schluessel)}
        except Exception:
            alt_zeilen = {}

    felder = list(neue[0].keys())
    if markierung not in felder:
        felder.append(markierung)

    zeilen, gehalten = [], []
    for r in neue:
        k = r.get(schluessel)
        neu_d = r.get(datum_feld) or ""
        alt_d = alt_datum.get(k, "")
        # Nur zurueckhalten, wenn BEIDE ein Datum haben und das alte
        # spaeter liegt. Ohne Datum kein Urteil - dann gilt der Abruf.
        if k and neu_d and alt_d and alt_d > neu_d and k in alt_zeilen:
            behalten = dict(alt_zeilen[k])
            # Auf das aktuelle Spaltenbild bringen: fehlende Felder leer,
            # damit der DictWriter nicht ueber unbekannte Schluessel faellt.
            # Zahlen zurueckverwandeln, siehe _zahl().
            zeile = {f: _zahl(behalten.get(f, "")) for f in felder}
            zeile[markierung] = 1
            zeilen.append(zeile)
            gehalten.append({"ticker": k, "gehalten": alt_d, "abruf": neu_d})
        else:
            r[markierung] = 0
            zeilen.append(r)

    if gehalten:
        print(f"  ! STAND GEHALTEN: {len(gehalten)} Werte behalten den "
              f"gespeicherten, juengeren Stand aus "
              f"{os.path.basename(pfad)} - der frische Abruf war aelter.")
        for g in sorted(gehalten, key=lambda x: x["ticker"]):
            print(f"      {g['ticker']:10s} behalten {g['gehalten']} "
                  f"(Abruf lieferte {g['abruf']})")
    return zeilen, gehalten


def vergleichsstaende(pfad, schluessel: str = "ticker",
                      datum_feld: str = "datum") -> dict[str, str]:
    """Fuer Skripte ohne eigene CSV: was marktdaten.csv als Stand kennt.

    Damit koennen sie melden, dass ihre eigene Rechnung auf aelteren
    Kerzen steht - zurueckholen koennen sie den Tag nicht.
    """
    return gespeicherte_staende(pfad, schluessel, datum_feld)
