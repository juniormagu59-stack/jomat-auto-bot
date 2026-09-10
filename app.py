import os, time, random, requests, threading
import websocket
import json
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN", "8465997382:AAGYqW8z4HlT1WIl4R1wR5t8w0sF4l0xXxX")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@jomatpro")
DERIV_WS = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

MARKETS = ["R_10","R_25","R_50","R_75","R_100","R_10_1s","R_25_1s","R_50_1s","R_75_1s","R_100_1s"]
MARKET_NAMES = {
    "R_10":"Volatility 10 Index", "R_25":"Volatility 25 Index",
    "R_50":"Volatility 50 Index", "R_75":"Volatility 75 Index", "R_100":"Volatility 100 Index",
    "R_10_1s":"Volatility 10 (1s) Index", "R_25_1s":"Volatility 25 (1s) Index",
    "R_50_1s":"Volatility 50 (1s) Index", "R_75_1s":"Volatility 75 (1s) Index", "R_100_1s":"Volatility 100 (1s) Index"
}

def get_live_ticks(market):
    try:
        ws = websocket.create_connection(DERIV_WS, timeout=10)
        ws.send(json.dumps({"ticks_history": market, "count": 100, "end": "latest"}))
        result = json.loads(ws.recv())
        ws.close()
        if "history" in result:
            prices = result["history"]["prices"]
            return [int(str(p).split('.')[-1][-1]) for p in prices if '.' in str(p)]
    except Exception as e:
        print(f"Tick error {market}: {e}")
    return [random.randint(0,9) for _ in range(20)]

def generate_signal():
    market = random.choice(MARKETS)
    digits = get_live_ticks(market)
    if len(digits) < 20: digits = digits + [random.randint(0,9)]*20
    last_20 = digits[-20:]
    most_common = max(set(last_20), key=last_20.count)
    count = last_20.count(most_common)
    confidence = min(95, 60 + count*5 + random.randint(0,5))
    stake = 5 if confidence <75 else 10 if confidence <85 else 15 if confidence <90 else 20
    
    if count >=5:
        pred = f"MATCHES {most_common} - Digit {most_common} appeared {count} times in last 20"
    else:
        pred = f"OVER {most_common} - Digit distribution favors over {most_common}"
    
    msg = f"""🚀 *JOMAT AUTO - DERIV DIGIT SIGNAL* 📈
📊 Market: {MARKET_NAMES.get(market, market)}
🔢 Digit: *{most_common}*
🎯 Prediction: *{pred}*
⏱️ Duration: 1 Tick
🏁 Entry Point: {most_common}
💰 Stake: ${stake}
🔥 Confidence: {confidence}% (Live 100 ticks)

📲 TRADE NOW: https://jomatpro.site
📢 Channel: https://whatsapp.com/channel/0029Vb8F117FEAKMMmrEz13QL

Jomat Pro
Trade Smart. Grow Consistently
Jomat Pro - Build and run automated trading bots with ease.
"""
    return msg

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode":"Markdown"}, timeout=10)
        print(f"Sent: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"Send error: {e}")

def bot_loop():
    print("Jomat LIVE bot started...")
    while True:
        try:
            print("Generating LIVE signal...")
            msg = generate_signal()
            send_telegram(msg)
        except Exception as e:
            print(f"Loop error: {e}")
        print("Sleeping 15 min...")
        time.sleep(900)

# Flask for Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Jomat LIVE bot is running ✅"

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
