import time
from fetcher import get_scarab_prices

def run():
    print ('======================================')
    print ('  Path of Exile Scarab Price Tracker  ')
    print ('======================================')

    while True:
        print('Fetching scarab prices...')

        get_scarab_prices()

        print('Waiting for the next update...')
        print('Press Ctrl+C to stop the tracker.')
        print('======================================')

        time.sleep(300)  # Wait for 5 minutes/300 seconds before the next update

run()