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


promotions = {
    'atv-3-by-2' : {
        'category' : 'discount',
        'condition' : 'atv.units > 3',
        'reward' : 'atv.price = -(atv.price * atv.units//3)',
        'description' : 'For each 3 Apple TVs you buy, 1 is for free!'
    },
    'ipd-cheap' : {
        'category' : 'discount',
        'condition' : 'ipd.units > 4',
        'reward' : 'ipd.price = ipd.price - (50.00 * ipd.units)',
        'description' : 'Buy more than 4 Super Ipads and pay only $499.99 on each!'
    },
    'gift-vga' : {
        'category' : 'gift',
        'condition' : 'mbp.units > 0',
        'reward' : [
            'vga.units = mbp.units',
            'vga.price = $0.00'
        ],
        'description' : 'Each MacBook Pro comes with a free VGA adapter!'
    }
}
