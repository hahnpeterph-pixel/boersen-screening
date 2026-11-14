"""Machbarkeitstest Insiderdaten (14.11.2026, Peter): Was liefert Yahoo (yfinance) je Wert?
Laeuft nur auf dem Testzweig insider-test, beruehrt das Screening nicht. Schreibt test/insider_test.csv und test/insider_test.txt."""
import yfinance as yf, pandas as pd

WERTE = ["NVDA", "AXON", "AMAT"]
teile, bericht = [], [f"yfinance {yf.__version__}"]
for tk in WERTE:
    t = yf.Ticker(tk)
    for feld in ["insider_transactions", "insider_purchases", "insider_roster_holders"]:
        try:
            d = getattr(t, feld)
            if d is None or len(d) == 0:
                bericht.append(f"{tk} {feld}: leer"); continue
            bericht.append(f"{tk} {feld}: {len(d)} Zeilen, Spalten {list(d.columns)}")
            if feld == "insider_transactions":
                dd = d.copy(); dd.insert(0, "ticker", tk); teile.append(dd)
                datum = pd.to_datetime(dd.get("Start Date"), errors="coerce")
                bericht.append(f"   Zeitraum {datum.min().date()} bis {datum.max().date()}")
            else:
                bericht.append("   " + d.head(8).to_string().replace("\n", "\n   "))
        except Exception as e:
            bericht.append(f"{tk} {feld}: FEHLER {type(e).__name__}: {e}")
if teile:
    pd.concat(teile).to_csv("test/insider_test.csv", index=False)
open("test/insider_test.txt", "w").write("\n".join(bericht) + "\n")
print("\n".join(bericht))
