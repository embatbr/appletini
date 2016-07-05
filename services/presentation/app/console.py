"""
"""


class Reader(object):

    def read(self):
        cmdline = input('>>> ')

        return cmdline


class Writer(object):

    def write(self, screen):
        print(screen)

    def write_help(self):
        screen = '\tCOMMANDS'
        screen = '%s\nhelp\t\tshows this list' % screen
        screen = '%s\nproducts\tshows list of products' % screen
        screen = '%s\nbasket\t\tshows current basket' % screen
        screen = '%s\nbuy <SKU>\tadds product to basket given SKU' % screen
        screen = '%s\nrm <SKU> [all] \tremoves product (1-by-1 or all items) from basket' % screen
        screen = '%s\nclear\t\tremoves all products (clears) from basket' % screen
        screen = '%s\ncheckout\tfinishes shopping and shows basket' % screen
        screen = '%s\npay\t\tgenerates invoice and cleans basket' % screen
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
        self.reader = reader
        self.writer = writer
        self.alive = False
        self.cmd = None

        self.screens = set([
            'help',
            'products',
            'basket',
            'exit'
        ])

    def init(self):
        print('Welcome to APPLETINI\n')

        self.alive = True
        self.writer.write_help()

    def run(self):
        self.init()
        while self.alive:
            self.cmd = self.reader.read()

            if self.cmd in self.screens:
                func = getattr(self, self.cmd)
                func()
            else:
                self.writer.write('Unknown command')
                self.help()

    def help(self):
        self.writer.write_help()

    def products(self):
        self.writer.write_products()

    def basket(self):
        self.writer.write_basket()

    def exit(self):
        self.alive = False

        self.writer.write('Thanks. Come back soon.')