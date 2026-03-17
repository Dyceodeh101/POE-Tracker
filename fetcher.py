import requests
from analyzer import find_spikes, find_our_spikes
from storage import save_history

LEAGUE = "Mirage"

ITEM_TYPES = {
    "Scarab": f"https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type=Scarab",
    "DivinationCard": f"https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type=DivinationCard",
    "Fossil": f"https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type=Fossil",
    "Currency": f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency",
}

def fetch_items(item_type, url):
    response = requests.get(url)
    data = response.json()
    items = data.get("lines", [])
    return items

def get_scarab_data():
    all_items = []
    for item_type, url in ITEM_TYPES.items():
        print(f"Fetching {item_type}s...")
        items = fetch_items(item_type, url)
        # Tag each item with its type
        for item in items:
            item["itemType"] = item_type
        save_history(items, category=item_type)
        all_items.extend(items)
    return all_items,

def get_scarab_prices():
    all_items, = get_scarab_data()

    opportunities = find_spikes(all_items)
    if opportunities:
        print("SPIKING ITEMS (poe.ninja data):\n")
        for item in opportunities:
            print(f"[{item['item_type']}] {item['name']} | {item['chaos_value']}c | +{item['change']}%")
    else:
        print("No major spikes detected from poe.ninja data.")

    print()

    our_opportunities = find_our_spikes()
    if our_opportunities:
        print("SPIKING ITEMS (our own history):\n")
        for item in our_opportunities:
            print(f"{item['name']} | {item['old_price']}c → {item['current_price']}c | +{item['change']}%")
    else:
        print("No major spikes detected from our own history yet.")