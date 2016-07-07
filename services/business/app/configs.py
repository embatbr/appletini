class BaseError(Exception):

    def __init__(self, message):
        self.message = message


# This should be in the storage service
products = {
    'items' : {
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
}


promotions = {
    'promo-3-by-2-atv-' : {
        'type' : 'discount',
        'condition' : 'units > 3',
        'reward' : 'price = -(price * units//3)'
    },
    'promo-ipd-50-usd-discount' : {
        'type' : 'discount',
        'condition' : 'units > 4',
        'reward' : 'price = price - (50.00 * units)'
    },
    'promo-free-vga-mbp' : {
        'type' : 'gift',
        'condition' : 'mbp in purchases',
        'reward' : 'vga.units = mbp.units'
    }
}
