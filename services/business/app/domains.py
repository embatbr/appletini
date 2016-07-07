"""This module contains the models (products, pricing rules and etc.).

Validations of correct parameter type are not necessary, since those are
guaranteed by the callers.
"""


import re

from decimal import Decimal

from configs import BaseError


class Product(object):

    def __init__(self, sku, name, price):
        self.sku = sku.strip()
        self.name = name.strip()
        self.price = Decimal(price)

    def describe(self):
        return '%s %s $%s' % (self.sku, self.name, str(self.price))


class Promotion(object):

    def __init__(self, code, category, condition, reward, description):
        self.code = code
        self.category = category
        self.condition = condition
        self.reward = reward
        self.description = description

    def describe(self):
        return self.description


class Purchase(object):

    def __init__(self, product, units):
        self.product = product
        self.units = units

    def increase_units(self):
        self.units = self.units + 1

    def decrease_units(self):
        self.units = self.units - 1

    def calculate_price(self):
        return (self.units * self.product.price)

    def get_invoice(self):
        total_price = self.calculate_price()

        return {
            'name' : self.product.name,
            'units' : self.units,
            'price' : str(total_price)
        }


class PurchaseBasket(object):

    def __init__(self):
        self.purchases = dict()

    def add_product(self, product):
        if product.sku in self.purchases:
            self.purchases[product.sku].increase_units()
        else:
            self.purchases[product.sku] = Purchase(product, 1)

    def remove_product(self, sku):
        if sku not in self.purchases:
            raise BaseError('Cannot remove a non-purchased product.')

        self.purchases[sku].decrease_units()
        if self.purchases[sku].units == 0:
            del self.purchases[sku]

    def clear(self):
        if self.is_empty():
            raise BaseError('Cannot clear empty basket.')

        del self.purchases
        self.purchases = dict()

    def is_empty(self):
        return not self.purchases

    def has_purchase(self, sku):
        return (sku in self.purchases)

    def get_purchase_units(self, sku):
        return self.purchases[sku].units

    def get_purchase_product_price(self, sku):
        return self.purchases[sku].product.price

    def calculate_price(self):
        return sum([purchase.calculate_price() for purchase in self.purchases.values()])

    def get_invoice(self):
        invoice = {
            'items' : dict(),
            'total_price' : self.calculate_price()
        }

        for sku in self.purchases:
            purchase = self.purchases[sku]
            invoice['items'][sku] = purchase.get_invoice()

        return invoice
