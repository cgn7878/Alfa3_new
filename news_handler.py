# news_handler.py

import requests
import datetime
from config import NEWS_API_KEY

KEYWORDS = [
    "crypto", "bitcoin", "ethereum", "solana", "altcoin",
    "SEC", "ETF", "Binance", "Coinbase", "crypto regulation",
    "crypto hack", "blockchain", "crypto ban", "crypto market"
]

EXCLUDED_SOURCES = ["prnewswire.com", "businesswire.com", "globewire.com"]

def fetch_crypto_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={' OR '.join(KEYWORDS)}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            print("Haber API hatası:", data)
            return []

        news_items = []
        for article in data["articles"]:
            source = article.get("source", {}).get("name", "").lower()
            if any(blocked in source for blocked in EXCLUDED_SOURCES):
                continue

            title = article.get("title", "")
            description = article.get("description", "")
            url = article.get("url", "")
            published = article.get("publishedAt", "")

            news_items.append({
                "title": title,
                "description": description,
                "url": url,
                "published": published
            })

        return news_items

    except Exception as e:
        print(f"Haber çekme hatası: {e}")
        return []


def analyze_news_item(news):
    text = f"{news['title']}. {news['description']}"
    text = text.lower()

    # Basit kelime analizleri
    if "etf approved" in text or "etf accepted" in text or "spot bitcoin etf" in text:
        return "Pozitif 🚀: Spot Bitcoin ETF onayı haberi!"
    elif "sec sues" in text or "sec investigation" in text:
        return "Negatif ⚠️: SEC soruşturması veya dava haberi!"
    elif "hack" in text or "stolen" in text or "breach" in text:
        return "Negatif 🚨: Hack veya güvenlik ihlali haberi!"
    elif "partnership" in text or "adoption" in text:
        return "Pozitif 🤝: Ortaklık veya benimsenme haberi!"
    elif "ban" in text or "prohibit" in text:
        return "Negatif ⛔️: Yasaklama veya engelleme haberi!"

    return None
