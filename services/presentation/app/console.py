"""
"""


class Reader(object):

    def read(self):
        cmdline = input('>>> ')

        return cmdline


class Writer(object):

    def write(self, screen):
        print(screen)

    def write_commands(self):
        screen = '\tCOMMANDS'
        screen = '%s\nhelp\t\tshows this list' % screen
        screen = '%s\nproducts\tshows list of products' % screen
        screen = '%s\nbasket\t\tshows current basket' % screen
        screen = '%s\nbuy <SKU>\tadd product to basket given SKU' % screen
        screen = '%s\nrm <SKU> [all]\tremoves product from basket' % screen
        screen = '%s\ncheckout\tfinished shopping and show basket' % screen
        screen = '%s\npay\t\tpay products and cleans basket' % screen
        screen = '%s\nexit\t\tleaves APPLETINI' % screen
        screen = '%s\n' % screen

        self.write(screen)

    def write_products(self):
        screen = '\tPRODUCTS\nSKU---NAME----------PRICE-----\n%s' % ('-' * 30)
        screen = '%s\nipd---Super iPad----$549.99---' % screen
        screen = '%s\nmbp---MacBook Pro---$1399.99--' % screen
        screen = '%s\natv---Apple TV------$109.50---' % screen
        screen = '%s\nvga---VGA adapter---$30.00----' % screen
        screen = '%s\n%s\n' % (screen, '-' * 30)

        self.write(screen)

    def write_basket(self):
        screen = '\tBASKET\nSKU---AMOUNT--------PRICE-----\n%s' % ('-' * 30)
        screen = '%s\nipd---%s----%s---' % (screen, 'A', 'P')
        screen = '%s\nmbp---%s---%s--' % (screen, 'A', 'P')
        screen = '%s\natv---%s------%s---' % (screen, 'A', 'P')
        screen = '%s\nvga---%s---%s----' % (screen, 'A', 'P')
        screen = '%s\n%s\n' % (screen, '-' * 30)
        screen = '%sTOTAL: ' % (screen)

        self.write(screen)


class Terminal(object):

    def __init__(self, reader, writer):
        """There are 3 screens: SHOPPING, PAYMENT, INVOICE
        """
        self.reader = reader
        self.writer = writer
        self.alive = False
        self.cmd = None

        self.screens = {
            'help' : 'write_commands',
            'products' : 'write_products',
            'basket' : 'write_basket',
            'exit' : 'end'
        }

    def init(self):
        print('Welcome to APPLETINI\n')

        self.alive = True
        self.writer.write_commands()

    def run(self):
        self.init()
        while self.alive:
            self.cmd = self.reader.read()

            screen_func = self.screens[self.cmd]
            func = getattr(self, screen_func, None)

            if not func:
                func = getattr(self.writer, screen_func, None)

            func()


    def end(self):
        self.alive = False