import requests
from analyzer import find_spikes, find_our_spikes
from storage import save_history
from alerts import send_spike_email

LEAGUE = "Mirage"

BASE_URL = "https://poe.ninja/poe1/api/economy/exchange/current"

ITEM_TYPES = {
    "Scarab":         f"{BASE_URL}/overview?league={LEAGUE}&type=Scarab",
    "DivinationCard": f"{BASE_URL}/overview?league={LEAGUE}&type=DivinationCard",
    "Fossil":         f"{BASE_URL}/overview?league={LEAGUE}&type=Fossil",
    "Currency":       f"{BASE_URL}/overview?league={LEAGUE}&type=Currency",
}

HEADERS = {
    "User-Agent": "poe-economy-tracker/1.0 contact@youremail.com"
}

def fetch_items(item_type, url, divine_rate=1):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    lines = data.get("lines", [])
    items = data.get("items", [])

    # Build id -> name lookup
    name_lookup = {item["id"]: item["name"] for item in items}

    # Attach readable name and normalize field names
    result = []
    for line in lines:
        item_id = line.get("id")
        line["name"] = name_lookup.get(item_id, item_id)
    
        primary_value = line.get("primaryValue", 0)

        if primary_value == 0:
            continue

        line["chaosValue"] = primary_value
        line["sparkLine"] = line.get("sparkline", {})
        result.append(line)

    return result

def get_divine_rate():
    url = f"{BASE_URL}/overview?league={LEAGUE}&type=Currency"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    core = data.get("core", {})
    rates = core.get("rates", {})
    divine_chaos_rate = rates.get("divine", 1)
    
    # rate is chaos-per-divine inverted, so we flip it
    return 1 / divine_chaos_rate if divine_chaos_rate else 1

def get_scarab_data():
    divine_rate = get_divine_rate()
    all_items = []
    for item_type, url in ITEM_TYPES.items():
        print(f"📦 Fetching {item_type}s...")
        items = fetch_items(item_type, url, divine_rate)
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