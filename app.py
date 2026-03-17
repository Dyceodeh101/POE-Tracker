from flask import Flask, render_template
from fetcher import get_scarab_data
from analyzer import find_spikes, find_our_spikes

app = Flask(__name__)

@app.route("/")
def index():
    all_items, divine_rate = get_scarab_data()
    poe_spikes = find_spikes(all_items)
    our_spikes = find_our_spikes()
    
    # Sort all items by price, filter out cheap junk under 2c
    all_items = sorted(
        [i for i in all_items if (i.get("chaosValue") or i.get("chaosEquivalent", 0)) >= 2],
        key=lambda x: x.get("chaosValue") or x.get("chaosEquivalent", 0),
        reverse=True
    )
    
    return render_template("index.html", poe_spikes=poe_spikes, our_spikes=our_spikes, all_items=all_items, divine_rate=divine_rate)

if __name__ == "__main__":
    app.run(debug=True)