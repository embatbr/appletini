"""Service starting point.
"""


import falcon

from web_api import RESTfulServer
from logic import Shopping
from domains import Product, Promotion, PurchaseBasket
from configs import products as products_configs
from configs import promotions as promotions_configs


def __generate_products():
    products = dict()

    for sku in products_configs:
        name = products_configs[sku]['name']
        price = products_configs[sku]['price']

        products[sku] = Product(sku, name, price)

    return products


def __generate_promotions():
    promotions = dict()

    for code in promotions_configs:
        promotion_configs = promotions_configs[code]

        condition = promotion_configs['condition']
        reward = promotion_configs['reward']
        description = promotion_configs['description']

        promotions[code] = Promotion(code, condition, reward, description)

    return promotions


# run using `gunicorn app[:falcon_api]`; `application` is by default used by gunicorn
falcon_api = application = falcon.API()

products = __generate_products()
promotions = __generate_promotions()
purchase_basket = PurchaseBasket()

shopping = Shopping(products, promotions, purchase_basket)

restful_endpoint = RESTfulServer(falcon_api, shopping)
restful_endpoint.expose()