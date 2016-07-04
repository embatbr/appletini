"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal
from datetime import datetime

from app.domains import Item, ItemError, Purchase, PurchaseError, PurchaseBasket
from app.domains import PurchaseBasketError


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


class PurchaseTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'item_sku'
        self.name = 'item_name'
        self.price = ('usd', '1.99')

    def test_should_not_purchase_a_None_item(self):
        with self.assertRaises(PurchaseError) as catched:
            purchase = Purchase(None, 1, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`item` must be of type `Item`.')

    def test_should_not_purchase_an_item_of_another_class_than_Item(self):
        with self.assertRaises(PurchaseError) as catched:
            purchase = Purchase(1, 1, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`item` must be of type `Item`.')

    def test_should_not_purchase_an_item_with_None_amount(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, None, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`amount` must be of type int.')

    def test_should_not_purchase_an_item_with_non_integer_amount(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, '1', datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, '`amount` must be of type int.')

    def test_should_not_purchase_less_than_one_item(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 0, datetime.utcnow())

        error = catched.exception
        self.assertEqual(error.message, 'Must purchase at least 1 item.')

    def test_should_not_purchase_with_None_timestamp(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 1, None)

        error = catched.exception
        self.assertEqual(error.message, '`timestamp` must be of type datetime.datetime')

    def test_should_not_purchase_with_non_datetime_timestamp(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 1, 1)

        error = catched.exception
        self.assertEqual(error.message, '`timestamp` must be of type datetime.datetime')

    def test_should_purchase_an_item(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3, now)

        clone = Item(self.sku, self.name, self.price)

        self.assertEqual(purchase.item.sku, clone.sku)
        self.assertEqual(purchase.item.name, clone.name)
        self.assertEqual(purchase.item.price.amount, clone.price.amount)
        self.assertEqual(purchase.item.price.currency, clone.price.currency)
        self.assertEqual(purchase.amount, 3)
        self.assertEqual(purchase.timestamp.year, now.year)
        self.assertEqual(purchase.timestamp.month, now.month)
        self.assertEqual(purchase.timestamp.day, now.day)
        self.assertEqual(purchase.timestamp.hour, now.hour)
        self.assertEqual(purchase.timestamp.minute, now.minute)
        self.assertEqual(purchase.timestamp.second, now.second)
        self.assertEqual(purchase.timestamp.microsecond, now.microsecond)
        self.assertFalse(purchase.finished)

    def test_should_not_increase_item_amount_for_finished_purchase(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3, now)

        purchase.finish()

        with self.assertRaises(PurchaseError) as catched:
            purchase.increase_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Purchase already finished.')

    def test_should_increase_item_amount_by_one(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3, now)

        purchase.increase_amount()

        self.assertEqual(purchase.amount, 4)

    def test_should_not_decrease_item_amount_for_finished_purchase(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3, now)

        purchase.finish()

        with self.assertRaises(PurchaseError) as catched:
            purchase.decrease_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Purchase already finished.')

    def test_should_not_decrease_item_amount_to_less_than_one(self):
        now = datetime.utcnow()

        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 1, now)
            purchase.decrease_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Item amount cannot be less than 1.')

    def test_should_decrease_item_amount_by_one(self):
        now = datetime.utcnow()

        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3, now)

        purchase.decrease_amount()

        self.assertEqual(purchase.amount, 2)


class PurchaseBasketTestCase(unittest.TestCase):

    def setUp(self):
        self.purchase_basket = PurchaseBasket()
        self.item = Item('ipd', 'Super iPad', ('usd', '549.99'))

    def test_should_not_add_existing_item(self):
        self.purchase_basket.add_item(self.item)

        self.assertEqual(len(self.purchase_basket.purchases), 1)

        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.add_item(self.item)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot add an existing item.')

    def test_should_add_new_item(self):
        self.assertEqual(len(self.purchase_basket.purchases), 0)

        self.purchase_basket.add_item(self.item)

        self.assertEqual(len(self.purchase_basket.purchases), 1)
        self.assertIn(self.item.sku, self.purchase_basket.purchases)

    def test_should_not_increase_item_amount_for_non_existing_item(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.increase_item_amount(self.item.sku)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot increase amount of non-existing item.')

    def test_should_increase_item_amount(self):
        self.assertEqual(len(self.purchase_basket.purchases), 0)

        self.purchase_basket.add_item(self.item)

        self.assertEqual(len(self.purchase_basket.purchases), 1)
        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

        self.purchase_basket.increase_item_amount(self.item.sku)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 2)

    def test_should_not_decrease_item_amount_for_non_existing_item(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.decrease_item_amount(self.item.sku)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot decrease amount of non-existing item.')

    def test_should_decrease_item_amount(self):
        self.assertEqual(len(self.purchase_basket.purchases), 0)

        self.purchase_basket.add_item(self.item)

        self.assertEqual(len(self.purchase_basket.purchases), 1)
        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

        self.purchase_basket.increase_item_amount(self.item.sku)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 2)

        self.purchase_basket.decrease_item_amount(self.item.sku)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

    def test_should_not_remove_all_items_for_non_existing_given_sku(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.remove_item(self.item.sku)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot remove non-existing item.')

    def test_should_remove_all_items_for_given_sku(self):
        self.assertEqual(len(self.purchase_basket.purchases), 0)

        self.purchase_basket.add_item(self.item)

        self.assertIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.remove_item(self.item.sku)

        self.assertEqual(len(self.purchase_basket.purchases), 0)
        self.assertNotIn(self.item.sku, self.purchase_basket.purchases)

    def test_should_not_clear_empty_purchase_basket(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.clear()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot clear empty basket.')

    def test_should_clear_purchase_basket(self):
        self.purchase_basket.add_item(self.item)

        self.assertIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.purchases.clear()

        self.assertEqual(len(self.purchase_basket.purchases), 0)