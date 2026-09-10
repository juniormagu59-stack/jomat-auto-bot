import os
import random
import time
import threading
from flask import Flask
import requests

# Soma majina yote - yako ni TELEGRAM_*
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")

MARKETS = ["R_10","R_25","R_50","R_75","R_100","R_10_1s","R_25_1s","R_50_1s","R_75_1s","R_100_1s"]

def get_live_ticks(market):
    print(f"Generating {market} with random - bypass Deriv for test")
    return [random.randint(0,9) for _ in range(20)]

def send_telegram(text):
    if not BOT_TOKEN or not CHANNEL_ID:
        print(f"ERROR: TOKEN={bool(BOT_TOKEN)} CHAT={bool(CHANNEL_ID)}")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}, timeout=15)
        print(f"Sent: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"Telegram error: {e}")

def generate_signal():
    market = random.choice(MARKETS)
    ticks = get_live_ticks(market)
    from collections import Counter
    c = Counter(ticks)
    digit, freq = c.most_common(1)[0]
    percent = int(freq / len(ticks) * 100)
    if percent < 65:
        return None
    return f"🔥 *JOMAT LIVE SIGNAL* 🔥\n\nMarket: `{market}`\nDigit: *{digit}* - {percent}%\nTicks: {''.join(map(str,ticks[-10:]))}\n\nStake: $1 - Martingale 2 steps"

def bot_loop():
    print("Jomat LIVE bot started - TEST MODE")
    time.sleep(5)
    while True:
        try:
            print("Generating LIVE signal...")
            sig = generate_signal()
            if sig:
                print("Sending...")
                send_telegram(sig)
            else:
                print("No strong signal this round")
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(120) # kila dakika 2 kwa test

app = Flask(__name__)
@app.route('/')
def home():
    return "Jomat Auto Bot is LIVE - Test Mode"

if __name__!= "__main__":
    t = threading.Thread(target=bot_loop, daemon=True)
    t.start()

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
