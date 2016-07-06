"""This module executes the business logic (e.g., sum all prices, calculate
discounts).
"""


from domains import Product, PurchaseBasket, PurchaseBasketError


class ShoppingError(Exception):

    def __init__(self, message):
        self.message = message


class Shopping(object):
    """
        SHOPPING - acquiring or removing products
        PAYMENT  - finished the shopping, waiting for user to pay (TODO poder voltar para SHOPPING)
        INVOICE  - user paid, shopping ended
    """
    def __init__(self, products):
        # all products available to buy
        self.products = products

        self.purchase_basket = PurchaseBasket()
        self.state = 'SHOPPING'

    def purchase_product(self, sku):
        if self.state != 'SHOPPING':
            raise ShoppingError('Purchases are allowed only when state is SHOPPING.')

        if sku not in self.products:
            raise ShoppingError('Cannot purchase an invalid product.')

        self.purchase_basket.add_product(self.products[sku])

        return self.purchase_basket.get_invoice()

    def return_product(self, sku):
        if self.state != 'SHOPPING':
            raise ShoppingError('Returns are allowed only when state is SHOPPING.')

        if sku not in self.products:
            raise ShoppingError('Cannot return an invalid product.')

        try:
            self.purchase_basket.remove_product(sku)
        except PurchaseBasketError as err:
            raise err

        return self.purchase_basket.get_invoice()

    def checkout(self):
        if self.state != 'SHOPPING':
            raise ShoppingError('Checkouts are allowed only when state is SHOPPING.')

        if self.purchase_basket.is_empty():
            raise ShoppingError('Cannot checkout with an empty basket.')

        self.state = 'PAYMENT'

    def charge(self):
        if self.state != 'PAYMENT':
            raise ShoppingError('Payments are allowed only when state is PAYMENT.')

        self.state = 'INVOICE'
