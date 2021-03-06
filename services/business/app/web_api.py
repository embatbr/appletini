"""This module contains the routes and methods to receive HTTP requests.
"""


import falcon
import ast

from configs import BaseError


class RESTfulServer(object):

    def __init__(self, falcon_api, shopping):
        self.falcon_api = falcon_api

        self.restful_endpoints = {
            '/shopping/{action}': RESTfulShopping(shopping),
            '/purchase' : RESTfulPurchaseReturn(shopping),
            '/return' : RESTfulPurchaseReturn(shopping)
        }

    def expose(self):
        for (key, restful_endpoint) in self.restful_endpoints.items():
            self.falcon_api.add_route(key, restful_endpoint)


class RESTfulShopping(object):

    def __init__(self, shopping):
        self.shopping = shopping

    def on_get(self, req, resp, action):
        actions = ['products', 'basket', 'clear-basket', 'checkout', 'promotions']
        if action not in actions:
            resp.status = falcon.HTTP_400
            return

        payload = None
        success = False
        if action in ['clear-basket', 'checkout']:
            try:
                payload = getattr(self.shopping, action.replace('-', '_'))()
                success = True

            except BaseError as err:
                payload = err.message

        else:
            payload = getattr(self.shopping, 'export_%s' % action)()
            success = True

        resp.body = str({
            'success' : success,
            'payload' : str(payload)
        })

        resp.status = falcon.HTTP_200


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
            getattr(self.shopping, '%s_product' % action)(sku)
            invoice = self.shopping.export_basket()

            resp.body = str({
                'success' : True,
                'payload' : str(invoice)
            })

        except BaseError as err:
            resp.body = str({
                'success' : False,
                'payload' : err.message
            })

        resp.status = falcon.HTTP_200
