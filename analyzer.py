from storage import load_history

def find_spikes(scarabs, min_chaos=2, spike_threshold=10):
    opportunities = []

    for scarab in scarabs:
        name = scarab["name"]
        chaos_value = scarab["chaosValue"]
        change = scarab.get("sparkline", {}).get("totalChange", 0)

        if chaos_value >= min_chaos and change >= spike_threshold:
            opportunities.append({
                "name": name,
                "chaos_value": chaos_value,
                "change": change
            })

    opportunities.sort(key=lambda x: x["change"], reverse=True)
    return opportunities


def find_our_spikes(min_chaos=2, spike_threshold=15):
    history = load_history()
    our_spikes = []

    for name, entries in history.items():
        # Need at least 2 data points to compare
        if len(entries) < 2:
            continue

        oldest_price = entries[0]["price"]
        latest_price = entries[-1]["price"]
        latest_time = entries[-1]["time"]

        # Avoid dividing by zero
        if oldest_price == 0:
            continue

        # Calculate our own % change
        our_change = ((latest_price - oldest_price) / oldest_price) * 100

        if latest_price >= min_chaos and our_change >= spike_threshold:
            our_spikes.append({
                "name": name,
                "old_price": oldest_price,
                "current_price": latest_price,
                "change": round(our_change, 1),
                "last_seen": latest_time
            })

    our_spikes.sort(key=lambda x: x["change"], reverse=True)
    return our_spikes