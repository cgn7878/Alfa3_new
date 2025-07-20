# news_analyzer.py

import requests
from config import NEWS_API_KEY

def fetch_crypto_news(coin_name):
    try:
        url = f"https://newsapi.org/v2/everything?q={coin_name}+crypto&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt&pageSize=5"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [article["title"] + " - " + article["description"] for article in articles if article.get("title")]
        else:
            return []
    except Exception as e:
        print(f"Haber alma hatası: {e}")
        return []

def analyze_news_sentiment(news_list):
    positive_keywords = ["bull", "surge", "gain", "rise", "record", "growth"]
    negative_keywords = ["bear", "drop", "fall", "crash", "loss", "scam"]

    score = 0
    for news in news_list:
        lower = news.lower()
        if any(word in lower for word in positive_keywords):
            score += 1
        if any(word in lower for word in negative_keywords):
            score -= 1

    if score > 1:
        return "🟢 Pozitif Haber Etkisi"
    elif score < -1:
        return "🔴 Negatif Haber Etkisi"
    else:
        return "🟡 Nötr Haber Etkisi"
