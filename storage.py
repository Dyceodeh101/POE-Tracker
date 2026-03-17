import json
import os
from datetime import datetime

HISTORY_FILE = "price_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(items, category="Unknown"):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in items:
        # Currency items use different name field
        name = item.get("name") or item.get("currencyTypeName", "Unknown")
        chaos_value = item.get("chaosValue") or item.get("chaosEquivalent", 0)

        # Use category:name as key to avoid conflicts
        key = f"{category}:{name}"

        if key not in history:
            history[key] = []

        history[key].append({
            "time": timestamp,
            "price": chaos_value,
            "category": category
        })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"{category} prices saved at {timestamp}")