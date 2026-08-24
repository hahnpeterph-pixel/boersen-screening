"""Ersatzmodul fuer yfinance - liefert deterministische Testkurse."""
import pandas as pd, numpy as np

_CDNS = None
def _cdns():
    """Tageskerzen, die die dokumentierte CDNS-Struktur nachbauen:
    Tiefs 373,2 (05.06) / 358,5 (26.06) / 320,07 (20.07) / 319,46 (14.08) / 311,47 (20.08)
    Zwischentief 333,00 (06.08) liegt UEBER 320,07 -> darf nicht zaehlen.
    Hochs 416,69 / 406,67 / 391,00 / 355,59 - jedes unter dem vorigen."""
    punkte = [("2026-05-20",416.69,"H"),("2026-06-05",373.20,"T"),
              ("2026-06-12",406.67,"H"),("2026-06-26",358.50,"T"),
              ("2026-07-08",391.00,"H"),("2026-07-20",320.07,"T"),
              ("2026-08-01",348.00,"H"),("2026-08-06",333.00,"T"),("2026-08-11",355.59,"H"),
              ("2026-08-14",319.46,"T"),("2026-08-18",340.00,"H"),
              ("2026-08-20",311.47,"T"),("2026-08-21",319.02,"H")]
    tage, werte = [], []
    for k,(d,v,_) in enumerate(punkte):
        ziel = pd.Timestamp(d)
        if k==0:
            tage.append(ziel); werte.append(v); continue
        vor_d, vor_v = tage[-1], werte[-1]
        n = max(1,(ziel-vor_d).days)
        for j in range(1,n+1):
            tage.append(vor_d+pd.Timedelta(days=j))
            werte.append(vor_v+(v-vor_v)*j/n)
    idx = pd.DatetimeIndex(tage)
    c = np.array(werte,dtype=float)
    df = pd.DataFrame({"Open":c,"High":c*1.004,"Low":c*0.996,
                       "Close":c,"Volume":np.full(len(c),1e6)},index=idx)
    # Wendepunkte exakt setzen
    for d,v,art in punkte:
        t=pd.Timestamp(d)
        if art=="T": df.loc[t,"Low"]=v; df.loc[t,"High"]=v*1.006
        else: df.loc[t,"High"]=v; df.loc[t,"Low"]=v*0.994
    return df

def download(tickers=None,*a,**k):
    global _CDNS
    if _CDNS is None: _CDNS=_cdns()
    return _CDNS.copy()

class Ticker:
    def __init__(self,t): self.ticker=t
    def history(self,*a,**k): return download()
    @property
    def info(self): return {}
