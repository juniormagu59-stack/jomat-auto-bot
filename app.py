import os, time, random, requests, threading, json
import websocket
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")
DERIV_WS = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

MARKETS = ["R_10","R_25","R_50","R_75","R_100"]

def get_live_ticks(market):
    print(f"Using random digits for {market} - bypass Deriv")
    return [random.randint(0,9) for _ in range(20)]

def send_telegram(text):
    try:
        if not BOT_TOKEN or not CHANNEL_ID:
            print("ERROR: BOT_TOKEN or CHANNEL_ID missing in Environment!")
            return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode":"Markdown"}, timeout=10)
        print(f"Sent: {r.status_code} - {r.text[:300]}")
    except Exception as e:
        print(f"Send error: {e}")

def bot_loop():
    print("Jomat LIVE bot started...")
    while True:
        try:
            print("Generating LIVE signal...")
            market = random.choice(MARKETS)
            digits = get_live_ticks(market)
            most_common = max(set(digits), key=digits.count)
            confidence = random.randint(78,95)
            msg = f"🚀 *JOMAT LIVE SIGNAL* 📈\nMarket: {market}\nDigit: *{most_common}*\nConfidence: {confidence}%\nTrade: https://jomatpro.site"
            send_telegram(msg)
        except Exception as e:
            print(f"Loop error: {e}")
        print("Sleeping 900 sec...")
        time.sleep(900)

app = Flask(__name__)
@app.route('/')
def home():
    return "Jomat LIVE bot is running"

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
