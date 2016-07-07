"""This module executes the business logic (e.g., sum all prices, calculate
discounts).
"""


from configs import BaseError


class Shopping(object):
    def __init__(self, products, promotions, purchase_basket):
        self.products = products # products available
        self.promotions = promotions

        self.purchase_basket = purchase_basket

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

    def export_promotions(self):
        ret = dict()

        for code in self.promotions:
            promotion = self.promotions[code]

            ret[code] = {
                'description' : promotion.describe()
            }

        return ret

    def purchase_product(self, sku):
        if sku not in self.products:
            raise BaseError('Cannot purchase an invalid product.')

        self.purchase_basket.add_product(self.products[sku])

        return self.purchase_basket.get_invoice()

    def return_product(self, sku):
        if sku not in self.products:
            raise BaseError('Cannot return an invalid product.')

        try:
            self.purchase_basket.remove_product(sku)
        except BaseError as err:
            raise err

        return self.purchase_basket.get_invoice()

    def checkout(self):
        if self.purchase_basket.is_empty():
            raise BaseError('Cannot checkout with an empty basket.')

        invoice = self.purchase_basket.get_invoice()
        self.clear_basket()

        return invoice