"""Contains implementations for clients of other services (e.g., business and storage).
"""


import urllib
import urllib.request
import urllib.parse
import ast


class BusinessClient(Exception):

    def __init__(self, message):
        self.message = message


class BusinessClient(object):

    def __init__(self, configs):
        self.protocol = configs['protocol']
        self.host = configs['host']
        self.port = configs['port']

        self.baseurl = '%s://%s:%s' % (self.protocol, self.host, self.port)

    def get_products(self):
        return self.shopping_gets('products')

    def get_basket(self):
        return self.shopping_gets('basket')

    def clear_basket(self):
        return self.shopping_gets('clear-basket')

    def checkout(self):
        return self.shopping_gets('checkout')

    def get_promotions(self):
        return self.shopping_gets('promotions')

    def shopping_gets(self, action):
        url = '%s/shopping/%s' % (self.baseurl, action)

        try:
            response = urllib.request.urlopen(url)
            resp_message = response.read().decode('utf-8')

            return ast.literal_eval(resp_message)

        except urllib.error.HTTPError as err:
            return err

    def add(self, sku):
        return self.add_or_remove('purchase', sku)

    def remove(self, sku):
        return self.add_or_remove('return', sku)

    def add_or_remove(self, action, sku):
        url = '%s/%s' % (self.baseurl, action)
        body = {
            'action' : action,
            'sku' : sku
        }

        data = bytes(str(body), 'utf-8')

        try:
            response = urllib.request.urlopen(url, data)
            resp_message = response.read().decode('utf-8')

            return ast.literal_eval(resp_message)

        except urllib.error.HTTPError as err:
            return err