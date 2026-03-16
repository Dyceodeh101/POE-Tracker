import requests

def get_scarab_prices():
    url = "https://poe.ninja/api/data/itemoverview?league=Mirage&type=Scarab"
    response = requests.get(url)
    data  = response.json()

    scarab = data['lines']

    for scarab in scarab:
        name = scarab['name']
        chaos_value = scarab['chaosValue']
        change = scarab.get("sparkline", {}).get("totalChange", 0)

        print(f"{name} | {chaos_value}c | Change: {change}%")

