"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal

from app.domains import Item, ItemError


class ItemTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_create_an_item_properly(self):
        sku = 'item_sku'
        name = 'item_name'
        price = ('usd', '1.99')

        # Preventing `sku` with value None
        with self.assertRaises(ItemError) as catched:
            Item(None, name, price)
        error = catched.exception
        self.assertEqual(error.message, '`sku` must be a string')

        # Preventing `sku` with non-string value
        with self.assertRaises(ItemError) as catched:
            Item(1, name, price)
        error = catched.exception
        self.assertEqual(error.message, '`sku` must be a string')

        # Preventing `name` with value None
        with self.assertRaises(ItemError) as catched:
            Item(sku, None, price)
        error = catched.exception
        self.assertEqual(error.message, '`name` must be a string')

        # Preventing `name` with non-string value
        with self.assertRaises(ItemError) as catched:
            Item(sku, 1, price)
        error = catched.exception
        self.assertEqual(error.message, '`name` must be a string')

        # Preventing `price` with first value None
        with self.assertRaises(ItemError) as catched:
            Item(sku, name, (None, price[1]))
        error = catched.exception
        self.assertEqual(error.message, '`price[0]` must be a string')

        # Preventing `price` with non-string first value
        with self.assertRaises(ItemError) as catched:
            Item(sku, name, (1, price[1]))
        error = catched.exception
        self.assertEqual(error.message, '`price[0]` must be a string')

        # Preventing `price` with second value None
        with self.assertRaises(ItemError) as catched:
            Item(sku, name, (price[0], None))
        error = catched.exception
        self.assertEqual(error.message, '`price[1]` must be a string')

        # Preventing `price` with non-string second value
        with self.assertRaises(ItemError) as catched:
            Item(sku, name, (price[0], 1))
        error = catched.exception
        self.assertEqual(error.message, '`price[1]` must be a string')

        # Preventing `price` with second value not in currency format
        with self.assertRaises(ItemError) as catched:
            Item(sku, name, (price[0], '1.9'))
        error = catched.exception
        self.assertEqual(error.message, 'Amount 1.9 is not in the correct format.')

        # Creating Item object correctly
        item = Item(sku, name, price)
        self.assertEqual(item.sku, sku)
        self.assertEqual(item.name, name)
        self.assertEqual(item.price.currency, price[0].upper())
        self.assertEqual(item.price.amount, Decimal(price[1]))