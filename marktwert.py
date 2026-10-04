"""marktwert.py V1.0 (04.10.2026, Peter: "nach Marktkapitalisierung schauen? Sind die groesseren Werte die besseren?" /
"was die jeweiligen Branchenplayer sind").
Einmaliger Abruf (laeuft nur ueber den Workflow "Marktwert", beruehrt das Screening nicht): je Ticker aus universe.json der
heutige Boersenwert, die Aktienzahl und die Waehrung von Yahoo. Ergebnis docs/marktwert.csv.
Fruehere Boersenwerte rechnet die Auswertung naeherungsweise als Boersenwert heute x (Kurs damals / Kurs heute)."""
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


def main():
    rows = []
    for t in ticker_liste():
        mc = sh = cur = None
        for _ in range(3):
            try:
                fi = yf.Ticker(t).fast_info
                mc, sh, cur = fi.get("market_cap"), fi.get("shares"), fi.get("currency")
                if mc:
                    break
            except Exception:  # noqa: BLE001
                time.sleep(2)
        if not mc:
            try:
                inf = yf.Ticker(t).info
                mc, sh, cur = inf.get("marketCap"), inf.get("sharesOutstanding"), inf.get("currency")
            except Exception:  # noqa: BLE001
                pass
        rows.append(dict(ticker=t, marktwert=mc, aktien=sh, waehrung=cur))
        time.sleep(0.3)
    df = pd.DataFrame(rows)
    df.to_csv("docs/marktwert.csv", index=False)
    print(len(df), "Werte,", int(df.marktwert.notna().sum()), "mit Boersenwert")


if __name__ == "__main__":
    main()
