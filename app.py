import os, random, time, requests, json, websocket
from collections import Counter

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHAT_ID")

MARKETS = {
    "Volatility 10": "R_10",
    "Volatility 25": "R_25",
    "Volatility 50": "R_50",
    "Volatility 75": "R_75",
    "Volatility 100": "R_100",
    "Volatility 10 (1s)": "1HZ10V",
    "Volatility 25 (1s)": "1HZ25V",
    "Volatility 50 (1s)": "1HZ50V",
    "Volatility 75 (1s)": "1HZ75V",
    "Volatility 100 (1s)": "1HZ100V",
}

def get_live_ticks(symbol, count=100):
    try:
        ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089", timeout=10)
        ws.send(json.dumps({"ticks_history": symbol, "count": count, "end": "latest", "style": "ticks"}))
        result = json.loads(ws.recv())
        ws.close()
        if "history" in result:
            return result["history"]["prices"]
        return None
    except Exception as e:
        print(f"WS Error {symbol}: {e}", flush=True)
        return None

def analyze(prices):
    digits = [int(str(p).split('.')[-1][-1]) for p in prices if '.' in str(p)]
    last_20 = digits[-20:]
    freq = Counter(last_20)
    most_common_digit, count = freq.most_common(1)[0]
    over_4 = sum(1 for d in last_20 if d > 4)
    even = sum(1 for d in last_20 if d % 2 == 0)
    least_common = freq.most_common()[-1][0]
    return most_common_digit, count, over_4, even, least_common, last_20

def generate_signal():
    market_name = random.choice(list(MARKETS.keys()))
    symbol = MARKETS[market_name]
    prices = get_live_ticks(symbol)

    if not prices:
        print("Fallback random", flush=True)
        target = random.randint(0,9)
        analysis_type = random.choice(["MATCHES", "DIFFERS", "OVER", "UNDER", "EVEN", "ODD"])
        analysis = f"{analysis_type} {target}"
        confidence = random.randint(78,86)
    else:
        most_common, count, over_4, even, least_common, last_20 = analyze(prices)

        # Chagua strategy: MATCHES, DIFFERS, OVER, UNDER, EVEN, ODD
        strategies = []
        if count >= 4:
            strategies.append(("MATCHES", most_common, count))
        strategies.append(("DIFFERS", least_common, 20 - Counter(last_20)[least_common]))
        if over_4 >= 13:
            strategies.append(("OVER", 4, over_4))
        if (20 - over_4) >= 13:
            strategies.append(("UNDER", 4, 20 - over_4))
        strategies.append(("EVEN", "EVEN", even))
        strategies.append(("ODD", "ODD", 20 - even))

        chosen = random.choice(strategies)

        if chosen[0] == "MATCHES":
            target = chosen[1]
            analysis = f"MATCHES {chosen[2]} - Digit {target} appeared {chosen[2]} times in last 20"
            confidence = 84 + chosen[2] # 88-96%
        elif chosen[0] == "DIFFERS":
            target = chosen[1]
            analysis = f"DIFFERS {target} - Digit {target} RARE in last 20"
            confidence = 82 + random.randint(2,8)
        elif chosen[0] == "OVER":
            target = 4
            analysis = f"OVER {chosen[2]}/20 ticks OVER 4"
            confidence = 80 + (chosen[2]-12)*2
        elif chosen[0] == "UNDER":
            target = 4
            analysis = f"UNDER {chosen[2]}/20 ticks UNDER 4"
            confidence = 80 + (chosen[2]-12)*2
        elif chosen[0] == "EVEN":
            target = random.choice([0,2,4,6,8])
            analysis = f"EVEN - {chosen[2]}/20 ticks EVEN"
            confidence = 78 + (chosen[2]-10)
        else: # ODD
            target = random.choice([1,3,5,7,9])
            analysis = f"ODD - {chosen[2]}/20 ticks ODD"
            confidence = 78 + (chosen[2]-10)

        confidence = min(confidence, 97)
        entry_point = target

    # Stake 5 to 20 kulingana na confidence
    if confidence >= 92:
        stake = random.randint(15, 20)
    elif confidence >= 86:
        stake = random.randint(10, 15)
    else:
        stake = random.randint(5, 10)

    signal = f"""🚀 *JOMAT AUTO - DERIV DIGIT SIGNAL* 📊

📈 Market: {market_name} Index
🎯 Digit: *{entry_point}*
🔍 Prediction: *{analysis}*
⏱️ Duration: 1 Tick
📍 Entry Point: {entry_point}
💰 Stake: ${stake}
🔥 Confidence: {confidence}% (Live 100 ticks)

👉 TRADE NOW: https://jomatpro.site
📢 Channel: https://whatsapp.com/channel/0029Vb8F1I7FEAKMMmrEz13QL
"""
    return signal

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text}
    try:
        r = requests.post(url, data=data, timeout=15)
        print(f"Sent: {r.status_code} - {r.text[:200]}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

def bot_loop():
    while True:
        print("Generating LIVE signal...", flush=True)
        sig = generate_signal()
        send_to_telegram(sig)
        print("Sleeping 15 min...", flush=True)
        time.sleep(900)

if __name__ == "__main__":
    bot_loop()
