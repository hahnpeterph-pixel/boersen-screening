"""datenpruefung.py - Pruefung aller Kursdaten vor jeder Auswertung (03.10.2026, Peter: "Wenn alles vorliegt,
pruefst du die Daten doch. Und erst dann wertest du aus. Und wenn Fehler vorhanden sind, muessen die sofort
korrigiert werden").

Prueft docs/kursverlauf* (alle Werte, alle Tage) und docs/kerzen/tag*.csv.gz:
  - Platzhalter-Kerzen (Eroeffnung = Hoch = Tief = Schluss, Volumen 0) - Yahoo-Fehler, kurse.py repariert sie
    aus Stundenkerzen; was hier noch steht, ist NICHT repariert
  - unlogische Kerzen (Hoch unter Tief, Eroeffnung oder Schluss ausserhalb von Hoch/Tief)
  - Ausreisser: Schluss springt um mehr als 25 % und am Folgetag wieder zurueck
  - fehlende Tage bei Aktien (aus docs/datenluecken.csv, Spalte fehlend)
Schreibt docs/datenpruefung.md (Kurzbericht, oben eine Zeile "OK" oder "FEHLER") und docs/datenpruefung.csv.
Bricht nie ab - der Bericht ist die Pflichtlektuere vor jeder Auswertung.
"""
import os
import pandas as pd

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def _kursverlauf():
    return {k: pd.read_csv(os.path.join(DOCS, f"kursverlauf{s}.csv"), index_col=0)
            for k, s in (("o", "_eroeffnung"), ("h", "_hoch"), ("l", "_tief"), ("c", ""), ("v", "_volumen"))}


def main():
    zeilen = []
    K = _kursverlauf()
    o, h, l, c = (K[k].copy() for k in "ohlc")
    v = K["v"].reindex_like(c)
    roh = lambda t: t.endswith("=F") or t.endswith("=X") or t.startswith("^")
    platz = (o == h) & (h == l) & (l == c) & ((v == 0) | v.isna()) & c.notna()
    unlog = (h < l) | (c > h * 1.0001) | (c < l * 0.9999) | (o > h * 1.0001) | (o < l * 0.9999)
    r = c.pct_change(axis=1, fill_method=None); rn = r.shift(-1, axis=1)
    vm = v.T.rolling(20, min_periods=5).median().shift().T
    sprung = (r.abs() > 0.25) & (rn.abs() > 0.20) & (r * rn < 0) & ~(v > 3 * vm)   # echte Kursspruenge kommen mit hohem Volumen (Moderna 19.08.2026: 46-fach)
    for art, m in (("Platzhalter", platz), ("unlogisch", unlog), ("Ausreisser", sprung)):
        for t in m.index:
            for d in m.columns[m.loc[t].fillna(False).values]:
                zeilen.append(dict(quelle="kursverlauf", art=art, ticker=t, tag=d, rohstoff_fx=roh(t)))
    try:
        dl = pd.read_csv(os.path.join(DOCS, "datenluecken.csv"), dtype=str).fillna("")
        for z in dl.itertuples():
            for d in str(z.fehlend).split():
                zeilen.append(dict(quelle="kursverlauf", art="fehlt", ticker=z.ticker, tag=d, rohstoff_fx=roh(z.ticker)))
    except FileNotFoundError:
        pass
    for datei in ("tag.csv.gz", "tag_archiv.csv.gz"):
        p = os.path.join(DOCS, "kerzen", datei)
        if not os.path.exists(p):
            continue
        T = pd.read_csv(p, dtype={"ticker": str, "zeit": str})
        m = (T.o == T.h) & (T.h == T.l) & (T.l == T.c) & (T.v == 0)
        u = (T.h < T.l) | (T.c > T.h * 1.0001) | (T.c < T.l * 0.9999)
        for art, mm in (("Platzhalter", m), ("unlogisch", u)):
            for z in T[mm].itertuples():
                zeilen.append(dict(quelle=f"kerzen/{datei}", art=art, ticker=z.ticker, tag=z.zeit, rohstoff_fx=roh(z.ticker)))
    E = pd.DataFrame(zeilen, columns=["quelle", "art", "ticker", "tag", "rohstoff_fx"])
    E.to_csv(os.path.join(DOCS, "datenpruefung.csv"), index=False)
    akt = E[~E.rohstoff_fx]
    stand = c.columns[-1]
    kopf = "**OK - keine Fehler bei Aktien**" if akt.empty else f"**FEHLER - {len(akt)} Befunde bei Aktien, vor der Auswertung klaeren**"
    md = [f"# Datenpruefung (Kurse bis {stand})", "", kopf, ""]
    if len(E):
        g = E.groupby(["quelle", "art", "rohstoff_fx"]).size().reset_index(name="anzahl")
        md += ["| Quelle | Art | Rohstoff/Devise | Anzahl |", "|---|---|---|---|"]
        md += [f"| {z.quelle} | {z.art} | {'ja' if z.rohstoff_fx else 'nein'} | {z.anzahl} |" for z in g.itertuples()]
        md += ["", "Aktien (hoechstens 60):", ""]
        md += [f"- {z.quelle} · {z.art} · {z.ticker} · {z.tag}" for z in akt.sort_values("tag", ascending=False).head(60).itertuples()]
    open(os.path.join(DOCS, "datenpruefung.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:12]))


if __name__ == "__main__":
    main()
