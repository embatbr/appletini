"""This module contains the models (products, pricing rules and etc.).

Validations of correct parameter type are not necessary, since those are
guaranteed by the callers.
"""


import re

from money import Money


class ProductError(Exception):

    def __init__(self, message):
        self.message = message


class Product(object):

    def __init__(self, sku, name, price):
        if not re.match('^[0-9]+\.[0-9]{2}$', price):
            raise ProductError('Amount %s is not in the correct format.' % price)

        self.sku = sku.strip()
        self.name = name.strip()
        self.price = Money(price, 'USD')

    def describe(self):
        return '%s %s $%s' % (self.sku, self.name, self.price.amount)


class PurchaseError(Exception):

    def __init__(self, message):
        self.message = message


class Purchase(object):

    def __init__(self, product, amount):
        if amount < 1:
            raise PurchaseError('Must purchase at least 1 item.')

        self.product = product
        self.amount = amount

    def increase_amount(self):
        self.amount = self.amount + 1

    def decrease_amount(self):
        if self.amount == 1:
            raise PurchaseError('Product amount cannot be less than 1.')

        self.amount = self.amount - 1

    def calculate_price(self):
        total_price = self.amount * self.product.price
        return total_price.amount


class PurchaseBasketError(Exception):

    def __init__(self, message):
        self.message = message


class PurchaseBasket(object):

    def __init__(self):
        self.purchases = dict()

    def add_product(self, product):
        if product.sku in self.purchases:
            self.purchases[product.sku].increase_amount()
        else:
            self.purchases[product.sku] = Purchase(product, 1)

    def remove_product(self, sku, remove_all=False):
        if sku not in self.purchases:
            raise PurchaseBasketError('Cannot remove non-existing product item.')

        if remove_all or self.purchases[sku].amount == 1:
            del self.purchases[sku]
        else:
            self.purchases[sku].amount = self.purchases[sku].amount - 1

    def clear(self):
        if not self.purchases:
            raise PurchaseBasketError('Cannot clear empty basket.')

        del self.purchases
        self.purchases = dict()

    def is_empty(self):
        return not self.purchases

    def calculate_price(self):
        return sum([purchase.calculate_price() for purchase in self.purchases.values()])


class Invoice(object):

    def __init__(self, purchase_basket):
        self.items = list()
        self.total_price = None

        self.__process(purchase_basket)

    def __process(self, purchase_basket):
        for (sku, purchase) in purchase_basket.purchases.items():
            # purchase = purchases[sku]
            amount = purchase.amount
            price = amount * purchase.product.price

            item = (sku, str(amount), '$%s' % price.amount)
            self.items.append(item)

        self.total_price = purchase_basket.calculate_price()

    # def report(self):
    #     report = map(lambda item: '---'.join(item), self.items)
    #     report = list(report)
    #     report = '\n'.join(report)

    #     report = '%s\n%s\n$%s' % (report, '-'*15, self.total_price)

    #     return report