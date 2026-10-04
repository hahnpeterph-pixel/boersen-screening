"""hochstufungen.py V1.0 (04.10.2026, Peter: Score-Idee "im besten Fall innerhalb der letzten ein bis zwei Wochen hochgestuft ...
je mehr hochgestuft, desto besser ... sowohl der Zielkurs, aber vor allem die Einstufung" -> Rueckpruefung).
Einmaliger Abruf (laeuft nur ueber den Workflow "Hochstufungen", beruehrt das Screening nicht): je Ticker aus universe.json die
komplette Historie der Zu-/Abstufungen von Yahoo (yfinance upgrades_downgrades). Ergebnis docs/hochstufungen.csv.gz mit
ticker, datum, firma, aktion (up/down/main/reit/init), von, nach, ziel_aktion, ziel_neu, ziel_alt."""
import json, time
import pandas as pd
import yfinance as yf


def ticker_liste():
    u = json.load(open("universe.json", encoding="utf-8"))
    out = []
    for k, v in u.items():
        if k.startswith("_") or k in ("COMMODITIES", "CRYPTO", "benchmarks"):
            continue
        for x in v:
            t = x if isinstance(x, str) else (x.get("ticker") or x.get("symbol") if isinstance(x, dict) else None)
            if t and t not in out:
                out.append(t)
    return out


SPALTEN = {"Firm": "firma", "Action": "aktion", "FromGrade": "von", "ToGrade": "nach",
           "priceTargetAction": "ziel_aktion", "currentPriceTarget": "ziel_neu", "priorPriceTarget": "ziel_alt"}


def main():
    teile, ohne = [], []
    for t in ticker_liste():
        df = None
        for _ in range(3):
            try:
                df = yf.Ticker(t).upgrades_downgrades
                break
            except Exception:  # noqa: BLE001
                time.sleep(2)
        if df is None or len(df) == 0:
            ohne.append(t)
            continue
        df = df.reset_index().rename(columns={"GradeDate": "datum", **SPALTEN})
        df["datum"] = pd.to_datetime(df["datum"]).dt.strftime("%Y-%m-%d")
        df.insert(0, "ticker", t)
        teile.append(df[[c for c in ["ticker", "datum", *SPALTEN.values()] if c in df.columns]])
        time.sleep(0.3)
    A = pd.concat(teile, ignore_index=True).sort_values(["ticker", "datum"])
    A.to_csv("docs/hochstufungen.csv.gz", index=False, compression="gzip")
    print(len(A), "Eintraege,", A.ticker.nunique(), "Werte, frueheste", A.datum.min(), "| ohne Daten:", len(ohne), ohne[:20])


if __name__ == "__main__":
    main()
