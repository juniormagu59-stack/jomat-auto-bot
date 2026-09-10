from flask import Flask, request
import requests, os, random, time
from threading import Thread
from datetime import datetime

app = Flask(__name__)

# --- CONFIG - WEKA HAPA ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.environ.get("WHATSAPP_PHONE_ID")
WHATSAPP_CHANNEL_ID = os.environ.get("WHATSAPP_CHANNEL_ID")

VERIFY_TOKEN = "jomat123"


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
⏰ Duration: 1 Tick
🎯 Entry Point: {random.randint(0,9)}
💰 Stake: ${stake}
🎯 Confidence: {random.randint(82,97)}%

⏱️ {datetime.now().strftime('%H:%M:%S')}

👇 TRADE NOW:
https://jomatpro.site
""" 
signal_msg += f"\n📢 WhatsApp Channel: https://whatsapp.com/channel/0029Vb8fI7FEAKWMmrEz1J0L"
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
        time.sleep(1800)  # 30 minutes

# Anza loop automatically
Thread(target=auto_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
