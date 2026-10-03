"""
kerzen.py - Rohkerzen Stunde / Woche / Monat fuer die Kaufvorlage ohne Charts.
Angelegt 28.09.2026 (Peter: "so bauen, dass wir die Qualitaet gerne auch noch
hochfahren koennen, ohne dass wir die Charts kuenftig benoetigen").

Bisher lagen im Repo nur Tageskerzen (kursverlauf*.csv seit 23.03.2026) und
20 Jahre Schlusskurse (markthistorie.csv.gz). Stunden-, Wochen- und Monats-
kerzen musste Peter als Chartbild schicken. Diese Datei legt sie als Zahlen ab.

Aufruf:
  python kerzen.py --stunde   Stundenkerzen der letzten Handelstage, je Tag eine
                              Datei docs/kerzen/stunde/JJJJ-MM-TT.csv.gz.
                              Nur neue oder geaenderte Tage werden geschrieben,
                              Tage aelter als STUNDE_TAGE Handelstage geloescht
                              (haelt das Repo klein: ~30 KB je Tag statt eine
                              grosse Datei, die taeglich komplett neu kaeme).
  python kerzen.py --lang     Wochen- und Monatskerzen so lang wie verfuegbar, Tageskerzen ab 2005 (seit 28.09.2026).
                              Bis 31.12.2025 in *_archiv.csv.gz (einmalig, nur
                              neu mit --neu), ab 2026 in woche.csv.gz / monat.csv.gz.

Spalten: ticker, zeit (UTC bei Stunden, Wochen-/Monatsbeginn sonst),
o, h, l, c, v. Nur Aktien (wie unterstuetzungen.py), keine Positionsdaten.
Laeuft mit continue-on-error: ein Yahoo-Aussetzer darf nichts anderes kippen.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf
import kurse

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
KZ = os.path.join(DOCS, "kerzen")
STD = os.path.join(KZ, "stunde")
STUNDE_TAGE = 30          # so viele Handelstage Stundenkerzen bleiben liegen
STUNDE_NEU = 3            # die juengsten 3 Tage werden bei jedem Lauf neu geschrieben
ARCHIV_BIS = "2025-12-31"
TAG_AB = "2005-01-01"      # Tageskerzen (OHLCV) ab hier, fuer Kennzahlen wie Stochastik, MFI, Kerzenmuster
BATCH = 40
SPALTEN = ["ticker", "zeit", "o", "h", "l", "c", "v"]


def _tickers() -> list[str]:
    m = pd.read_csv(os.path.join(DOCS, "marktdaten.csv"))
    m = m[m["art"] == "Aktie"] if "art" in m.columns else m
    return sorted(t for t in m["ticker"] if isinstance(t, str))


def _laden(tickers, period, interval) -> pd.DataFrame:
    """Batch-Download als lange Tabelle (SPALTEN). Fehlende Werte fehlen einfach."""
    teile = []
    for i in range(0, len(tickers), BATCH):
        teil = tickers[i:i + BATCH]
        try:
            d = yf.download(teil, period=period, interval=interval, auto_adjust=False,
                            group_by="ticker", threads=True, progress=False, ignore_tz=(interval != "1h"))
        except Exception as exc:  # noqa: BLE001
            print(f"  ! Abruf {interval} {teil[0]}..: {exc}")
            continue
        for t in teil:
            try:
                x = d[t] if isinstance(d.columns, pd.MultiIndex) else d
            except KeyError:
                continue
            x = x.dropna(subset=["Open", "High", "Low", "Close"])
            if interval != "1h":   # 03.10.2026: Yahoo-Platzhalter (O=H=L=C, Volumen 0) verwerfen, unlogische Kerzen bereinigen
                x = kurse._platzhalter_weg(x, letzte_behalten=False)
            if not len(x):
                continue
            idx = x.index
            if interval == "1h":
                # UTC (28.09.2026): yfinance rechnet einen gemischten Abruf in EINE Zeitzone um
                # (Xetra stand dann in New Yorker Zeit). UTC ist eindeutig; die Kaufvorlage
                # rechnet je Boerse in Ortszeit zurueck. Ohne Zeitzone = schon UTC.
                zeit = (idx.tz_convert("UTC").tz_localize(None) if idx.tz is not None else idx).strftime("%Y-%m-%d %H:%M")
            else:
                zeit = (idx.tz_localize(None) if idx.tz is not None else idx).strftime("%Y-%m-%d")
            teile.append(pd.DataFrame({
                "ticker": t, "zeit": zeit,
                "o": x["Open"].round(4).values, "h": x["High"].round(4).values,
                "l": x["Low"].round(4).values, "c": x["Close"].round(4).values,
                "v": x["Volume"].fillna(0).astype("int64").values}))
    return pd.concat(teile, ignore_index=True) if teile else pd.DataFrame(columns=SPALTEN)


def _mit_kursverlauf(df: pd.DataFrame) -> pd.DataFrame:
    """03.10.2026: Fuer die Tage, die docs/kursverlauf* fuehrt (rund 6 Monate), gilt deren Kerze - dort sind
    Platzhalter bereits aus Stundenkerzen ersetzt (kurse._loecher_fuellen). Aeltere Platzhalter bleiben
    verworfen (fehlender Tag statt falscher Kerze)."""
    try:
        K = {k: pd.read_csv(os.path.join(DOCS, f"kursverlauf{s}.csv"), index_col=0)
             for k, s in (("o", "_eroeffnung"), ("h", "_hoch"), ("l", "_tief"), ("c", ""), ("v", "_volumen"))}
    except Exception as exc:  # noqa: BLE001
        print(f"  ! kursverlauf nicht lesbar ({exc}) - Tageskerzen ohne Abgleich")
        return df
    lang = pd.concat({k: d.stack() for k, d in K.items()}, axis=1).reset_index()
    lang.columns = ["ticker", "zeit", "o", "h", "l", "c", "v"]
    lang = lang.dropna(subset=["o", "h", "l", "c"])
    lang = lang[~((lang.o == lang.h) & (lang.h == lang.l) & (lang.l == lang.c) & (lang.v.fillna(0) == 0))]   # nie Platzhalter uebernehmen
    lang = lang[lang.ticker.isin(set(df.ticker))]
    lang["v"] = lang["v"].fillna(0).astype("int64")
    ab = lang.zeit.min()
    df = pd.concat([df[df.zeit < ab], df[(df.zeit >= ab) & ~df.set_index(["ticker", "zeit"]).index.isin(
        lang.set_index(["ticker", "zeit"]).index)], lang], ignore_index=True)
    return df[SPALTEN]


def _schreiben(df: pd.DataFrame, pfad: str) -> bool:
    """Schreibt nur, wenn sich der Inhalt geaendert hat (spart Repo-Groesse)."""
    df = df.sort_values(["ticker", "zeit"]).reset_index(drop=True)
    if os.path.exists(pfad):
        try:
            alt = pd.read_csv(pfad, dtype={"ticker": str, "zeit": str})
            if len(alt) == len(df) and alt.round(4).equals(df.round(4)):
                return False
        except Exception:  # noqa: BLE001
            pass
    df.to_csv(pfad, index=False, compression={"method": "gzip", "mtime": 0})
    return True


def stunde() -> None:
    os.makedirs(STD, exist_ok=True)
    tick = _tickers()
    print(f"Stundenkerzen fuer {len(tick)} Werte ...")
    df = _laden(tick, "1mo", "1h")
    if df.empty:
        print("  keine Stundenkerzen erhalten - nichts geschrieben")
        return
    # Handelstag in Boersen-Ortszeit (UTC-Datum waere fuer alle hier gehandelten Boersen gleich)
    df["tag"] = df.zeit.str[:10]
    tage = sorted(df.tag.unique())
    vorhanden = sorted(f[:10] for f in os.listdir(STD) if f.endswith(".csv.gz"))
    neu = 0
    for tg in tage:
        # heutiger unvollstaendiger Tag wird beim naechsten Lauf ueberschrieben
        if tg in vorhanden and tg not in tage[-STUNDE_NEU:]:
            continue
        if _schreiben(df[df.tag == tg][SPALTEN], os.path.join(STD, f"{tg}.csv.gz")):
            neu += 1
    alle = sorted(f[:10] for f in os.listdir(STD) if f.endswith(".csv.gz"))
    weg = alle[:-STUNDE_TAGE] if len(alle) > STUNDE_TAGE else []
    for tg in weg:
        os.remove(os.path.join(STD, f"{tg}.csv.gz"))
    print(f"  {len(df)} Stundenkerzen, {df.ticker.nunique()} Werte, Tage {tage[0]} bis {tage[-1]}; "
          f"geschrieben {neu}, geloescht {len(weg)} - {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC")


def lang(neu: bool = False) -> None:
    os.makedirs(KZ, exist_ok=True)
    tick = _tickers()
    for name, iv in (("woche", "1wk"), ("monat", "1mo"), ("tag", "1d")):
        print(f"{name.capitalize()}(es)kerzen fuer {len(tick)} Werte ...")
        df = _laden(tick, "max", iv)
        if name == "tag":   # 28.09.2026: Tageskerzen mit Hoch/Tief/Volumen ab 2005 (Kennzahl-Auswertung je Wert)
            df = df[df.zeit >= TAG_AB]
            df = _mit_kursverlauf(df)   # 03.10.2026: reparierte Tage aus docs/kursverlauf* uebernehmen
        if df.empty:
            print(f"  keine {name.capitalize()}nkerzen erhalten")
            continue
        arch = os.path.join(KZ, f"{name}_archiv.csv.gz")
        if neu or not os.path.exists(arch):
            _schreiben(df[df.zeit <= ARCHIV_BIS], arch)
            print(f"  Archiv geschrieben: {(df.zeit <= ARCHIV_BIS).sum()} Kerzen")
        else:   # 03.10.2026: bestehendes Archiv von Yahoo-Platzhaltern befreien (O=H=L=C, Volumen 0), unlogische Kerzen bereinigen
            a = pd.read_csv(arch, dtype={"ticker": str, "zeit": str})
            platz = (a.o == a.h) & (a.h == a.l) & (a.l == a.c) & (a.v == 0)
            a = a[~platz].copy()
            a["h"], a["l"] = a[["o", "h", "l", "c"]].max(axis=1), a[["o", "h", "l", "c"]].min(axis=1)
            if _schreiben(a[SPALTEN], arch):
                print(f"  Archiv bereinigt: {int(platz.sum())} Platzhalter entfernt")
        akt = df[df.zeit > ARCHIV_BIS]
        _schreiben(akt, os.path.join(KZ, f"{name}.csv.gz"))
        print(f"  {name}: {df.ticker.nunique()} Werte, ab {df.zeit.min()}, aktuell {len(akt)} Kerzen")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--stunde" in a:
        stunde()
    if "--lang" in a:
        lang(neu="--neu" in a)
    if not a:
        print(__doc__)
