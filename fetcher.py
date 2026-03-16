import requests
from analyzer import find_our_spikes, find_spikes 
from storage import save_history

def get_scarab_prices():
    url = "https://poe.ninja/api/data/itemoverview?league=Mirage&type=Scarab"
    response = requests.get(url)
    data  = response.json()

    scarab = data['lines']

    save_history(scarab)

    #poe.ninja spike detector
    opportunities = find_spikes(scarab)
    if opportunities:
        print('Price Spikes Detected:')
        for item in opportunities:
            print(f"{item['name']}: {item['chaos_value']}c (Change: {item['change']}%)")
    else:
        print('No significant price spikes detected.')

    print()

    #My own spike detector
    our_opportunities = find_our_spikes()
    if our_opportunities:
        print('Potential Opportunities Based on Our Data:')
        for item in our_opportunities:
            print(f"{item['name']}: {item['current_price']}c (Change: {item['change']}%) - Last seen: {item['last_seen']}")

    else:
        print('No significant opportunities detected based on our data.')