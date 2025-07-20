# core.py

import time
from datetime import datetime
from storage import get_followed_coins
from analyzer import check_coin_status
from news_handler import fetch_crypto_news, analyze_news_item
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests

sent_news_links = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram hatası: {e}")

def run_bot():
    while True:
        print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bot çalışıyor...")

        coins = get_followed_coins()
        for coin in coins:
            result = check_coin_status(coin)
            if result:
                send_telegram_message(result)

        news_items = fetch_crypto_news()
        for news in news_items:
            if news["url"] in sent_news_links:
                continue

            analysis = analyze_news_item(news)
            if analysis:
                msg = f"📰 Haber Analizi ({news['published']}):\n{analysis}\n\n{news['title']}\n{news['url']}"
                send_telegram_message(msg)
                sent_news_links.add(news["url"])

        time.sleep(300)  # 5 dakika
