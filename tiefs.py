"""
tiefs.py - Markante Tiefs, Volumen und Pruefung der eigenen Kaufregel.

Laeuft unabhaengig von screener.py im selben GitHub-Workflow.
Schreibt docs/tiefs.md

KAUFREGEL (die eigentliche Aufgabe dieses Skripts):
Die Knock-out-Schwelle des Scheins soll UNTER einem markanten Tief des
Basiswerts liegen - mit etwas Abstand, damit ein erneuter Test dieses
Tiefs den Schein nicht sofort ausknockt.

Definition markantes Tief (Swing-Tief):
Ein Handelstag, dessen Tagestief niedriger ist als das Tagestief der
LINKS Tage davor UND der RECHTS Tage danach. Der laufende Tag zaehlt nie
mit, weil noch offen ist, ob ein Tief haelt.

Geprueft wird gegen zwei Bezugspunkte:
  - juengstes bestaetigtes Swing-Tief  (aktuelle Trendstruktur)
  - tiefstes Tief im Fenster           (strengerer Massstab)
Das Gesamturteil richtet sich nach dem STRENGEREN der beiden.

Konfiguration in watchlist.json.
"""

import json
import os
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

HIER = os.path.dirname(os.path.abspath(__file__))
WATCHLIST = os.path.join(HIER, "watchlist.json")
AUSGABE = os.path.join(HIER, "docs", "tiefs.md")

STANDARD = {
    "fenster_tage": 50,
    "links": 3,
    "rechts": 3,
    "atr_tage": 14,
    "puffer_atr": 2.0,
    "knapp_ab_atr": 1.0,
    "mindestabstand_absolut": 1.0,
    "bezug": "juengstes",
    "unbestaetigtes_tief_zulassen": True,
    "einheit_euro": 150.0,
    "min_einsatz_euro": 50.0,
    "werte": [],
}


def konfig_laden():
    if not os.path.exists(WATCHLIST):
        print(f"WARNUNG: {WATCHLIST} fehlt - nichts zu tun.")
        return STANDARD
    with open(WATCHLIST, encoding="utf-8") as f:
        k = json.load(f)
    for schluessel, wert in STANDARD.items():
        k.setdefault(schluessel, wert)
    return k


def kerzen_laden(ticker, tage):
    zeitraum = f"{max(int(tage * 2.0), 120)}d"
    try:
        df = yf.Ticker(ticker).history(period=zeitraum, interval="1d",
                                       auto_adjust=False)
    except Exception as e:
        print(f"  {ticker}: Abruf fehlgeschlagen ({e})")
        return None
    if df is None or df.empty or "Low" not in df.columns:
        print(f"  {ticker}: keine Daten")
        return None
    df = df.dropna(subset=["Low"])
    if df.empty:
        return None
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def swing_tiefs(df, links, rechts, fenster_tage, unbestaetigt=False):
    """Alle Swing-Tiefs im Fenster, juengstes zuerst.

    unbestaetigt=True nimmt zusaetzlich das Tief des zuletzt abgeschlossenen
    Tages auf, wenn es unter den LINKS Tagen davor liegt - auch ohne die
    sonst noetigen RECHTS Bestaetigungstage. Solche Eintraege sind mit
    "bestaetigt": False markiert.
    """
    if df is None or len(df) < links + rechts + 2:
        return []
    lows = df["Low"].values
    daten = df.index
    vols = df["Volume"].values if "Volume" in df.columns else [None] * len(df)
    grenze = daten[-1] - pd.Timedelta(days=fenster_tage)

    treffer = []
    for i in range(links, len(df) - rechts):
        if daten[i] < grenze:
            continue
        wert = lows[i]
        if all(lows[i - j] > wert for j in range(1, links + 1)) and \
           all(lows[i + j] > wert for j in range(1, rechts + 1)):
            v = vols[i]
            treffer.append({
                "datum": daten[i],
                "tief": float(wert),
                "volumen": None if v is None or pd.isna(v) else int(v),
                "index": i,
                "bestaetigt": True,
            })

    if unbestaetigt:
        i = len(df) - 1
        wert = lows[i]
        schon_da = any(t["index"] == i for t in treffer)
        if not schon_da and i >= links and daten[i] >= grenze and \
           all(lows[i - j] > wert for j in range(1, links + 1)):
            v = vols[i]
            treffer.append({
                "datum": daten[i],
                "tief": float(wert),
                "volumen": None if v is None or pd.isna(v) else int(v),
                "index": i,
                "bestaetigt": False,
            })

    treffer.sort(key=lambda t: t["datum"], reverse=True)
    return treffer


def atr(df, tage=14):
    """Average True Range - mittlere Tagesschwankung inkl. Kursluecken."""
    if df is None or len(df) < tage + 1:
        return None
    hoch, tief, schluss = df["High"], df["Low"], df["Close"]
    vortag = schluss.shift(1)
    tr = pd.concat([hoch - tief, (hoch - vortag).abs(), (tief - vortag).abs()],
                   axis=1).max(axis=1)
    wert = tr.tail(tage).mean()
    return None if pd.isna(wert) else float(wert)


def durchschnittsvolumen(df, bis_index, tage=20):
    if "Volume" not in df.columns:
        return None
    teil = df["Volume"].iloc[max(0, bis_index - tage):bis_index].dropna()
    return None if teil.empty else float(teil.mean())


def abstand(tief, ko):
    """Wie weit liegt der KO unter dem Tief? Positiv = KO darunter = gut."""
    if tief is None or ko is None or tief == 0:
        return None
    return (tief - ko) / tief * 100.0


def urteil(einheiten, soll, knapp):
    """einheiten = Abstand KO zum Tief, gemessen in ATR."""
    if einheiten is None:
        return "k.A."
    if einheiten < 0:
        return "REGELBRUCH (KO ueber Tief)"
    if einheiten < knapp:
        return "zu knapp"
    if einheiten < soll:
        return "knapp"
    return "OK"


def ampel(einheiten, soll, knapp):
    if einheiten is None:
        return "-"
    if einheiten < 0:
        return "X"
    if einheiten < knapp:
        return "!!"
    if einheiten < soll:
        return "!"
    return "+"


def einsatz(einheiten, soll, einheit, minimum, regel1_ok):
    """Regel 2+3: Mindesteinsatz bei Puffer ~0, volle Einheit ab SOLL x ATR,
    dazwischen linear."""
    if not regel1_ok:
        return 0.0, 0.0, "Regel 1 verletzt - kein Kauf"
    if einheiten is None:
        return None, None, "keine ATR-Daten"
    faktor = max(0.0, min(1.0, einheiten / soll))
    betrag = round(minimum + (einheit - minimum) * faktor, 2)
    return betrag, faktor, ""


def de(x, nk=2):
    if x is None:
        return "k.A."
    return f"{x:,.{nk}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def stk(x):
    if x is None:
        return "k.A."
    if x >= 1_000_000:
        return de(x / 1_000_000, 1) + " Mio."
    return de(x / 1_000, 0) + " Tsd."


def main():
    k = konfig_laden()
    werte = k["werte"]
    if not werte:
        print("Keine Werte in watchlist.json - Abbruch.")
        return

    soll = float(k["puffer_atr"])
    knapp = float(k["knapp_ab_atr"])
    atr_tage = int(k["atr_tage"])
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    kopf = [
        "# Tiefs, Volumen und Kaufregel-Check",
        "",
        f"_Erstellt {jetzt}. Fenster: letzte {k['fenster_tage']} Kalendertage. "
        f"Ein Swing-Tief ist ein Tag, dessen Tagestief unter dem der "
        f"{k['links']} Tage davor und der {k['rechts']} Tage danach liegt. "
        f"Der laufende Tag zaehlt nie mit._",
        "",
        "## Kaufregel",
        "",
        f"Die Knock-out-Schwelle soll **unter** einem markanten Tief liegen, mit "
        f"mindestens **{de(soll, 1)} x ATR({atr_tage})** Abstand. Die ATR ist die "
        f"mittlere Tagesschwankung des Basiswerts - ein fester Prozentsatz taugt "
        f"nicht, weil er bei ruhigen und bei volatilen Werten voellig "
        f"Unterschiedliches bedeutet.",
        "",
        "Geprueft wird gegen zwei Bezugspunkte: das **juengste bestaetigte** "
        "Swing-Tief (aktuelle Trendstruktur) und das **tiefste** Tief im Fenster "
        "(strenger Massstab). Das Urteil richtet sich nach dem strengeren.",
        "",
        ("_Als juengstes Tief zaehlt auch das Tief des zuletzt abgeschlossenen "
         "Tages, sofern es unter den Vortagen liegt - im Report mit 'unbest.' "
         "markiert, weil die Bestaetigung durch Folgetage noch aussteht._"
         if k.get("unbestaetigtes_tief_zulassen", True) else
         "_Es zaehlen nur durch Folgetage bestaetigte Tiefs._"),
        "",
        f"**Regel 1 (harte Sperre):** Der KO muss mindestens "
        f"{de(k['mindestabstand_absolut'], 2)} unter dem Tief liegen - in der "
        f"Waehrung des Basiswerts. Verhindert nur, dass der KO auf dem Tief "
        f"klebt; als alleiniges Mass taugt sie nicht.",
        "",
        f"**Regel 2+3 (Positionsgroesse):** {de(k['min_einsatz_euro'], 0)} EUR bei "
        f"gerade noch erfuelltem Puffer, {de(k['einheit_euro'], 0)} EUR ab "
        f"{de(soll, 1)} x ATR, dazwischen linear. Bezugstief ist das "
        f"**{k.get('bezug', 'juengstes')}** Tief.",
        "",
        "### Bestehende Positionen",
        "",
        "| Wert | KO | juengstes Tief | tiefstes Tief | Abstand | Regel 1 | Urteil | |",
        "|---|---|---|---|---|---|---|---|",
    ]

    empfehlung = [
        "", "### Empfohlene KO-Schwelle", "",
        f"Tief minus {de(soll, 1)} x ATR. Die Hebelangabe ist das, was sich bei diesem "
        f"KO rechnerisch ergibt - sie zeigt, welchen Hebel deine eigene Regel "
        f"zulaesst.",
        "",
        "| Wert | Kurs | ATR | nach Trendtief | Hebel | konservativ | Hebel |",
        "|---|---|---|---|---|---|---|",
    ]

    groesse = [
        "", "### Positionsgroesse nach Regel 2", "",
        "| Wert | Bezugstief | Puffer | Faktor | Einsatz | Hinweis |",
        "|---|---|---|---|---|---|",
    ]

    detail = ["", "## Tiefs im Detail mit Volumen", "",
              "| Wert | Datum | Tief | Volumen | rel. zu \u00d8 20 T | Tief -> KO |",
              "|---|---|---|---|---|---|"]
    warnungen = []
    fehlend = []

    for eintrag in werte:
        ticker = eintrag["ticker"]
        name = eintrag.get("name", ticker)
        ko = eintrag.get("ko")
        art = eintrag.get("typ", "Bestand")
        etikett = f"{name} ({ticker})" + ("" if art == "Bestand" else f" _{art}_")
        print(f"{ticker} ...")

        df = kerzen_laden(ticker, k["fenster_tage"])
        treffer = swing_tiefs(df, k["links"], k["rechts"], k["fenster_tage"],
                              bool(k.get("unbestaetigtes_tief_zulassen", True)))
        a = atr(df, atr_tage)
        kurs = float(df["Close"].iloc[-1]) if df is not None and len(df) else None

        if not treffer:
            kopf.append(f"| {etikett} | {de(ko)} | kein Swing-Tief im Fenster "
                        f"| | | - | k.A. | - |")
            fehlend.append(
                f"- **{name}**: kein bestaetigtes Swing-Tief im Fenster. Entweder "
                f"laeuft der Wert seit Wochen aufwaerts, oder `links`/`rechts` "
                f"sind zu gross eingestellt.")
            continue

        juengstes = treffer[0]
        tiefstes = min(treffer, key=lambda t: t["tief"])
        bezug = juengstes if k.get("bezug", "juengstes") == "juengstes" else tiefstes

        def in_atr(tief):
            if a in (None, 0) or ko is None:
                return None
            return (tief - ko) / a

        e_neu, e_tief = in_atr(juengstes["tief"]), in_atr(tiefstes["tief"])
        massgeblich = in_atr(bezug["tief"])

        mind_abs = float(k["mindestabstand_absolut"])
        regel1 = None if ko is None else (bezug["tief"] - ko) >= mind_abs
        r1txt = "-" if regel1 is None else ("erfuellt" if regel1 else "VERLETZT")

        kopf.append(
            f"| {etikett} | {de(ko)} | {de(juengstes['tief'])} "
            f"({juengstes['datum']:%d.%m.}"
            f"{'' if juengstes.get('bestaetigt', True) else ', unbest.'}) | "
            f"{de(tiefstes['tief'])} "
            f"({tiefstes['datum']:%d.%m.}) | "
            f"{de(massgeblich, 1) + ' x ATR' if massgeblich is not None else 'k.A.'} | "
            f"{r1txt} | "
            f"{urteil(massgeblich, soll, knapp)} | "
            f"{ampel(massgeblich, soll, knapp)} |")

        betrag, faktor, hinweis = einsatz(
            massgeblich, soll, float(k["einheit_euro"]),
            float(k["min_einsatz_euro"]), regel1 is not False)
        groesse.append(
            f"| {etikett} | {de(bezug['tief'])} ({bezug['datum']:%d.%m.}"
            f"{'' if bezug.get('bestaetigt', True) else ', unbest.'}) | "
            f"{de(massgeblich, 2) + ' x ATR' if massgeblich is not None else 'k.A.'} | "
            f"{de(faktor, 2) if faktor is not None else '-'} | "
            f"**{de(betrag, 2) if betrag is not None else 'k.A.'} EUR** | "
            f"{hinweis if hinweis else 'kaufbar'} |")

        if massgeblich is not None and massgeblich < knapp:
            warnungen.append(
                f"- **{name}**: Die KO-Schwelle {de(ko)} liegt nur "
                f"{de(massgeblich, 2)} x ATR unter dem Tief {de(bezug['tief'])} "
                f"vom {bezug['datum']:%d.%m.%Y}. Nach Regel 2 bedeutet das "
                f"reduzierten Einsatz, kein Ausschluss.")

        if a and kurs:
            def vorschlag(tief):
                empf = tief - soll * a
                if empf <= 0 or kurs <= empf:
                    return "-", "-"
                hebel = kurs / (kurs - empf)
                return de(empf), de(hebel, 1) + "x"
            k_neu, h_neu = vorschlag(juengstes["tief"])
            k_alt, h_alt = vorschlag(tiefstes["tief"])
            empfehlung.append(
                f"| {etikett} | {de(kurs)} | {de(a)} | {k_neu} | {h_neu} | "
                f"{k_alt} | {h_alt} |")

        for t in treffer[:3]:
            avg = durchschnittsvolumen(df, t["index"], 20)
            rel = (t["volumen"] / avg) if (avg and t["volumen"]) else None
            if rel is None:
                relt = "k.A."
            elif rel >= 1.5:
                relt = f"{de(rel)}x (Kapitulation)"
            elif rel >= 1.2:
                relt = f"{de(rel)}x (erhoeht)"
            elif rel >= 0.8:
                relt = f"{de(rel)}x"
            else:
                relt = f"{de(rel)}x (duenn)"
            ab = abstand(t["tief"], ko)
            detail.append(
                f"| {etikett} | {t['datum']:%d.%m.%Y} | {de(t['tief'])} | "
                f"{stk(t['volumen'])} | {relt} | "
                f"{de(ab, 1) + ' %' if ab is not None else '-'} |")

    zeilen = kopf
    zeilen += ["", f"_Legende: `+` erfuellt (ab {de(soll,1)} x ATR), `!` knapp, "
                   f"`!!` zu knapp (unter {de(knapp,1)} x ATR), `X` Regelbruch._"]
    if warnungen:
        zeilen += ["", "## Achtung", ""] + warnungen
    if fehlend:
        zeilen += ["", "## Ohne Befund", ""] + fehlend
    zeilen += groesse
    zeilen += ["", "_Einsatz inklusive Ordergebuehr. Das tiefste Tief des Fensters "
                   "steht in der Tabelle oben weiterhin zur Einordnung, geht aber "
                   "nicht in die Bewertung ein._"]
    zeilen += empfehlung
    zeilen += ["", "_'nach Trendtief' orientiert sich am juengsten Tief und laesst "
                   "mehr Hebel zu. 'konservativ' orientiert sich am tiefsten Tief "
                   "des Fensters und ueberlebt auch einen Rueckfall dorthin._"]
    zeilen += detail
    zeilen += [
        "",
        "---",
        "",
        "_Automatisch erzeugt. Kursdaten von Yahoo Finance ueber yfinance. "
        "Volumen ist das Tagesvolumen der jeweiligen Referenzboerse. "
        "Keine Anlageberatung._",
    ]

    os.makedirs(os.path.dirname(AUSGABE), exist_ok=True)
    with open(AUSGABE, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")
    print(f"Geschrieben: {AUSGABE}")


if __name__ == "__main__":
    main()
