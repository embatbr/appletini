"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal
from datetime import datetime

from app.domains import Item, ItemError, Order, OrderError


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

    def test_should_describe_an_item(self):
        item = Item(self.sku, self.name, self.price)
        self.assertEqual(item.describe(), '%s %s $%s' % (self.sku, self.name, self.price[1]))


class OrderTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'item_sku'
        self.name = 'item_name'
        self.price = ('usd', '1.99')

    def test_should_not_order_a_None_item(self):
        with self.assertRaises(OrderError) as catched:
            order = Order(None, 1, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`item` must be of type `Item`.')

    def test_should_not_order_an_item_of_another_class_than_Item(self):
        with self.assertRaises(OrderError) as catched:
            order = Order(1, 1, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`item` must be of type `Item`.')

    def test_should_not_order_an_item_with_None_amount(self):
        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, None, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`amount` must be of type int.')

    def test_should_not_order_an_item_with_non_integer_amount(self):
        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, '1', datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`amount` must be of type int.')

    def test_should_not_order_less_than_one_item(self):
        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, 0, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, 'Must order at least 1 item.')

    def test_should_not_order_with_None_timestamp(self):
        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, 1, None)

        error = catched.exception
        self.assertEqual(error.message, '`timestamp` must be of type datetime.datetime')

    def test_should_not_order_with_non_datetime_timestamp(self):
        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, 1, 1)

        error = catched.exception
        self.assertEqual(error.message, '`timestamp` must be of type datetime.datetime')

    def test_should_order_an_item(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        order = Order(item, 3, now)

        clone = Item(self.sku, self.name, self.price)

        self.assertEqual(order.item.sku, clone.sku)
        self.assertEqual(order.item.name, clone.name)
        self.assertEqual(order.item.price.amount, clone.price.amount)
        self.assertEqual(order.item.price.currency, clone.price.currency)
        self.assertEqual(order.amount, 3)
        self.assertEqual(order.timestamp.year, now.year)
        self.assertEqual(order.timestamp.month, now.month)
        self.assertEqual(order.timestamp.day, now.day)
        self.assertEqual(order.timestamp.hour, now.hour)
        self.assertEqual(order.timestamp.minute, now.minute)
        self.assertEqual(order.timestamp.second, now.second)
        self.assertEqual(order.timestamp.microsecond, now.microsecond)

    def test_should_increase_item_amount_by_one(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        order = Order(item, 3, now)

        order.increase_amount()

        self.assertEqual(order.amount, 4)

    def test_should_decrease_item_amount_by_one(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        order = Order(item, 3, now)

        order.decrease_amount()

        self.assertEqual(order.amount, 2)

    def test_should_not_decrease_item_amount_to_less_than_one(self):
        now = datetime.utcnow()

        with self.assertRaises(OrderError) as catched:
            item = Item(self.sku, self.name, self.price)
            order = Order(item, 1, now)
            order.decrease_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Item amount cannot be less than 1.')