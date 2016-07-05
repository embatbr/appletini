"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal

from app.domains import Item, ItemError, Purchase, PurchaseError, PurchaseBasket
from app.domains import PurchaseBasketError


class ItemTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'ipd'
        self.name = 'Super iPad'
        self.price = '549.99'

    def test_should_not_create_an_item_with_price_in_wrong_format(self):
        with self.assertRaises(ItemError) as catched:
            Item(self.sku, self.name, '1.9')

        error = catched.exception
        self.assertEqual(error.message, 'Amount 1.9 is not in the correct format.')

    def test_should_create_an_item(self):
        item = Item(self.sku, self.name, self.price)

        self.assertEqual(item.sku, self.sku)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price.amount, Decimal(self.price))

    def test_should_describe_an_item(self):
        item = Item(self.sku, self.name, self.price)
        self.assertEqual(item.describe(), '%s %s $%s' % (self.sku, self.name, self.price))


class PurchaseTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'ipd'
        self.name = 'Super iPad'
        self.price = '549.99'

    def test_should_not_purchase_less_than_one_item(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 0)

        error = catched.exception
        self.assertEqual(error.message, 'Must purchase at least 1 item.')

    def test_should_purchase_an_item(self):
        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3)

        self.assertEqual(purchase.item.sku, self.sku)
        self.assertEqual(purchase.item.name, self.name)
        self.assertEqual(purchase.item.price.amount, Decimal(self.price))

        self.assertEqual(purchase.amount, 3)

    def test_should_increase_item_amount_by_one(self):
        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3)

        self.assertEqual(purchase.amount, 3)

        purchase.increase_amount()

        self.assertEqual(purchase.amount, 4)

    def test_should_not_decrease_item_amount_to_less_than_one(self):
        with self.assertRaises(PurchaseError) as catched:
            item = Item(self.sku, self.name, self.price)
            purchase = Purchase(item, 1)
            purchase.decrease_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Item amount cannot be less than 1.')

    def test_should_decrease_item_amount_by_one(self):
        item = Item(self.sku, self.name, self.price)
        purchase = Purchase(item, 3)

        self.assertEqual(purchase.amount, 3)

        purchase.decrease_amount()

        self.assertEqual(purchase.amount, 2)


class PurchaseBasketTestCase(unittest.TestCase):

    def setUp(self):
        self.purchase_basket = PurchaseBasket()
        self.item = Item('ipd', 'Super iPad', '549.99')

    def test_should_add_a_new_item(self):
        self.assertNotIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_item(self.item)

        self.assertIn(self.item.sku, self.purchase_basket.purchases)
        self.assertIsNotNone(self.purchase_basket.purchases[self.item.sku])
        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

    def test_should_increment_amount_by_one_of_existing_item(self):
        self.purchase_basket.purchases[self.item.sku] = Purchase(self.item, 1)
        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

        self.purchase_basket.add_item(self.item)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 2)

    def test_should_not_remove_item_for_non_existing_given_sku(self):
        self.assertNotIn(self.item.sku, self.purchase_basket.purchases)

        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.remove_item(self.item.sku)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot remove non-existing item.')

    def test_should_delete_item_when_removing_purchase_of_amount_one(self):
        self.purchase_basket.add_item(self.item)

        self.assertIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.remove_item(self.item.sku)

        self.assertNotIn(self.item.sku, self.purchase_basket.purchases)

    def test_should_decrease_item_amount_when_removing_purchase_of_amount_higher_than_one(self):
        self.purchase_basket.add_item(self.item)

        self.assertIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_item(self.item)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 2)

        self.purchase_basket.remove_item(self.item.sku)

        self.assertEqual(self.purchase_basket.purchases[self.item.sku].amount, 1)

    def test_should_not_clear_empty_purchase_basket(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.clear()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot clear empty basket.')

    def test_should_clear_purchase_basket(self):
        self.assertFalse(self.purchase_basket.purchases)

        self.purchase_basket.add_item(self.item)

        self.assertTrue(self.purchase_basket.purchases)
        self.assertIn(self.item.sku, self.purchase_basket.purchases)

        self.purchase_basket.purchases.clear()

        self.assertFalse(self.purchase_basket.purchases)

    def test_should_be_considered_empty_if_has_no_purchase(self):
        self.assertTrue(self.purchase_basket.is_empty())

        self.purchase_basket.add_item(self.item)

        self.assertFalse(self.purchase_basket.is_empty())