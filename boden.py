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
CSV_RENDITE = AUS / "boden_rendite_werte.csv"
CSV_ANKER = AUS / "boden_anker_werte.csv"
ANKER_QUELLE = AUS / "boden_anker_werte.csv"   # taegliche Anzeige liest immer den Vollauf
CSV_HEUTE = AUS / "boden_heute.csv"
MD_HEUTE = AUS / "boden_heute.md"
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
PUFFER_SIM = (1.0, 2.0, 3.0)   # KO-Abstand unter dem Bezugstief (ATR) fuer die Renditeprobe
PUFFER_ANKER = tuple(round(0.25 * k, 2) for k in range(1, 17))   # 0,25 ... 4,00 ATR
ANKER_HALTE = 0.60       # Anker-Regel 19.09.2026: niedrigster Puffer mit Halterate >= 60 %
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


# ── Renditeprobe KO-Schein ─────────────────────────────────────────

def ko_handel(O, H, L, C, d: int, ko: float, t: float, ad: float) -> float:
    """Vereinfachter Turbo-Long-Handel ab Schluss des Pruefttags (24.09.2026,
    Peter: "Rendite je Punktestufe"). Wert des Scheins = Kurs - KO, also
    ohne Aufgeld, Spread, Gebuehren und Finanzierung. Ein spaeterer Einstieg
    (weiter ueber dem Tief) hat damit automatisch weniger Hebel.

    Tag fuer Tag, hoechstens 63 Handelstage:
      1. Tagestief am oder unter KO -> Knock-out, -100 %.
      2. Tagestief am oder unter (hoechster Stand bis Vortag - T ATR) ->
         Verkauf zu dieser Marke (bei Eroeffnung darunter: zur Eroeffnung).
         Das ist dasselbe Anstiegsende wie bei Chance A.
      3. Sonst nach 63 Tagen Verkauf zum Schluss.
    KO wird vor dem Stopp geprueft - im Zweifel zaehlt der schlechtere Fall.
    Rueckgabe: Rendite als Bruch (0,5 = +50 %).

    Im Lauf rechnet ko_handel_raster() dasselbe fuer alle Puffer auf einmal;
    diese Schleifenfassung bleibt als lesbare Referenz fuer die Nachrechnung."""
    einsatz = C[d] - ko
    m = C[d]
    for j in range(d + 1, d + 1 + FENSTER):
        if L[j] <= ko:
            return -1.0
        stopp = m - t * ad
        if L[j] <= stopp:
            verkauf = min(O[j], stopp)
            return (verkauf - ko) / einsatz - 1.0
        if H[j] > m:
            m = H[j]
    return (C[d + FENSTER] - ko) / einsatz - 1.0


def ko_handel_raster(O, H, L, C, d: int, bez: float, t: float, ad: float,
                     puffer=PUFFER_ANKER) -> np.ndarray:
    """ko_handel() fuer alle Puffer auf einmal - dieselben Regeln, nur ohne
    Schleife (sonst dauert der Lauf bei 16 Puffern zu lange). Der Stopp
    haengt nicht vom KO ab; je Puffer wird nur gefragt, ob der KO VOR dem
    Stopp (oder am selben Tag) fiel. Puffer mit KO ueber dem Einstieg: nan."""
    lw, hw, ow = L[d + 1:d + 1 + FENSTER], H[d + 1:d + 1 + FENSTER], O[d + 1:d + 1 + FENSTER]
    m_vor = np.maximum.accumulate(np.concatenate(([C[d]], hw[:-1])))
    stopp = m_vor - t * ad
    tr = np.flatnonzero(lw <= stopp)
    js = int(tr[0]) if len(tr) else FENSTER
    ko = bez - np.asarray(puffer, dtype=float) * ad
    einsatz = C[d] - ko
    # erster Tag mit Tief <= KO: laufendes Minimum faellt monoton
    ko_i = np.searchsorted(-np.minimum.accumulate(lw), -ko, side="left")
    if js < FENSTER:
        verkauf = min(ow[js], stopp[js])
    else:
        verkauf = C[d + FENSTER]
    erg = (verkauf - ko) / einsatz - 1.0
    erg = np.where(ko_i <= js, -1.0, erg)
    erg = np.where(ko_i >= FENSTER, (verkauf - ko) / einsatz - 1.0, erg)
    return np.where(einsatz > 0, erg, np.nan)


# ── Pruefttage eines Werts ─────────────────────────────────────────

def pruefttage(ticker: str, df: pd.DataFrame,
               nur_letzter: bool = False) -> tuple[list[dict], dict]:
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
    for d in (range(n - 1, n) if nur_letzter else range(30, n)):
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
        # Boden-Punkte (Vorschlag 24.09.2026): die drei eng verwandten
        # Erholungszeichen zaehlen zusammen nur EINEN Punkt.
        z["erholung_begonnen"] = float(max(z["kein_neues_tief"],
                                           z["schluss_ueber_vortageshoch"], z["zweig_b"]))
        z["punkte"] = int(z["erholung_begonnen"] + (z["rsi_tief_rang"] == 1)
                          + (z["erholung_vol"] == 1))

        # Ergebnis - nur mit vollem 63-Tage-Fenster
        for k in ("risiko", "rueckgang", "chance_b", "chance_a", "tage_a", "offen_a"):
            z[k] = np.nan
        for pp in PUFFER_SIM:
            z[f"rendite_p{pp:g}"] = np.nan
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
            raster = ko_handel_raster(O, H, L, C, d, bez, t, ad)
            z["_raster"] = raster
            for pp in PUFFER_SIM:
                z[f"rendite_p{pp:g}"] = float(raster[PUFFER_ANKER.index(pp)])
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


# ── Anker je Punktestufe, je Wert ──────────────────────────────────

GRUPPEN = {
    "0 P": lambda g: g["punkte"] == 0,
    "1 P": lambda g: g["punkte"] == 1,
    "2+ P": lambda g: g["punkte"] >= 2,
    "2+ P, Tief>=2": lambda g: (g["punkte"] >= 2) & (g["tief_ab_2"] == 1),
    "2+ P, Tief>=2, RSI<50": lambda g: ((g["punkte"] >= 2) & (g["tief_ab_2"] == 1)
                                        & (g["rsi_unter_50"] == 1)),
    "alt: Tief>=2, RSI<50": lambda g: (g["tief_ab_2"] == 1) & (g["rsi_unter_50"] == 1),
}


def _anker(risiko: np.ndarray) -> float:
    """Niedrigster Puffer, bei dem mind. 60 % der Faelle 63 Tage halten."""
    for pp in PUFFER_ANKER:
        if np.mean(risiko < pp) >= ANKER_HALTE:
            return pp
    return np.nan


def anker_je_wert(ticker: str, g: pd.DataFrame) -> list[dict]:
    """Anker aus 2019-2022 bestimmt, Rendite damit 2019-2022 (Lernzeitraum)
    und ab 2023 (Pruefzeitraum, nicht zum Bestimmen benutzt). Dazu der
    Anker ueber alle Jahre fuer die taegliche Anzeige."""
    g = g[g["risiko"].notna()]
    vor = pd.to_datetime(g["datum"]) < TEILUNG
    zeilen = []
    for name, bed in GRUPPEN.items():
        h = g[bed(g)]
        a, b = h[vor[h.index]], h[~vor[h.index]]
        z = {"ticker": ticker, "gruppe": name, "faelle_bis2022": len(a),
             "faelle_ab2023": len(b),
             "anker_gesamt": _anker(h["risiko"].values) if len(h) >= MIN_FAELLE else np.nan}
        anker = _anker(a["risiko"].values) if len(a) >= MIN_FAELLE else np.nan
        z["anker_bis2022"] = anker
        for zr, x in (("bis2022", a), ("ab2023", b)):
            if np.isfinite(anker) and len(x) >= MIN_FAELLE:
                k = PUFFER_ANKER.index(anker)
                r = np.array([v[k] for v in x["_raster"]], dtype=float)
                z[f"rendite_{zr}"] = round(100 * np.nanmean(r), 1)
                z[f"ko_{zr}"] = round(100 * np.mean(r == -1.0), 1)
                z[f"haelt_{zr}"] = round(100 * np.mean(x["risiko"].values < anker), 1)
            else:
                z[f"rendite_{zr}"] = z[f"ko_{zr}"] = z[f"haelt_{zr}"] = np.nan
        zeilen.append(z)
    return zeilen


def anker_bericht(aw: pd.DataFrame) -> list[str]:
    aus = ["## Anker je Punktestufe", "",
           "Anker = niedrigster Puffer unter dem Bezugstief, bei dem mind. 60 % "
           "der Faelle 63 Tage halten (Anker-Regel 19.09.2026), je Wert aus "
           "2019-2022 bestimmt. Rendite am Anker (Renditeprobe wie unten): "
           "2019-2022 = Lernzeitraum, ab 2023 = Pruefung mit dem alten Anker. "
           "Median ueber die Werte.", "",
           "| Gruppe | Anker | R 19-22 | R ab 23 | Haelt ab 23 |",
           "|---|---|---|---|---|"]
    zaehl = []
    for name in GRUPPEN:
        g = aw[(aw["gruppe"] == name) & aw["rendite_ab2023"].notna()]
        if not len(g):
            continue
        aus.append(f"| {name} | {f(g['anker_bis2022'].median(), 2)} | "
                   f"{f(g['rendite_bis2022'].median(), 0)} % | "
                   f"{f(g['rendite_ab2023'].median(), 0)} % | "
                   f"{f(g['haelt_ab2023'].median(), 0)} % |")
        zaehl.append(f"{name}: {len(g)}")
    aus += ["", "Werte je Gruppe: " + " · ".join(zaehl), ""]
    return aus


# ── Rendite je Punktestufe, je Wert ────────────────────────────────

def rendite_je_stufe(kand: pd.DataFrame) -> pd.DataFrame:
    """Je Wert, Zeitraum, Puffer und Punktestufe: mittlere Rendite und
    KO-Quote. Mittelwert, nicht Median - fuer das Geld zaehlt der
    Erwartungswert, ein Knock-out wiegt voll."""
    k = kand.copy()
    k["zeitraum"] = np.where(pd.to_datetime(k["datum"]) < TEILUNG, "bis2022", "ab2023")
    zeilen = []
    for pp in PUFFER_SIM:
        sp = f"rendite_p{pp:g}"
        h = k[k[sp].notna()]
        for (ticker, zr, stufe), g in h.groupby(["ticker", "zeitraum", "punkte"]):
            zeilen.append({"ticker": ticker, "zeitraum": zr, "puffer": pp, "punkte": stufe,
                           "faelle": len(g), "rendite_mittel": round(100 * g[sp].mean(), 1),
                           "rendite_median": round(100 * g[sp].median(), 1),
                           "ko_quote": round(100 * (g[sp] == -1.0).mean(), 1)})
    return pd.DataFrame(zeilen)


def rendite_bericht(rw: pd.DataFrame) -> list[str]:
    aus = ["## Rendite je Punktestufe (Renditeprobe KO-Schein)", "",
           "Punkte: 1 Erholung begonnen (kein neues Tief / Schluss ueber "
           "Vortageshoch / Umkehr b) + 1 RSI am Tief unter 7 von 10 frueheren "
           "Boeden + 1 gruene Erholungskerze mit Volumen.",
           "Schein: KO = Bezugstief minus Puffer, Einstieg Schluss Pruefttag, "
           "Ausstieg beim Ruecksetzer um T ATR vom Hoch oder nach 63 Tagen, "
           "Knock-out = -100 %. Ohne Aufgeld, Spread, Gebuehren.",
           f"Je Wert Mittelwert (mind. {MIN_FAELLE} Faelle), dann Median ueber "
           "die Werte. KO = Median der KO-Quoten.", ""]
    ok = rw[rw["faelle"] >= MIN_FAELLE]
    for pp in PUFFER_SIM:
        g = ok[ok["puffer"] == pp]
        aus += [f"### Puffer {pp:g} ATR", "",
                "| Punkte | 19-22 | ab 23 | KO | Werte |", "|---|---|---|---|---|"]
        for stufe in sorted(g["punkte"].unique()):
            a = g[(g["punkte"] == stufe) & (g["zeitraum"] == "bis2022")]
            b = g[(g["punkte"] == stufe) & (g["zeitraum"] == "ab2023")]
            ko = g[g["punkte"] == stufe]["ko_quote"].median()
            aus.append(f"| {stufe} | {f(a['rendite_mittel'].median(), 0)} % | "
                       f"{f(b['rendite_mittel'].median(), 0)} % | {f(ko, 0)} % | "
                       f"{a['ticker'].nunique()}/{b['ticker'].nunique()} |")
        # Werte, bei denen Stufe >= 2 in BEIDEN Zeitraeumen besser als Stufe 0
        breit = g.pivot_table(index=["ticker", "zeitraum"], columns="punkte",
                              values="rendite_mittel")
        hoch = breit[[c for c in breit.columns if c >= 2]].mean(axis=1) if any(
            c >= 2 for c in breit.columns) else None
        if hoch is not None and 0 in breit.columns:
            vgl = (hoch - breit[0]).dropna().unstack("zeitraum").dropna()
            if {"bis2022", "ab2023"} <= set(vgl.columns):
                besser = int(((vgl["bis2022"] > 0) & (vgl["ab2023"] > 0)).sum())
                schlechter = int(((vgl["bis2022"] < 0) & (vgl["ab2023"] < 0)).sum())
                aus.append("")
                aus.append(f"Stufe 2-3 gegen 0, je Wert: besser in beiden Zeitraeumen "
                           f"{besser}, schlechter in beiden {schlechter}, von {len(vgl)}.")
        aus.append("")
    return aus


# ── Bericht ────────────────────────────────────────────────────────

def f(x, nk=1):
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nk}f}"


def bericht(profil: pd.DataFrame, zf: pd.DataFrame, kand: pd.DataFrame,
            jahre: int, stand: str, rw: pd.DataFrame | None = None,
            aw: pd.DataFrame | None = None) -> str:
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
    if aw is not None and len(aw):
        aus += anker_bericht(aw)
    if rw is not None and len(rw):
        aus += rendite_bericht(rw)

    letzter = kand["datum"].max()
    heute = kand[kand["datum"] == letzter].sort_values("ticker")
    aus += [f"## Pruefttage am {letzter} (nur Information)", "",
            "| Wert | Tief | RSI | Punkte |", "|---|---|---|---|"]
    for _, r in heute.sort_values(["punkte", "ticker"], ascending=[False, True]).iterrows():
        warn = " (Umkehr a)" if r["zweig_a"] == 1 and r["erholung_begonnen"] == 0 else ""
        aus.append(f"| {r['ticker']} | {r['position']} | {f(r['rsi'], 0)} | "
                   f"{int(r['punkte'])}{warn} |")
    aus.append("")
    return "\n".join(aus)


# ── Taegliche Anzeige (Stufe 2) ────────────────────────────────────

# Kandidat im Parallel-Screening (Peter 24.09.2026: "so, dass es
# bestmoeglich ins Profil passt"): Umkehrzeichen wie Block 1, die alten
# Filter Tief >= 2 und RSI < 50 bleiben (am Anker in beiden Zeitraeumen
# leicht besser), dazu mind. 2 Boden-Punkte.
KANDIDATEN_GRUPPE = "2+ P, Tief>=2, RSI<50"


def gruppe_von(z: pd.Series) -> str:
    alt = z["tief_ab_2"] == 1 and z["rsi_unter_50"] == 1
    if z["punkte"] >= 2:
        return KANDIDATEN_GRUPPE if alt else "2+ P"
    return "1 P" if z["punkte"] == 1 else "0 P"


def heute(daten: dict[str, pd.DataFrame]) -> int:
    """Pruefttage des letzten fertigen Handelstags mit Punkten, Gruppe und
    Anker aus dem letzten Vollauf. Schreibt boden_heute.csv/.md."""
    zeilen = []
    for ticker, df in sorted(daten.items()):
        try:
            z, _ = pruefttage(ticker, df, nur_letzter=True)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {ticker}: {exc}")
            continue
        zeilen += z
    AUS.mkdir(parents=True, exist_ok=True)
    stand = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not zeilen:
        MD_HEUTE.write_text(f"# Boden-Screening heute (Stand {stand})\n\nKeine Pruefttage.\n",
                            encoding="utf-8")
        return 0
    k = pd.DataFrame(zeilen)
    # Wie heute.py: nur Werte mit dem neuesten Handelstag, veraltete fallen raus
    tag = k["datum"].max()
    veraltet = sorted(t for t, d in daten.items() if f"{d.index[-1]:%Y-%m-%d}" != tag)
    k = k[k["datum"] == tag].copy()
    k["gruppe"] = k.apply(gruppe_von, axis=1)
    k["kandidat"] = (k["gruppe"] == KANDIDATEN_GRUPPE).astype(int)
    k["anker"] = np.nan
    if ANKER_QUELLE.exists():
        aw = pd.read_csv(ANKER_QUELLE).set_index(["ticker", "gruppe"])["anker_gesamt"]
        k["anker"] = [aw.get((t, g), np.nan) for t, g in zip(k["ticker"], k["gruppe"])]
    k["ko_marke"] = (k["bezugstief"] - k["anker"] * k["atr"]).round(2)
    spalten = ["ticker", "datum", "kandidat", "gruppe", "punkte", "position", "rsi",
               "erholung_begonnen", "rsi_tief_rang", "erholung_vol", "zweig_a",
               "einstieg", "bezugstief", "bezugstief_datum", "atr", "anker", "ko_marke",
               "korr_atr", "korr_rang"]
    k = k.sort_values(["kandidat", "punkte", "ticker"], ascending=[False, False, True])
    k[spalten].to_csv(CSV_HEUTE, index=False)

    kand = k[k["kandidat"] == 1]
    aus = [f"# Boden-Screening {tag} (Stand {stand})", "",
           "Parallellauf, nur Information. Kandidat = Block-1-Umkehrzeichen + "
           "Tief >= 2 + RSI < 50 + mind. 2 Boden-Punkte. Anker = niedrigster "
           "Puffer mit 60 % Halterate fuer diese Gruppe und diesen Wert "
           "(Vollauf), KO-Marke = Bezugstief - Anker x ATR.", "",
           f"## Kandidaten ({len(kand)})", ""]
    if len(kand):
        aus += ["| Wert | Tief | RSI | Anker | KO-Marke |", "|---|---|---|---|---|"]
        for _, r in kand.iterrows():
            aus.append(f"| {r['ticker']} | {r['position']} | {f(r['rsi'], 0)} | "
                       f"{f(r['anker'], 2)} | {f(r['ko_marke'], 2)} |")
    else:
        aus.append("_Keine._")
    rest = k[k["kandidat"] == 0]
    aus += ["", f"## Weitere Pruefttage ({len(rest)})", "",
            "| Wert | Punkte | Grund |", "|---|---|---|"]
    for _, r in rest.iterrows():
        gruende = []
        if r["punkte"] < 2:
            gruende.append(f"{int(r['punkte'])} P")
        if r["position"] < 2:
            gruende.append("Tief 1")
        if not r["rsi_unter_50"] == 1:
            gruende.append("RSI >= 50")
        if r["zweig_a"] == 1 and r["erholung_begonnen"] == 0:
            gruende.append("Umkehr a")
        aus.append(f"| {r['ticker']} | {int(r['punkte'])} | {', '.join(gruende)} |")
    if veraltet:
        aus += ["", "Nicht aktuell (kein Kurs vom " + tag + "): " + ", ".join(veraltet)]
    aus.append("")
    MD_HEUTE.write_text("\n".join(aus), encoding="utf-8")
    print(f"  {tag}: {len(kand)} Kandidaten, {len(rest)} weitere Pruefttage "
          f"-> {CSV_HEUTE.name}, {MD_HEUTE.name}")
    return 0


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
    # Unfertige Tageskerze verwerfen (24.09.2026): der erste Lauf startete
    # 15:46 UTC bei offener US-Boerse, die Liste "Pruefttage am 24.09." beruhte
    # auf halben Kerzen. Dieselbe Regel wie marktdaten.py (EU ab 17:00 UTC,
    # sonst ab 21:00 UTC fertig) - gerechnet wird dann auf Stand Vortag.
    jetzt = datetime.now(timezone.utc)
    daten = {}
    for t, d in roh.items():
        if len(d):
            d = marktdaten.unfertige_heutige_kerze_verwerfen(d, t, jetzt)
        if len(d) > 120:
            daten[t] = d
    return daten


def auswerten(daten: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    teile, profile, anker = [], [], []
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
        if "_raster" in g:
            anker += anker_je_wert(ticker, g)
            g = g.drop(columns="_raster")
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
    return kand, pd.DataFrame(profile), pd.DataFrame(anker)


def schreiben(kand: pd.DataFrame, profil: pd.DataFrame, jahre: int,
              aw: pd.DataFrame | None = None) -> None:
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
    rw = rendite_je_stufe(kand)
    rw.to_csv(CSV_RENDITE, index=False)
    if aw is not None:
        aw.to_csv(CSV_ANKER, index=False)
    MD_AUS.write_text(bericht(profil, zf, kand, jahre, stand, rw, aw), encoding="utf-8")
    print(f"  geschrieben: {CSV_KAND.name}, {CSV_PROFIL.name}, "
          f"{CSV_MERKMALE.name}, {CSV_RENDITE.name}, {MD_AUS.name}")


def main() -> int:
    jahre = JAHRE
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])
    tickers = universum()
    if "--nur" in sys.argv:
        # Testlauf mit wenigen Werten: eigener Unterordner, damit die
        # vollstaendige Auswertung nicht ueberschrieben wird.
        global AUS, CSV_KAND, CSV_PROFIL, CSV_MERKMALE, MD_AUS, CSV_RENDITE, CSV_ANKER
        tickers = [t.strip() for t in
                   sys.argv[sys.argv.index("--nur") + 1].split(",") if t.strip()]
        AUS = AUS / "test"
        CSV_KAND, CSV_PROFIL = AUS / CSV_KAND.name, AUS / CSV_PROFIL.name
        CSV_MERKMALE, MD_AUS = AUS / CSV_MERKMALE.name, AUS / MD_AUS.name
        CSV_RENDITE, CSV_ANKER = AUS / CSV_RENDITE.name, AUS / CSV_ANKER.name
        global CSV_HEUTE, MD_HEUTE
        CSV_HEUTE, MD_HEUTE = AUS / CSV_HEUTE.name, AUS / MD_HEUTE.name
    daten = lade(tickers, jahre)
    if not daten:
        print("Keine Kursdaten - Abbruch.")
        return 1
    if "--heute" in sys.argv:
        return heute(daten)
    kand, profil, anker = auswerten(daten)
    if kand.empty:
        print("Keine Pruefttage - Abbruch.")
        return 1
    abw = profil[profil.get("pivot_kontrolle", pd.Series(dtype=float)) == 0]
    if len(abw):
        print(f"  ! Wendepunkt-Kontrolle bei {len(abw)} Werten abweichend: "
              + ", ".join(abw["ticker"]))
    print(f"  {len(kand)} Pruefttage aus {len(profil)} Werten.")
    schreiben(kand, profil, jahre, anker)
    return 0


if __name__ == "__main__":
    sys.exit(main())
