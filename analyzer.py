from storage import load_history

def find_spikes(items, min_chaos=2, spike_threshold=10):
    opportunities = []

    for item in items:
        name = item.get("name") or item.get("currencyTypeName", "Unknown")
        chaos_value = item.get("chaosValue") or item.get("chaosEquivalent", 0)
        change = item.get("sparkline", {}).get("totalChange", 0)
        item_type = item.get("itemType", "Unknown")

        if chaos_value >= min_chaos and change >= spike_threshold:
            opportunities.append({
                "name": name,
                "chaos_value": chaos_value,
                "change": change,
                "item_type": item_type
            })

    opportunities.sort(key=lambda x: x["change"], reverse=True)
    return opportunities


def find_our_spikes(min_chaos=2, spike_threshold=15):
    history = load_history()
    our_spikes = []

    for key, entries in history.items():
        valid_entries = [e for e in entries if "price" in e]

        if len(valid_entries) < 2:
            continue

        oldest_price = valid_entries[0]["price"]
        latest_price = valid_entries[-1]["price"]
        latest_time = valid_entries[-1].get("time", "N/A")
        category = valid_entries[-1].get("category", "Unknown")

        if oldest_price == 0:
            continue

        our_change = ((latest_price - oldest_price) / oldest_price) * 100

        if latest_price >= min_chaos and our_change >= spike_threshold:
            # Split key back into category and name
            name = key.split(":", 1)[-1]
            our_spikes.append({
                "name": name,
                "category": category,
                "old_price": oldest_price,
                "current_price": latest_price,
                "change": round(our_change, 1),
                "last_seen": latest_time
            })

    our_spikes.sort(key=lambda x: x["change"], reverse=True)
    return our_spikes