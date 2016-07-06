"""This module executes the business logic (e.g., sum all prices, calculate
discounts).
"""


from configs import BaseError


class Shopping(object):
    """
        SHOPPING - acquiring or removing products
        PAYMENT  - finished the shopping, waiting for user to pay (TODO poder voltar para SHOPPING)
        INVOICE  - user paid, shopping ended
    """
    def __init__(self, products, purchase_basket):
        self.products = products # products available

        self.purchase_basket = purchase_basket
        self.state = 'SHOPPING'

    def export_products(self):
        ret = dict()

        for sku in self.products:
            product = self.products[sku]

            ret[sku] = {
                'name' : product.name,
                'price' : str(product.price.amount)
            }

        return ret

    def export_basket(self):
        return self.purchase_basket.get_invoice()

    def clear_basket(self):
        try:
            self.purchase_basket.clear()
            return self.export_basket()

        except BaseError as err:
            raise err

    def purchase_product(self, sku):
        if self.state != 'SHOPPING':
            raise BaseError('Purchases are allowed only when state is SHOPPING.')

        if sku not in self.products:
            raise BaseError('Cannot purchase an invalid product.')

        self.purchase_basket.add_product(self.products[sku])

        return self.purchase_basket.get_invoice()

    def return_product(self, sku):
        if self.state != 'SHOPPING':
            raise BaseError('Returns are allowed only when state is SHOPPING.')

        if sku not in self.products:
            raise BaseError('Cannot return an invalid product.')

        try:
            self.purchase_basket.remove_product(sku)
        except BaseError as err:
            raise err

        return self.purchase_basket.get_invoice()

    def checkout(self):
        if self.state != 'SHOPPING':
            raise BaseError('Checkouts are allowed only when state is SHOPPING.')

        if self.purchase_basket.is_empty():
            raise BaseError('Cannot checkout with an empty basket.')

        self.state = 'PAYMENT'

    def charge(self):
        if self.state != 'PAYMENT':
            raise BaseError('Payments are allowed only when state is PAYMENT.')

        self.state = 'INVOICE'
