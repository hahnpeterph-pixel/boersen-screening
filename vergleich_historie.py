"""vergleich_historie.py - Sind die alten Jahre fuer heute noch aussagekraeftig? (Version 1, 27.09.2026)

Peter 27.09.2026: "Inwiefern waere es sinnvoll, den Betrachtungszeitraum von sieben Jahren
(deutlich) zu erhoehen? Ist die aeltere Historie noch aussagekraeftig fuer aktuell?"

Laedt 20 Jahre Tageskerzen fuer dasselbe Universum wie historie.py, sucht die Tiefs mit
DENSELBEN Regeln (historie.faelle_je_wert, unveraendert importiert) und vergleicht die
Halteraten (63 Handelstage) zwischen
    ALT = Tiefs vor dem 27.09.2019   und   NEU = Tiefs ab dem 27.09.2019 (= heutige 7 Jahre).

Schreibt NUR nach docs/vergleich/ - keine bestehende Datei wird angefasst, das taegliche
Screening bleibt unberuehrt:
    docs/vergleich/historie_20j.md       Vergleichsbericht
    docs/vergleich/faelle_20j.csv.gz     alle Tief-Faelle (auch fuer die spaetere Monats-Auswertung
                                         Ziel zuerst / KO zuerst: Tage bis Bruch je Puffer, Tage bis Ziel)

Aufruf: python vergleich_historie.py [--jahre 20]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import historie as H

AUS = H.DOCS / "vergleich"
GRENZE = pd.Timestamp("2019-09-27")
PUFFER_VGL = (1.0, 2.0, 3.0, 4.0)
BLOECKE = [(2006, 2008), (2009, 2011), (2012, 2014), (2015, 2017), (2018, 2020), (2021, 2023), (2024, 2026)]


def hr(df: pd.DataFrame, p: float) -> tuple[float | None, int]:
    g = df[df.beobachtet >= H.QUARTAL]
    if len(g) == 0:
        return None, 0
    return float((g.benoetigt_atr <= p + 1e-9).mean() * 100), len(g)


def fmt(v: float | None) -> str:
    return "–" if v is None else f"{v:.0f} %".replace(".", ",")


def main() -> int:
    jahre = 20
    if "--jahre" in sys.argv:
        jahre = int(sys.argv[sys.argv.index("--jahre") + 1])
    tickers = H.universum()
    # "max" statt "20y": Yahoo kennt feste Zeitraeume sicher; danach auf die letzten N Jahre kuerzen.
    roh = H.kurse.kerzen_batch(tickers, period="max", auto_adjust=True)
    ab = pd.Timestamp.today().normalize() - pd.DateOffset(years=jahre)
    daten = {}
    for t, d in roh.items():
        d = d[d.index.tz_localize(None) >= ab] if getattr(d.index, "tz", None) else d[d.index >= ab]
        if len(d) > 120:
            daten[t] = d
    print(f"{len(daten)} Werte mit Kursdaten.")
    alle: list[dict] = []
    for t, df in daten.items():
        try:
            alle += H.faelle_je_wert(t, df)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {t}: {exc}")
    fest = [f for f in alle if not f["laufend"]]
    if not fest:
        print("Keine Faelle - Abbruch.")
        return 1

    zeilen = []
    for f in fest:
        z = {k: f[k] for k in ("ticker", "datum", "position", "serie_laenge", "beobachtet",
                                "benoetigt_atr", "benoetigt_ganz_atr", "resthistorie", "einstieg")}
        for p, tg in f["tage_bis_bruch"].items():
            z[f"bruch_{p:g}"] = tg
        for zz, tg in f["tage_bis_ziel"].items():
            z[f"ziel_{zz:g}"] = tg
        zeilen.append(z)
    F = pd.DataFrame(zeilen)
    F["datum"] = pd.to_datetime(F["datum"])
    AUS.mkdir(parents=True, exist_ok=True)
    F.to_csv(AUS / "faelle_20j.csv.gz", index=False, compression="gzip")

    alt, neu = F[F.datum < GRENZE], F[F.datum >= GRENZE]
    start = {t: df.index[0] for t, df in daten.items()}
    lang = sum(1 for d in start.values() if d <= pd.Timestamp("2008-01-01"))

    md = [f"# Vergleich Historie ALT (vor 27.09.2019) gegen NEU (ab 27.09.2019) – {jahre} Jahre",
          "",
          f"Stand {pd.Timestamp.today():%d.%m.%Y}. Werte mit Kursdaten: {len(daten)}, davon {lang} mit Daten ab 2008 oder früher.",
          f"Tief-Fälle (abgeschlossen): ALT {len(alt)} · NEU {len(neu)}. Halterate = Anteil der Fälle, die in 63 Handelstagen "
          "nicht tiefer als der Puffer unter das Tief liefen (normale ATR, wie Spalte „Tief N“).",
          "",
          "## 1. Halterate je Tiefposition",
          "",
          "| Position | Fälle ALT | Fälle NEU | " + " | ".join(f"{p:g} ATR ALT | {p:g} ATR NEU" for p in PUFFER_VGL) + " |",
          "|---|---|---|" + "---|---|" * len(PUFFER_VGL)]
    for name, sel in [("Tief 2", lambda d: d.position == 2), ("Tief 3", lambda d: d.position == 3),
                      ("Tief 4", lambda d: d.position == 4), ("Tief 5+", lambda d: d.position >= 5),
                      ("alle ab Tief 2", lambda d: d.position >= 2)]:
        a, n = alt[sel(alt)], neu[sel(neu)]
        cells = []
        for p in PUFFER_VGL:
            cells += [fmt(hr(a, p)[0]), fmt(hr(n, p)[0])]
        md.append(f"| {name} | {hr(a, 1)[1]} | {hr(n, 1)[1]} | " + " | ".join(cells) + " |")

    md += ["", "## 2. Halterate je Dreijahres-Block (ab Tief 2)", "",
           "| Block | Fälle | " + " | ".join(f"{p:g} ATR" for p in PUFFER_VGL) + " |",
           "|---|---|" + "---|" * len(PUFFER_VGL)]
    ab2 = F[F.position >= 2]
    for von, bis in BLOECKE:
        g = ab2[(ab2.datum.dt.year >= von) & (ab2.datum.dt.year <= bis)]
        md.append(f"| {von}–{bis} | {hr(g, 1)[1]} | " + " | ".join(fmt(hr(g, p)[0]) for p in PUFFER_VGL) + " |")

    md += ["", "## 3. Je Wert: weicht ALT von NEU ab? (ab Tief 2, nur Werte mit mind. 5 Fällen in beiden Zeiträumen)", ""]
    rows = []
    for t in sorted(F.ticker.unique()):
        a, n = alt[(alt.ticker == t) & (alt.position >= 2)], neu[(neu.ticker == t) & (neu.position >= 2)]
        if hr(a, 1)[1] < 5 or hr(n, 1)[1] < 5:
            continue
        r = {"ticker": t, "n_alt": hr(a, 1)[1], "n_neu": hr(n, 1)[1]}
        for p in (2.0, 3.0):
            r[f"alt_{p:g}"], r[f"neu_{p:g}"] = hr(a, p)[0], hr(n, p)[0]
            r[f"diff_{p:g}"] = r[f"alt_{p:g}"] - r[f"neu_{p:g}"]
        rows.append(r)
    W = pd.DataFrame(rows)
    if len(W):
        for p in (2.0, 3.0):
            d = W[f"diff_{p:g}"]
            md.append(f"- **{p:g} ATR:** {len(W)} Werte · Abweichung ALT minus NEU im Median {d.median():+.0f} Punkte · "
                      f"innerhalb ±10 Punkte: {(d.abs() <= 10).mean() * 100:.0f} % der Werte · "
                      f"innerhalb ±20 Punkte: {(d.abs() <= 20).mean() * 100:.0f} % · "
                      f"ALT besser: {(d > 0).sum()} · NEU besser: {(d < 0).sum()}")
        W.round(1).to_csv(AUS / "je_wert_20j.csv", index=False)
        md += ["", "Einzelwerte: `docs/vergleich/je_wert_20j.csv`."]
    else:
        md.append("Zu wenige Werte mit Fällen in beiden Zeiträumen.")

    md += ["", "## 4. Fallzahlen je Wert (ab Tief 2): 7 Jahre gegen 20 Jahre", ""]
    n7 = neu[neu.position >= 2].groupby("ticker").size()
    n20 = F[F.position >= 2].groupby("ticker").size()
    md.append(f"- Median Fälle je Wert: 7 Jahre {n7.median():.0f} · 20 Jahre {n20.median():.0f}")

    (AUS / "historie_20j.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
