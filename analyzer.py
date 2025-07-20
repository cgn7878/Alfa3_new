import requests
import pandas as pd
from analyzer import check_coin_status
def fetch_ohlcv(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=2&interval=hourly"
    response = requests.get(url)
    data = response.json()

    if "prices" not in data:
        return None

    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["price"] = df["price"].astype(float)
    return df

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]

def calculate_macd(prices):
    ema12 = prices.ewm(span=12, adjust=False).mean()
    ema26 = prices.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    macd_cross = macd_line.iloc[-2] < signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]
    return macd_cross

def analyze_coin(coin):
    df = fetch_ohlcv(coin)
    if df is None or len(df) < 30:
        return None

    prices = df["price"]
    rsi = calculate_rsi(prices)
    macd_cross = calculate_macd(prices)
    current_price = prices.iloc[-1]

    return {
        "rsi": round(rsi, 2),
        "macd_cross": macd_cross,
        "price": round(current_price, 3)
    }
