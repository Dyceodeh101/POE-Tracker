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

def get_divine_rate():
    url = f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency"
    response = requests.get(url)
    data = response.json()
    
    for currency in data.get("lines", []):
        if currency.get("currencyTypeName") == "Divine Orb":
            return currency.get("chaosEquivalent", 1)
    
    return 1  # fallback to avoid dividing by zero