"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal

from app.domains import Product, Purchase, PurchaseBasket
from app.configs import BaseError


class PurchaseTestCase(unittest.TestCase):

    def setUp(self):
        self.product = Product('ipd', 'Super iPad', '549.99')
        self.purchase = Purchase(self.product, 1)

    def test_should_increase_units_by_one(self):
        self.assertEqual(self.purchase.units, 1)

        self.purchase.increase_units()

        self.assertEqual(self.purchase.units, 2)

    def test_should_decrease_units_by_one(self):
        self.assertEqual(self.purchase.units, 1)

        self.purchase.decrease_units()

        self.assertEqual(self.purchase.units, 0)

    def test_should_multiply_product_price_by_purchase_units(self):
        expected_price = self.product.price * self.purchase.units

        self.assertEqual(self.purchase.calculate_price(), expected_price)

        self.purchase.increase_units()

        self.assertEqual(self.purchase.units, 2)

        expected_price = self.product.price * self.purchase.units

        self.assertEqual(self.purchase.calculate_price(), expected_price)

    def test_should_return_a_dictionary_with_name_units_and_price(self):
        invoice = self.purchase.get_invoice()

        self.assertIsInstance(invoice, dict)
        self.assertIn('name', invoice)
        self.assertEqual(invoice['name'], self.product.name)
        self.assertIn('units', invoice)
        self.assertEqual(invoice['units'], self.purchase.units)
        self.assertIn('price', invoice)
        self.assertEqual(invoice['price'], str(self.purchase.calculate_price()))


class PurchaseBasketTestCase(unittest.TestCase):

    def setUp(self):
        self.purchase_basket = PurchaseBasket()
        self.product = Product('ipd', 'Super iPad', '549.99')

    def test_should_create_a_purchase_object_when_purchasing_a_non_existing_product(self):
        self.assertNotIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)
        self.assertIsNotNone(self.purchase_basket.purchases[self.product.sku])
        self.assertEqual(self.purchase_basket.purchases[self.product.sku].units, 1)

    def test_should_increment_units_by_one_when_purchasing_an_existing_product(self):
        self.purchase_basket.purchases[self.product.sku] = Purchase(self.product, 1)
        self.assertEqual(self.purchase_basket.purchases[self.product.sku].units, 1)

        self.purchase_basket.add_product(self.product)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].units, 2)

    def test_should_delete_product_when_removing_purchase_with_one_unit(self):
        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.remove_product(self.product.sku)

        self.assertNotIn(self.product.sku, self.purchase_basket.purchases)

    def test_should_decrease_product_units_when_removing_purchase_more_than_one_unit(self):
        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].units, 2)

        self.purchase_basket.remove_product(self.product.sku)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].units, 1)

    def test_should_clear_purchase_basket(self):
        self.assertFalse(self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertTrue(self.purchase_basket.purchases)
        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.purchases.clear()

        self.assertFalse(self.purchase_basket.purchases)
