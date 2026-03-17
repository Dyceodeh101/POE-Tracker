import requests
from analyzer import find_spikes, find_our_spikes
from storage import save_history
from alerts import send_spike_email

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

def get_divine_rate():
    url = f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency"
    response = requests.get(url)
    data = response.json()
    
    for currency in data.get("lines", []):
        if currency.get("currencyTypeName") == "Divine Orb":
            return currency.get("chaosEquivalent", 1)
    
    return 1

def get_scarab_data():
    all_items = []
    for item_type, url in ITEM_TYPES.items():
        print(f"📦 Fetching {item_type}s...")
        items = fetch_items(item_type, url)
        for item in items:
            item["itemType"] = item_type
        save_history(items, category=item_type)
        all_items.extend(items)
    
    divine_rate = get_divine_rate()
    return all_items, divine_rate

def get_scarab_prices():
    all_items, divine_rate = get_scarab_data()

    opportunities = find_spikes(all_items)
    send_spike_email(opportunities)

    if opportunities:
        print("🚀 SPIKING ITEMS (poe.ninja data):\n")
        for item in opportunities:
            print(f"[{item['item_type']}] {item['name']} | {item['chaos_value']}c | +{item['change']}%")
    else:
        print("No major spikes detected from poe.ninja data.")

    print()

    our_opportunities = find_our_spikes()
    if our_opportunities:
        print("📈 SPIKING ITEMS (our own history):\n")
        for item in our_opportunities:
            print(f"{item['name']} | {item['old_price']}c → {item['current_price']}c | +{item['change']}%")
    else:
        print("No major spikes detected from our own history yet.")