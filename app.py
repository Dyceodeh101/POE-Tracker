from flask import Flask, render_template
from fetcher import get_scarab_data
from analyzer import find_spikes, find_our_spikes

app = Flask(__name__)

@app.route("/")
def index():
    scarabs, = get_scarab_data()
    poe_spikes = find_spikes(scarabs)
    our_spikes = find_our_spikes()
    return render_template("index.html", poe_spikes=poe_spikes, our_spikes=our_spikes)

if __name__ == "__main__":
    app.run(debug=True)