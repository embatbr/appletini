"""This module contains the models (items, pricing rules and etc.).
"""


import re
from datetime import datetime

from money import Money


class ItemError(Exception):

    def __init__(self, message):
        self.message = message


class Item(object):

    def __init__(self, sku, name, price):
        """Type and "None" validation are executed in the module `logic`.
        """
        if not re.match('^[0-9]+\.[0-9]{2}$', price):
            raise ItemError('Amount %s is not in the correct format.' % price)

        self.sku = sku.strip()
        self.name = name.strip()
        self.price = Money(price, 'USD')

    def describe(self):
        return '%s %s $%s' % (self.sku, self.name, self.price.amount)


class PurchaseError(Exception):

    def __init__(self, message):
        self.message = message


class Purchase(object):

    def __init__(self, item, amount, timestamp):
        if amount < 1:
            raise PurchaseError('Must purchase at least 1 item.')

        self.item = item
        self.amount = amount
        self.timestamp = timestamp

    def increase_amount(self):
        self.amount = self.amount + 1

    def decrease_amount(self):
        if self.amount == 1:
            raise PurchaseError('Item amount cannot be less than 1.')

        self.amount = self.amount - 1


class PurchaseBasketError(Exception):

    def __init__(self, message):
        self.message = message


class PurchaseBasket(object):

    def __init__(self):
        self.purchases = dict()

    def add_item(self, item):
        if item.sku in self.purchases:
            self.purchases[item.sku].increase_amount()
        else:
            self.purchases[item.sku] = Purchase(item, 1, datetime.utcnow())

    def remove_item(self, sku, remove_all=False):
        if sku not in self.purchases:
            raise PurchaseBasketError('Cannot remove non-existing item.')

        if remove_all or self.purchases[sku].amount == 1:
            del self.purchases[sku]
        else:
            self.purchases[sku].amount = self.purchases[sku].amount - 1

    def clear(self):
        if not self.purchases:
            raise PurchaseBasketError('Cannot clear empty basket.')

        del self.purchases
        self.purchases = dict()