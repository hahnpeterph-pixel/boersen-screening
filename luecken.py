#!/usr/bin/env python3
"""luecken.py - Kursluecken (Gaps) je Wert, mit Schliessungsverhalten.

Eine Luecke entsteht, wenn die Eroeffnung eines Tages ausserhalb der
Spanne des Vortages liegt:
  Aufwaerts-Luecke:  Open(heute) > High(gestern)
  Abwaerts-Luecke:   Open(heute) < Low(gestern)

"Geschlossen" heisst: der Kurs ist spaeter wieder bis in die Luecke
zurueckgelaufen, also bei einer Aufwaerts-Luecke ein Tief <= High(gestern),
bei einer Abwaerts-Luecke ein Hoch >= Low(gestern). Gemessen wird auf
Tages-Hoch/Tief, nicht auf Schlusskursen - eine Luecke gilt als
geschlossen, sobald sie intraday beruehrt wurde - auch noch am Tag ihrer
Entstehung (Korrektur vom 11.09.2026, siehe luecken_eines_werts).

Datenbasis: sieben Jahre Tageskerzen je Wert (seit 23.09.2026, Frage 115;
vorher 400 Tage).

FORTSCHREIBEN STATT NEU LADEN (26.09.2026, Peter: "frisst massig Zeit,
obwohl es immer nur um 1 Tag neuer wird"). Taeglich werden KEINE sieben
Jahre mehr bei Yahoo geholt. Stattdessen:
  - bestehende docs/luecken.csv lesen,
  - die neuen Tageskerzen aus docs/kursverlauf*.csv nehmen (holt das
    Screening ohnehin, gleiche ungeglaettete Kurse wie hier),
  - offene Luecken gegen die neuen Tage pruefen, neue Luecken der neuen Tage
    anhaengen, Alter um die Zahl neuer Tage erhoehen.
Stand je Wert (letzter verarbeiteter Tag) in state/luecken_stand.json.
Vollstaendig neu (sieben Jahre von Yahoo) wird gerechnet mit --voll, fuer
einen Wert ohne Stand oder ohne passende Kerzen im Kursverlauf, wenn die
Stand-Datei fehlt und wenn der letzte Vollabruf ("_voll" in der
Stand-Datei) sechs oder mehr Tage zurueckliegt - also einmal pro Woche. Das
faengt Aktiensplits und nachtraegliche Kurskorrekturen von Yahoo ab.

Ausgabe:
  docs/luecken.csv  - eine Zeile je Luecke, alle Werte
  docs/luecken.md   - Zusammenfassung je Wert (Schliessquote, Dauer)

Die Auswertung erfolgt AUSSCHLIESSLICH je Wert (Entscheidung 77) - es
gibt bewusst keine wertuebergreifenden Mediane oder Sammelklassen.
"""

import csv
import json
import os
import sys

import pandas as pd

import kurse
from marktdaten import UNIVERSUM

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CSV_AUS = os.path.join(DOCS, "luecken.csv")
MD_AUS = os.path.join(DOCS, "luecken.md")
STAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state", "luecken_stand.json")
FELDER = ["ticker", "name", "datum", "richtung", "kante", "eroeffnung", "groesse",
          "groesse_atr", "groesse_pct", "geschlossen", "tage_bis_schluss",
          "datum_schluss", "alter_tage", "reif"]

# Luecken unterhalb dieser Groesse werden ignoriert - sonst zaehlt jedes
# Eroeffnungsrauschen als Luecke. In ATR gemessen, damit der Wert fuer
# Zalando (ATR 0,59) und Broadcom (ATR 13,26) gleich streng wirkt.
MIN_ATR = 0.10

# Nur Luecken, die alt genug sind, um ueberhaupt schliessen zu koennen,
# gehen in die Schliessquote ein. Frische Luecken werden getrennt gezeigt.
REIFEZEIT_TAGE = 21

# Zeitraum der Kurshistorie (Frage 115, 23.09.2026: vorher "400d").
ZEITRAUM = "7y"

# Offene Luecken in luecken.md: nur die der letzten 364 Kalendertage.
ANZEIGE_TAGE = 364


def anhaengen(lang, neu):
    """Haengt an die lange Reihe nur die Tage aus 'neu' an, die NACH ihrem
    letzten Tag liegen. Die Historie bleibt so lang wie sie war."""
    spalten = ["Open", "High", "Low", "Close"]
    neu = neu[neu.index > lang.index[-1]]
    if neu.empty:
        return lang
    teil = neu[[c for c in lang.columns if c in neu.columns]]
    if not all(c in teil.columns for c in spalten):
        return lang
    return pd.concat([lang, teil]).sort_index()


def atr(df, n=14):
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vor = schluss.shift(1)
    spanne = pd.concat([hoch - tief, (hoch - vor).abs(), (tief - vor).abs()], axis=1).max(axis=1)
    return spanne.ewm(alpha=1 / n, adjust=False).mean()


def luecken_eines_werts(ticker, name, df, nur_nach=None):
    """Findet alle Luecken und prueft je Luecke, ob und wann sie schloss.
    nur_nach (JJJJ-MM-TT): nur Luecken, die NACH diesem Tag entstanden
    (Fortschreiben - die aelteren stehen schon in luecken.csv)."""
    if df is None or len(df) < 30:
        return []

    df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
    df["atr14"] = atr(df)

    zeilen = []
    hoch = df["High"].values
    tief = df["Low"].values
    offen = df["Open"].values
    atrw = df["atr14"].values
    daten = df.index

    for i in range(1, len(df)):
        if nur_nach is not None and daten[i].strftime("%Y-%m-%d") <= nur_nach:
            continue
        if pd.isna(atrw[i]) or atrw[i] <= 0:
            continue

        if offen[i] > hoch[i - 1]:
            richtung, kante, groesse = "aufwaerts", hoch[i - 1], offen[i] - hoch[i - 1]
        elif offen[i] < tief[i - 1]:
            richtung, kante, groesse = "abwaerts", tief[i - 1], tief[i - 1] - offen[i]
        else:
            continue

        groesse_atr = groesse / atrw[i]
        if groesse_atr < MIN_ATR:
            continue

        # Schliessung suchen - AB DEM ENTSTEHUNGSTAG SELBST, nicht erst ab
        # dem Folgetag.
        #
        # Korrektur vom 11.09.2026. Die alte Fassung startete bei i + 1 und
        # uebersah damit Luecken, die noch am Tag ihrer Entstehung wieder
        # zuliefen. Aufgefallen bei Intuitive Surgical: Der Wert eroeffnete
        # am 10.09.2026 bei 348,20 unter dem Vortagestief von 349,86, lief
        # dann aber bis 362,475 und hatte die Zone laengst durchschritten.
        # Die Datei fuehrte sie trotzdem als offen. Peter sah im Chart keine
        # Luecke und hatte recht.
        #
        # Betroffen sind ausschliesslich Luecken mit Alter 0 bis 1 - wer am
        # Entstehungstag nicht zurueckkommt, wird auch von der alten Logik
        # richtig erfasst. Die Folgen waren trotzdem spuerbar: solche
        # Scheinluecken tauchen dauerhaft als offen auf, verfaelschen die
        # Lueckenquote je Wert und landen als vermeintliches Kursziel oder
        # Risiko in jeder Kaufvorlage.
        #
        # tage_bis_schluss ist dann 0 - "am selben Tag geschlossen". Das ist
        # ein gueltiger Wert und kein Fehlen: die Quantile ueber
        # tage_bis_schluss (p75, p90) werden dadurch korrekt kleiner, statt
        # dass die Faelle ganz fehlen.
        # Am Entstehungstag genuegt dieselbe Pruefung wie an jedem anderen:
        # Hoch und Tief dieses Tages schliessen die Eroeffnung bereits ein,
        # ein Beruehren der Kante ist also zwangslaeufig eine Bewegung NACH
        # der Eroeffnung zurueck in die Luecke hinein. Eine Sonderbehandlung
        # fuer j == i braucht es deshalb nicht.
        geschlossen, tage_bis, datum_zu = 0, None, None
        for j in range(i, len(df)):
            beruehrt = ((tief[j] <= kante) if richtung == "aufwaerts"
                        else (hoch[j] >= kante))
            if beruehrt:
                geschlossen, tage_bis, datum_zu = 1, j - i, daten[j]
                break

        alter_tage = len(df) - 1 - i
        zeilen.append({
            "ticker": ticker,
            "name": name,
            "datum": daten[i].strftime("%Y-%m-%d"),
            "richtung": richtung,
            "kante": round(float(kante), 4),
            "eroeffnung": round(float(offen[i]), 4),
            "groesse": round(float(groesse), 4),
            "groesse_atr": round(float(groesse_atr), 3),
            "groesse_pct": round(float(groesse / kante * 100), 3),
            "geschlossen": geschlossen,
            "tage_bis_schluss": tage_bis if tage_bis is not None else "",
            "datum_schluss": datum_zu.strftime("%Y-%m-%d") if datum_zu is not None else "",
            "alter_tage": alter_tage,
            "reif": int(alter_tage >= REIFEZEIT_TAGE),
        })

    return zeilen


def lade_voll(ticker):
    """Sieben Jahre Tageskerzen von Yahoo (mit Frische-Pruefung), nur fertige Tage."""
    try:
        # Sieben Jahre statt 400 Tage (Frage 115, Peter 23.09.2026: "OK").
        # 400 Tage lieferten je Wert und Richtung oft nur eine Handvoll
        # reifer Luecken - zu duenn fuer p90-Fenster und die Frage "wie
        # viele schlossen noch, nachdem sie X Tage offen waren". Sieben
        # Jahre wie historie.py und markthistorie.py.
        #
        # Preis dafuer: der Cache-Schluessel in kurse.py enthaelt den
        # Zeitraum, marktdaten.py holt 400d - hier kommt also je Wert ein
        # zweiter Yahoo-Abruf dazu (eine Anfrage je Wert, nur mehr Zeilen).
        df = kurse.kerzen(ticker, period=ZEITRAUM)
    except Exception as fehler:
        print(f"  {ticker}: Abruf fehlgeschlagen ({fehler})")
        return None

    # Yahoo "erfolgreich" heisst nicht zwangslaeufig aktuell - siehe
    # marktdaten.py (01.09.2026, DAX+ASML blieben tagelang auf altem
    # Schluss haengen, ohne dass kerzen() je einen Fehler warf).
    # luecken.py hatte diese Pruefung bisher NICHT (Fund vom
    # 05.09.2026, Peters Frage nach der neuen Applied-Materials-
    # Luecke deckte auf, dass die Datei einen Tag zurueckhing).
    # Dieselbe Freshness-Pruefung wie in marktdaten.py: fuer DAX-Werte
    # und ASML zusaetzlich Stooq und Twelve Data einholen und die
    # insgesamt aktuellste Quelle nehmen.
    if df is not None and (ticker.endswith(".DE") or ticker == "ASML"):
        kandidaten_quellen = [("Yahoo", df)]
        df_stooq = kurse.kerzen_stooq(ticker)
        if df_stooq is not None:
            kandidaten_quellen.append(("Stooq", df_stooq))
        df_td = kurse.kerzen_twelvedata(ticker)
        if df_td is not None:
            kandidaten_quellen.append(("Twelve Data", df_td))
        bester_name, bestes_df = max(
            kandidaten_quellen, key=lambda x: x[1].index[-1])
        if bester_name != "Yahoo":
            print(f"  {ticker}: Yahoo veraltet ({df.index[-1].date()}), "
                  f"{bester_name} aktueller ({bestes_df.index[-1].date()}) "
                  f"- neuere Tage von {bester_name} angehaengt")
            # ANHAENGEN statt ersetzen (23.09.2026, mit Frage 115): Twelve
            # Data liefert nur 30 Tage. Die alte Fassung tauschte die ganze
            # Reihe aus und haette die sieben Jahre an einem solchen Tag
            # auf einen Monat geschrumpft - die Luecken-Statistik des
            # Werts waere fuer diesen Lauf praktisch leer gewesen.
            df = anhaengen(df, bestes_df)

    # NUR FERTIGE TAGESKERZEN (23.09.2026). Ein Lauf tagsueber (Fund:
    # Lauf 11:18 MESZ) nahm die halbfertige Kerze von heute mit - bei
    # DAX-Werten und Futures standen dadurch Luecken vom 23.09. aus
    # Vormittagskursen in luecken.csv. Dieselbe Grenze wie kurse.py:
    # der letzte Tag, dessen Handelsschluss (UTC) schon vorbei ist.
    # Rohstoffe/Devisen haben keinen Kalender - dort gilt 21 Uhr UTC.
    if df is not None and len(df):
        fertig = kurse.letzter_fertiger_tag(kurse.boerse(ticker))
        df = df[df.index.date <= fertig]
    return df


def werte():
    """(ticker, name) wie bisher: Aktien und Rohstoffe, Spot/Future ueber den Future."""
    aus = []
    for eintrag in UNIVERSUM:
        kandidaten, name, art = eintrag[0], eintrag[1], eintrag[2]
        # Bis 05.09.2026 stand hier `if art != "Aktie": continue` - dadurch
        # enthielt docs/luecken.csv NIE einen Rohstoff. Aufgefallen, als
        # Erdgas und Zucker erstmals als Block-1-Kandidaten auftauchten und
        # ihre Kaufvorlage bei den Luecken leer blieb. Rohstoffe sind laut
        # Merkregel 13 vollwertige Kaufkandidaten und brauchen dieselbe
        # Luecken-Statistik wie Aktien. Waehrungen (art "Spot") bleiben
        # draussen: EUR/USD ist kein Kaufkandidat.
        if art not in ("Aktie", "Future", "Spot/Future"):
            continue
        # Bei Rohstoffen mit Spot+Future-Kette (Gold, Silber, Platin,
        # Palladium) steht der Spot-Ticker vorn, der bei Yahoo unzuverlaessig
        # ist. marktdaten.csv arbeitet fuer diese Werte mit dem
        # Future-Ticker - der letzte Eintrag der Kette. Ohne diese Wahl
        # stuenden in luecken.csv Ticker (XAUUSD=X), die in marktdaten.csv
        # gar nicht vorkommen, und heute.py faende sie nicht wieder.
        if isinstance(kandidaten, (list, tuple)):
            ticker = kandidaten[-1] if art == "Spot/Future" else kandidaten[0]
        else:
            ticker = kandidaten
        aus.append((ticker, name))
    return aus


def kurz_kerzen():
    """Tageskerzen aus docs/kursverlauf*.csv als {ticker: DataFrame}."""
    teile = {}
    for spalte, datei in (("Open", "kursverlauf_eroeffnung.csv"), ("High", "kursverlauf_hoch.csv"),
                          ("Low", "kursverlauf_tief.csv"), ("Close", "kursverlauf.csv")):
        pfad = os.path.join(DOCS, datei)
        if not os.path.exists(pfad):
            return {}
        teile[spalte] = pd.read_csv(pfad, index_col=0)
    aus = {}
    for t in teile["Close"].index:
        if not all(t in teile[c].index for c in teile):
            continue
        df = pd.DataFrame({c: pd.to_numeric(teile[c].loc[t], errors="coerce") for c in teile})
        df.index = pd.to_datetime(df.index)
        aus[t] = df.dropna(subset=["Open", "High", "Low", "Close"])
    return aus


def fortschreiben(ticker, name, alte, bis, df):
    """Schreibt die Luecken eines Werts um die Tage nach 'bis' fort.
    alte: Zeilen aus luecken.csv (Texte). df: kurze Kerzenreihe, nur fertige
    Tage. Gibt (zeilen, neuer_stand) zurueck oder None, wenn die kurze Reihe
    den Stand-Tag nicht enthaelt (dann Vollabruf)."""
    tage = [d.strftime("%Y-%m-%d") for d in df.index]
    if bis not in tage:
        return None
    pos = tage.index(bis)
    neue_tage = tage[pos + 1:]
    if not neue_tage:
        return alte, bis
    hoch, tief = df["High"].values, df["Low"].values
    n = len(neue_tage)
    for z in alte:
        alter = int(z["alter_tage"])
        if str(z["geschlossen"]) != "1":
            kante = float(z["kante"])
            for k in range(1, n + 1):
                j = pos + k
                if (tief[j] <= kante) if z["richtung"] == "aufwaerts" else (hoch[j] >= kante):
                    z["geschlossen"], z["tage_bis_schluss"] = 1, alter + k
                    z["datum_schluss"] = tage[j]
                    break
        z["alter_tage"] = alter + n
        z["reif"] = int(alter + n >= REIFEZEIT_TAGE)
    neu = luecken_eines_werts(ticker, name, df, nur_nach=bis)
    return alte + neu, tage[-1]


def main():
    argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
    nur = argumente or None
    voll = "--voll" in sys.argv
    stand = {}
    heute = pd.Timestamp.utcnow().strftime("%Y-%m-%d")
    if os.path.exists(STAND) and os.path.exists(CSV_AUS) and not voll:
        with open(STAND, encoding="utf-8") as f:
            stand = json.load(f)
        zuletzt_voll = stand.pop("_voll", "")
        if not zuletzt_voll or (pd.Timestamp(heute) - pd.Timestamp(zuletzt_voll)).days >= 6:
            print(f"Letzter Vollabruf {zuletzt_voll or 'unbekannt'} - heute woechentlich komplett neu")
            voll, stand = True, {}
    else:
        voll = True
    bestand = {}
    if not voll:
        with open(CSV_AUS, encoding="utf-8", newline="") as f:
            for z in csv.DictReader(f):
                bestand.setdefault(z["ticker"], []).append(z)
    kurz = {} if voll else kurz_kerzen()
    print("Modus:", "VOLL (sieben Jahre von Yahoo)" if voll else "Fortschreiben aus kursverlauf")

    alle, neuer_stand, voll_geholt = [], dict(stand), []
    zuletzt_voll = heute if voll else zuletzt_voll
    for ticker, name in werte():
        if nur and ticker not in nur:
            alle.extend(bestand.get(ticker, []))
            continue
        ergebnis = None
        if not voll and ticker in stand and ticker in kurz:
            df = kurz[ticker]
            fertig = kurse.letzter_fertiger_tag(kurse.boerse(ticker))
            df = df[df.index.date <= fertig]
            ergebnis = fortschreiben(ticker, name, bestand.get(ticker, []), stand[ticker], df)
        if ergebnis is None:
            df = lade_voll(ticker)
            if df is None or not len(df):
                alle.extend(bestand.get(ticker, []))
                continue
            voll_geholt.append(ticker)
            zeilen, bis = luecken_eines_werts(ticker, name, df), df.index[-1].strftime("%Y-%m-%d")
        else:
            zeilen, bis = ergebnis
        neuer_stand[ticker] = bis
        alle.extend(zeilen)
    if not voll:
        print(f"  fortgeschrieben: {len(neuer_stand) - len(voll_geholt)} Werte, "
              f"voll geholt: {len(voll_geholt)} {' '.join(voll_geholt[:20])}")

    if not alle:
        print("Keine Luecken gefunden.")
        return

    os.makedirs(DOCS, exist_ok=True)
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER)
        w.writeheader()
        w.writerows(alle)
    os.makedirs(os.path.dirname(STAND), exist_ok=True)
    with open(STAND, "w", encoding="utf-8") as f:
        json.dump({"_voll": zuletzt_voll, **neuer_stand}, f, indent=0, sort_keys=True)
    print(f"Geschrieben: {CSV_AUS} ({len(alle)} Zeilen)")

    d = pd.DataFrame(alle)
    # Fortgeschriebene Zeilen kommen als Text aus luecken.csv - fuer die
    # Auswertung unten Zahlen draus machen (sonst gilt "1" != 1).
    for spalte in ("geschlossen", "alter_tage", "reif"):
        d[spalte] = pd.to_numeric(d[spalte], errors="coerce").astype(int)
    with open(MD_AUS, "w", encoding="utf-8") as f:
        f.write("# Kursluecken je Wert\n\n")
        f.write(f"_Datenbasis {ZEITRAUM.replace('y', ' Jahre')} Tageskerzen je Wert. Mindestgroesse {MIN_ATR} ATR. Als 'reif' gilt eine Luecke ab "
                f"{REIFEZEIT_TAGE} Handelstagen Alter - nur reife Luecken gehen in "
                f"die Schliessquote ein._\n\n")
        f.write("Aufwaerts- und Abwaerts-Luecken werden getrennt ausgewiesen: eine "
                "Aufwaerts-Luecke schliesst sich, wenn der Kurs FAELLT (Risiko fuer "
                "eine Long-Position), eine Abwaerts-Luecke, wenn er STEIGT (Kursziel "
                "fuer eine Long-Position). Beides zusammenzuwerfen verwischt genau "
                "diesen Unterschied.\n\n")

        for richtung, ueberschrift in [("aufwaerts", "Aufwaerts-Luecken (schliessen bei fallendem Kurs)"),
                                       ("abwaerts", "Abwaerts-Luecken (schliessen bei steigendem Kurs)")]:
            f.write(f"## {ueberschrift}\n\n")
            f.write("| Wert | reif | geschlossen | Quote | Median Tage | p75 | p90 | offen |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for ticker, teil in d[d["richtung"] == richtung].groupby("ticker"):
                reif = teil[teil["reif"] == 1]
                if reif.empty:
                    continue
                zu = reif[reif["geschlossen"] == 1]
                tage = pd.to_numeric(zu["tage_bis_schluss"], errors="coerce")
                med = f"{tage.median():.0f}" if len(zu) else "-"
                p75 = f"{tage.quantile(0.75):.0f}" if len(zu) else "-"
                p90 = f"{tage.quantile(0.90):.0f}" if len(zu) else "-"
                f.write(f"| {teil['name'].iloc[0]} ({ticker}) | {len(reif)} | {len(zu)} | "
                        f"{100*len(zu)/len(reif):.0f}% | {med} | {p75} | {p90} | "
                        f"{len(reif)-len(zu)} |\n")
            f.write("\n")

        # Kernfrage bei einer konkreten offenen Luecke: sie ist SCHON X Tage offen -
        # wie viele vergleichbare Luecken wurden danach ueberhaupt noch geschlossen?
        # Die Gesamtquote taugt dafuer nicht, weil die meisten Luecken am ersten Tag
        # schliessen und die Quote nach oben ziehen.
        f.write("## Schliesst eine Luecke noch, die schon laenger offen ist?\n\n")
        f.write("_Je Wert und Richtung: von den Luecken, die nach X Tagen noch offen "
                "waren, wurden spaeter noch so viele geschlossen._\n\n")
        f.write("| Wert | Richtung | noch offen nach 5T | nach 21T | nach 63T |\n")
        f.write("|---|---|---|---|---|\n")
        for (ticker, richtung), teil in d.groupby(["ticker", "richtung"]):
            reif = teil[teil["reif"] == 1]
            if len(reif) < 5:
                continue
            zeile = f"| {teil['name'].iloc[0]} ({ticker}) | {richtung} "
            for schwelle in (5, 21, 63):
                # Nur Luecken, die alt genug sind, um die Schwelle beurteilen zu koennen
                pruefbar = reif[reif["alter_tage"] >= schwelle]
                tage = pd.to_numeric(pruefbar["tage_bis_schluss"], errors="coerce")
                noch_offen = pruefbar[tage.isna() | (tage > schwelle)]
                if len(noch_offen) == 0:
                    zeile += "| keine Faelle "
                    continue
                spaeter_zu = noch_offen[noch_offen["geschlossen"] == 1]
                zeile += (f"| {len(spaeter_zu)}/{len(noch_offen)} "
                          f"({100*len(spaeter_zu)/len(noch_offen):.0f}%) ")
            f.write(zeile + "|\n")

        # Nur offene Luecken der letzten 364 Kalendertage anzeigen (Peter
        # 23.09.2026) - die Statistik oben nutzt alle sieben Jahre.
        ab = (pd.Timestamp.today().normalize()
              - pd.Timedelta(days=ANZEIGE_TAGE)).strftime("%Y-%m-%d")
        f.write(f"\n## Offene Luecken je Wert (entstanden in den letzten {ANZEIGE_TAGE} Tagen)\n\n")
        offen = d[(d["geschlossen"] == 0) & (d["datum"] >= ab)]
        if offen.empty:
            f.write("_Keine offenen Luecken._\n")
        else:
            f.write("| Wert | Datum | Richtung | Kante | Groesse ATR | Groesse % | Alter (Tage) |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for _, z in offen.sort_values(["ticker", "datum"]).iterrows():
                f.write(f"| {z['name']} ({z['ticker']}) | {z['datum']} | {z['richtung']} | "
                        f"{z['kante']} | {z['groesse_atr']} | {z['groesse_pct']} | {z['alter_tage']} |\n")
    print(f"Geschrieben: {MD_AUS}")


if __name__ == "__main__":
    main()
