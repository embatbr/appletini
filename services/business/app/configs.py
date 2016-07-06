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
