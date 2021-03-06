"""This module executes the business logic (e.g., sum all prices, calculate
discounts).
"""


from decimal import Decimal

try:
    from configs import BaseError
except ImportError:
    from app.configs import BaseError


class Shopping(object):
    def __init__(self, products, promotions, purchase_basket):
        self.products = products # products available
        self.promotions = promotions

        self.purchase_basket = purchase_basket

    def purchase_product(self, sku):
        if sku not in self.products:
            raise BaseError('Cannot purchase an invalid product.')

        self.purchase_basket.add_product(self.products[sku])

    def return_product(self, sku):
        if sku not in self.products:
            raise BaseError('Cannot return an invalid product.')

        if not self.purchase_basket.has_purchase(sku):
            raise BaseError('Cannot return a non-purchased product.')

        try:
            self.purchase_basket.remove_product(sku)

        except BaseError as err:
            raise err

    def clear_basket(self):
        if self.purchase_basket.is_empty():
            raise BaseError('Cannot clear empty basket.')

        self.purchase_basket.clear()
        return self.export_basket()

    def checkout(self):
        if self.purchase_basket.is_empty():
            raise BaseError('Cannot checkout with an empty basket.')

        invoice = self.get_invoice()
        self.clear_basket()

        return invoice

    def export_products(self):
        ret = dict()

        for sku in self.products:
            product = self.products[sku]

            ret[sku] = {
                'name' : product.name,
                'price' : str(product.price)
            }

        return ret

    def export_basket(self):
        return self.get_invoice()

    def export_promotions(self):
        ret = dict()

        for code in self.promotions:
            promotion = self.promotions[code]

            ret[code] = {
                'description' : promotion.description
            }

        return ret

    def get_invoice(self):
        promotions = dict()
        total_discount = Decimal('0.00')
        # applying promotions
        for code in self.promotions:
            promotion = self.promotions[code]

            if promotion.condition(self):
                discount = promotion.reward(self)
                total_discount = total_discount + discount

                promotions[code] = {
                    'price' : str(discount)
                }

        invoice = self.purchase_basket.get_invoice()

        invoice['promotions'] = promotions

        total_price = self.purchase_basket.calculate_price() + total_discount
        invoice['total_price'] = str(total_price)

        return invoice