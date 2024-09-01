#!/usr/bin/env python
# Finds the cheapest Dunkin in your area by comparing the (pre-tax) price of 
# an item across nearby locations
# Usage: python dunkScout.py <-lat LAT> <-long LONG> [-item ITEM] [-dist DIST]

import argparse
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


### CONSTANTS ###
# BEARER_TOKEN: Required for Dunkin App API, hardcoded because it doesn't appear to expire.. if it does though
# you will need to sniff another token from a Dunkin app API request
# DEFAULT_ITEM: Item to price out if no item argument is specified.
BEARER_TOKEN = "d2f28b0ab69842ac91412d448ad10680"
DEFAULT_ITEM = "Original Blend Iced Coffee"


def main():
    global DEFAULT_ITEM
    parser = argparse.ArgumentParser(description='Find the cheapest Dunkin in your area')
    parser.add_argument('-lat', type=float, help='Latitude of your location', required=True)
    parser.add_argument('-long', type=float, help='Longitude of your location', required=True)
    parser.add_argument('-item', type=str, help='Item to compare prices for', default=DEFAULT_ITEM)
    parser.add_argument('-dist', type=int, help='Max distance away, in freedom units (stores further will not be searched)', default=5)
    args = parser.parse_args()

    store_list = find_locations(args.lat, args.long, args.dist)
    lowest_price = float('inf')
    lowest_price_store = None

    print(f'Found {len(store_list)} locations.')
    print("Finding item price in nearby stores..")
    for store in store_list: # Find price of item at each store within search parameters
        address = pretty_print(store["address"])
        storeId = store["storeId"]
        dist = store["distance"]
        store_price = price_at_store(storeId, args.item)

        if store_price is None:
            print(f'\nCouldn\'t find item at store {address}! Make sure the item name is typed exactly as it appears on the menu.')
            input('Press any key to keep searching other stores, or close the program...')
        else:
            print(f'\nPrice at {address} ({dist:.2f}mi away):')
            print(f'${store_price}')
            if store_price < lowest_price:
                lowest_price = store_price
                lowest_price_store = (address, dist)

    if lowest_price_store is None:
        print('Search failed. Perhaps there are no Dunkins in this area?')
    else:
        print(f'\n\nThe cheapest location for {args.item} is ${lowest_price} at {lowest_price_store[0]}, {lowest_price_store[1]:.2f}mi away.')


        
# Create dict of store locations from latitude and longitude, and filter by distance
def find_locations(lat, long, maxDist):
        url = f'https://mapi-dun.prod.ddmprod.dunkindonuts.com/location/v1/stores?longitude={long:.6f}&latitude={lat:.6f}'
        json_data = api_request(url)
        print("Gathering stores near you...")

        store_info = []
        for store in json_data['data']:
            store_info.append({
                "storeId": store["storeId"],
                "distance": store["distance"],
                "address": {
                    "line1": store["address"]["line1"],
                    "city": store["address"]["city"],
                    "state": store["address"]["state"],
                    "postalCode": store["address"]["postalCode"]
                }
            })
        
        # Remove any stores further than the max distance
        store_info = [store for store in store_info if store["distance"] <= int(maxDist)]

        return store_info

# Price item at store by ID
def price_at_store(storeId, item_name):
        url = f'https://mapi-dun.prod.ddmprod.dunkindonuts.com/menu-management/v1/menus/v4/{storeId}'
        menu_data = api_request(url)
        
        price = find_item_price(menu_data, item_name)
        return price


# Finds price of an item from specific store menu
def find_item_price(data, item_name):
        if isinstance(data, dict):
            if "menuItems" in data:
                for item in data["menuItems"]:
                    if item.get("displayName") == item_name:
                        return item.get("price")
            for key in data:
                result = find_item_price(data[key], item_name)
                if result is not None:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = find_item_price(item, item_name)
                if result is not None:
                    return result
        
        return None


# Prints JSON address object in readable format
def pretty_print(json_address):
        line = json_address["line1"]
        city = json_address["city"]
        state = json_address["state"]
        zip_code = json_address["postalCode"]
        return f'{line}, {city}, {state} {zip_code}'


# Places Dunkin API request with token and returns parsed JSON response
def api_request(url):
        global BEARER_TOKEN
        req = Request(url)
        req.add_header('Authorization', f'bearer {BEARER_TOKEN}')
        req.add_header('User-Agent', 'DunkScout')
        
        try:
            content = urlopen(req).read()
        except HTTPError as e:
            print("\nAPI Call failed")
            return None

        return json.loads(content)     
        


if __name__ == "__main__":
    main()