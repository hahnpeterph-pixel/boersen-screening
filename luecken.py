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
geschlossen, sobald sie intraday beruehrt wurde.

Ausgabe:
  docs/luecken.csv  - eine Zeile je Luecke, alle Werte
  docs/luecken.md   - Zusammenfassung je Wert (Schliessquote, Dauer)

Die Auswertung erfolgt AUSSCHLIESSLICH je Wert (Entscheidung 77) - es
gibt bewusst keine wertuebergreifenden Mediane oder Sammelklassen.
"""

import csv
import os
import sys

import pandas as pd

import kurse
from marktdaten import UNIVERSUM

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CSV_AUS = os.path.join(DOCS, "luecken.csv")
MD_AUS = os.path.join(DOCS, "luecken.md")

# Luecken unterhalb dieser Groesse werden ignoriert - sonst zaehlt jedes
# Eroeffnungsrauschen als Luecke. In ATR gemessen, damit der Wert fuer
# Zalando (ATR 0,59) und Broadcom (ATR 13,26) gleich streng wirkt.
MIN_ATR = 0.10

# Nur Luecken, die alt genug sind, um ueberhaupt schliessen zu koennen,
# gehen in die Schliessquote ein. Frische Luecken werden getrennt gezeigt.
REIFEZEIT_TAGE = 21


def atr(df, n=14):
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vor = schluss.shift(1)
    spanne = pd.concat([hoch - tief, (hoch - vor).abs(), (tief - vor).abs()], axis=1).max(axis=1)
    return spanne.ewm(alpha=1 / n, adjust=False).mean()


def luecken_eines_werts(ticker, name, df):
    """Findet alle Luecken und prueft je Luecke, ob und wann sie schloss."""
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

        # Ab dem Folgetag suchen: schliesst der Kurs die Luecke wieder?
        geschlossen, tage_bis, datum_zu = 0, None, None
        for j in range(i + 1, len(df)):
            beruehrt = (tief[j] <= kante) if richtung == "aufwaerts" else (hoch[j] >= kante)
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


def main():
    nur = sys.argv[1:] if len(sys.argv) > 1 else None
    alle = []

    for eintrag in UNIVERSUM:
        kandidaten, name, art = eintrag[0], eintrag[1], eintrag[2]
        if art != "Aktie":
            continue
        ticker = kandidaten[0] if isinstance(kandidaten, (list, tuple)) else kandidaten
        if nur and ticker not in nur:
            continue

        try:
            # 400d wie marktdaten.py und kursverlauf.py - NICHT aendern:
            # der Cache-Schluessel in kurse.py enthaelt den Zeitraum. Ein
            # abweichender Wert (etwa 800d) laesst alle Werte ein zweites
            # Mal bei Yahoo abrufen, statt den vorhandenen Cache zu nutzen.
            # Rund anderthalb Jahre reichen fuer die Luecken-Statistik.
            df = kurse.kerzen(ticker, period="400d")
        except Exception as fehler:
            print(f"  {ticker}: Abruf fehlgeschlagen ({fehler})")
            continue

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
                      f"- {bester_name} verwendet")
                df = bestes_df

        zeilen = luecken_eines_werts(ticker, name, df)
        alle.extend(zeilen)
        reif = [z for z in zeilen if z["reif"]]
        zu = sum(z["geschlossen"] for z in reif)
        quote = f"{100*zu/len(reif):.0f}%" if reif else "keine reifen Faelle"
        print(f"  {ticker}: {len(zeilen)} Luecken, davon reif {len(reif)}, geschlossen {quote}")

    if not alle:
        print("Keine Luecken gefunden.")
        return

    os.makedirs(DOCS, exist_ok=True)
    with open(CSV_AUS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(alle[0].keys()))
        w.writeheader()
        w.writerows(alle)
    print(f"Geschrieben: {CSV_AUS} ({len(alle)} Zeilen)")

    d = pd.DataFrame(alle)
    with open(MD_AUS, "w", encoding="utf-8") as f:
        f.write("# Kursluecken je Wert\n\n")
        f.write(f"_Mindestgroesse {MIN_ATR} ATR. Als 'reif' gilt eine Luecke ab "
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

        f.write("\n## Offene Luecken je Wert\n\n")
        offen = d[d["geschlossen"] == 0]
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
