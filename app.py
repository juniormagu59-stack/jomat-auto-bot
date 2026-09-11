import os
import time
import threading
import json
from flask import Flask
import requests
import websocket

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")

MARKETS = ["R_10", "R_25", "R_50", "R_75", "R_100", "1HZ10V", "1HZ25V", "1HZ50V", "1HZ75V", "1HZ100V"]

def get_live_ticks(market):
    """REAL Deriv ticks - sio random tena"""
    try:
        ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089", timeout=10)
        req = {"ticks_history": market, "count": 20, "end": "latest", "style": "ticks"}
        ws.send(json.dumps(req))
        result = ws.recv()
        ws.close()
        data = json.loads(result)
        # Deriv inarudisha prices kama 1234.56 -> tunachukua last digit
        prices = data.get("history", {}).get("prices", [])
        if not prices:
            print(f"Deriv empty for {market}: {data}", flush=True)
            return None
        digits = [int(str(p).replace('.','')[-1]) for p in prices]
        print(f"REAL {market}: {digits}", flush=True)
        return digits
    except Exception as e:
        print(f"Deriv error {market}: {e}", flush=True)
        return None

def send_telegram(text):
    if not BOT_TOKEN or not CHANNEL_ID:
        print(f"ERROR: TOKEN={bool(BOT_TOKEN)} CHAT={bool(CHANNEL_ID)}", flush=True)
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}, timeout=15)
        print(f"Telegram Sent: {r.status_code}", flush=True)
    except Exception as e:
        print(f"Telegram error: {e}", flush=True)

def generate_signal():
    import random
    from collections import Counter
    market = random.choice(MARKETS)
    ticks = get_live_ticks(market)
    if not ticks or len(ticks) < 10:
        return None
    c = Counter(ticks)
    digit, freq = c.most_common(1)[0]
    percent = int(freq / len(ticks) * 100)
    if percent < 60: # ongeza threshold
        print(f"{market} digit {digit} only {percent}% - skip", flush=True)
        return None
    return f"🔥 *JOMAT LIVE SIGNAL* 🔥\n\nMarket: `{market}`\nDigit: *{digit}* - {percent}%\nTicks: {''.join(map(str,ticks[-10:]))}\n\nStake: $1 - Martingale 2 steps\nSource: *REAL Deriv*"

def bot_loop():
    print(">>> JOMAT LIVE BOT STARTED - REAL MODE <<<", flush=True)
    time.sleep(10)
    while True:
        try:
            sig = generate_signal()
            if sig:
                send_telegram(sig)
            else:
                print("No strong real signal this round", flush=True)
        except Exception as e:
            print(f"Loop error: {e}", flush=True)
        time.sleep(900) # kila dakika 3 - real market usichoke API

app = Flask(__name__)
@app.route('/')
def home():
    return "Jomat Auto Bot is LIVE - REAL MODE"

# Hii ndio fix ya Render + Gunicorn
threading.Thread(target=bot_loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
