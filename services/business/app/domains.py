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
        if (not sku) or (not isinstance(sku, str)):
            raise ItemError('`sku` must be a string')

        self.sku = sku.strip()

        if (not name) or (not isinstance(name, str)):
            raise ItemError('`name` must be a string')

        self.name = name.strip()

        currency = price[0]
        if (not currency) or (not isinstance(currency, str)):
            raise ItemError('`price[0]` must be a string')

        currency = currency.strip().upper()

        amount = price[1]
        if (not amount) or (not isinstance(amount, str)):
            raise ItemError('`price[1]` must be a string')

        amount = amount.strip()

        amount_regex = '^[0-9]+\.[0-9]{2}$'
        if not re.match(amount_regex, amount):
            raise ItemError('Amount %s is not in the correct format.' % amount)

        self.price = Money(amount, currency)

    def describe(self):
        return '%s %s $%s' % (self.sku, self.name, self.price.amount)


class PurchaseError(Exception):

    def __init__(self, message):
        self.message = message


class Purchase(object):

    def __init__(self, item, amount, timestamp):
        if (not item) or (not isinstance(item, Item)):
            raise PurchaseError('`item` must be of type `Item`.')

        if (amount is None) or (not isinstance(amount, int)):
            raise PurchaseError('`amount` must be of type int.')

        if amount < 1:
            raise PurchaseError('Must purchase at least 1 item.')

        if (timestamp is None) or (not isinstance(timestamp, datetime)):
            raise PurchaseError('`timestamp` must be of type datetime.datetime')

        self.item = item
        self.amount = amount
        self.timestamp = timestamp
        self.finished = False

    def increase_amount(self):
        if self.finished:
            raise PurchaseError('Purchase already finished.')

        self.amount = self.amount + 1

    def decrease_amount(self):
        if self.finished:
            raise PurchaseError('Purchase already finished.')

        if self.amount == 1:
            raise PurchaseError('Item amount cannot be less than 1.')

        self.amount = self.amount - 1

    def finish(self):
        self.finished = True


class PurchaseBasketError(Exception):

    def __init__(self, message):
        self.message = message


class PurchaseBasket(object):

    def __init__(self):
        self.purchases = dict()

    def add_item(self, item):
        if item.sku in self.purchases:
            raise PurchaseBasketError('Cannot add an existing item.')

        self.purchases[item.sku] = Purchase(item, 1, datetime.utcnow())

    def increase_item_amount(self, sku):
        if sku not in self.purchases:
            raise PurchaseBasketError('Cannot increase amount of non-existing item.')

        self.purchases[sku].increase_amount()

    def decrease_item_amount(self, sku):
        if sku not in self.purchases:
            raise PurchaseBasketError('Cannot decrease amount of non-existing item.')

        self.purchases[sku].decrease_amount()

    def remove_item(self, sku):
        if sku not in self.purchases:
            raise PurchaseBasketError('Cannot remove non-existing item.')

        del self.purchases[sku]

    def clear(self):
        if not self.purchases:
            raise PurchaseBasketError('Cannot clear empty basket.')

        del self.purchases
        self.purchases = dict()