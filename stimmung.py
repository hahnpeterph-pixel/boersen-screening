"""Marktstimmung: VIX, VDAX-NEW und CNN Fear & Greed (Peter 25.09.2026).

NICHT als Kaufwert, sondern als Stimmungsbestimmung der Maerkte.

Zwei Aufgaben:

1. Taeglich (Schritt im Screening-Workflow): Reihen abrufen, in
   docs/stimmung.csv fortschreiben und die Stimmungszeile fuer die
   Tagesausgabe in docs/stimmung.md schreiben.

2. Mit --auswertung (eigener Workflow stimmung.yml, Sa frueh und bei
   Aenderung dieses Skripts): Wie gut hielten Tiefs je nach Stimmung am
   Tag des Tiefs? Grundlage docs/puffer_je_tief.csv.gz, dieselbe
   Halte-Definition wie heute.py (_haelt_flex): ein Puffer haelt, wenn
   benoetigt_atr <= Puffer, nur Faelle mit >= 63 beobachteten Tagen.
   WERTSPEZIFISCH (keine Pools): Vergleich ruhig gegen unruhig je Wert,
   danach erst die Zusammenfassung ueber die Werte.
   US-Werte gegen VIX und Fear & Greed, .DE-Werte gegen VDAX-NEW.

Quellen:
- VIX: Yahoo ^VIX.
- VDAX-NEW: Yahoo, Kuerzel nicht sicher bekannt - es werden mehrere
  Kandidaten probiert, der erste mit Daten gewinnt und wird in stimmung.md
  genannt. Letzter Rueckfall ist VSTOXX (europaeisch, nicht DAX).
- Fear & Greed: CNN-Datenschnittstelle hinter cnn.com/markets/fear-and-greed
  (keine offizielle API). Liefert nur rund ein Jahr rueckwirkend, deshalb
  wird die Reihe in stimmung.csv fortgeschrieben und nie gekuerzt.
  Faellt der Abruf aus, bleibt der gespeicherte Stand stehen.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import requests
import yfinance as yf

DOCS = "docs"
CSV = os.path.join(DOCS, "stimmung.csv")
MD = os.path.join(DOCS, "stimmung.md")
AUSW_MD = os.path.join(DOCS, "stimmung_auswertung.md")
AUSW_CSV = os.path.join(DOCS, "stimmung_halten.csv")
TIEFS = os.path.join(DOCS, "puffer_je_tief.csv.gz")

VIX = "^VIX"
VDAX_KANDIDATEN = ["^V1X", "V1X.DE", "^VDAX", "VDAX.DE", "^V2TX", "V2TX.DE"]
FG_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{start}"
FG_KOPF = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://edition.cnn.com/markets/fear-and-greed",
    "Origin": "https://edition.cnn.com",
}
START = "2018-01-01"
MELDUNGEN: list[str] = []


def melde(text: str) -> None:
    print(text)
    MELDUNGEN.append(text)

HALTE_FENSTER = 63
PUFFER = [1.0, 1.5, 2.0, 2.5, 3.0]
MIN_FAELLE = 10  # je Wert und Lage, sonst kein Vergleich

# Lagen. Feste Grenzen statt Quantilen, damit "ruhig" heute dasselbe
# bedeutet wie 2019. VDAX-NEW liegt ueblicherweise 2-3 Punkte ueber VIX.
LAGEN = {
    "vix":  [(0, 16, "ruhig"), (16, 22, "normal"), (22, 1e9, "unruhig")],
    "vdax": [(0, 18, "ruhig"), (18, 24, "normal"), (24, 1e9, "unruhig")],
    "fg":   [(0, 45, "Angst"), (45, 55, "neutral"), (55, 101, "Gier")],
    # Gemessene DAX-Schwankung (Rueckfall ohne VDAX-NEW) liegt niedriger als
    # die erwartete. Grenzen so gesetzt, dass die Anteile denen des VIX
    # entsprechen (ruhig 34 %, unruhig 26 % der Tage 2018-2026).
    "vdax_gem": [(0, 13, "ruhig"), (13, 19, "normal"), (19, 1e9, "unruhig")],
}
FG_TEXT = [(0, 25, "extreme Angst"), (25, 45, "Angst"), (45, 55, "neutral"),
           (55, 75, "Gier"), (75, 101, "extreme Gier")]
REIHENFOLGE = {"vix": ["ruhig", "normal", "unruhig"],
               "vdax": ["ruhig", "normal", "unruhig"],
               "fg": ["Angst", "neutral", "Gier"],
               "vdax_gem": ["ruhig", "normal", "unruhig"]}


def vdax_art(df: pd.DataFrame) -> str:
    q = df["vdax_quelle"].dropna().iloc[-1] if df["vdax_quelle"].notna().any() else ""
    return "vdax_gem" if str(q).startswith("gemessen") else "vdax"


def de(x, n=1):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    return f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def lage(wert, art):
    if wert is None or pd.isna(wert):
        return None
    for lo, hi, name in LAGEN[art]:
        if lo <= wert < hi:
            return name
    return None


def fg_text(wert):
    if wert is None or pd.isna(wert):
        return "–"
    for lo, hi, name in FG_TEXT:
        if lo <= wert < hi:
            return name
    return "–"


# ---------------------------------------------------------------- Abruf

def schluss(ticker: str) -> pd.Series | None:
    try:
        roh = yf.Ticker(ticker).history(start=START, interval="1d", auto_adjust=False)
    except Exception as e:  # noqa: BLE001
        melde(f"  {ticker}: Abruf fehlgeschlagen ({e})")
        return None
    if roh is None or roh.empty or "Close" not in roh:
        melde(f"  {ticker}: keine Daten")
        return None
    s = roh["Close"].dropna()
    s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
    s = s[~s.index.duplicated(keep="last")]
    if len(s) < 50:
        melde(f"  {ticker}: nur {len(s)} Kerzen - verworfen")
        return None
    melde(f"  {ticker}: {len(s)} Kerzen bis {s.index[-1].date()}")
    return s


STOOQ_KANDIDATEN = ["^vdax", "vdax", "^v1x", "v1x.de", "^vstoxx", "^v2tx"]


def stooq(sym: str) -> pd.Series | None:
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        r = requests.get(url, headers={"User-Agent": FG_KOPF["User-Agent"]}, timeout=30)
        if r.status_code != 200 or not r.text.startswith("Date"):
            melde(f"  Stooq {sym}: HTTP {r.status_code}, {r.text[:60]!r}")
            return None
        from io import StringIO
        d = pd.read_csv(StringIO(r.text), parse_dates=["Date"]).set_index("Date")["Close"].dropna()
    except Exception as e:  # noqa: BLE001
        melde(f"  Stooq {sym}: Abruf fehlgeschlagen ({e})")
        return None
    d = d[d.index >= START]
    if len(d) < 50:
        melde(f"  Stooq {sym}: nur {len(d)} Kerzen")
        return None
    melde(f"  Stooq {sym}: {len(d)} Kerzen bis {d.index[-1].date()}")
    return d


def dax_schwankung() -> pd.Series | None:
    """Rueckfall, wenn kein VDAX-NEW zu bekommen ist: gemessene Schwankung
    des DAX (Standardabweichung der Tagesrenditen ueber 21 Tage, auf das
    Jahr hochgerechnet, in Prozent). Gleiche Groessenordnung wie VDAX-NEW,
    aber rueckblickend statt erwartet - in stimmung.md so benannt."""
    try:
        roh = yf.Ticker("^GDAXI").history(start="2017-11-01", interval="1d", auto_adjust=False)
        c = roh["Close"].dropna()
        c.index = pd.to_datetime(c.index).tz_localize(None).normalize()
    except Exception as e:  # noqa: BLE001
        melde(f"  ^GDAXI: Abruf fehlgeschlagen ({e})")
        return None
    s = (np.log(c).diff().rolling(21).std() * np.sqrt(252) * 100).dropna()
    s = s[s.index >= START]
    melde(f"  DAX-Schwankung (gemessen, 21T): {len(s)} Tage bis {s.index[-1].date()}")
    return s if len(s) >= 50 else None


FG_HIST_URL = "https://raw.githubusercontent.com/whit3rabbit/fear-greed-data/main/fear-greed.csv"
# Stichproben aus Peters finhacker.cz-Ausdrucken (25.09.2026) zur Kontrolle.
FG_KONTROLLE = {"2021-02-23": 57, "2022-01-24": 23, "2022-05-12": 3,
                "2023-06-09": 76, "2024-08-02": 41, "2025-11-06": 24}


def fear_greed_historie() -> pd.Series | None:
    """Tageswerte ab 2011 (Sammlung whit3rabbit/fear-greed-data: bis
    29.01.2021 eingefrorene Altdaten, danach CNN). Die CNN-Schnittstelle
    selbst liefert nur rund ein Jahr; ohne diese Reihe waere die
    Auswertung auf 2025/26 beschraenkt."""
    try:
        r = requests.get(FG_HIST_URL, timeout=60)
        r.raise_for_status()
        from io import StringIO
        d = pd.read_csv(StringIO(r.text), parse_dates=["Date"]).set_index("Date")["Fear Greed"].dropna()
    except Exception as e:  # noqa: BLE001
        melde(f"  Fear & Greed Historie: Abruf fehlgeschlagen ({e})")
        return None
    d.index = pd.to_datetime(d.index).normalize()
    ok = [f"{t}: {d.get(pd.Timestamp(t), float('nan')):.0f} (PDF {w})" for t, w in FG_KONTROLLE.items()]
    melde(f"  Fear & Greed Historie: {len(d)} Tage {d.index[0].date()} bis {d.index[-1].date()}; Kontrolle " + ", ".join(ok))
    return d


def fear_greed() -> pd.Series | None:
    # Aelteres Startdatum als rund ein Jahr liefert HTTP 500 (25.09.2026,
    # mit 2018-01-01 getestet). Deshalb 360 Tage zurueck, dann ohne Datum.
    j = None
    start = (dt.date.today() - dt.timedelta(days=360)).isoformat()
    for url in (FG_URL.format(start=start), FG_URL.format(start="").rstrip("/")):
        try:
            r = requests.get(url, headers=FG_KOPF, timeout=30)
            if r.status_code != 200:
                melde(f"  Fear & Greed {url[-20:]}: HTTP {r.status_code}, Antwort: {r.text[:120]!r}")
                continue
            j = r.json()
            break
        except Exception as e:  # noqa: BLE001
            melde(f"  Fear & Greed: Abruf fehlgeschlagen ({e})")
    if j is None:
        return None
    punkte = (j.get("fear_and_greed_historical") or {}).get("data") or []
    werte = {}
    for p in punkte:
        try:
            tag = pd.Timestamp(dt.datetime.utcfromtimestamp(p["x"] / 1000).date())
            werte[tag] = float(p["y"])
        except (KeyError, TypeError, ValueError):
            continue
    aktuell = j.get("fear_and_greed") or {}
    try:
        tag = pd.Timestamp(pd.to_datetime(aktuell["timestamp"]).tz_localize(None).date())
        werte[tag] = float(aktuell["score"])
    except (KeyError, TypeError, ValueError, AttributeError):
        pass
    if not werte:
        melde(f"  Fear & Greed: Antwort ohne Werte, Schluessel {list(j)[:5]}")
        return None
    s = pd.Series(werte).sort_index()
    melde(f"  Fear & Greed: {len(s)} Tage bis {s.index[-1].date()}")
    return s


def fortschreiben() -> pd.DataFrame:
    alt = None
    if os.path.exists(CSV):
        alt = pd.read_csv(CSV, parse_dates=["datum"]).set_index("datum")

    neu = {}
    vix = schluss(VIX)
    if vix is not None:
        neu["vix"] = vix
    vdax_quelle = None
    for k in VDAX_KANDIDATEN:
        s = schluss(k)
        if s is not None:
            neu["vdax"] = s
            vdax_quelle = k
            break
    # Stooq am 25.09.2026 von GitHub aus nicht erreichbar (Timeout) - nicht mehr versucht.
    if vdax_quelle is None:
        s = dax_schwankung()
        if s is not None:
            neu["vdax"] = s
            vdax_quelle = "gemessen:^GDAXI"
    fg = fear_greed()
    hist = fear_greed_historie()
    if fg is not None and hist is not None:
        fg = fg.combine_first(hist)  # CNN direkt gewinnt
    elif hist is not None:
        fg = hist
    if fg is not None:
        neu["fg"] = fg

    df = pd.DataFrame(neu)
    if alt is not None:
        # Neuer Abruf gewinnt, gespeicherte Tage bleiben erhalten
        # (wichtig fuer Fear & Greed, das nur ein Jahr rueckwirkend liefert).
        df = df.combine_first(alt[[c for c in ("vix", "vdax", "fg") if c in alt]])
        if vdax_quelle is None and "vdax_quelle" in alt:
            vdax_quelle = alt["vdax_quelle"].dropna().iloc[-1] if alt["vdax_quelle"].notna().any() else None
    for c in ("vix", "vdax", "fg"):
        if c not in df:
            df[c] = np.nan
    df = df[["vix", "vdax", "fg"]].sort_index()
    df["vdax_quelle"] = vdax_quelle
    df.index.name = "datum"
    os.makedirs(DOCS, exist_ok=True)
    df.to_csv(CSV, float_format="%.2f")
    return df


# ---------------------------------------------------------------- Tageszeile

def _stand(s: pd.Series, tage: int = 5):
    s = s.dropna()
    if s.empty:
        return None, None, None
    jetzt = s.iloc[-1]
    vor = s.iloc[-1 - tage] if len(s) > tage else None
    return jetzt, (None if vor is None else jetzt - vor), s.index[-1]


def tageszeile(df: pd.DataFrame) -> str:
    teile = []
    v, d, t = _stand(df["vix"])
    if v is not None:
        teile.append(f"VIX {de(v)} ({lage(v, 'vix')}, 5T {'+' if d and d > 0 else ''}{de(d)}, {t:%d.%m.})")
    q = df["vdax_quelle"].dropna().iloc[-1] if df["vdax_quelle"].notna().any() else None
    v, d, t = _stand(df["vdax"])
    if v is not None:
        name = ("VSTOXX" if q and ("V2TX" in q.upper() or "VSTOXX" in q.upper())
                else "DAX-Schwankung gemessen" if q and q.startswith("gemessen") else "VDAX-NEW")
        teile.append(f"{name} {de(v)} ({lage(v, vdax_art(df))}, 5T {'+' if d and d > 0 else ''}{de(d)}, {t:%d.%m.})")
    v, d, t = _stand(df["fg"], 1)
    if v is not None:
        teile.append(f"Fear & Greed {de(v, 0)} ({fg_text(v)}, Vortag {'+' if d and d > 0 else ''}{de(d, 0)}, {t:%d.%m.})")
    return "Stimmung: " + (" · ".join(teile) if teile else "keine Daten")


def schreibe_md(df: pd.DataFrame) -> None:
    q = df["vdax_quelle"].dropna().iloc[-1] if df["vdax_quelle"].notna().any() else "keine"
    zeilen = [
        "# Marktstimmung",
        "",
        f"Stand Abruf: {dt.datetime.utcnow():%d.%m.%Y %H:%M} UTC",
        "",
        f"**{tageszeile(df)}**",
        "",
        "Lagen: VIX ruhig < 16 · normal 16–22 · unruhig > 22 | "
        "VDAX-NEW ruhig < 18 · normal 18–24 · unruhig > 24 (gemessene DAX-Schwankung: < 13 · 13–19 · > 19) | "
        "Fear & Greed 0–25 extreme Angst · 25–45 Angst · 45–55 neutral · 55–75 Gier · 75–100 extreme Gier.",
        "",
        f"Quellen: VIX = Yahoo ^VIX · VDAX = Yahoo {q} · Fear & Greed = CNN.",
        "",
        "Nur Stimmung, kein Kaufsignal. Ob die Lage fuer unsere Tiefs etwas aussagt: siehe stimmung_auswertung.md.",
        "",
        "| Tag | VIX | VDAX | F&G |",
        "|---|---|---|---|",
    ]
    for tag, z in df.tail(10).iloc[::-1].iterrows():
        zeilen.append(f"| {tag:%d.%m.%Y} | {de(z['vix'])} | {de(z['vdax'])} | {de(z['fg'], 0)} |")
    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")


# ---------------------------------------------------------------- Auswertung

def _haelt(benoetigt: np.ndarray, puffer: float):
    if len(benoetigt) == 0:
        return np.nan
    return float((benoetigt <= puffer + 1e-9).mean() * 100)


def auswertung(df: pd.DataFrame) -> None:
    tiefs = pd.read_csv(TIEFS, usecols=["ticker", "datum", "position", "beobachtet", "benoetigt_atr"],
                        parse_dates=["datum"])
    tiefs = tiefs[~tiefs["ticker"].str.contains(r"=|\^", regex=True)]
    tiefs = tiefs[(tiefs["beobachtet"] >= HALTE_FENSTER) & tiefs["benoetigt_atr"].notna()]
    tiefs["eu"] = tiefs["ticker"].str.endswith(".DE") | tiefs["ticker"].str.endswith(".AS")
    tiefs["pos"] = tiefs["position"].clip(upper=3).astype(int)  # 1, 2, 3+

    # Stimmung am Tag des Tiefs (oder letzter Handelstag davor).
    reihen = {}
    for art in ("vix", "vdax", "fg"):
        s = df[art].dropna().sort_index()
        if s.empty:
            continue
        st = tiefs[["datum"]].copy().reset_index()
        st = st.sort_values("datum")
        m = pd.merge_asof(st, s.rename("wert").reset_index().rename(columns={"datum": "tag"}),
                          left_on="datum", right_on="tag", direction="backward",
                          tolerance=pd.Timedelta(days=5))
        reihen[art] = m.set_index("index")["wert"]
    for art, w in reihen.items():
        tiefs[art] = w

    zuordnung = [("vix", ~tiefs["eu"], "US-Werte gegen VIX"),
                 ("vdax", tiefs["eu"], "Deutsche Werte gegen VDAX-NEW" if vdax_art(df) == "vdax" else "Deutsche Werte gegen gemessene DAX-Schwankung (kein VDAX-NEW verfuegbar)"),
                 ("fg", ~tiefs["eu"], "US-Werte gegen Fear & Greed")]

    csv_zeilen = []
    md = ["# Stimmung und Tiefs – Auswertung", "",
          f"Stand: {dt.datetime.utcnow():%d.%m.%Y %H:%M} UTC. Grundlage: puffer_je_tief.csv.gz, "
          f"nur Tiefs mit mindestens {HALTE_FENSTER} beobachteten Tagen. "
          "Haelt = KO faellt in 63 Tagen nicht (benoetigt_atr <= Puffer), wie in heute.py.", "",
          "Lesart: Zuerst je Wert verglichen (unruhig gegen ruhig bzw. Angst gegen Gier), "
          f"nur Werte mit je mindestens {MIN_FAELLE} Faellen in beiden Lagen. "
          "Die Gesamtzeile ist nur zur Orientierung.", ""]

    for art, maske, titel in zuordnung:
        if art not in tiefs:
            md += [f"## {titel}", "", "Keine Stimmungsdaten.", ""]
            continue
        t = tiefs[maske & tiefs[art].notna()].copy()
        art_l = vdax_art(df) if art == "vdax" else art
        t["lage"] = t[art].map(lambda v: lage(v, art_l))
        lagen = REIHENFOLGE[art_l]
        tief_l, hoch_l = lagen[0], lagen[-1]
        if art == "fg":
            tief_l, hoch_l = "Gier", "Angst"  # Angst ist die "unruhige" Seite
        von = t["datum"].min()
        bis = t["datum"].max()
        md += [f"## {titel}", "",
               f"{len(t)} Tiefs, {t['ticker'].nunique()} Werte, Zeitraum "
               f"{'–' if pd.isna(von) else f'{von:%m/%Y}'} bis {'–' if pd.isna(bis) else f'{bis:%m/%Y}'}.", ""]

        # 1) Gesamtuebersicht
        md += ["| Lage | Faelle | haelt 1,5 ATR | haelt 2 ATR | haelt 3 ATR | Median benoetigt |",
               "|---|---|---|---|---|---|"]
        for l in lagen:
            b = t.loc[t["lage"] == l, "benoetigt_atr"].to_numpy(float)
            md.append(f"| {l} | {len(b)} | {de(_haelt(b, 1.5), 0)} % | {de(_haelt(b, 2.0), 0)} % | "
                      f"{de(_haelt(b, 3.0), 0)} % | {de(np.median(b) if len(b) else np.nan, 2)} ATR |")
        md.append("")

        # 2) Wertspezifisch
        diffs = {p: [] for p in PUFFER}
        med_diff = []
        je_wert = []
        for tick, g in t.groupby("ticker"):
            a = g.loc[g["lage"] == tief_l, "benoetigt_atr"].to_numpy(float)
            b = g.loc[g["lage"] == hoch_l, "benoetigt_atr"].to_numpy(float)
            for pos in (1, 2, 3):
                for l in lagen:
                    x = g.loc[(g["lage"] == l) & (g["pos"] == pos), "benoetigt_atr"].to_numpy(float)
                    if len(x):
                        csv_zeilen.append({"reihe": art, "ticker": tick, "tief": pos if pos < 3 else "3+",
                                           "lage": l, "faelle": len(x),
                                           **{f"haelt_{p:g}_pct": round(_haelt(x, p), 1) for p in PUFFER},
                                           "median_benoetigt_atr": round(float(np.median(x)), 3)})
            if len(a) >= MIN_FAELLE and len(b) >= MIN_FAELLE:
                for p in PUFFER:
                    diffs[p].append(_haelt(b, p) - _haelt(a, p))
                med_diff.append(float(np.median(b) - np.median(a)))
                je_wert.append((tick, len(a), len(b), _haelt(a, 2.0), _haelt(b, 2.0)))

        n = len(je_wert)
        md += [f"**Je Wert ({hoch_l} gegen {tief_l}), {n} Werte vergleichbar:**", ""]
        if n:
            md += ["| Puffer | Median Unterschied haelt | Werte schlechter | Werte besser |",
                   "|---|---|---|---|"]
            for p in PUFFER:
                d = np.array(diffs[p])
                md.append(f"| {de(p, 2)} ATR | {'+' if np.median(d) > 0 else ''}{de(float(np.median(d)), 1)} Pp | "
                          f"{int((d < -0.5).sum())} | {int((d > 0.5).sum())} |")
            md += ["", f"Benoetigter Puffer ({hoch_l} minus {tief_l}), Median ueber die Werte: "
                   f"{'+' if np.median(med_diff) > 0 else ''}{de(float(np.median(med_diff)), 2)} ATR.", ""]
            je_wert.sort(key=lambda x: x[4] - x[3])
            md += [f"Staerkste Unterschiede bei 2 ATR (haelt {tief_l} → {hoch_l}):", ""]
            for tick, na, nb, ha, hb in je_wert[:5] + je_wert[-3:]:
                md.append(f"- {tick}: {de(ha, 0)} % ({na}) → {de(hb, 0)} % ({nb})")
            md.append("")
        else:
            md += ["Zu wenige Faelle je Wert fuer einen Vergleich.", ""]

    pd.DataFrame(csv_zeilen).to_csv(AUSW_CSV, index=False)
    md += ["Je Wert, Tief-Position (1, 2, 3+) und Lage: docs/stimmung_halten.csv "
           "(fuer die Kaufvorlage: \"Bei heutiger Lage hielt Tief N dieses Werts x %\")."]
    with open(AUSW_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Auswertung geschrieben: {AUSW_MD}, {AUSW_CSV} ({len(csv_zeilen)} Zeilen)")


LOG = os.path.join(DOCS, "stimmung_log.txt")


def main() -> int:
    """Jeder Teil einzeln abgesichert; Fehler landen mit Traceback in
    docs/stimmung_log.txt (wird mit gespeichert), damit sie ohne Zugang
    zu den Actions-Protokollen lesbar sind."""
    import traceback
    ap = argparse.ArgumentParser()
    ap.add_argument("--auswertung", action="store_true")
    ap.add_argument("--ohne-abruf", action="store_true", help="nur gespeicherte stimmung.csv nutzen")
    args = ap.parse_args()
    log = [f"Lauf {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC, pandas {pd.__version__}, "
           f"yfinance {getattr(yf, '__version__', '?')}"]
    fehler = False
    df = None
    try:
        if not args.ohne_abruf:
            fortschreiben()
        # Immer aus der Datei lesen: gleiche Datentypen wie im getesteten Pfad.
        log.extend(MELDUNGEN)
        df = pd.read_csv(CSV, parse_dates=["datum"]).set_index("datum")
        log.append(f"stimmung.csv: {len(df)} Tage, VIX {df['vix'].notna().sum()}, "
                   f"VDAX {df['vdax'].notna().sum()}, F&G {df['fg'].notna().sum()}")
        schreibe_md(df)
        log.append(tageszeile(df))
        print(tageszeile(df))
    except Exception:  # noqa: BLE001
        fehler = True
        log.append("FEHLER Abruf/Tageszeile:\n" + traceback.format_exc())
    if args.auswertung and df is not None:
        try:
            auswertung(df)
            log.append("Auswertung geschrieben.")
        except Exception:  # noqa: BLE001
            fehler = True
            log.append("FEHLER Auswertung:\n" + traceback.format_exc())
    os.makedirs(DOCS, exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
