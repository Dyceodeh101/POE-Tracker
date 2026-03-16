import json
import os
from datetime import datetime

HISTORY_FILE = "price_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(scarabs):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for scarab in scarabs:
        name = scarab['name']
        chaos_value = scarab['chaosValue']

        if name not in history:
            history[name] = []

        history[name].append({
            "timestamp": timestamp,
            "price": chaos_value
        })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    print(f'Prices saved at {timestamp}')