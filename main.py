import time
from config import BYBIT_API_KEY, BYBIT_API_SECRET, TRADING_PAIRS
from bybit_data import fetch_candles, compute_indicators
from strategies import STRATEGIES

def analyze_market():
    signals = []

    for symbol in TRADING_PAIRS:
        try:
            df = fetch_candles(symbol)
            df = compute_indicators(df)

            confidence_total = 0
            valid_signals = 0
            direction = None

            for strat in STRATEGIES:
                signal, conf = strat(df)
                if signal:
                    if direction is None:
                        direction = signal
                    elif direction != signal:
                        direction = "CONFLICT"
                    confidence_total += conf
                    valid_signals += 1

            if direction in ["BUY", "SELL"]:
                avg_conf = round(confidence_total / valid_signals, 2) if valid_signals else 0
                signals.append((symbol, direction, avg_conf))
        except Exception as e:
            print(f"Error on {symbol}: {e}")

    signals.sort(key=lambda x: x[2], reverse=True)
    return signals[:4]

if __name__ == "__main__":
    while True:
        print("\n--- SIGNAL SCAN START ---")
        top_signals = analyze_market()
        for s in top_signals:
            print(f"{s[0]} - {s[1]} - Confidence: {s[2]}%")
        print("--- Waiting 10 mins ---\n")
        time.sleep(600)