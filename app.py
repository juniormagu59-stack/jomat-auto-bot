import random
import time
import requests
import os
import threading
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHAT_ID")
print(f"TOKEN CHECK: {BOT_TOKEN[:10] if BOT_TOKEN else 'MISSING'}", flush=True)
print(f"CHAT_ID CHECK: {CHANNEL_ID}", flush=True)

def generate_signal():
    target = random.choice(list(range(10)))
    market = random.choice(["Volatility 100", "Volatility 75", "Volatility 50"])
    analysis = random.choice(["OVER", "UNDER", "EVEN", "ODD", "MATCHES", "DIFFERS"])
    stake = random.randint(1, 5)
    entry_point = random.randint(0, 9)
    deriv_link = "https://track.deriv.com/_5c0o3oG2d4qKqXqXqXqX?action=login"

    signal = f"""🚀 *JOMAT AUTO - DERIV DIGIT SIGNAL*

📊 Market: {market} Index
🔢 Digit: *{target}*
📈 Prediction: *{analysis} {random.randint(0,4)}*
⏰ Duration: 1 Tick
🎯 Entry Point: {entry_point}
💰 Stake: ${stake}
🔥 Confidence: {random.randint(82,97)}%

🔗 TRADE NOW: {deriv_link}
🌐 https://jomatpro.site
📢 Channel: https://whatsapp.com/channel/0029Vb8fI7FEAKWMmrEz1J0L
"""
    return signal

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=data, timeout=10)
        print(f"Sent: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error: {e}")

def bot_loop():
    print("BOT LOOP STARTED...", flush=True)
    while True:
        try:
            print("Generating signal...", flush=True)
            sig = generate_signal()
            print(f"Signal generated, length: {len(sig)}", flush=True)
            send_to_telegram(sig)
            print("Sleeping 15 min...", flush=True)
            time.sleep(900)  # 15 min
        except Exception as e:
            print(f"LOOP ERROR: {e}", flush=True)
            time.sleep(60)

@app.route("/")
def home():
    return "JOMAT BOT IS LIVE - Running 24/7"
@app.route('/webhook', methods=['POST'])
def webhook():
    return "ok", 200
# Start bot in background thread
threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
