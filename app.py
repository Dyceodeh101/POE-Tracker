from flask import Flask, render_template, jsonify
from fetcher import get_scarab_data
from analyzer import find_spikes, find_our_spikes
from storage import load_history

app = Flask(__name__)

@app.route("/")
def index():
    all_items, divine_rate = get_scarab_data()
    poe_spikes = find_spikes(all_items)
    our_spikes = find_our_spikes()

    all_items = sorted(
        [i for i in all_items if (i.get("chaosValue") or i.get("chaosEquivalent", 0)) >= 2 and i.get("count", 0) >= 10],  # at least 10 real transactions
        key=lambda x: x.get("chaosValue") or x.get("chaosEquivalent", 0),
        reverse=True
    )


    return render_template("index.html", poe_spikes=poe_spikes, our_spikes=our_spikes, all_items=all_items, divine_rate=divine_rate)

@app.route("/history/<path:item_key>")
def item_history(item_key):
    history = load_history()
    entries = history.get(item_key, [])
    return jsonify(entries)

if __name__ == "__main__":
    app.run(debug=True)