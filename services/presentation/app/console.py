"""Non-graphic user interface.
"""


import ast


class Reader(object):

    def read(self):
        cmdline = input('>>> ')

        return cmdline.split(' ')


class Writer(object):

    def write(self, screen):
        print(screen)

    def write_error(self, err):
        self.write('err: %s' % err)

    def write_help(self):
        screen = '\n\tHELP\nCOMMAND\t\tDESCRIPTION\n'
        screen = '%s\nhelp\t\tshows this list' % screen
        screen = '%s\nproducts\tshows list of products' % screen
        screen = '%s\nbasket\t\tshows current basket' % screen
        screen = '%s\nbuy <SKU>\tadds product to basket given SKU' % screen
        screen = '%s\nrm <SKU> \tremoves product from basket' % screen
        screen = '%s\nclear\t\tremoves all products (clears) from basket' % screen
        screen = '%s\ncheckout\tfinishes shopping and shows basket' % screen
        screen = '%s\npay\t\tgenerates invoice and cleans basket' % screen
        screen = '%s\npromotions\tshows current promotions' % screen
        screen = '%s\nexit\t\tleaves APPLETINI' % screen
        screen = '%s\n' % screen

        self.write(screen)

    # TODO get from service **business** (and later, from **storage**)
    def write_products(self, products):
        screen = '\n\tPRODUCTS\nSKU\tNAME\t\tPRICE\n'

        for sku in products:
            product = products[sku]

            name = product['name']
            price = product['price']

            screen = '%s\n%s\t%s\t$%s' % (screen, sku, name, price)

        screen = '%s\n' % screen

        self.write(screen)

    def write_basket(self, basket):
        screen = '\n\tBASKET\nSKU\tNAME\t\tAMOUNT\tPRICE\n'

        items = basket['items']
        for sku in items:
            item = items[sku]

            name = item['name']
            amount = item['amount']
            price = item['price']

            screen = '%s\n%s\t%s\t%s\t$%s' % (screen, sku, name, amount, price)

        screen = '%s\n\nTOTAL:\t\t\t\t$%s\n' % (screen, basket['total_price'])

        self.write(screen)


class Terminal(object):

    def __init__(self, reader, writer, business_client):
        self.reader = reader
        self.writer = writer
        self.business_client = business_client

        self.alive = False
        self.cmd = None

        self.screens = set([
            'help',
            'products',
            'basket',
            'buy',
            'rm',
            'exit'
        ])

    def init(self):
        self.writer.write('Welcome to APPLETINI\n')

        self.alive = True
        self.writer.write_help()

    def run(self):
        self.init()
        while self.alive:
            cmdline = self.reader.read()
            self.cmd = cmdline[0]
            args = cmdline[1 : ]

            if self.cmd in self.screens:
                func = getattr(self, self.cmd)
                func(args)
            else:
                self.writer.write('Unknown command.')
                self.help(args)

    def help(self, args):
        self.writer.write_help()

    def products(self, args):
        try:
            ret = self.business_client.get_products()
            payload = ret['payload']

            if ret['success']:
                payload = ast.literal_eval(payload)
                self.writer.write_products(payload)
            else:
                self.writer.write_error(payload)

        except Exception as err:
            self.writer.write_error(err)

    def basket(self, args):
        pass

    def buy(self, args):
        self.buy_or_rm('purchase', args)

    def rm(self, args):
        self.buy_or_rm('return', args)

    def buy_or_rm(self, action, args):
        if not args:
            self.writer.write('You must provide the SKU.')
            self.writer.write_help()
            return

        try:
            sku = args[0]

            ret = self.business_client.buy_or_rm(action, sku)
            payload = ret['payload']

            if ret['success']:
                payload = ast.literal_eval(payload)
                self.writer.write_basket(payload)
            else:
                self.writer.write_error(payload)

        except Exception as err:
            self.writer.write_error(err)

    def exit(self, args):
        self.alive = False

        self.writer.write('Thanks. Come back soon.')