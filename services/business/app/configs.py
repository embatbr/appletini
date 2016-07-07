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
    total_price = purchase_basket.calculate_price()

    units = purchase_basket.get_purchase_units('atv')
    price = purchase_basket.get_purchase_product_price('atv')

    discount_units = units // 3
    discount = price * discount_units
    discount = -discount

    return discount


promotions = {
    'atv3by2' : {
        'category' : 'discount',
        'condition' : condition_atv3by2,
        'reward' : reward_atv3by2,
        'description' : 'For each 3 Apple TVs you buy, 1 is for free!'
    }
    # },
    # 'cheapipd' : {
    #     'category' : 'discount',
    #     'condition' : 'ipd.units > 4',
    #     'reward' : 'total_price = total_price - (50.00 * ipd.units)',
    #     'description' : 'Buy more than 4 Super Ipads and pay only $499.99 on each!'
    # },
    # 'vgagift' : {
    #     'category' : 'gift',
    #     'condition' : 'mbp.units > 0',
    #     'reward' : [
    #         'vga.units = vga.units + mbp.units',
    #         'total_price = total_price - (mbp.units * vga.price)'
    #     ],
    #     'description' : 'Each MacBook Pro comes with a free VGA adapter!'
    # }
}
