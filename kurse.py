"""
kurse.py - ein Abruf, ein Cache, alle Skripte bedienen sich daraus.

Vorher holten screener.py, tiefs.py und marktdaten.py dieselben Kerzen
getrennt: sechs Abrufe plus einer plus einer, dreimal ueber die Leitung.
Das kostet Laufzeit im 30-Minuten-Fenster und provoziert Rate-Limits bei
Yahoo, die dann als "keine Daten" durchschlagen.

Weil die drei Skripte als getrennte Workflow-Schritte laufen, also in
getrennten Prozessen, reicht ein Cache im Arbeitsspeicher nicht - er muss
auf die Platte. Der Runner behaelt das Verzeichnis ueber alle Schritte
eines Laufs hinweg.

Der Cache liegt bewusst NICHT in state/, weil der Workflow "git add docs
state" macht und die Kursdateien sonst jeden Tag ins Repository wandern.
.kurse_cache/ gehoert in .gitignore.

Frische: ein Kalendertag. Ein zweiter Lauf am selben Tag liest aus dem
Cache, der naechste Morgen holt neu.
"""

from __future__ import annotations

import os
import shutil
from datetime import date

import pandas as pd
import yfinance as yf

HIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HIER, ".kurse_cache")

# Version im Dateinamen: aendert sich das Format oder die Aufbereitung,
# darf ein alter Cache nicht stillschweigend weiterbenutzt werden. Genau
# dieser Fehler ist beim Fundamentaldaten-Cache schon einmal passiert.
CACHE_VERSION = 1

MINDESTKERZEN = 30

# ── Abweichende Kursquellen ────────────────────────────────────────
# Einige Werte notieren an mehreren Boersen, und der Report rechnete
# bisher auf der falschen. ASML steht im Universum als "ASML" und wurde
# damit von der New Yorker Registry-Notierung in USD geholt - waehrend der
# Knock-out-Schein auf die Euro-Notierung lautet und der Chart im
# Orderbuch (Frage 9: Kurs 1508,00, Wochentief 1489,40) ebenfalls in Euro
# gelesen wurde. Der ausgewiesene Puffer war deshalb frei erfunden; bei
# ASML war er sechsmal zu gross.
#
# Der Ticker als Name bleibt unveraendert, damit alle Verknuepfungen mit
# analysten.csv und universe.json halten. Getauscht wird nur, WOHER die
# Kerzen kommen. Betroffen sind Kurs, ATR und Tiefs, also alles, was
# marktdaten.py und tiefs.py rechnen - screener.py holt seine Kurse
# getrennt und vergleicht dort Kurs und Kursziel weiter in derselben
# Waehrung, bleibt also in sich stimmig.
#
# BEWUSST OHNE RUECKFALL auf die andere Notierung: ein stiller Wechsel
# zurueck in eine fremde Waehrung wuerde genau den Fehler wieder
# einbauen, den diese Liste behebt. Liefert die Quelle nichts, faellt der
# Wert mit Meldung aus - sichtbar statt falsch.
#
# Der Quellencheck vom 24.08.2026 hat geprueft, welche Werte ueberhaupt
# betroffen sind: NXPI.AS kennt Yahoo nicht, NXP ist also kein
# Zweitnotierungsfall. AZN und CCEP haben ihre Ratings ohnehin auf der
# US-Seite. Bleibt ASML.
KURSQUELLE: dict[str, dict[str, str]] = {
    "ASML": {
        "ticker": "ASML.AS",
        "waehrung": "EUR",
        "grund": "Schein und Chart laufen auf der Euro-Notierung, "
                 "nicht auf der New Yorker Registry-Notierung",
    },
}


def quelle(ticker: str) -> str:
    """Von welchem Yahoo-Ticker die Kerzen dieses Wertes kommen."""
    return KURSQUELLE.get(ticker, {}).get("ticker", ticker)


def waehrung(ticker: str) -> str:
    """Waehrung der Kursreihe, leer wenn keine Ausnahme hinterlegt ist."""
    return KURSQUELLE.get(ticker, {}).get("waehrung", "")


def quellen(tickers: list[str]) -> dict[str, str]:
    """Name auf Quellticker fuer einen ganzen Stapel.

    Fuer historie.py, tagesreaktion.py und phasen.py: die drei holen ihre
    Kerzen aus Zeitgruenden gebuendelt ueber yf.download statt einzeln
    ueber kerzen(), brauchen aber dieselbe Zuordnung. Ohne sie rechneten
    die Halteraten und Puffer-Verteilungen fuer ASML weiter auf der
    Dollar-Reihe, waehrend der Tagesbericht in Euro rechnet - und ein Tief
    in Dollar ist keines in Euro, wenn der Wechselkurs dazwischenlaeuft.

    Angefragt wird beim Quellticker, abgelegt unter dem Namen.
    """
    zuordnung = {t: quelle(t) for t in tickers}
    for name, q in zuordnung.items():
        if q != name:
            print(f"  {name}: Kurse von {q} ({waehrung(name)})")
    return zuordnung


_MEM: dict[tuple, pd.DataFrame] = {}


def _pfad(ticker: str, period: str, auto_adjust: bool = False) -> str:
    sicher = "".join(c if c.isalnum() or c in "-_" else "_" for c in ticker)
    suffix = "_adj" if auto_adjust else ""
    return os.path.join(CACHE, f"v{CACHE_VERSION}_{sicher}_{period}{suffix}.csv")


def aufraeumen() -> None:
    """Cache-Dateien von frueheren Tagen oder Versionen entfernen."""
    if not os.path.isdir(CACHE):
        return
    heute = date.today().isoformat()
    for name in os.listdir(CACHE):
        pfad = os.path.join(CACHE, name)
        try:
            alt = date.fromtimestamp(os.path.getmtime(pfad)).isoformat()
            if alt != heute or not name.startswith(f"v{CACHE_VERSION}_"):
                os.remove(pfad)
        except OSError:
            pass


def leeren() -> None:
    """Cache vollstaendig verwerfen - fuer Tests."""
    _MEM.clear()
    shutil.rmtree(CACHE, ignore_errors=True)


def _aufbereiten(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < MINDESTKERZEN:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def kerzen(ticker: str, period: str = "400d", auto_adjust: bool = False) -> pd.DataFrame | None:
    """Tageskerzen fuer einen Ticker. None, wenn keine brauchbaren Daten.

    Reihenfolge: Arbeitsspeicher, dann Tagescache auf der Platte, dann
    Yahoo. Ein Fehlschlag wird als None gemerkt, damit ein toter Ticker
    nicht bei jedem Aufruf erneut abgefragt wird.

    auto_adjust=False ist die Voreinstellung und bleibt es fuer alle
    bisherigen Aufrufer (marktdaten.py, tiefs.py, phasen.py, historie.py,
    hochs.py, ruecksetzer.py) unveraendert. screener.py rechnete bisher
    mit auto_adjust=True (dividenden-/split-bereinigt) - beim Umzug auf
    diese Funktion (30.08.2026) bewusst NICHT stillschweigend
    vereinheitlicht, das waere eine Methodikaenderung, keine reine
    Code-Zusammenlegung. Beide Varianten leben nebeneinander im Cache
    (Dateiname mit "_adj"-Endung fuer die angepasste Reihe), sodass sie
    sich nicht gegenseitig ueberschreiben.
    """
    key = (ticker, period, auto_adjust)
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    # Ab hier zaehlt die Quelle, nicht der Name. Cache und Abruf laufen
    # unter dem Quellticker, damit zwei Namen auf dieselbe Reihe nicht
    # zwei Abrufe ausloesen.
    holen = quelle(ticker)
    if holen != ticker:
        print(f"  {ticker}: Kurse von {holen} ({waehrung(ticker)})")

    pfad = _pfad(holen, period, auto_adjust)
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {holen}: Cache unlesbar ({e}), hole neu")

    try:
        roh = yf.Ticker(holen).history(period=period, interval="1d",
                                       auto_adjust=auto_adjust)
    except Exception as e:
        print(f"  {holen}: Abruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _aufbereiten(roh)
    _MEM[key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {holen}: Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()


def kerzen_batch(tickers: list[str], period: str = "400d",
                  auto_adjust: bool = False) -> dict[str, pd.DataFrame]:
    """Tageskerzen fuer VIELE Ticker in einem Rutsch statt einzeln.

    Fuer screener.py entstanden (30.08.2026): das Skript braucht alle
    ~200 Werte auf einmal fuer die 10-Jahres-Historie zum Allzeithoch. Ein
    Abruf je Ticker ueber kerzen() waere hier falsch - erst recht ohne
    Cache-Treffer aus einem anderen Skript, weil kein anderes Skript mit
    demselben Zeitraum arbeitet. Genau das Problem, das kurse.py
    eigentlich verhindern soll (Laufzeit im 30-Minuten-Fenster,
    Rate-Limits bei Yahoo), waere durch einen naiven Umstieg auf
    kerzen() zurueckgekommen, nur diesmal in screener.py statt verteilt
    auf drei Skripte.

    Nutzt denselben Cache wie kerzen() - ein spaeterer einzelner
    kerzen()-Aufruf fuer denselben Ticker, Zeitraum und dieselbe
    auto_adjust-Einstellung liest den hier gefuellten Cache, und
    umgekehrt.

    Anders als kerzen() merkt sich das hier NICHT einzeln, welcher Ticker
    fehlgeschlagen ist - eine Batch-Anfrage soll selten laufen (einmal
    pro Skriptlauf ueber das ganze Universum), wiederholte Fehlschlaege
    sind dabei kein Problem.
    """
    ergebnis: dict[str, pd.DataFrame] = {}
    frisch: list[str] = []
    quelle_von = {t: quelle(t) for t in tickers}

    for t in tickers:
        key = (t, period, auto_adjust)
        if key in _MEM:
            wert = _MEM[key]
            if wert is not None:
                ergebnis[t] = wert.copy()
            continue
        pfad = _pfad(quelle_von[t], period, auto_adjust)
        if os.path.exists(pfad):
            try:
                if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                    df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                    if len(df) >= MINDESTKERZEN:
                        _MEM[key] = df
                        ergebnis[t] = df.copy()
                        continue
            except Exception as e:
                print(f"  {t}: Cache unlesbar ({e}), hole neu")
        frisch.append(t)

    quellticker = sorted({quelle_von[t] for t in frisch})
    roh_je_quelle: dict[str, pd.DataFrame] = {}
    chunk = 40
    for i in range(0, len(quellticker), chunk):
        batch = quellticker[i:i + chunk]
        try:
            data = yf.download(batch, period=period, interval="1d",
                                auto_adjust=auto_adjust, group_by="ticker",
                                threads=True, progress=False)
        except Exception as e:
            print(f"  ! Batch-Download fehlgeschlagen ({batch[0]}...): {e}")
            continue
        for q in batch:
            try:
                roh_je_quelle[q] = (data[q] if isinstance(data.columns, pd.MultiIndex)
                                     else data)
            except Exception:
                continue

    os.makedirs(CACHE, exist_ok=True)
    for t in frisch:
        q = quelle_von[t]
        df = _aufbereiten(roh_je_quelle.get(q))
        _MEM[(t, period, auto_adjust)] = df
        if df is not None:
            ergebnis[t] = df.copy()
            try:
                df.to_csv(_pfad(q, period, auto_adjust))
            except OSError as e:
                print(f"  {q}: Cache nicht schreibbar ({e})")
    return ergebnis


# ── Stundenkerzen ──────────────────────────────────────────────────
# Bewusst eine eigene Funktion statt eines interval-Parameters an
# kerzen(): die Stundenreihe hat andere Eigenschaften und darf die
# Tagesreihe nirgends versehentlich ersetzen.
#
#   - Yahoo liefert 1h nur rund zwei Jahre zurueck, nicht 400 Tage
#     plus Reserve wie bei 1d. Fuer Halteraten und Puffer-Verteilungen
#     taugt sie deshalb NICHT (siehe Gespraech vom 25.08.2026) - sie ist
#     ausschliesslich fuer den Blick auf den laufenden Tag gedacht.
#   - MINDESTKERZEN aus der Tageslogik passt nicht: ein einzelner
#     US-Handelstag hat rund 7 Stundenkerzen. Ein Tag mit Feiertag oder
#     verkuerztem Handel haette danach "keine Daten".
#
# Der Cache laeuft ueber denselben Tagesmechanismus wie die Tagesreihe,
# mit eigenem Praefix im Dateinamen.
STUNDEN_MINDESTKERZEN = 3


def _aufbereiten_stunden(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < STUNDEN_MINDESTKERZEN:
        return None
    # Zeitzone behalten waere ehrlicher, macht aber jeden Vergleich mit
    # der Tagesreihe zum Sonderfall. Stattdessen auf die Boersenzeit des
    # jeweiligen Wertes normalisiert und dann tz-frei - wie bei kerzen().
    df.index = pd.to_datetime(df.index)
    try:
        df.index = df.index.tz_localize(None)
    except TypeError:
        df.index = df.index.tz_convert(None)
    return df


def stundenkerzen(ticker: str, period: str = "5d", auto_adjust: bool = False) -> pd.DataFrame | None:
    """Stundenkerzen fuer einen Ticker. None, wenn keine brauchbaren Daten.

    Fuenf Handelstage reichen fuer den laufenden Tag samt Vergleich zu
    den Vortagen und halten die Antwort klein. Wer mehr braucht, gibt
    period ausdruecklich groesser an - Yahoo deckelt bei rund zwei Jahren.

    auto_adjust wie bei kerzen(): Voreinstellung False bleibt fuer
    bisherige Aufrufer unveraendert, screener.py ruft mit True auf, um
    sein bisheriges Verhalten zu erhalten (30.08.2026).
    """
    key = (ticker, period, "1h", auto_adjust)
    if key in _MEM:
        wert = _MEM[key]
        return None if wert is None else wert.copy()

    holen = quelle(ticker)
    pfad = _pfad(f"h_{holen}", period, auto_adjust)
    if os.path.exists(pfad):
        try:
            if date.fromtimestamp(os.path.getmtime(pfad)) == date.today():
                df = pd.read_csv(pfad, index_col=0, parse_dates=True)
                if len(df) >= STUNDEN_MINDESTKERZEN:
                    _MEM[key] = df
                    return df.copy()
        except Exception as e:
            print(f"  {holen}: Stunden-Cache unlesbar ({e}), hole neu")

    try:
        roh = yf.Ticker(holen).history(period=period, interval="1h",
                                       auto_adjust=auto_adjust)
    except Exception as e:
        print(f"  {holen}: Stundenabruf fehlgeschlagen ({e})")
        _MEM[key] = None
        return None

    df = _aufbereiten_stunden(roh)
    _MEM[key] = df
    if df is not None:
        os.makedirs(CACHE, exist_ok=True)
        try:
            df.to_csv(pfad)
        except OSError as e:
            print(f"  {holen}: Stunden-Cache nicht schreibbar ({e})")
    return None if df is None else df.copy()
