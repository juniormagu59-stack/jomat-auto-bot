from flask import Flask, request
import requests, random
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
TOKEN = "8697863047:AAHYZDhck6ttyuqR67sLehvXcxfmAu-CDqU"
CHANNEL_ID = "-1004320643772"
URL = f"https://api.telegram.org/bot{TOKEN}/"

MARKETS = ["V10", "V10 (1s)", "V25", "V25 (1s)", "V50", "V50 (1s)", "V75", "V75 (1s)", "V100", "V100 (1s)"]

def send_digit_signal():
    market = random.choice(MARKETS)
    trade = random.choice(["EVEN", "ODD", "OVER 3", "UNDER 6"])
    conf = random.randint(85, 95)
    if trade == "EVEN":
        icon = "EVEN (0,2,4,6,8)"
    elif trade == "ODD":
        icon = "ODD (1,3,5,7,9)"
    else:
        icon = trade
          import random

    # Entry point logic - 1 digit smart kulingana na AI
    if "OVER" in trade:
        digit = int(trade.split()[-1])
        # OVER 3 = chagua random digit kubwa kuliko 3
        possible = list(range(digit + 1, 10))
        entry_point = random.choice(possible) if possible else 9
        
    elif "UNDER" in trade:
        digit = int(trade.split()[-1])
        # UNDER 3 = chagua random digit ndogo kuliko 3
        possible = list(range(0, digit))
        entry_point = random.choice(possible) if possible else 0
        
    else:
        # EVEN / ODD - chagua random digit kutoka kwa set
        if "ODD" in trade:
            entry_point = random.choice([1,3,5,7,9])
        else:  # EVEN
            entry_point = random.choice([0,2,4,6,8])  

    WEBSITE = "https://jomatpro.site"

    msg = f"""Jomat pro bots -deriv official
JOMAT DIGIT SIGNAL

Market {market} Index
Trade {icon}
Entry Point: {entry_point}
Time {datetime.now().strftime('%H:%M')} EAT
Confidence {conf}%
Duration 1 Tick

👇 TRADE NOW:
{WEBSITE}"""

    try:
        # Button ya website
        keyboard = {"inline_keyboard": [[{"text": "🚀 TRADE NOW", "url": WEBSITE}]]}
        requests.post(URL + "sendMessage", json={"chat_id": CHANNEL_ID, "text": msg, "reply_markup": keyboard})
    except:
        pass

scheduler = BackgroundScheduler()
scheduler.add_job(send_digit_signal, 'interval', minutes=5)
scheduler.start()

@app.route('/', methods=['POST'])
def webhook():
    return "ok"

@app.route('/')
def home():
    return "JOMAT BOT LIVE"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
