import requests
import pandas as pd

def fetch_ohlcv(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": "2", "interval": "hourly"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        prices = data["prices"]
        return pd.DataFrame(prices, columns=["timestamp", "price"])
    except Exception as e:
        print(f"{coin} verileri alınamadı: {e}")
        return None

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else None

def calculate_macd(prices, short=12, long=26, signal=9):
    short_ema = prices.ewm(span=short, adjust=False).mean()
    long_ema = prices.ewm(span=long, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    macd_cross = macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]
    return macd_cross

def analyze_coin(coin):
    df = fetch_ohlcv(coin)
    if df is None or df.empty:
        return None

    df["price"] = df["price"].astype(float)
    rsi = calculate_rsi(df["price"])
    macd_cross = calculate_macd(df["price"])
    current_price = df["price"].iloc[-1]

    return {
        "rsi": round(rsi, 2) if rsi else None,
        "macd_cross": macd_cross,
        "price": round(current_price, 2)
    }

def check_coin_status(coin):
    analysis = analyze_coin(coin)
    if analysis is None:
        return None

    rsi = analysis["rsi"]
    macd = analysis["macd_cross"]
    price = analysis["price"]

    if rsi < 30 and macd:
        return f"📈 Acil Al❗️\nCoin: {coin.upper()}\nRSI: {rsi}\nFiyat: ${price}"

    if rsi > 70:
        return f"📉 Acil Sat❗️\nCoin: {coin.upper()}\nRSI: {rsi}\nFiyat: ${price}"

    return None
