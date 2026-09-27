"""test20_vergleich.py - vergleicht docs/heute.csv mit 7 Jahren (Basis) und mit 20 Jahren (Test).
Aufruf: python test20_vergleich.py BASIS.csv TEST.csv AUSGABE.md"""
import sys
import pandas as pd

b = pd.read_csv(sys.argv[1]).set_index("ticker")
t = pd.read_csv(sys.argv[2]).set_index("ticker")
L = ["# Testlauf 20 Jahre – Vergleich der Tagesauswertung (heute.csv)", "",
     "Basis = heute.py mit den bestehenden 7-Jahres-Dateien. Test = heute.py mit 20 Jahren "
     "(historie, rsi_schwellen, phasen, markthistorie neu gerechnet). Gleicher Kursstand.", ""]
drin_b = set(b.index[b.filter_ergebnis == "drin"]) if "filter_ergebnis" in b else set(b.index)
drin_t = set(t.index[t.filter_ergebnis == "drin"]) if "filter_ergebnis" in t else set(t.index)
L += [f"- Werte in heute.csv: Basis {len(b)} · Test {len(t)}",
      f"- nach Filtern „drin“: Basis {len(drin_b)} · Test {len(drin_t)}",
      f"- nur Basis: {', '.join(sorted(drin_b - drin_t)) or '–'}",
      f"- nur Test: {', '.join(sorted(drin_t - drin_b)) or '–'}", ""]
L += ["| Wert | Tief | Anker 7J | Anker 20J | Tief-N 2 ATR 7J (n) | 20J (n) | Tief-N 3 ATR 7J (n) | 20J (n) | Kette 7J | Kette 20J |",
      "|---|---|---|---|---|---|---|---|---|---|"]
def z(df, tk, p):
    try:
        return f"{float(df.loc[tk, f'p{p}_haelt63_position_pct']):.0f} % ({int(df.loc[tk, f'p{p}_haelt63_position_n'])})"
    except Exception:
        return "–"
def k(df, tk):
    s = str(df.loc[tk, "fortsetzungskette"]) if tk in df.index else ""
    m = [x for x in s.split(" · ") if "»" in x]
    return m[0] if m else "–"
for tk in sorted(set(b.index) | set(t.index)):
    pos = int(b.loc[tk, "position"]) if tk in b.index else int(t.loc[tk, "position"])
    ab = b.loc[tk, "anker_atr"] if tk in b.index else "–"
    at = t.loc[tk, "anker_atr"] if tk in t.index else "–"
    L.append(f"| {tk} | {pos} | {ab} | {at} | {z(b, tk, 2.0)} | {z(t, tk, 2.0)} | {z(b, tk, 3.0)} | {z(t, tk, 3.0)} | {k(b, tk)} | {k(t, tk)} |")
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
