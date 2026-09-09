from flask import Flask, request
import requests, os, random, time
from threading import Thread
from datetime import datetime

app = Flask(__name__)

# --- CONFIG - WEKA HAPA ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8697863047:AAGsKQsP0YxM7tziO5Zl83QvMwMVJzUQAHM")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID", "1004320643772")
WHATSAPP_TOKEN = os.environ.get("EAGVEmR4ZBS6wBSSUxJ74KSGU6U1hU8yyVJZBFNdcRUsZBKmD8xBKR3u5WwjlEgbhGZC2WZCjlZA4jVtdUXqxeZBpZCzO0QrPfeuxYSYVMBiQqBmebsm4yg1GyO6pYCemBNZARrF8I4KyOHkLfnfIrZBZAXAzHN5CEisZBNcZCFvdZA3ti61UFpYnhZBs3aMgv8INzfYxgZDZD", "")
WHATSAPP_PHONE_ID = os.environ.get("1240710109133208", "")
WHATSAPP_CHANNEL_ID = os.environ.get("2283812449106025", "") # kwa channel

VERIFY_TOKEN = "jomat123"

app = Flask(__name__)

@app.route('/')
def home():
    return "JOMAT BOT LIVE ✅ - Telegram + WhatsApp Channel Active"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    return "OK", 200

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
        print("Telegram sent ✅")
    except Exception as e:
        print(f"Telegram error: {e}")

def send_whatsapp_channel(text):
    try:
        if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
            print("WhatsApp token bado")
            return
        url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        # Kwa WhatsApp Channel, tunatuma kama message
        payload = {
            "messaging_product": "whatsapp",
            "to": WHATSAPP_CHANNEL_ID, # au number ya channel
            "type": "text",
            "text": {"body": text}
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"WhatsApp sent: {r.text}")
    except Exception as e:
        print(f"WhatsApp error: {e}")

def generate_signal():
    digits = list(range(10))
    target = random.choice(digits)
    market = random.choice(["Volatility 100", "Volatility 75", "Volatility 50"])
    analysis = random.choice(["OVER", "UNDER"])
    stake = random.randint(1, 5)
    
    signal = f"""🚀 *JOMAT AUTO - DERIV DIGIT SIGNAL*

📊 Market: {market} Index
🔢 Digit: *{target}*
📈 Prediction: *{analysis} {random.randint(0,4)}*
⏰ Duration: 5 Ticks
💰 Stake: ${stake}
🎯 Confidence: {random.randint(82,97)}%

⏱️ {datetime.now().strftime('%H:%M:%S')} 
_Trade wisely!_ 🔥
"""
    return signal

def auto_loop():
    print("Bot loop started...")
    while True:
        try:
            sig = generate_signal()
            print(sig)
            send_telegram(sig)
            send_whatsapp_channel(sig)
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(300)  # 5 minutes

# Anza loop automatically
Thread(target=auto_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
