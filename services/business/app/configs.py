from domains import Product


def __generate_products(items):
    products = dict()

    for sku in items:
        name = items[sku]['name']
        price = items[sku]['price']

        products[sku] = Product(sku, name, price)

    return products


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
    },
    'generator' : __generate_products
}
