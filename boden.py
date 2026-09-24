"""
boden.py - Boden-Screening, Stufe 1: 7-Jahres-Auswertung je Wert.

PARALLELLAUF (Peter 24.09.2026): eigener Lauf, eigene Dateien unter
docs/boden/. Das bestehende Screening (marktdaten.py, heute.py, historie.py,
tiefs_regel.py) wird NICHT veraendert - es wird nur importiert und gelesen.
"Sonst ist alles fuer die Katz."

LEITFRAGE
An welchen Pruefttagen lag der Einstieg nahe am echten Boden - danach ging
es kaum noch tiefer, aber ordentlich hoch? Und welche Merkmale am Pruefttag
(Korrektur-Reife, RSI, Volumen, Bodenmuster) erkennen das VORHER?

PRUEFTTAG (Peter 24.09.2026 abends: "Zeitpunkt unveraendert", "alle
aufnehmen"): jeder Tag mit einem der drei Block-1-Umkehrzeichen aus heute.py
  a) frisches Tief (Tagestief unter Vortagestief) UND gruene Kerze
  b) hoeheres Hoch als am Vortag UND rote Vortageskerze
  c) Hammer (marktdaten.hammer, unveraendert importiert)
OHNE RSI<50 und OHNE Tief-1-Ausschluss. Beide alten Filter laufen als
Merkmale mit und werden mitgeprueft - passen sie weiter, bleiben sie.
Die Analystenquote gibt es historisch nicht, sie ist nicht rueckrechenbar.

Einstieg = Schluss des Pruefttags. BEZUGSTIEF exakt wie heute.py: das
Tagestief, wenn es unter dem juengsten Swing-Tief (90 Kalendertage, wie
marktdaten.swing_tiefs) liegt, sonst dieses Swing-Tief. Tiefposition exakt
wie heute.py (tiefserie + Positionskorrektur vom 19.09.2026), aber AUS SICHT
DES PRUEFTTAGS - nur Kerzen bis zu diesem Tag.

KORREKTURSCHWELLE T JE WERT (Peter: "Median"): Median der Korrekturtiefen
des Werts wie in historie.py gemessen (korr_serie_atr: letztes Hoch vor der
Serie bis Serienende, ATR am Serienende), abgeschlossene Serien, 7 Jahre.
Mit T laeuft ein Zickzack: die Richtung wechselt erst nach T ATR
Gegenbewegung. Daraus das Korrektur-Profil (wie oft, wie tief, wie lang).

ERGEBNIS JE PRUEFTTAG (alles in ATR des Pruefttags)
  risiko     wie weit der Kurs binnen 63 Handelstagen noch UNTER das
             Bezugstief fiel (0 = nie darunter)
  rueckgang  wie weit binnen 63 Handelstagen unter den Einstieg
  chance_b   hoechstes Hoch binnen 63 Handelstagen ueber dem Einstieg
  chance_a   Anstieg bis zum ersten Ruecksetzer um T ATR vom laufenden
             Hoch - ohne Zeitgrenze, zaehlt auch, wenn das alte Hoch nie
             wieder erreicht wird (Peters Einwand zu "ueber Starthoch").
             Laeuft der Anstieg bis heute: Wert bis heute, offen_a = 1.
  ratio_x    chance_x / max(rueckgang, 0,1)
GUT (Peter "Mischung"), getrennt fuer Chance A und B:
  risiko im besten Drittel DIESES Werts
  UND (chance ueber dem Median DIESES Werts
       ODER ratio im besten Drittel DIESES Werts).
Die Grenzen stehen je Wert in boden_profile.csv; die Rohwerte stehen in
boden_kandidaten.csv.gz, damit die Definition ohne neuen Lauf geaendert
werden kann.

MERKMALE werden nur aus Kerzen BIS zum Pruefttag gebildet. Vergleiche mit
"frueheren Korrekturen/Boeden" nutzen nur Korrekturen, die am Pruefttag
schon abgeschlossen waren (mindestens 5, sonst leer). Leer heisst: in der
Pruefung weder "mit" noch "ohne".

PRUEFUNG je Merkmal, JE WERT (keine Pools), getrennt 2019-2022 / ab 2023:
Quote "gut" mit und ohne Merkmal. Stoppregel 17.09.2026: tragfaehig nur mit
mindestens 8 Prozentpunkten in BEIDEN Zeitraeumen. Der Bericht zaehlt, bei
wie vielen Werten das zutrifft.

Das Repository ist oeffentlich: keine Positionen, keine Trades (E58).

Aufruf:  python boden.py [--jahre 7] [--nur AAPL,MSFT]
"""

from __future__ import annotations

import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import kurse
import marktdaten
import tiefs_regel as regel

BASE = Path(__file__).resolve().parent
AUS = BASE / "docs" / "boden"
CSV_KAND = AUS / "boden_kandidaten.csv.gz"
CSV_PROFIL = AUS / "boden_profile.csv"
CSV_MERKMALE = AUS / "boden_merkmale_werte.csv"
MD_AUS = AUS / "boden.md"

JAHRE = 7
ATR_TAGE = 14            # wie marktdaten.py / historie.py
RSI_TAGE = 14
FENSTER = 63             # Handelstage, rund drei Monate (wie historie.QUARTAL)
VOL_TAGE = 20            # Volumen-Durchschnitt, wie in der Analysemethodik
AUSVERKAUF = 2.0         # Volumen am Tief >= 2x Durchschnitt
ERHOLUNG_VOL = 1.5       # Volumen an gruener Erholungskerze >= 1,5x
DOPPEL_ATR = 0.5         # Doppelboden: zweites Tief hoechstens 0,5 ATR entfernt
DOPPEL_ABSTAND = 5       # ... und mindestens 5 Handelstage auseinander
RANG_HOCH = 0.7          # "tiefer/laenger als 7 von 10 frueheren"
RANG_TIEF = 0.3          # "RSI tiefer als 7 von 10 frueheren Boeden"
MIN_VORFAELLE = 5        # so viele fruehere Korrekturen braucht ein Rang
RATIO_BODEN = 0.1        # Mindestnenner fuer Chance/Rueckgang
TEILUNG = pd.Timestamp("2023-01-01")   # Stoppregel: bis 2022 / ab 2023
MIN_FAELLE = 10          # je Gruppe und Zeitraum fuer eine Quote
STOPP_PP = 8.0           # Stoppregel: mindestens 8 Prozentpunkte

# Merkmal -> Klartext. Reihenfolge = Reihenfolge im Bericht.
MERKMALE = {   # Schluessel: (kurz fuer die Tabelle, Erklaerung)
    "reif": ("Korrektur >= T", "Korrektur mind. so tief wie der Median des Werts (T)"),
    "korr_tief_rang": ("Korr. tiefer 7/10", "Korrektur tiefer als 7 von 10 frueheren des Werts"),
    "korr_lang_rang": ("Korr. laenger 7/10", "Korrektur laenger als 7 von 10 frueheren des Werts"),
    "rsi_tief_rang": ("RSI Tief unter 7/10", "RSI am Tief unter dem RSI an 7 von 10 frueheren Boeden"),
    "rsi_unter_50": ("RSI < 50 (alt)", "RSI am Pruefttag unter 50 - alter Block-1-Filter"),
    "divergenz": ("RSI-Divergenz", "Positive Divergenz: tieferes Tief, hoeherer RSI als am vorigen Tief"),
    "ausverkauf": ("Ausverkauf", "Volumen am Tief mind. 2x 20-Tage-Schnitt"),
    "erschoepfung": ("Erschoepfung", "Neues Tief mit weniger Volumen als am vorigen Tief"),
    "erholung_vol": ("Erholung + Vol.", "Gruene Erholungskerze nach dem Tief mit mind. 1,5x Volumen"),
    "zweig_a": ("Umkehr a", "Frisches Tief + gruene Kerze"),
    "zweig_b": ("Umkehr b", "Hoeheres Hoch nach roter Vortageskerze"),
    "hammer": ("Hammer", "Umkehrzeichen c: Hammer (marktdaten.hammer)"),
    "doppelboden": ("Doppelboden", "Zweites Tief in der Korrektur max. 0,5 ATR vom Bezugstief, mind. 5 Tage Abstand"),
    "schluss_ueber_vortageshoch": ("Schluss > VT-Hoch", "Schluss ueber dem Vortageshoch"),
    "kein_neues_tief": ("Kein neues Tief", "Pruefttag ohne neues Tief - das Bezugstief liegt zurueck"),
    "ueber_ema200": ("Ueber EMA200", "Schluss ueber der EMA200"),
    "tief_ab_2": ("Tief >= 2 (alt)", "Tiefposition 2 oder hoeher - alter Filter: Tief 1 raus"),
}
ZIELE = {"gut_a": "gut (Chance A)", "gut_b": "gut (Chance B)",
         "haelt2": "haelt 2 ATR (63 T)"}


# ── Kennzahlen (dieselben Formeln wie historie.py / marktdaten.py) ──

def atr(df: pd.DataFrame) -> np.ndarray:
    h, t, c = df["High"], df["Low"], df["Close"]
    vor = c.shift(1)
    tr = pd.concat([h - t, (h - vor).abs(), (t - vor).abs()], axis=1).max(axis=1)
    return tr.rolling(ATR_TAGE).mean().values


def rsi(df: pd.DataFrame) -> np.ndarray:
    d = df["Close"].diff()
    auf = d.clip(lower=0).ewm(alpha=1 / RSI_TAGE, adjust=False).mean()
    ab = (-d.clip(upper=0)).ewm(alpha=1 / RSI_TAGE, adjust=False).mean()
    r = 100 - 100 / (1 + auf / ab.replace(0, np.nan))
    # marktdaten.rsi: kein Abwaertstag im Fenster -> 100
    r = r.where(~((ab == 0) & (auf > 0)), 100.0)
    return r.values


def rang(wert: float, frueher: np.ndarray) -> float:
    """Anteil frueherer Werte, die KLEINER sind. nan bei zu wenig Faellen."""
    if not np.isfinite(wert) or len(frueher) < MIN_VORFAELLE:
        return np.nan
    return float(np.mean(frueher < wert))


# ── Wendepunkte aus Sicht jedes Tages ──────────────────────────────

def pivot_verlauf(df: pd.DataFrame):
    """Dieselbe Schleife wie tiefs_regel.pivots(), aber mit dem Tag, an dem
    jeder Wendepunkt bestaetigt wurde, und dem juengsten Swing-Tief AUS
    SICHT jedes Tages (bestaetigt oder laufend, wie swing_tiefs mit
    unbestaetigt=True). Ob die Schleife identisch rechnet, prueft main()
    fuer jeden Wert gegen tiefs_regel.pivots()."""
    hoch, tief = df["High"].values, df["Low"].values
    n = len(df)
    punkte: list[tuple[str, int, int]] = []
    juengstes = np.full(n, -1, dtype=int)
    anzahl_best = np.zeros(n, dtype=int)
    richtung, kandidat, gipfel, letztes_tief = "ab", 0, 0, -1
    juengstes[0] = 0
    for i in range(1, n):
        if richtung == "ab":
            if regel._unter(tief[i], tief[kandidat]):
                kandidat = i
            elif regel._ueber(hoch[i], hoch[kandidat]):
                punkte.append(("tief", kandidat, i))
                letztes_tief = kandidat
                richtung, gipfel = "auf", i
        else:
            if regel._ueber(hoch[i], hoch[gipfel]):
                gipfel = i
            elif regel._unter(tief[i], tief[gipfel]):
                punkte.append(("hoch", gipfel, i))
                richtung, kandidat = "ab", i
        juengstes[i] = kandidat if richtung == "ab" else letztes_tief
        anzahl_best[i] = len(punkte)
    return punkte, juengstes, anzahl_best


def korrekturschwelle(df: pd.DataFrame, a: np.ndarray) -> tuple[float | None, int]:
    """Median der Korrekturtiefe je abgeschlossener Serie - dieselbe
    Messung wie korr_serie_atr in historie.py."""
    hoch_w, tief_w = df["High"].values, df["Low"].values
    hochs = [h["i"] for h in regel.swing_hochs(df)]
    werte = []
    for s in regel.sequenzen(df):
        if s["laufend"]:
            continue
        davor = [h for h in hochs if h < s["start_i"]]
        ae = a[s["ende_i"]]
        if davor and np.isfinite(ae) and ae > 0:
            werte.append((float(hoch_w[davor[-1]]) - float(tief_w[s["ende_i"]])) / float(ae))
    if not werte:
        return None, 0
    return float(np.median(werte)), len(werte)


def zickzack(df: pd.DataFrame, a: np.ndarray, t: float):
    """Zickzack mit Mindestschwung t ATR (ATR des jeweiligen Tages).

    Rueckgabe je Tag: Zustand (1 auf, -1 ab), laufendes Extrem, Hoch, an
    dem die laufende Korrektur begann; dazu die Liste abgeschlossener
    Korrekturen mit dem Tag, an dem sie bestaetigt waren."""
    hoch, tief = df["High"].values, df["Low"].values
    n = len(df)
    zustand = np.zeros(n, dtype=int)
    extrem = np.full(n, -1, dtype=int)
    k_hoch = np.full(n, -1, dtype=int)
    korrekturen: list[dict] = []
    gueltig = np.flatnonzero(np.isfinite(a) & (a > 0))
    if not len(gueltig):
        return zustand, extrem, k_hoch, korrekturen
    start = int(gueltig[0])
    z, e, letztes_hoch = 1, start, -1
    for i in range(start, n):
        ai = a[i]
        if not (np.isfinite(ai) and ai > 0):
            ai = a[i - 1]
        if z == 1:
            if hoch[i] > hoch[e]:
                e = i
            elif hoch[e] - tief[i] >= t * ai:
                letztes_hoch, z, e = e, -1, i
        else:
            if tief[i] < tief[e]:
                e = i
            elif hoch[i] - tief[e] >= t * ai:
                if letztes_hoch >= 0 and np.isfinite(a[e]) and a[e] > 0:
                    korrekturen.append({
                        "hoch_i": letztes_hoch, "tief_i": e, "am": i,
                        "tiefe": (hoch[letztes_hoch] - tief[e]) / a[e],
                        "dauer": e - letztes_hoch})
                z, e = 1, i
        zustand[i], extrem[i], k_hoch[i] = z, e, letztes_hoch
    return zustand, extrem, k_hoch, korrekturen


# ── Pruefttage eines Werts ─────────────────────────────────────────

def pruefttage(ticker: str, df: pd.DataFrame) -> tuple[list[dict], dict]:
    df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
    n = len(df)
    info = {"ticker": ticker, "kerzen": n}
    if n < 260:
        info["fehler"] = "zu wenig Kerzen"
        return [], info
    O, H, L, C = (df[k].values.astype(float) for k in ("Open", "High", "Low", "Close"))
    V = (df["Volume"].values.astype(float) if "Volume" in df.columns
         else np.full(n, np.nan))
    V = np.where(V > 0, V, np.nan)
    daten = df.index
    a = atr(df)
    r = rsi(df)
    ema200 = df["Close"].ewm(span=200, adjust=False).mean().values
    vol_schnitt = pd.Series(V).shift(1).rolling(VOL_TAGE, min_periods=VOL_TAGE).mean().values

    punkte, juengstes, anzahl_best = pivot_verlauf(df)
    kontrolle = [(art, i) for art, i, _ in punkte] == regel.pivots(df)
    info["pivot_kontrolle"] = int(kontrolle)
    if not kontrolle:
        print(f"  ! {ticker}: Wendepunkte weichen von tiefs_regel.pivots ab")
    piv_tief_i = np.array([i for art, i, _ in punkte if art == "tief"], dtype=int)
    piv_tief_am = np.array([b for art, _, b in punkte if art == "tief"], dtype=int)

    t, n_serien = korrekturschwelle(df, a)
    info["t_atr"], info["t_serien"] = t, n_serien
    if t is None:
        info["fehler"] = "keine abgeschlossene Serie"
        return [], info
    zustand, extrem, k_hoch, korrekturen = zickzack(df, a, t)
    info["korrekturen"] = korrekturen
    k_am = np.array([k["am"] for k in korrekturen], dtype=int)
    k_tiefe = np.array([k["tiefe"] for k in korrekturen], dtype=float)
    k_dauer = np.array([k["dauer"] for k in korrekturen], dtype=float)
    k_rsi = np.array([r[k["tief_i"]] for k in korrekturen], dtype=float)

    serie_cache: dict[int, tuple] = {}
    swing_grenze = pd.Timedelta(days=marktdaten.FENSTER_TAGE)
    zeilen = []
    for d in range(30, n):
        ad = a[d]
        if not (np.isfinite(ad) and ad > 0):
            continue
        # Umkehrzeichen wie heute.block1_treffer
        zweig_a = bool(L[d] < L[d - 1] and C[d] > O[d])
        zweig_b = bool(H[d] > H[d - 1] and C[d - 1] < O[d - 1])
        zweig_c = bool(marktdaten.hammer(df.iloc[d - 5:d + 1], float(ad)))
        if not (zweig_a or zweig_b or zweig_c):
            continue

        # Bezugstief wie heute.py
        j = juengstes[d]
        if j >= 0 and daten[j] < daten[d] - swing_grenze:
            j = -1
        if j >= 0 and not (L[d] < L[j]):
            b_i = j
        else:
            b_i = d
        bez = float(L[b_i])

        # Tiefposition wie heute.py, aus Sicht des Pruefttags
        kb = int(anzahl_best[d])
        if kb not in serie_cache:
            serie_cache[kb] = regel.tiefserie(df.iloc[:d + 1])
        anz, _, stand = serie_cache[kb]
        if anz != "" and anz and stand != "":
            position = int(anz) + (1 if regel._unter(bez, float(stand)) else 0)
        else:
            position = 1

        # Korrektur aus Sicht des Pruefttags (Zickzack mit T)
        h_i = k_hoch[d] if zustand[d] == -1 else extrem[d]
        korr_atr = korr_tage = np.nan
        if h_i >= 0:
            tiefster = h_i + int(np.argmin(L[h_i:d + 1]))
            korr_atr = (H[h_i] - L[tiefster]) / ad
            korr_tage = float(tiefster - h_i)
        fertig = k_am <= d
        korr_tief_r = rang(korr_atr, k_tiefe[fertig])
        korr_lang_r = rang(korr_tage, k_dauer[fertig])
        rsi_tief = r[b_i]
        rsi_r = rang(rsi_tief, k_rsi[fertig])

        # Voriges Tief in derselben Korrektur (feine Wendepunkte)
        in_korr = (piv_tief_am <= d) & (piv_tief_i > max(h_i, 0)) & (piv_tief_i != b_i)
        vor = piv_tief_i[in_korr & (piv_tief_i < b_i)]
        p = int(vor[-1]) if len(vor) else -1
        divergenz = erschoepfung = np.nan
        if p >= 0:
            neues = regel._unter(L[b_i], L[p])
            divergenz = float(neues and np.isfinite(r[b_i]) and np.isfinite(r[p])
                              and r[b_i] > r[p])
            if np.isfinite(V[b_i]) and np.isfinite(V[p]):
                erschoepfung = float(neues and V[b_i] < V[p])
        andere = piv_tief_i[in_korr]
        doppel = float(any(abs(L[q] - bez) <= DOPPEL_ATR * ad
                           and abs(q - b_i) >= DOPPEL_ABSTAND for q in andere))

        vol_tief = (V[b_i] / vol_schnitt[b_i]
                    if np.isfinite(V[b_i]) and np.isfinite(vol_schnitt[b_i]) else np.nan)
        vol_tag = (V[d] / vol_schnitt[d]
                   if np.isfinite(V[d]) and np.isfinite(vol_schnitt[d]) else np.nan)

        z = {
            "ticker": ticker, "datum": f"{daten[d]:%Y-%m-%d}",
            "einstieg": round(C[d], 4), "bezugstief": round(bez, 4),
            "bezugstief_datum": f"{daten[b_i]:%Y-%m-%d}", "atr": round(ad, 4),
            "t_atr": round(t, 3), "position": position,
            "abstand_atr": round((C[d] - bez) / ad, 3),
            "rsi": round(float(r[d]), 2) if np.isfinite(r[d]) else np.nan,
            "rsi_tief": round(float(rsi_tief), 2) if np.isfinite(rsi_tief) else np.nan,
            "rsi_rang": rsi_r, "korr_atr": korr_atr, "korr_tage": korr_tage,
            "korr_rang": korr_tief_r, "korr_dauer_rang": korr_lang_r,
            "vol_rel_tief": vol_tief, "vol_rel_tag": vol_tag,
            # Merkmale (1/0, leer = nicht bestimmbar)
            "reif": float(korr_atr >= t) if np.isfinite(korr_atr) else np.nan,
            "korr_tief_rang": float(korr_tief_r >= RANG_HOCH) if np.isfinite(korr_tief_r) else np.nan,
            "korr_lang_rang": float(korr_lang_r >= RANG_HOCH) if np.isfinite(korr_lang_r) else np.nan,
            "rsi_tief_rang": float(rsi_r <= RANG_TIEF) if np.isfinite(rsi_r) else np.nan,
            "rsi_unter_50": float(r[d] < 50) if np.isfinite(r[d]) else np.nan,
            "divergenz": divergenz,
            "ausverkauf": float(vol_tief >= AUSVERKAUF) if np.isfinite(vol_tief) else np.nan,
            "erschoepfung": erschoepfung,
            "erholung_vol": (float(C[d] > O[d] and b_i != d and vol_tag >= ERHOLUNG_VOL)
                             if np.isfinite(vol_tag) else np.nan),
            "zweig_a": float(zweig_a), "zweig_b": float(zweig_b), "hammer": float(zweig_c),
            "doppelboden": doppel,
            "schluss_ueber_vortageshoch": float(C[d] > H[d - 1]),
            "kein_neues_tief": float(b_i != d),
            "ueber_ema200": float(C[d] > ema200[d]) if d >= 199 else np.nan,
            "tief_ab_2": float(position >= 2),
        }

        # Ergebnis - nur mit vollem 63-Tage-Fenster
        for k in ("risiko", "rueckgang", "chance_b", "chance_a", "tage_a", "offen_a"):
            z[k] = np.nan
        if d + FENSTER < n:
            lo = L[d + 1:d + 1 + FENSTER].min()
            hi = H[d + 1:d + 1 + FENSTER].max()
            z["risiko"] = max(0.0, (bez - lo) / ad)
            z["rueckgang"] = max(0.0, (C[d] - lo) / ad)
            z["chance_b"] = (hi - C[d]) / ad
            rest_h, rest_l = H[d + 1:], L[d + 1:]
            m_vor = np.maximum.accumulate(np.concatenate(([C[d]], rest_h[:-1])))
            tr = np.flatnonzero(rest_l <= m_vor - t * ad)
            if len(tr):
                k = int(tr[0])
                z["chance_a"], z["tage_a"], z["offen_a"] = (m_vor[k] - C[d]) / ad, k + 1, 0
            else:
                z["chance_a"] = (max(C[d], rest_h.max()) - C[d]) / ad
                z["tage_a"], z["offen_a"] = len(rest_h), 1
        zeilen.append(z)
    info["pruefttage"] = len(zeilen)
    return zeilen, info


# ── Gutes Tief je Wert ─────────────────────────────────────────────

def bewerten(g: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Setzt gut_a, gut_b, haelt2 fuer einen Wert; Grenzen aus DIESEM Wert."""
    g = g.copy()
    for s in ("a", "b"):
        g[f"ratio_{s}"] = g[f"chance_{s}"] / g["rueckgang"].clip(lower=RATIO_BODEN)
    fertig = g["risiko"].notna()
    grenzen = {}
    if fertig.sum() >= MIN_FAELLE:
        f = g[fertig]
        grenzen["risiko_p33"] = float(f["risiko"].quantile(1 / 3))
        for s in ("a", "b"):
            grenzen[f"chance_{s}_median"] = float(f[f"chance_{s}"].median())
            grenzen[f"ratio_{s}_p67"] = float(f[f"ratio_{s}"].quantile(2 / 3))
        for s in ("a", "b"):
            gut = (f["risiko"] <= grenzen["risiko_p33"]) & (
                (f[f"chance_{s}"] > grenzen[f"chance_{s}_median"])
                | (f[f"ratio_{s}"] >= grenzen[f"ratio_{s}_p67"]))
            g.loc[fertig, f"gut_{s}"] = gut.astype(float)
        g.loc[fertig, "haelt2"] = (f["risiko"] < 2.0).astype(float)
    for k in ("gut_a", "gut_b", "haelt2"):
        if k not in g:
            g[k] = np.nan
    return g, grenzen


# ── Merkmalspruefung je Wert ───────────────────────────────────────

def merkmale_pruefen(alle: pd.DataFrame) -> pd.DataFrame:
    alle = alle[alle["risiko"].notna()].copy()
    alle["zeitraum"] = np.where(pd.to_datetime(alle["datum"]) < TEILUNG,
                                "bis2022", "ab2023")
    zeilen = []
    for ticker, g in alle.groupby("ticker"):
        for m in MERKMALE:
            for ziel in ZIELE:
                z = {"ticker": ticker, "merkmal": m, "ziel": ziel}
                for zr in ("bis2022", "ab2023"):
                    h = g[(g["zeitraum"] == zr) & g[m].notna() & g[ziel].notna()]
                    mit, ohne = h[h[m] == 1], h[h[m] == 0]
                    z[f"n_mit_{zr}"], z[f"n_ohne_{zr}"] = len(mit), len(ohne)
                    z[f"q_mit_{zr}"] = round(100 * mit[ziel].mean(), 1) if len(mit) else np.nan
                    z[f"q_ohne_{zr}"] = round(100 * ohne[ziel].mean(), 1) if len(ohne) else np.nan
                    ok = len(mit) >= MIN_FAELLE and len(ohne) >= MIN_FAELLE
                    z[f"diff_{zr}"] = (round(z[f"q_mit_{zr}"] - z[f"q_ohne_{zr}"], 1)
                                       if ok else np.nan)
                zeilen.append(z)
    return pd.DataFrame(zeilen)


def zusammenfassung(mw: pd.DataFrame) -> pd.DataFrame:
    zeilen = []
    for (m, ziel), g in mw.groupby(["merkmal", "ziel"], sort=False):
        beide = g[g["diff_bis2022"].notna() & g["diff_ab2023"].notna()]
        plus = beide[(beide["diff_bis2022"] >= STOPP_PP) & (beide["diff_ab2023"] >= STOPP_PP)]
        minus = beide[(beide["diff_bis2022"] <= -STOPP_PP) & (beide["diff_ab2023"] <= -STOPP_PP)]
        zeilen.append({
            "merkmal": m, "ziel": ziel, "werte": len(beide),
            "plus_beide": len(plus), "minus_beide": len(minus),
            "median_diff_bis2022": beide["diff_bis2022"].median() if len(beide) else np.nan,
            "median_diff_ab2023": beide["diff_ab2023"].median() if len(beide) else np.nan,
        })
    return pd.DataFrame(zeilen)


# ── Bericht ────────────────────────────────────────────────────────

def f(x, nk=1):
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nk}f}"


def bericht(profil: pd.DataFrame, zf: pd.DataFrame, kand: pd.DataFrame,
            jahre: int, stand: str) -> str:
    aus = [f"# Boden-Screening - Stufe 1 (Stand {stand}, {jahre} Jahre)", "",
           "Parallellauf, aendert nichts am bestehenden Screening. "
           "Pruefttage = alle Tage mit Block-1-Umkehrzeichen (ohne RSI- und "
           "Tief-1-Filter). Einstieg = Schluss, Bezugstief wie heute.py.", "",
           f"Werte: {len(profil)} · Pruefttage: {len(kand)} · davon mit "
           f"63-Tage-Ergebnis: {int(kand['risiko'].notna().sum())}", ""]

    fertig = profil[profil["gut_a_pct"].notna()]
    aus += ["## Gutes Tief - Anteil je Wert", "",
            "| | Median | p25 | p75 |", "|---|---|---|---|"]
    for k, t in (("gut_a_pct", "gut A"), ("gut_b_pct", "gut B"),
                 ("haelt2_pct", "haelt 2 ATR")):
        x = fertig[k]
        aus.append(f"| {t} | {f(x.median())} % | {f(x.quantile(.25))} % | {f(x.quantile(.75))} % |")
    aus += ["", "Korrekturschwelle T (Median je Wert): "
            f"Median {f(profil['t_atr'].median(), 2)} ATR, "
            f"Spanne {f(profil['t_atr'].min(), 2)}-{f(profil['t_atr'].max(), 2)} ATR.", ""]

    aus += ["## Merkmale einzeln - je Wert gezaehlt", "",
            f"Werte = Werte mit mind. {MIN_FAELLE} Faellen mit UND ohne Merkmal in "
            f"beiden Zeitraeumen. Plus/Minus = Werte mit mind. {STOPP_PP:.0f} "
            "Prozentpunkten besser/schlechter in BEIDEN Zeitraeumen. "
            "Diff = Median ueber die Werte (Prozentpunkte, bis 2022 / ab 2023).", ""]
    for ziel, titel in ZIELE.items():
        aus += [f"### {titel}", "", "| Merkmal | Werte | Plus | Minus | Diff |",
                "|---|---|---|---|---|"]
        for m, (text, _) in MERKMALE.items():
            r = zf[(zf["merkmal"] == m) & (zf["ziel"] == ziel)]
            if not len(r):
                continue
            r = r.iloc[0]
            aus.append(f"| {text} | {r['werte']} | {r['plus_beide']} | {r['minus_beide']} | "
                       f"{f(r['median_diff_bis2022'])} / {f(r['median_diff_ab2023'])} |")
        aus.append("")

    aus += ["### Erklaerung der Merkmale", ""]
    aus += [f"- **{kurz}**: {lang}" for kurz, lang in MERKMALE.values()]
    aus.append("")

    letzter = kand["datum"].max()
    heute = kand[kand["datum"] == letzter].sort_values("ticker")
    aus += [f"## Pruefttage am {letzter} (nur Information)", "",
            "| Wert | Tief | RSI | Korr ATR (Rang) |", "|---|---|---|---|"]
    for _, r in heute.iterrows():
        rg = "" if not np.isfinite(r["korr_rang"]) else f" ({r['korr_rang'] * 10:.0f}/10)"
        aus.append(f"| {r['ticker']} | {r['position']} | {f(r['rsi'], 0)} | "
                   f"{f(r['korr_atr'], 2)}{rg} |")
    aus.append("")
    return "\n".join(aus)


# ── Ablauf ─────────────────────────────────────────────────────────

def universum() -> list[str]:
    """Aktien aus universe.json (Gruppen mit Benchmark). Rohstoffe, FX und
    Krypto sind seit 09.09.2026 nicht mehr im Screening."""
    roh = json.loads((BASE / "universe.json").read_text(encoding="utf-8"))
    werte: list[str] = []
    for gruppe in roh.get("benchmarks", {}):
        werte += roh.get(gruppe, [])
    return sorted({t for t in werte if not t.endswith(("=F", "=X"))})


def lade(tickers: list[str], jahre: int) -> dict[str, pd.DataFrame]:
    """Wie historie.lade(): kurse.kerzen_batch, bereinigt, >120 Kerzen."""
    print(f"Lade {len(tickers)} Werte, {jahre} Jahre ...")
    roh = kurse.kerzen_batch(tickers, period=f"{jahre}y", auto_adjust=True)
    return {t: d for t, d in roh.items() if len(d) > 120}


def auswerten(daten: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    teile, profile = [], []
    for i, (ticker, df) in enumerate(sorted(daten.items()), start=1):
        try:
            zeilen, info = pruefttage(ticker, df)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {ticker}: {exc}")
            continue
        if i % 25 == 0:
            print(f"  {i}/{len(daten)} Werte ...")
        korr = info.pop("korrekturen", [])
        if not zeilen:
            profile.append(info)
            continue
        g, grenzen = bewerten(pd.DataFrame(zeilen))
        teile.append(g)
        tiefe = np.array([k["tiefe"] for k in korr])
        dauer = np.array([k["dauer"] for k in korr])
        jahre = max((df.index[-1] - df.index[0]).days / 365.25, 0.1)
        p = dict(info)
        p.update({
            "korrekturen": len(korr), "korrekturen_je_jahr": round(len(korr) / jahre, 2),
            **{f"tiefe_p{q}": (round(float(np.percentile(tiefe, q)), 2) if len(tiefe) else np.nan)
               for q in (25, 50, 75, 90)},
            **{f"dauer_p{q}": (round(float(np.percentile(dauer, q)), 1) if len(dauer) else np.nan)
               for q in (25, 50, 75, 90)},
            "mit_ergebnis": int(g["risiko"].notna().sum()),
            **{k: round(v, 3) for k, v in grenzen.items()},
            "gut_a_pct": round(100 * g["gut_a"].mean(), 1) if g["gut_a"].notna().any() else np.nan,
            "gut_b_pct": round(100 * g["gut_b"].mean(), 1) if g["gut_b"].notna().any() else np.nan,
            "haelt2_pct": round(100 * g["haelt2"].mean(), 1) if g["haelt2"].notna().any() else np.nan,
        })
        profile.append(p)
    kand = pd.concat(teile, ignore_index=True) if teile else pd.DataFrame()
    return kand, pd.DataFrame(profile)


def schreiben(kand: pd.DataFrame, profil: pd.DataFrame, jahre: int) -> None:
    AUS.mkdir(parents=True, exist_ok=True)
    stand = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    runden = kand.copy()
    for c in runden.columns:
        if runden[c].dtype.kind == "f":
            runden[c] = runden[c].round(4)
    with gzip.open(CSV_KAND, "wt", encoding="utf-8", newline="") as fh:
        runden.to_csv(fh, index=False)
    profil.to_csv(CSV_PROFIL, index=False)
    mw = merkmale_pruefen(kand)
    mw.to_csv(CSV_MERKMALE, index=False)
    zf = zusammenfassung(mw)
    MD_AUS.write_text(bericht(profil, zf, kand, jahre, stand), encoding="utf-8")
    print(f"  geschrieben: {CSV_KAND.name}, {CSV_PROFIL.name}, "
          f"{CSV_MERKMALE.name}, {MD_AUS.name}")


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])
    tickers = universum()
    if "--nur" in sys.argv:
        # Testlauf mit wenigen Werten: eigener Unterordner, damit die
        # vollstaendige Auswertung nicht ueberschrieben wird.
        global AUS, CSV_KAND, CSV_PROFIL, CSV_MERKMALE, MD_AUS
        tickers = [t.strip() for t in
                   sys.argv[sys.argv.index("--nur") + 1].split(",") if t.strip()]
        AUS = AUS / "test"
        CSV_KAND, CSV_PROFIL = AUS / CSV_KAND.name, AUS / CSV_PROFIL.name
        CSV_MERKMALE, MD_AUS = AUS / CSV_MERKMALE.name, AUS / MD_AUS.name
    daten = lade(tickers, jahre)
    if not daten:
        print("Keine Kursdaten - Abbruch.")
        return 1
    kand, profil = auswerten(daten)
    if kand.empty:
        print("Keine Pruefttage - Abbruch.")
        return 1
    abw = profil[profil.get("pivot_kontrolle", pd.Series(dtype=float)) == 0]
    if len(abw):
        print(f"  ! Wendepunkt-Kontrolle bei {len(abw)} Werten abweichend: "
              + ", ".join(abw["ticker"]))
    print(f"  {len(kand)} Pruefttage aus {len(profil)} Werten.")
    schreiben(kand, profil, jahre)
    return 0


if __name__ == "__main__":
    sys.exit(main())
