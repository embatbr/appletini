"""This module executes the business logic (e.g., sum all prices, calculate
discounts).
"""


from app.domains import Item, PurchaseBasket


class ShoppingError(Exception):

    def __init__(self, message):
        self.message = message


class Shopping(object):

    SHOPPING_STATES = [
        'SHOPPING', # acquiring or removing items
        'PAYMENT',  # finished the shopping, waiting for user to pay (may return to SHOPPING)
        'CHARGED'   # user paid, shopping ended
    ]

    def __init__(self):
        # all items available to buy
        self.items = {
            'ipd' : Item('ipd', 'Super iPad', '549.99'),
            'mbp' : Item('mbp', 'MacBook Pro', '1399.99'),
            'atv' : Item('atv', 'Apple TV', '109.50'),
            'vga' : Item('vga', 'VGA adapter', '30.00')
        }

        self.purchase_basket = PurchaseBasket()
        self.state = 'SHOPPING'

    def purchase_item(self, sku):
        if self.state != 'SHOPPING':
            raise ShoppingError('Purchases are allowed only when state is SHOPPING.')

        if sku not in self.items:
            raise ShoppingError('Cannot purchase an invalid item.')

        self.purchase_basket.add_item(self.items[sku])

    def return_item(self, sku, return_all=False):
        if self.state != 'SHOPPING':
            raise ShoppingError('Returns are allowed only when state is SHOPPING.')

        if sku not in self.items:
            raise ShoppingError('Cannot return an invalid item.')

        self.purchase_basket.remove_item(sku, remove_all=return_all)

    def checkout(self):
        if self.state != 'SHOPPING':
            raise ShoppingError('Checkouts are allowed only when state is SHOPPING.')

        if self.purchase_basket.is_empty():
            raise ShoppingError('Cannot checkout with an empty basket.')

        self.state = 'PAYMENT'

    def charge(self):
        if self.state != 'PAYMENT':
            raise ShoppingError('Payments are allowed only when state is PAYMENT.')

        self.state = 'CHARGED'

        # TODO return an app.domains.Invoice object