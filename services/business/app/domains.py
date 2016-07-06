"""This module contains the models (products, pricing rules and etc.).

Validations of correct parameter type are not necessary, since those are
guaranteed by the callers.
"""


import re

from money import Money

from configs import BaseError


class Product(object):

    def __init__(self, sku, name, price):
        self.sku = sku.strip()
        self.name = name.strip()
        self.price = Money(price, 'USD')

    def describe(self):
        return '%s %s $%s' % (self.sku, self.name, self.price.amount)


class Purchase(object):

    def __init__(self, product, amount):
        self.product = product
        self.amount = amount

    def increase_amount(self):
        self.amount = self.amount + 1

    def decrease_amount(self):
        self.amount = self.amount - 1

    def calculate_price(self):
        total_price = self.amount * self.product.price
        return total_price.amount

    def get_invoice(self):
        return {
            'name' : self.product.name,
            'amount' : self.amount,
            'price' : str(self.calculate_price())
        }


class PurchaseBasket(object):

    def __init__(self):
        self.purchases = dict()

    def add_product(self, product):
        if product.sku in self.purchases:
            self.purchases[product.sku].increase_amount()
        else:
            self.purchases[product.sku] = Purchase(product, 1)

    def remove_product(self, sku):
        if sku not in self.purchases:
            raise BaseError('Cannot remove a non-purchased product.')

        self.purchases[sku].decrease_amount()
        if self.purchases[sku].amount == 0:
            del self.purchases[sku]

    def clear(self):
        if self.is_empty():
            raise BaseError('Cannot clear empty basket.')

        del self.purchases
        self.purchases = dict()

    def is_empty(self):
        return not self.purchases

    def calculate_price(self):
        return sum([purchase.calculate_price() for purchase in self.purchases.values()])

    def get_invoice(self):
        ret = {
            'items' : dict(),
            'total_price' : str(self.calculate_price())
        }

        for sku in self.purchases:
            purchase = self.purchases[sku]
            ret['items'][sku] = purchase.get_invoice()

        return ret
