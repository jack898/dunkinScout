#!/usr/bin/env python3

import requests
from flask import Flask, render_template, request


BEARER_TOKEN = 'd2f28b0ab69842ac91412d448ad10680'
DEFAULT_MENU_ITEM = 'Original Blend Iced Coffee'
PRICES_URL = 'https://mapi-dun.prod.ddmprod.dunkindonuts.com/menu-management/v1/menus/v4/'
STORES_URL = 'https://mapi-dun.prod.ddmprod.dunkindonuts.com/location/v1/stores'


app = Flask(__name__)
session = requests.Session()
session.headers.update({
    'Authorization': f'bearer {BEARER_TOKEN}',
    'User-Agent': 'DunkScoutWeb',
})


# TODO: generate this based on the menu at the closest store
def _all_menu_items():
    with app.open_instance_resource('menu.txt', 'r') as f:
        return [i.strip() for i in f]
menu = _all_menu_items()


@app.route('/')
def index():
    context = {
        'menu': menu,
        'default_menu_item': DEFAULT_MENU_ITEM,
    }
    return render_template('index.html', **context)


@app.route('/prices')
def prices():
    # TODO: filter on currently open stores (store['status']['onlineStatus'] == 'Open')
    distance = request.args.get('distance', default=5.0, type=float)
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    menu_item = request.args.get('menuItem', default=DEFAULT_MENU_ITEM)

    stores = _get_stores(latitude, longitude, distance)
    for store in stores:
        store['price'] = _get_price(store['storeId'], menu_item)
    # `stores` comes pre-sorted by distance, so when they all have the same
    # price this returns in distance order
    stores = [s for s in stores if s['price'] is not None]
    stores.sort(key=lambda s: s['price'] or float('inf'))
    return stores


def _get_menu(data):
    items = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'menuItems':
                for row in value:
                    items[row['displayName']] = row['price']
            else:
                items.update(_get_menu(value))
    elif isinstance(data, list):
        for row in data:
            items.update(_get_menu(row))
    return items


def _get_price(store_id, menu_item):
    url = PRICES_URL + store_id
    resp = session.get(url)
    resp.raise_for_status()
    menu = _get_menu(resp.json())
    return menu.get(menu_item, None)


def _get_stores(latitude, longitude, distance):
    # returns stores sorted by distance
    url = STORES_URL + f'?latitude={latitude:.6f}&longitude={longitude:.6f}'
    resp = session.get(url)
    resp.raise_for_status()
    stores = [
        {
            'address': s['address'],
            'distance': s['distance'],
            'storeId': s['storeId'],
        }
        for s in resp.json()['data'] if s['distance'] <= distance
    ]
    stores.sort(key=lambda s: s['distance'])
    return stores
