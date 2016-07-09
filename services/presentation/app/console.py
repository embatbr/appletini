"""Non-graphic user interface.
"""


import ast


class Reader(object):

    def read(self):
        cmdline = input('>>> ')

        return cmdline.strip().split(' ')


class Writer(object):

    def write(self, screen):
        print(screen)

    def write_error(self, err):
        self.write('err: %s' % err)

    def write_help(self):
        screen = '\n\t\tHELP\nCOMMAND\t\t\tDESCRIPTION\n'
        screen = '%s\nhelp\t\t\tshows this list' % screen
        screen = '%s\nproducts\t\tshows list of products' % screen
        screen = '%s\nbasket\t\t\tshows current basket' % screen
        screen = '%s\nadd <SKU>\t\tadds product to basket given SKU' % screen
        screen = '%s\nremove <SKU> \t\tremoves product from basket given SKU' % screen
        screen = '%s\nclear\t\t\tremoves all products (clears) from basket' % screen
        screen = '%s\ncheckout\t\tfinishes shopping and shows basket' % screen
        screen = '%s\npromotions\t\tshows current promotions' % screen
        screen = '%s\nexit\t\t\tleaves APPLETINI' % screen
        screen = '%s\n' % screen

        self.write(screen)

    # TODO get from service **business** (and later, from **storage**)
    def write_products(self, products):
        screen = '\n\t\tPRODUCTS\nSKU\tNAME\t\t\tPRICE (USD)\n'

        for sku in products:
            product = products[sku]

            name = product['name']
            price = product['price']

            screen = '%s\n%s\t%s\t\t%10s' % (screen, sku, name, price)

        new_line = '\n' if products else ''
        screen = '%s%s' % (screen, new_line)

        self.write(screen)

    def write_basket(self, basket):
        screen = '\n\t\t\tBASKET\nSKU\t\tNAME\t\tUNITS\tPRICE (USD)\n'

        items = basket['items']
        for sku in items:
            item = items[sku]

            name = item['name']
            units = item['units']
            price = item['price']

            screen = '%s\n%s\t\t%s\t%05s\t%10s' % (screen, sku, name, units, price)

        new_line = '\n' if items else ''
        screen = '%s%s' % (screen, new_line)

        if 'promotions' in basket:
            promotions = basket['promotions']
            for code in promotions:
                promotion = promotions[code]

                price = promotion['price']

                screen = '%s\n%s\t\t\t\t\t%10s' % (screen, code, price)

            screen = '%s\n' % screen

        screen = '%s\nTOTAL:\t\t\t\t\t%10s\n' % (screen, basket['total_price'])

        self.write(screen)

    def write_promotions(self, promotions):
        screen = '\n\t\tPROMOTIONS\nCODE\t\t\tDESCRIPTION\n'

        for code in promotions:
            promotion = promotions[code]

            description = promotion['description']

            screen = '%s\n%s\t\t\t%s' % (screen, code, description)

        new_line = '\n' if promotions else ''
        screen = '%s%s' % (screen, new_line)

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
            'add',
            'remove',
            'clear',
            'checkout',
            'promotions',
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
                func = getattr(self, 'cmd_%s' % self.cmd)
                func(args)
            else:
                self.writer.write('Unknown command.')
                self.cmd_help(args)

    def cmd_help(self, args):
        self.writer.write_help()

    def cmd_products(self, args):
        self.__cmd_products_or_basket('products')

    def cmd_basket(self, args):
        self.__cmd_products_or_basket('basket')

    def __cmd_products_or_basket(self, action):
        try:
            ret = getattr(self.business_client, 'get_%s' % action)()
            payload = ret['payload']

            if ret['success']:
                payload = ast.literal_eval(payload)
                getattr(self.writer, 'write_%s' % action)(payload)
            else:
                self.writer.write_error(payload)

        except Exception as err:
            self.writer.write_error(err)

    def cmd_add(self, args):
        self.__cmd_add_or_remove('add', args)

    def cmd_remove(self, args):
        self.__cmd_add_or_remove('remove', args)

    def __cmd_add_or_remove(self, action, args):
        if not args:
            self.writer.write('You must provide the SKU.')
            self.writer.write_help()
            return

        try:
            sku = args[0]

            ret = getattr(self.business_client, '%s' % action)(sku)
            payload = ret['payload']

            if ret['success']:
                payload = ast.literal_eval(payload)
                self.writer.write_basket(payload)
            else:
                self.writer.write_error(payload)

        except Exception as err:
            self.writer.write_error(err)

    def cmd_clear(self, args):
        ret = self.business_client.clear_basket()
        payload = ret['payload']

        if ret['success']:
            payload = ast.literal_eval(payload)
            self.writer.write_basket(payload)
        else:
            self.writer.write_error(payload)

    def cmd_checkout(self, args):
        ret = self.business_client.checkout()
        payload = ret['payload']

        if ret['success']:
            payload = ast.literal_eval(payload)
            self.writer.write_basket(payload)
        else:
            self.writer.write_error(payload)

    def cmd_promotions(self, args):
        ret = self.business_client.get_promotions()
        payload = ret['payload']

        if ret['success']:
            payload = ast.literal_eval(payload)
            self.writer.write_promotions(payload)
        else:
            self.writer.write_error(payload)

    def cmd_exit(self, args):
        self.alive = False

        self.writer.write('Thanks. Come back soon.')