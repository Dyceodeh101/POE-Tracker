from flask import Flask, render_template, jsonify
from fetcher import get_scarab_data
from analyzer import find_spikes, find_our_spikes
from storage import load_history
from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def index():
    all_items, divine_rate = get_scarab_data()
    poe_spikes = find_spikes(all_items)
    our_spikes = find_our_spikes()

    filtered = sorted(
        [i for i in all_items if i.get("chaosValue", 0) >= 2 and i.get("volumePrimaryValue", 0) >= 10],
        key=lambda x: x.get("chaosValue", 0),
        reverse=True
    )

    # Group by item type
    grouped_items = defaultdict(list)
    for item in filtered:
        grouped_items[item["itemType"]].append(item)

    return render_template("index.html", poe_spikes=poe_spikes, our_spikes=our_spikes, grouped_items=grouped_items, divine_rate=divine_rate)

@app.route("/history/<path:item_key>")
def item_history(item_key):
    history = load_history()
    entries = history.get(item_key, [])
    return jsonify(entries)

if __name__ == "__main__":
    app.run(debug=True)
