"""
verkauf.py - Verkaufs-Check, Stufe 1: 7-Jahres-Auswertung je Wert.

PARALLELLAUF (Peter 24.09.2026), eigene Dateien unter docs/verkauf/, aendert
nichts am bestehenden Screening. Nutzt boden.py nur lesend (Kurse laden,
Pruefttage, ATR, RSI).

LEITFRAGE (Peter): Ein Wert im Depot macht ein neues Hoch. Kommt nur ein
kleiner Ruecksetzer und es geht weiter hoch (halten) - oder eine richtige
Korrektur, die den Gewinn wieder auffrisst (verkaufen)? "Richtig korrigieren
heisst, dass wir schon ein ganzes Stueck in den Gewinn gelaufen sind und mit
der Korrektur den ganzen Gewinn quasi wieder verlieren. Wenn ich ganz am
Anfang stecke, ist es was anderes."

AUFBAU
Kauf = jeder Pruefttag aus boden.py mit Tief >= 2 und RSI < 50 (die Technik
von Block 1), Einstieg = Schluss, ATR des Kauftags.
Entscheidungspunkt = jeder Tag innerhalb von 63 Handelstagen nach dem Kauf,
an dem das hoechste Hoch seit Kauf hoechstens 3 Tage zurueckliegt (wie beim
Ausstiegsalarm 187) und der Anstieg bis dahin mindestens 1 ATR betraegt.
Ergebnis ab dem Entscheidungspunkt (hoechstens 63 Handelstage):
  ganz_weg  Kurs faellt bis auf den Einstieg, BEVOR ein neues Hoch kommt
  halb_weg  Kurs gibt die Haelfte des Anstiegs ab, BEVOR ein neues Hoch kommt
  (am selben Tag neues Hoch und Tief darunter: zaehlt als Rueckfall)
Lauf-Stand = Anstieg bis zum Hoch geteilt durch den ueblichen Anstieg dieses
Werts (Median Chance A aus boden.py): frueh < 0,5 · mittel 0,5-1 ·
weit 1-1,5 · sehr weit > 1,5.

MERKMALE am Entscheidungstag (nur Vergangenheit): rote Kerze, rote Kerze mit
ueberdurchschnittlichem Volumen, Alarm 187 (Schluss > 3 ATR ueber Bezugstief,
Hoch seit Kauf in den letzten 3 Tagen, rote Kerze), RSI hoch gegen fruehere
Hochs des Werts, weit ueber EMA50 gegen fruehere Hochs, schneller Anstieg,
weit gelaufen (>= ueblicher Anstieg), Einstieg mit 2+ Boden-Punkten.

PRUEFUNG je Wert (keine Pools), 2019-2022 / ab 2023, Stoppregel 8 Pp.
Keine Positionsdaten im Repo (E58) - die Anwendung aufs Depot passiert lokal.

Stufe 2 (24.09.2026): Renditetest der Verkaufsregeln (Halten, Ruecksetzer T,
Alarm 187, Nachlauf 25/33/40 %), siehe handel().

Aufruf: python verkauf.py [--jahre 7] [--nur AAPL,MSFT]
"""

from __future__ import annotations

import gzip
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import boden

BASE = Path(__file__).resolve().parent
AUS = BASE / "docs" / "verkauf"
FENSTER = 63
MIN_ANSTIEG = 1.0        # ATR - darunter ist noch kein Gewinn zu sichern
HOCH_ALTER = 2           # Hoch hoechstens 3 Tage alt (heute, gestern, vorgestern)
ALARM_ATR = 3.0          # Alarm 187
RANG_HOCH = 0.7
MIN_VOR = 5
MIN_FAELLE = 10
STOPP_PP = 8.0
TEILUNG = pd.Timestamp("2023-01-01")
RUECKGABE_KLASSEN = ((-1.0, 0.1), (0.1, 0.25), (0.25, 0.4), (0.4, 9.0))
BAENDER = ((0.0, 0.5, "frueh"), (0.5, 1.0, "mittel"), (1.0, 1.5, "weit"), (1.5, 99.0, "sehr weit"))

MERKMALE = {   # Schluessel: (kurz, Erklaerung)
    "rot": ("Rote Kerze", "Schluss unter Eroeffnung am Entscheidungstag"),
    "rot_vol": ("Rot + Volumen", "Rote Kerze mit ueberdurchschnittlichem Volumen (20-Tage-Schnitt)"),
    "alarm187": ("Alarm 187", "Schluss > 3 ATR ueber Bezugstief, Hoch seit Kauf <= 3 Tage alt, rote Kerze"),
    "hoch_heute": ("Hoch heute", "Das Hoch seit Kauf ist am Entscheidungstag selbst"),
    "rsi_hoch": ("RSI hoch", "RSI ueber dem RSI an 7 von 10 frueheren Hochs des Werts"),
    "ema_weit": ("Weit ueber EMA50", "Abstand zur EMA50 groesser als an 7 von 10 frueheren Hochs"),
    "schnell": ("Schneller Anstieg", "Anstieg je Tag mehr als 1,5x so schnell wie ueblich"),
    "boden2": ("Kauf mit 2+ Punkten", "Einstieg hatte mind. 2 Boden-Punkte"),
}
ZIELE = {"ganz_weg": "Gewinn ganz weg", "halb_weg": "halber Gewinn weg"}


def band(r: float) -> str:
    for lo, hi, name in BAENDER:
        if lo <= r < hi:
            return name
    return "sehr weit"


def rang(wert: float, frueher: np.ndarray) -> float:
    if not np.isfinite(wert) or len(frueher) < MIN_VOR:
        return np.nan
    return float(np.mean(frueher < wert))


def punkte_je_wert(ticker: str, df: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    zeilen, info = boden.pruefttage(ticker, df)
    t = info.get("t_atr")
    if not zeilen or t is None:
        return [], []
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    n = len(df)
    O, H, L, C = (df[k].values.astype(float) for k in ("Open", "High", "Low", "Close"))
    V = df["Volume"].values.astype(float) if "Volume" in df.columns else np.full(n, np.nan)
    V = np.where(V > 0, V, np.nan)
    a = boden.atr(df)
    r = boden.rsi(df)
    ema50 = df["Close"].ewm(span=50, adjust=False).mean().values
    vs = pd.Series(V).shift(1).rolling(boden.VOL_TAGE, min_periods=boden.VOL_TAGE).mean().values
    idx = {f"{d:%Y-%m-%d}": i for i, d in enumerate(df.index)}

    # Fruehere Hochs (Zickzack mit T) fuer RSI- und EMA-Vergleich; bekannt ab
    # dem Tag, an dem die folgende Korrektur bestaetigt war (konservativ).
    _, _, _, korr = boden.zickzack(df, a, t)
    h_i = np.array([k["hoch_i"] for k in korr], dtype=int)
    h_am = np.array([k["am"] for k in korr], dtype=int)
    h_rsi = r[h_i] if len(h_i) else np.array([])
    h_ema = ((C[h_i] - ema50[h_i]) / a[h_i]) if len(h_i) else np.array([])

    ca = np.array([z["chance_a"] for z in zeilen if np.isfinite(z.get("chance_a", np.nan))])
    ta = np.array([z["tage_a"] for z in zeilen if np.isfinite(z.get("tage_a", np.nan))])
    typ_anstieg = float(np.median(ca)) if len(ca) else np.nan
    typ_tempo = (typ_anstieg / float(np.median(ta))) if len(ta) and np.median(ta) > 0 else np.nan

    aus = []
    for z in zeilen:
        if not (z["tief_ab_2"] == 1 and z["rsi_unter_50"] == 1):
            continue
        e = idx.get(z["datum"])
        if e is None:
            continue
        ce, a0, bez = C[e], a[e], z["bezugstief"]
        if not (np.isfinite(a0) and a0 > 0):
            continue
        hmax, hmax_i = -np.inf, -1
        for k in range(e + 1, min(n, e + 1 + FENSTER)):
            if H[k] > hmax:
                hmax, hmax_i = H[k], k
            anstieg = (hmax - ce) / a0
            if anstieg < MIN_ANSTIEG or k - hmax_i > HOCH_ALTER or k + FENSTER >= n:
                continue
            ganz = halb = 0
            grenze_halb = ce + 0.5 * (hmax - ce)
            for j in range(k + 1, k + 1 + FENSTER):
                if L[j] <= grenze_halb:
                    halb = 1
                if L[j] <= ce:
                    ganz = 1
                    break
                if H[j] > hmax:
                    break
            ak = a[k]
            fertig = h_am <= k
            rot = C[k] < O[k]
            vr = V[k] / vs[k] if np.isfinite(V[k]) and np.isfinite(vs[k]) else np.nan
            r_rel = anstieg / typ_anstieg if np.isfinite(typ_anstieg) and typ_anstieg > 0 else np.nan
            tempo = anstieg / max(hmax_i - e, 1)
            rsi_r = rang(r[k], h_rsi[fertig])
            ema_r = rang((C[k] - ema50[k]) / ak, h_ema[fertig])
            aus.append({
                "ticker": ticker, "kauf": z["datum"], "datum": f"{df.index[k]:%Y-%m-%d}",
                "tage_seit_kauf": k - e, "anstieg_atr": round(anstieg, 3),
                # Wie viel vom Anstieg am Schluss des Entscheidungstags schon
                # wieder abgegeben ist (0 = Schluss am Hoch, 1 = am Einstieg).
                "rueckgabe": round((hmax - C[k]) / (hmax - ce), 4),
                "anstieg_rel": round(r_rel, 3) if np.isfinite(r_rel) else np.nan,
                "band": band(r_rel) if np.isfinite(r_rel) else "",
                "ganz_weg": ganz, "halb_weg": halb,
                "rot": float(rot),
                "rot_vol": float(rot and vr >= 1.0) if np.isfinite(vr) else np.nan,
                "alarm187": float(rot and (C[k] - bez) / ak > ALARM_ATR),
                "hoch_heute": float(hmax_i == k),
                "rsi_hoch": float(rsi_r >= RANG_HOCH) if np.isfinite(rsi_r) else np.nan,
                "ema_weit": float(ema_r >= RANG_HOCH) if np.isfinite(ema_r) else np.nan,
                "schnell": (float(tempo > 1.5 * typ_tempo) if np.isfinite(typ_tempo) else np.nan),
                "weit_gelaufen": float(r_rel >= 1.0) if np.isfinite(r_rel) else np.nan,
                "boden2": float(z["punkte"] >= 2),
            })
    return aus, rendite_je_wert(ticker, df, zeilen, t, typ_anstieg)


# ── Renditetest (Stufe 2, Peter 24.09.2026) ─────────────────────────

HALTE_MAX = 126          # Handelstage, rund ein halbes Jahr - dann Verkauf zum Schluss
PUFFER_TEST = (2.0, 3.0) # KO = Bezugstief minus Puffer x ATR des Kauftags
STRATEGIEN = {
    "halten": "Halten bis Knock-out oder 126 Tage",
    "ruecksetzer_t": "Verkauf beim Ruecksetzer um T ATR vom Hoch (Chance A)",
    "alarm187": "Verkauf zum Schluss am ersten Tag mit Alarm 187",
    "nachlauf25": "Nachlauf: ab ueblichem Anstieg Verkauf, wenn 25 % des Anstiegs weg",
    "nachlauf33": "Nachlauf: ab ueblichem Anstieg Verkauf, wenn 33 % des Anstiegs weg",
    "nachlauf40": "Nachlauf: ab ueblichem Anstieg Verkauf, wenn 40 % des Anstiegs weg",
    "nachlauf33_frueh": "Nachlauf 33 %, aber schon ab halbem ueblichen Anstieg",
}


def handel(O, H, L, C, a, e: int, ko: float, bez: float, t: float, typ: float) -> dict:
    """Alle Strategien fuer einen Kauf in einem Durchgang. Wert des Scheins =
    Kurs - KO (ohne Aufgeld, Spread, Gebuehren). Je Tag zuerst Knock-out
    (Tief <= KO), dann die Verkaufsregel - im Zweifel der schlechtere Fall.
    Rueckgabe je Strategie: (Rendite, Haltetage)."""
    ce = C[e]
    a0 = a[e]
    einsatz = ce - ko
    offen = set(STRATEGIEN)
    erg = {}
    hmax = ce              # hoechstes Hoch seit Kauf (inkl. Einstieg), bis Vortag
    hmax_tag = e
    def zu(name, preis, tag):
        erg[name] = ((preis - ko) / einsatz - 1.0, tag - e)
        offen.discard(name)
    for k in range(e + 1, e + 1 + HALTE_MAX):
        if L[k] <= ko:
            for name in list(offen):
                zu(name, ko, k)          # Knock-out: Rest 0
            break
        anstieg = (hmax - ce)
        # Ruecksetzer um T vom Hoch bis Vortag (wie Chance A / Renditeprobe)
        if "ruecksetzer_t" in offen and L[k] <= hmax - t * a0:
            zu("ruecksetzer_t", min(O[k], hmax - t * a0), k)
        # Nachlauf-Regeln: aktiv, sobald der Anstieg bis Vortag die Schwelle erreicht
        for name, anteil, schwelle in (("nachlauf25", 0.25, 1.0), ("nachlauf33", 0.33, 1.0),
                                       ("nachlauf40", 0.40, 1.0), ("nachlauf33_frueh", 0.33, 0.5)):
            if name in offen and typ > 0 and anstieg / a0 >= schwelle * typ:
                stopp = hmax - anteil * anstieg
                if L[k] <= stopp:
                    zu(name, min(O[k], stopp), k)
        if H[k] > hmax:
            hmax, hmax_tag = H[k], k
        # Alarm 187 am Tagesschluss: Schluss > 3 ATR ueber Bezugstief, Hoch seit
        # Kauf hoechstens 3 Tage alt, rote Kerze
        if ("alarm187" in offen and C[k] < O[k] and k - hmax_tag <= HOCH_ALTER
                and (C[k] - bez) / a[k] > ALARM_ATR):
            zu("alarm187", C[k], k)
    else:
        k = e + HALTE_MAX
        for name in list(offen):
            zu(name, C[k], k)
    return erg


def rendite_je_wert(ticker: str, df: pd.DataFrame, zeilen: list[dict], t: float,
                    typ_anstieg: float) -> list[dict]:
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    n = len(df)
    O, H, L, C = (df[k].values.astype(float) for k in ("Open", "High", "Low", "Close"))
    a = boden.atr(df)
    idx = {f"{d:%Y-%m-%d}": i for i, d in enumerate(df.index)}
    aus = []
    for z in zeilen:
        if not (z["tief_ab_2"] == 1 and z["rsi_unter_50"] == 1):
            continue
        e = idx.get(z["datum"])
        if e is None or e + HALTE_MAX >= n or not (np.isfinite(a[e]) and a[e] > 0):
            continue
        for pp in PUFFER_TEST:
            ko = z["bezugstief"] - pp * a[e]
            if ko >= C[e]:
                continue
            for name, (rend, tage) in handel(O, H, L, C, a, e, ko, z["bezugstief"], t, typ_anstieg).items():
                aus.append({"ticker": ticker, "kauf": z["datum"], "puffer": pp, "strategie": name,
                            "rendite": round(rend, 4), "tage": tage, "punkte": z["punkte"]})
    return aus


def rendite_bericht(rd: pd.DataFrame) -> list[str]:
    rd = rd.copy()
    rd["zeitraum"] = np.where(pd.to_datetime(rd["kauf"]) < TEILUNG, "bis2022", "ab2023")
    je = rd.groupby(["ticker", "zeitraum", "puffer", "strategie"]).agg(
        r=("rendite", "mean"), tage=("tage", "mean"), n=("rendite", "size")).reset_index()
    je = je[je["n"] >= MIN_FAELLE]
    aus = ["## Renditetest Verkaufsregeln", "",
           "Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss, KO = Bezugstief "
           "minus Puffer. Schein ohne Aufgeld, Spread, Gebuehren; Knock-out = -100 %. "
           "Hoechstens 126 Handelstage. Je Wert Mittelwert (mind. 10 Kaeufe), dann Median "
           "ueber die Werte. 'Je Monat' = Rendite je 21 Handelstage Haltedauer (Geld ist "
           "frueher wieder frei). 'Besser als 187' = Werte, bei denen die Regel in BEIDEN "
           "Zeitraeumen mehr bringt als der Ausstiegsalarm 187.", ""]
    for pp in PUFFER_TEST:
        g = je[je["puffer"] == pp]
        breit = g.pivot_table(index=["ticker", "zeitraum"], columns="strategie", values="r")
        aus += [f"### Puffer {pp:g} ATR", "",
                "| Regel | Rendite 19-22 / ab 23 | Tage | je Monat | besser als 187 |",
                "|---|---|---|---|---|"]
        for name, text in STRATEGIEN.items():
            if name not in breit.columns:
                continue
            a_ = g[(g["strategie"] == name) & (g["zeitraum"] == "bis2022")]
            b_ = g[(g["strategie"] == name) & (g["zeitraum"] == "ab2023")]
            besser = "-"
            if name != "alarm187" and "alarm187" in breit.columns:
                d = (breit[name] - breit["alarm187"]).dropna().unstack("zeitraum").dropna()
                if {"bis2022", "ab2023"} <= set(d.columns):
                    besser = f"{int(((d['bis2022'] > 0) & (d['ab2023'] > 0)).sum())} / {len(d)}"
            gg = g[g["strategie"] == name]
            monat = (gg["r"] / gg["tage"].clip(lower=1) * 21).median()
            aus.append(f"| {name} | {f(100 * a_['r'].median())} / {f(100 * b_['r'].median())} % | "
                       f"{f(gg['tage'].median())} | {f(100 * monat)} % | {besser} |")
        aus.append("")
    aus += ["### Regeln", ""] + [f"- **{k}**: {v}" for k, v in STRATEGIEN.items()] + [""]
    return aus


def je_wert_pruefen(p: pd.DataFrame) -> pd.DataFrame:
    """Nur Entscheidungspunkte, an denen der Wert schon mindestens seinen
    ueblichen Anstieg gelaufen ist - Peters Fall ("schon ein ganzes Stueck in
    den Gewinn gelaufen"). Sonst misst jedes Merkmal, das mit einem grossen
    Anstieg einhergeht (RSI hoch, weit ueber EMA50), nur mit, dass der Weg
    zurueck zum Einstieg laenger ist."""
    p = p[p["anstieg_rel"] >= 1.0].copy()
    p["zeitraum"] = np.where(pd.to_datetime(p["datum"]) < TEILUNG, "bis2022", "ab2023")
    zeilen = []
    for ticker, g in p.groupby("ticker"):
        for m in MERKMALE:
            for ziel in ZIELE:
                z = {"ticker": ticker, "merkmal": m, "ziel": ziel}
                for zr in ("bis2022", "ab2023"):
                    h = g[(g["zeitraum"] == zr) & g[m].notna()]
                    mit, ohne = h[h[m] == 1], h[h[m] == 0]
                    z[f"n_mit_{zr}"], z[f"n_ohne_{zr}"] = len(mit), len(ohne)
                    ok = len(mit) >= MIN_FAELLE and len(ohne) >= MIN_FAELLE
                    # Innerhalb gleicher Rueckgabe vergleichen: Eine rote
                    # Kerze hat vom Anstieg schon etwas abgegeben, der Weg
                    # zurueck ist kuerzer - das waere sonst ein Rechen-
                    # effekt, kein Signal. Gewichtet nach Faellen mit Merkmal.
                    diffs, gew = [], []
                    for lo, hi in RUECKGABE_KLASSEN:
                        mk = mit[(mit["rueckgabe"] >= lo) & (mit["rueckgabe"] < hi)]
                        ok_ = ohne[(ohne["rueckgabe"] >= lo) & (ohne["rueckgabe"] < hi)]
                        if len(mk) >= 5 and len(ok_) >= 5:
                            diffs.append(mk[ziel].mean() - ok_[ziel].mean())
                            gew.append(len(mk))
                    z[f"diff_{zr}"] = (round(100 * float(np.average(diffs, weights=gew)), 1)
                                       if ok and diffs else np.nan)
                zeilen.append(z)
    return pd.DataFrame(zeilen)


def f(x, nk=0):
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nk}f}"


def bericht(p: pd.DataFrame, mw: pd.DataFrame, stand: str) -> str:
    p = p.copy()
    p["zeitraum"] = np.where(pd.to_datetime(p["datum"]) < TEILUNG, "bis2022", "ab2023")
    aus = [f"# Verkaufs-Check - Stufe 1 (Stand {stand})", "",
           "Parallellauf. Kauf = Pruefttag mit Tief >= 2 und RSI < 50, Einstieg Schluss. "
           "Entscheidungspunkt = Hoch seit Kauf hoechstens 3 Tage alt, Anstieg mind. 1 ATR. "
           "Ganz weg = Kurs faellt auf den Einstieg, bevor ein neues Hoch kommt; "
           "halb weg = die Haelfte des Anstiegs geht verloren, bevor ein neues Hoch kommt.", "",
           f"Werte: {p['ticker'].nunique()} · Kaeufe: {p.groupby('ticker')['kauf'].nunique().sum()} · "
           f"Entscheidungspunkte: {len(p)}", "",
           "## Wie weit gelaufen - Rueckfallquote je Wert (Median ueber die Werte)", "",
           "| Lauf-Stand | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |", "|---|---|---|"]
    for _, _, name in BAENDER:
        zeile = [name]
        for ziel in ZIELE:
            werte = []
            for zr in ("bis2022", "ab2023"):
                g = p[(p["band"] == name) & (p["zeitraum"] == zr)]
                q = g.groupby("ticker")[ziel].agg(["mean", "size"])
                q = q[q["size"] >= MIN_FAELLE]["mean"]
                werte.append(f(100 * q.median()) + " %" if len(q) else "-")
            zeile.append(" / ".join(werte))
        aus.append("| " + " | ".join(zeile) + " |")
    # Wie viel ist am Schluss schon abgegeben - und wie oft geht dann der Rest?
    w = p[p["anstieg_rel"] >= 1.0]
    aus += ["", "## Schon weit gelaufen: Rueckfall nach bereits abgegebenem Anteil", "",
            "| Schon abgegeben | ganz weg 19-22 / ab 23 | halb weg 19-22 / ab 23 |",
            "|---|---|---|"]
    for lo, hi in RUECKGABE_KLASSEN:
        name = f"{max(lo, 0) * 100:.0f}-{min(hi, 1) * 100:.0f} %" if hi < 9 else f"ueber {lo * 100:.0f} %"
        zeile = [name]
        for ziel in ZIELE:
            werte = []
            for zr in ("bis2022", "ab2023"):
                g = w[(w["rueckgabe"] >= lo) & (w["rueckgabe"] < hi) & (w["zeitraum"] == zr)]
                q = g.groupby("ticker")[ziel].agg(["mean", "size"])
                q = q[q["size"] >= MIN_FAELLE]["mean"]
                werte.append(f(100 * q.median()) + " %" if len(q) else "-")
            zeile.append(" / ".join(werte))
        aus.append("| " + " | ".join(zeile) + " |")
    aus += ["", "## Merkmale einzeln - nur wenn schon mind. der uebliche Anstieg gelaufen ist", "",
            f"Werte = mind. {MIN_FAELLE} Faelle mit UND ohne Merkmal in beiden Zeitraeumen. "
            "Verglichen wird nur bei gleicher bereits abgegebener Rueckgabe "
            "(0-10 / 10-25 / 25-40 / ueber 40 % des Anstiegs). "
            f"Plus = Rueckfall in beiden Zeitraeumen mind. {STOPP_PP:.0f} Prozentpunkte "
            "HAEUFIGER mit Merkmal (spricht fuer Verkauf), Minus = seltener. "
            "Diff = Median ueber die Werte (bis 2022 / ab 2023).", ""]
    for ziel, titel in ZIELE.items():
        aus += [f"### {titel}", "", "| Merkmal | Werte | Plus | Minus | Diff |", "|---|---|---|---|---|"]
        for m, (kurz, _) in MERKMALE.items():
            g = mw[(mw["merkmal"] == m) & (mw["ziel"] == ziel)]
            b = g[g["diff_bis2022"].notna() & g["diff_ab2023"].notna()]
            plus = int(((b["diff_bis2022"] >= STOPP_PP) & (b["diff_ab2023"] >= STOPP_PP)).sum())
            minus = int(((b["diff_bis2022"] <= -STOPP_PP) & (b["diff_ab2023"] <= -STOPP_PP)).sum())
            aus.append(f"| {kurz} | {len(b)} | {plus} | {minus} | "
                       f"{f(b['diff_bis2022'].median(), 1)} / {f(b['diff_ab2023'].median(), 1)} |")
        aus.append("")
    aus += ["### Erklaerung der Merkmale", ""]
    aus += [f"- **{k}**: {l}" for k, l in MERKMALE.values()]
    aus.append("")
    return "\n".join(aus)


def main() -> int:
    jahre = boden.JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])
    tickers = boden.universum()
    aus = AUS
    if "--nur" in sys.argv:
        tickers = [t.strip() for t in sys.argv[sys.argv.index("--nur") + 1].split(",") if t.strip()]
        aus = AUS / "test"
    daten = boden.lade(tickers, jahre)
    if not daten:
        print("Keine Kursdaten - Abbruch.")
        return 1
    alle, renditen = [], []
    for i, (t, df) in enumerate(sorted(daten.items()), start=1):
        try:
            pk, rd = punkte_je_wert(t, df)
            alle += pk
            renditen += rd
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {t}: {exc}")
        if i % 25 == 0:
            print(f"  {i}/{len(daten)} Werte ...")
    if not alle:
        print("Keine Entscheidungspunkte - Abbruch.")
        return 1
    p = pd.DataFrame(alle)
    aus.mkdir(parents=True, exist_ok=True)
    with gzip.open(aus / "verkauf_punkte.csv.gz", "wt", encoding="utf-8", newline="") as fh:
        p.to_csv(fh, index=False)
    mw = je_wert_pruefen(p)
    mw.to_csv(aus / "verkauf_merkmale_werte.csv", index=False)
    stand = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rd = pd.DataFrame(renditen)
    text = bericht(p, mw, stand)
    if len(rd):
        with gzip.open(aus / "verkauf_rendite.csv.gz", "wt", encoding="utf-8", newline="") as fh:
            rd.to_csv(fh, index=False)
        text += "\n" + "\n".join(rendite_bericht(rd))
    (aus / "verkauf.md").write_text(text, encoding="utf-8")
    print(f"  {len(p)} Entscheidungspunkte aus {p['ticker'].nunique()} Werten -> {aus}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
