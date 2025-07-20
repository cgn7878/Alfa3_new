import time
import requests
from analyzer import analyze_coin
from storage import get_followed_coins
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from news import get_latest_news

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")
        return False

def interpret_signal(analysis):
    if analysis is None:
        return None

    rsi = analysis["rsi"]
    macd_cross = analysis["macd_cross"]
    price = analysis["price"]

    if rsi < 30 and macd_cross:
        return f"Acil Al❗️\nFiyat: {price} $\nRSI: {rsi} (Düşük)\nMACD: Al Sinyali"
    elif rsi > 70 and not macd_cross:
        return f"Acil Sat❗️\nFiyat: {price} $\nRSI: {rsi} (Yüksek)\nMACD: Sat Sinyali"
    else:
        return None

def run_bot():
    last_news_sent = ""

    while True:
        coins = get_followed_coins()

        # 1. Coin analiz döngüsü
        for coin in coins:
            try:
                analysis = analyze_coin(coin)
                signal = interpret_signal(analysis)
                if signal:
                    send_telegram_message(f"{coin.upper()} için sinyal:\n\n{signal}")
            except Exception as e:
                print(f"{coin} analiz hatası: {e}")

        # 2. Haber kontrolü
        try:
            news = get_latest_news()
            if news and news != last_news_sent:
                send_telegram_message(f"📰 Haber Gelişmesi:\n\n{news}")
                last_news_sent = news
        except Exception as e:
            print(f"Haber alınamadı: {e}")

        time.sleep(300)  # 5 dakika bekle (300 saniye)
