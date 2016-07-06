"""This module contains the routes and methods to receive HTTP requests.
"""


import falcon
import ast

from logic import ShoppingError
from domains import PurchaseBasketError


class RESTfulServer(object):

    def __init__(self, falcon_api, shopping):
        self.falcon_api = falcon_api

        self.restful_endpoints = {
            '/purchase' : RESTfulPurchaseReturn(shopping),
            '/return' : RESTfulPurchaseReturn(shopping)
        }

    def expose(self):
        for (key, restful_endpoint) in self.restful_endpoints.items():
            self.falcon_api.add_route(key, restful_endpoint)


class RESTfulPurchaseReturn(object):

    def __init__(self, shopping):
        self.shopping = shopping

    def on_post(self, req, resp):
        req_body = req.stream.read().decode('utf-8')

        # Validating if request body is dictionary
        try:
            req_body = ast.literal_eval(req_body)

        except ValueError:
            resp.status = falcon.HTTP_400
            return

        # Validating content of request body
        if ('action' not in req_body) or (not req_body['action']) or (not isinstance(req_body['action'], str)) or (req_body['action'] not in ['purchase', 'return']):
            resp.status = falcon.HTTP_400
            return

        # Validating content of request body
        if ('sku' not in req_body) or (not req_body['sku']) or (not isinstance(req_body['sku'], str)):
            resp.status = falcon.HTTP_400
            return

        action = req_body['action']
        sku = req_body['sku']

        try:
            invoice = getattr(self.shopping, '%s_product' % action)(sku)

            resp.body = str({
                'success' : True,
                'payload' : str(invoice)
            })

        except ShoppingError as err:
            resp.body = str({
                'success' : False,
                'payload' : err.message
            })

        except PurchaseBasketError as err:
            resp.body = str({
                'success' : False,
                'payload' : err.message
            })

        resp.status = falcon.HTTP_200
