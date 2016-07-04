"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal

from app.domains import Item, ItemError


class ItemTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'item_sku'
        self.name = 'item_name'
        self.price = ('usd', '1.99')

    def test_should_create_an_item(self):
        item = Item(self.sku, self.name, self.price)

        self.assertEqual(item.sku, self.sku)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price.currency, self.price[0].upper())
        self.assertEqual(item.price.amount, Decimal(self.price[1]))

    def test_should_not_create_an_item_with_None_sku(self):
        with self.assertRaises(ItemError) as catched:
            Item(None, self.name, self.price)

        error = catched.exception
        self.assertEqual(error.message, '`sku` must be a string')

    def test_should_not_create_an_item_with_non_string_sku(self):
        with self.assertRaises(ItemError) as catched:
            Item(1, self.name, self.price)

        error = catched.exception
        self.assertEqual(error.message, '`sku` must be a string')

    def test_should_not_create_an_item_with_None_name(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, None, self.price)

        error = catched.exception
        self.assertEqual(error.message, '`name` must be a string')

    def test_should_not_create_an_item_with_non_string_name(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, 1, self.price)

        error = catched.exception
        self.assertEqual(error.message, '`name` must be a string')

    def test_should_not_create_an_item_with_None_currency(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, (None, self.price[1]))

        error = catched.exception
        self.assertEqual(error.message, '`price[0]` must be a string')

    def test_should_not_create_an_item_with_non_string_currency(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, (1, self.price[1]))

        error = catched.exception
        self.assertEqual(error.message, '`price[0]` must be a string')

    def test_should_not_create_an_item_with_None_amount(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, (self.price[0], None))

        error = catched.exception
        self.assertEqual(error.message, '`price[1]` must be a string')

    def test_should_not_create_an_item_with_non_string_amount(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, (self.price[0], 1))

        error = catched.exception
        self.assertEqual(error.message, '`price[1]` must be a string')

    def test_should_not_create_an_item_with_amount_in_wrong_format(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, (self.price[0], '1.9'))

        error = catched.exception
        self.assertEqual(error.message, 'Amount 1.9 is not in the correct format.')
