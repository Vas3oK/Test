def strategy_ema_cross(df):
    if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]:
        return "BUY", 75
    elif df["EMA20"].iloc[-1] < df["EMA50"].iloc[-1]:
        return "SELL", 75
    return None, 0

def strategy_rsi(df):
    if df["RSI"].iloc[-1] < 30:
        return "BUY", 80
    elif df["RSI"].iloc[-1] > 70:
        return "SELL", 80
    return None, 0

def dummy_strategy(df):
    return "BUY", 50

STRATEGIES = [strategy_ema_cross, strategy_rsi] + [dummy_strategy]*18