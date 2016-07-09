"""All configurations must be here. This is the only module from the application
that can be import inside other modules (excepto `app`). The reason is to maintain
a good decoupled design.
"""


from decimal import Decimal


class BaseError(Exception):

    def __init__(self, message):
        self.message = message


# This should be in the storage service
products = {
    'ipd' : {
        'name' : 'Super iPad',
        'price' : '549.99'
    },
    'mbp' : {
        'name' : 'MacBook Pro',
        'price' : '1399.99'
    },
    'atv' : {
        'name' : 'Apple TV',
        'price' : '109.50'
    },
    'vga' : {
        'name' : 'VGA adapter',
        'price' : '30.00'
    }
}


# These functions for conditions and rewards could be saved in a database

def condition_atv3by2(shopping):
    basket = shopping.purchase_basket

    return basket.get_purchase_units('atv') >= 3

def reward_atv3by2(shopping):
    basket = shopping.purchase_basket

    units = basket.get_purchase_units('atv')
    price = basket.get_purchase_product_price('atv')

    discount_units = units // 3
    discount = price * discount_units
    discount = -discount

    return discount


def condition_ipd4gt(shopping):
    basket = shopping.purchase_basket

    return basket.get_purchase_units('ipd') > 4

def reward_ipd4gt(shopping):
    basket = shopping.purchase_basket

    units = basket.get_purchase_units('ipd')

    discount = Decimal('50.00') * units
    discount = -discount

    return discount


# implementation may change according to the reviewer's answer
def condition_mbpvga(shopping):
    basket = shopping.purchase_basket

    return basket.has_purchase('mbp')

# implementation may change according to the reviewer's answer
def reward_mbpvga(shopping):
    basket = shopping.purchase_basket

    mbp_units = basket.get_purchase_units('mbp')
    vga_units = 0

    if basket.has_purchase('vga'):
        vga_units = basket.get_purchase_units('vga')

    while mbp_units > vga_units:
        shopping.purchase_product('vga')
        vga_units = basket.get_purchase_units('vga')

    price_vga = basket.get_purchase_product_price('vga')

    discount = price_vga * mbp_units
    discount = -discount

    return discount


promotions = {
    'atv3by2' : {
        'condition' : condition_atv3by2,
        'reward' : reward_atv3by2,
        'description' : 'For each 3 Apple TVs you buy, 1 is for free!'
    },
    'ipd4gt' : {
        'condition' : condition_ipd4gt,
        'reward' : reward_ipd4gt,
        'description' : 'Buy more than 4 Super Ipads and pay only $499.99 on each!'
    },
    'mbpvga' : {
        'condition' : condition_mbpvga,
        'reward' : reward_mbpvga,
        'description' : 'Each MacBook Pro comes with a free VGA adapter!'
    }
}
