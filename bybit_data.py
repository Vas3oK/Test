import requests
import pandas as pd

def fetch_candles(symbol, interval="15", limit=100):
    url = f"https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval={interval}&limit={limit}"
    r = requests.get(url)
    data = r.json()["result"]["list"]
    df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume","turnover"])
    df["close"] = pd.to_numeric(df["close"])
    return df

def compute_indicators(df):
    df["EMA20"] = df["close"].ewm(span=20).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()
    df["RSI"] = df["close"].rolling(window=14).apply(lambda x: 100 - (100 / (1 + ((x.diff().clip(lower=0).sum()) / (-x.diff().clip(upper=0).sum() + 1e-9)))))
    return df