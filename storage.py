import json
import os

DATA_FILE = "followed_coins.json"

def get_followed_coins():
    if not os.path.exists(DATA_FILE):
        return ["bitcoin", "ethereum", "solana"]  # Varsayılan coin listesi

    try:
        with open(DATA_FILE, "r") as f:
            coins = json.load(f)
        return coins
    except:
        return ["bitcoin", "ethereum", "solana"]

def add_coin(coin):
    coins = get_followed_coins()
    if coin not in coins:
        coins.append(coin)
        with open(DATA_FILE, "w") as f:
            json.dump(coins, f)

def remove_coin(coin):
    coins = get_followed_coins()
    if coin in coins:
        coins.remove(coin)
        with open(DATA_FILE, "w") as f:
            json.dump(coins, f)
