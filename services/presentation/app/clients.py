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
        return self.get_products_or_basket('products')

    def get_basket(self):
        return self.get_products_or_basket('basket')

    def get_products_or_basket(self, action):
        url = '%s/shopping/%s' % (self.baseurl, action)

        try:
            response = urllib.request.urlopen(url)
            resp_message = response.read().decode('utf-8')

            return ast.literal_eval(resp_message)

        except urllib.error.HTTPError as err:
            return err

    def buy_or_rm(self, action, sku):
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