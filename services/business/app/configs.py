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

def condition_atv3by2(purchase_basket):
    if not purchase_basket.has_purchase('atv'):
        return False

    if purchase_basket.get_purchase_units('atv') < 3:
        return False

    return True

def reward_atv3by2(purchase_basket):
    units = purchase_basket.get_purchase_units('atv')
    price = purchase_basket.get_purchase_product_price('atv')

    discount_units = units // 3
    discount = price * discount_units
    discount = -discount

    return discount


def condition_cheapipd(purchase_basket):
    if not purchase_basket.has_purchase('ipd'):
        return False

    if purchase_basket.get_purchase_units('ipd') < 5:
        return False

    return True

def reward_cheapipd(purchase_basket):
    units = purchase_basket.get_purchase_units('ipd')

    discount = Decimal('50.00') * units
    discount = -discount

    return discount


# implementation may change according to the reviewer's answer
def condition_mbpvga(purchase_basket):
    if (not purchase_basket.has_purchase('mbp')) or (not purchase_basket.has_purchase('vga')):
        return False

    return True

# implementation may change according to the reviewer's answer
def reward_mbpvga(purchase_basket):
    units_mbp = purchase_basket.get_purchase_units('mbp')
    units_vga = purchase_basket.get_purchase_units('vga')
    price_vga = purchase_basket.get_purchase_product_price('vga')

    units = min(units_mbp, units_vga)

    discount = price_vga * units
    discount = -discount

    return discount


promotions = {
    'atv3by2' : {
        'condition' : condition_atv3by2,
        'reward' : reward_atv3by2,
        'description' : 'For each 3 Apple TVs you buy, 1 is for free!'
    },
    'cheapipd' : {
        'condition' : condition_cheapipd,
        'reward' : reward_cheapipd,
        'description' : 'Buy more than 4 Super Ipads and pay only $499.99 on each!'
    },
    'mbpvga' : {
        'condition' : condition_mbpvga,
        'reward' : reward_mbpvga,
        'description' : 'Each MacBook Pro comes with a free VGA adapter!'
    }
}
