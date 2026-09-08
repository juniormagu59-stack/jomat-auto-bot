from flask import Flask
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
    
    # ENTRY POINT - NUMBER TU!
    if "OVER" in trade:
        d = int(trade.split()[-1])
        entry_point = random.choice([i for i in range(d+1, 10)]) if d < 9 else 9
    elif "UNDER" in trade:
        d = int(trade.split()[-1])
        entry_point = random.choice([i for i in range(0, d)]) if d > 0 else 0
    elif "ODD" in trade:
        entry_point = random.choice([1,3,5,7,9])
    else:
        entry_point = random.choice([0,2,4,6,8])
    
    msg = f"""JOMAT DIGIT SIGNAL

Market {market}
Trade {trade}
Entry Point: {entry_point}
Time {datetime.now().strftime('%H:%M')}
Confidence 94%
Duration 1 Tick

👇 TRADE NOW:
https://jomatpro.site"""
    
    requests.get(URL + f"sendMessage?chat_id={CHANNEL_ID}&text={msg}")

scheduler = BackgroundScheduler()
scheduler.add_job(send_digit_signal, 'interval', minutes=5)
scheduler.start()

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
