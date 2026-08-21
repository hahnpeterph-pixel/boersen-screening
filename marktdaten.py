"""
marktdaten.py - reiner Marktdaten-Abzug. Kennt KEINE Positionen.

Laeuft werktags im GitHub-Workflow und schreibt:
  docs/marktdaten.csv   eine Zeile je Wert, maschinenlesbar
  docs/marktdaten.md    kurze Uebersicht zum Reinschauen

Bewusst OHNE: Knock-out-Schwellen, Positionsgroessen, Regelpruefung,
Depotstand. All das aendert sich staendig und wird ausserhalb gerechnet.
Dadurch muss diese Datei nie wieder angefasst werden, egal was sich am
Depot aendert.

Geliefert wird je Wert:
  Kurs, ATR(14), RSI(14), EUR/USD,
  die drei juengsten Swing-Tiefs mit Datum und Volumenverhaeltnis,
  Kerzensignale: Hammer, hoeheres Hoch, bearishe Umkehrkerze,
  EMA(50) und EMA(200) auf Tagesbasis.
"""

import csv
import os
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

HIER = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HIER, "docs")
CSV_AUS = os.path.join(DOCS, "marktdaten.csv")
MD_AUS = os.path.join(DOCS, "marktdaten.md")

FENSTER_TAGE = 90
LINKS = RECHTS = 3
ATR_TAGE = RSI_TAGE = 14

# ── Rohstoffe ──────────────────────────────────────────────────────
# Erster Eintrag wird versucht, bei Fehlschlag der zweite (Rueckfallkette).
# Lauf vom 21.08.2026: die vier Edelmetall-Spot-Ticker lieferten bei Yahoo
# KEINE Daten. Deshalb Future als Rueckfall.
#
# WICHTIG fuer die KO-Pruefung: Zertifikate auf Edelmetalle referenzieren
# in der Regel SPOT, nicht den Future. Der Future notiert hoeher (Contango).
# Gemessene Basis am 21.08.2026: GC=F 4.639,20 gegen Spot 4.603,11,
# also +36,09 Punkte. Wird der Future genutzt, muss die Basis fuer die
# KO-Rechnung abgezogen werden - das passiert ausserhalb dieses Skripts.
ROHSTOFFE = [
    (["XAUUSD=X", "GC=F"], "Gold", "Spot/Future"),
    (["XAGUSD=X", "SI=F"], "Silber", "Spot/Future"),
    (["XPTUSD=X", "PL=F"], "Platin", "Spot/Future"),
    (["XPDUSD=X", "PA=F"], "Palladium", "Spot/Future"),
    (["BZ=F"], "Brent Oel", "Future"),
    (["CL=F"], "WTI Oel", "Future"),
    (["NG=F"], "Erdgas", "Future"),
    (["HG=F"], "Kupfer", "Future"),
    (["ZW=F"], "Weizen", "Future"),
    (["ZC=F"], "Mais", "Future"),
    (["KC=F"], "Kaffee", "Future"),
    (["CC=F"], "Kakao", "Future"),
    (["SB=F"], "Zucker", "Future"),
]

WAEHRUNG = [(["EURUSD=X"], "EUR/USD", "Spot")]

# ── Aktien: NASDAQ-100, Dow 30, DAX 40. Statisch, aendert sich selten.
# Am 21.08.2026 entfernt, weil bei Yahoo keine Daten mehr (uebernommen
# oder delistet): ANSS, EA, WBA, 1COV.DE.
US = """AAPL ABNB ADBE ADI ADP ADSK AEP AMAT AMD AMGN AMZN ARM ASML AVGO
AXP AZN BA BIIB BKNG BKR CAT CDNS CDW CEG CHTR CMCSA COST CPRT CRM CRWD CSCO
CSGP CSX CTAS CTSH DASH DDOG DIS DXCM EXC FANG FAST FTNT GEHC GILD GOOG
GOOGL GS HD HON IBM IDXX ILMN INTC INTU ISRG JNJ JPM KDP KHC KLAC KO LIN LRCX
LULU MAR MCD MCHP MDB MDLZ MELI META MMM MNST MRK MRNA MRVL MSFT MU NFLX NKE
NVDA NXPI ODFL ON ORCL ORLY PANW PAYX PCAR PDD PEP PG PLTR PYPL QCOM REGN ROP
ROST SBUX SHW SNPS SPGI TEAM TMUS TRV TSLA TTD TTWO TXN UNH V VRSK VRTX VZ
WBD WDAY WMT XEL ZS""".split()

DAX = """ADS.DE AIR.DE ALV.DE BAS.DE BAYN.DE BEI.DE BMW.DE BNR.DE CBK.DE CON.DE
DTG.DE DBK.DE DB1.DE DHL.DE DTE.DE EOAN.DE FRE.DE HNR1.DE HEI.DE HEN3.DE
IFX.DE MBG.DE MRK.DE MTX.DE MUV2.DE P911.DE PAH3.DE QIA.DE RHM.DE RWE.DE SAP.DE
SRT3.DE SIE.DE ENR.DE SHL.DE SY1.DE VOW3.DE VNA.DE ZAL.DE""".split()

UNIVERSUM = ([([t], t, "Aktie") for t in dict.fromkeys(US)]
             + [([t], t, "Aktie") for t in dict.fromkeys(DAX)]
             + ROHSTOFFE + WAEHRUNG)

# Ticker ohne brauchbares Volumen bei Yahoo
OHNE_VOLUMEN = {"XAUUSD=X", "XAGUSD=X", "XPTUSD=X", "XPDUSD=X", "EURUSD=X"}


# ── Berechnungen ───────────────────────────────────────────────────
def kerzen(ticker):
    try:
        df = yf.Ticker(ticker).history(period="400d", interval="1d",
                                       auto_adjust=False)
    except Exception as e:
        print(f"  {ticker}: Abruf fehlgeschlagen ({e})")
        return None
    if df is None or df.empty or "Low" not in df.columns:
        return None
    df = df.dropna(subset=["Low", "Close"])
    if len(df) < 30:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def atr(df, tage=ATR_TAGE):
    h, t, c = df["High"], df["Low"], df["Close"]
    v = c.shift(1)
    tr = pd.concat([h - t, (h - v).abs(), (t - v).abs()], axis=1).max(axis=1)
    w = tr.tail(tage).mean()
    return None if pd.isna(w) else float(w)


def rsi(df, tage=RSI_TAGE):
    d = df["Close"].diff()
    g = d.clip(lower=0).ewm(alpha=1 / tage, adjust=False).mean()
    v = (-d.clip(upper=0)).ewm(alpha=1 / tage, adjust=False).mean()
    if v.iloc[-1] == 0:
        return 100.0
    w = 100 - 100 / (1 + g.iloc[-1] / v.iloc[-1])
    return None if pd.isna(w) else float(w)


def ema(df, tage):
    w = df["Close"].ewm(span=tage, adjust=False).mean().iloc[-1]
    return None if pd.isna(w) else float(w)


def swing_tiefs(df):
    """Alle Swing-Tiefs im Fenster, juengstes zuerst. Der laufende Tag
    zaehlt nie mit. Das Tief des zuletzt abgeschlossenen Tages wird als
    unbestaetigt mitgenommen, wenn es unter den Vortagen liegt."""
    lows, daten = df["Low"].values, df.index
    vols = df["Volume"].values if "Volume" in df.columns else [None] * len(df)
    grenze = daten[-1] - pd.Timedelta(days=FENSTER_TAGE)
    tr = []
    for i in range(LINKS, len(df) - RECHTS):
        if daten[i] < grenze:
            continue
        w = lows[i]
        if all(lows[i - j] > w for j in range(1, LINKS + 1)) and \
           all(lows[i + j] > w for j in range(1, RECHTS + 1)):
            tr.append({"i": i, "datum": daten[i], "tief": float(w),
                       "vol": vols[i], "best": True})
    i = len(df) - 1
    if i >= LINKS and daten[i] >= grenze and not any(t["i"] == i for t in tr) \
       and all(lows[i - j] > lows[i] for j in range(1, LINKS + 1)):
        tr.append({"i": i, "datum": daten[i], "tief": float(lows[i]),
                   "vol": vols[i], "best": False})
    tr.sort(key=lambda t: t["datum"], reverse=True)
    return tr


def vol_rel(df, bis, tage=20):
    if "Volume" not in df.columns:
        return None
    teil = df["Volume"].iloc[max(0, bis - tage):bis].dropna()
    if teil.empty or teil.mean() == 0:
        return None
    v = df["Volume"].iloc[bis]
    return None if pd.isna(v) else float(v) / float(teil.mean())


def hammer(df, a):
    """Lange untere Lunte, kleiner Koerper oben, kaum obere Lunte,
    relevante Groesse, vorher abwaerts."""
    if len(df) < 6:
        return False
    z = df.iloc[-1]
    o, h, t, c = (float(z["Open"]), float(z["High"]),
                  float(z["Low"]), float(z["Close"]))
    sp = h - t
    if sp <= 0:
        return False
    koerper, unten, oben = abs(c - o), min(o, c) - t, h - max(o, c)
    if a and sp < 0.8 * a:
        return False
    if koerper > 0 and unten < 2.0 * koerper:
        return False
    if (max(o, c) - t) < 0.66 * sp:
        return False
    if oben > 0.15 * sp:
        return False
    return bool(c < float(df["Close"].iloc[-6]))


def hoeheres_hoch(df):
    return bool(float(df["High"].iloc[-1]) > float(df["High"].iloc[-2]))


def umkehrkerze(df):
    """Bearishes Warnsignal: Schluss unter Eroeffnung UND unter
    Vortageshoch UND unter Vortagestief."""
    h, v = df.iloc[-1], df.iloc[-2]
    return bool(h["Close"] < h["Open"] and h["Close"] < v["High"]
                and h["Close"] < v["Low"])


def z(x, nk=4):
    return "" if x is None else f"{round(float(x), nk)}"


# ── Hauptlauf ──────────────────────────────────────────────────────
def main():
    jetzt = datetime.now(timezone.utc)
    zeilen, fehler = [], []

    for kette, name, art in UNIVERSUM:
        df, ticker = None, kette[0]
        for kandidat in kette:
            df = kerzen(kandidat)
            if df is not None:
                ticker = kandidat
                break
        if df is None:
            fehler.append(" oder ".join(kette))
            print(f"  {'/'.join(kette)}: keine Daten")
            continue
        if ticker != kette[0]:
            print(f"  {kette[0]} leer -> Rueckfall auf {ticker}")

        a = atr(df)
        tr = swing_tiefs(df)
        kurs = float(df["Close"].iloc[-1])
        letzte = df.iloc[-1]
        mitvol = ticker not in OHNE_VOLUMEN

        r = {
            "ticker": ticker, "name": name, "art": art,
            "wunschticker": kette[0],
            "rueckfall": int(ticker != kette[0]),
            "datum": f"{df.index[-1]:%Y-%m-%d}",
            "kurs": z(kurs), "open": z(letzte["Open"]),
            "high": z(letzte["High"]), "low": z(letzte["Low"]),
            "atr14": z(a), "rsi14": z(rsi(df), 2),
            "ema50": z(ema(df, 50)), "ema200": z(ema(df, 200)),
            "hammer": int(hammer(df, a)),
            "hoeheres_hoch": int(hoeheres_hoch(df)),
            "umkehrkerze": int(umkehrkerze(df)),
        }
        for n in (1, 2, 3):
            t = tr[n - 1] if len(tr) >= n else None
            r[f"tief{n}"] = z(t["tief"]) if t else ""
            r[f"tief{n}_datum"] = f"{t['datum']:%Y-%m-%d}" if t else ""
            r[f"tief{n}_best"] = (int(t["best"]) if t else "")
            r[f"tief{n}_volrel"] = (z(vol_rel(df, t["i"]), 2)
                                    if (t and mitvol) else "")
        zeilen.append(r)
        print(f"  {ticker}: ok")

    os.makedirs(DOCS, exist_ok=True)
    felder = list(zeilen[0].keys()) if zeilen else []
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(zeilen)
    print(f"Geschrieben: {CSV_AUS} ({len(zeilen)} Zeilen)")

    fx = next((r["kurs"] for r in zeilen if r["ticker"] == "EURUSD=X"), "")
    sig = [r for r in zeilen if r["hammer"] or r["umkehrkerze"]]
    md = [
        "# Marktdaten", "",
        f"_Erstellt {jetzt:%Y-%m-%d %H:%M} UTC. {len(zeilen)} Werte, "
        f"Fenster {FENSTER_TAGE} Kalendertage. EUR/USD {fx}._", "",
        "Reiner Datenabzug. Knock-out-Schwellen, Positionsgroessen und "
        "Regelpruefung werden bewusst NICHT hier gerechnet - sie aendern "
        "sich staendig und wuerden diese Datei pflegebeduerftig machen.",
        "", "Vollstaendige Daten: `docs/marktdaten.csv`", "",
        "## Kerzensignale von gestern", "",
        "| Wert | Kurs | Hammer | hoeheres Hoch | Umkehrkerze | RSI |",
        "|---|---|---|---|---|---|",
    ]
    for r in sig:
        md.append(f"| {r['name']} ({r['ticker']}) | {r['kurs']} | "
                  f"{'ja' if r['hammer'] else '-'} | "
                  f"{'ja' if r['hoeheres_hoch'] else '-'} | "
                  f"{'ja' if r['umkehrkerze'] else '-'} | {r['rsi14']} |")
    if not sig:
        md.append("| _keine_ | | | | | |")
    if fehler:
        md += ["", "## Ohne Daten", "", ", ".join(fehler)]
    md += ["", "---", "",
           "_Kursdaten von Yahoo Finance ueber yfinance. Bei Spot-Tickern "
           "(Edelmetalle, Waehrungen) liefert Yahoo kein Volumen - die "
           "Volumenspalten bleiben dort leer. Keine Anlageberatung._"]
    with open(MD_AUS, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Geschrieben: {MD_AUS}")


if __name__ == "__main__":
    main()
