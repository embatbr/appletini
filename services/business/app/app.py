"""Service starting point.
"""


import falcon

from web_api import RESTfulServer
from logic import Shopping
from domains import Product
from configs import products as products_configs


def __generate_products(items):
    products = dict()

    for sku in items:
        name = items[sku]['name']
        price = items[sku]['price']

        products[sku] = Product(sku, name, price)

    return products


# run using `gunicorn app[:falcon_api]`; `application` is by default used by gunicorn
falcon_api = application = falcon.API()

items = products_configs['items']
shopping = Shopping(__generate_products(items))

restful_endpoint = RESTfulServer(falcon_api, shopping)
restful_endpoint.expose()