import requests
from analyzer import find_spikes
from storage import save_history

def get_scarab_prices():
    url = "https://poe.ninja/api/data/itemoverview?league=Mirage&type=Scarab"
    response = requests.get(url)
    data  = response.json()

    scarab = data['lines']

    save_history(scarab)

    opportunities = find_spikes(scarab)

    if opportunities:
        print('Price Spikes Detected:')
        for item in opportunities:
            print(f"{item['name']}: {item['chaos_value']}c (Change: {item['change']}%)")
    else:
        print('No significant price spikes detected.')
