"""Automated tests for module `app.logic`.
"""


import unittest

from app.domains import Product, Promotion, PurchaseBasket
from app.logic import Shopping
from app.configs import condition_atv3by2, condition_ipd50, condition_mbpvga
from app.configs import reward_atv3by2, reward_ipd50, reward_mbpvga
from app.configs import BaseError


class ShoppingTestCase(unittest.TestCase):

    def setUp(self):
        products = {
            'ipd' : Product('ipd', 'Super iPad', '549.99'),
            'mbp' : Product('mbp', 'MacBook Pro', '1399.99'),
            'atv' : Product('atv', 'Apple TV', '109.50'),
            'vga' : Product('vga', 'VGA adapter', '30.00')
        }

        promotions = {
            'atv3by2' : Promotion('atv3by2', condition_atv3by2, reward_atv3by2, 'For each 3 Apple TVs you buy, 1 is for free!'),
            'ipd50' : Promotion('ipd50', condition_ipd50, reward_ipd50, 'Buy more than 4 Super Ipads and pay only $499.99 on each!'),
            'mbpvga' : Promotion('mbpvga', condition_mbpvga, reward_mbpvga, 'Each MacBook Pro comes with a free VGA adapter!')
        }

        purchase_basket = PurchaseBasket()

        self.shopping = Shopping(products, promotions, purchase_basket)

    def test_should_not_purchase_a_product_with_invalid_sku(self):
        with self.assertRaises(BaseError) as catched:
            self.shopping.purchase_product('smsng')

        error = catched.exception
        self.assertEqual(error.message, 'Cannot purchase an invalid product.')

    def test_should_purchase_a_product(self):
        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.purchase_product('ipd')

        self.assertIn('ipd', self.shopping.purchase_basket.purchases)

    def test_should_not_return_a_product_with_invalid_sku(self):
        with self.assertRaises(BaseError) as catched:
            self.shopping.return_product('smsng')

        error = catched.exception
        self.assertEqual(error.message, 'Cannot return an invalid product.')

    def test_should_not_return_a_non_purchased_product(self):
        with self.assertRaises(BaseError) as catched:
            self.shopping.return_product('atv')

        error = catched.exception
        self.assertEqual(error.message, 'Cannot remove a non-purchased product.')

    def test_should_return_a_purchased_product(self):
        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.purchase_product('ipd')

        self.assertIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.return_product('ipd')

        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

    def test_should_not_clear_an_empty_purchase_basket(self):
        with self.assertRaises(BaseError) as catched:
            self.shopping.clear_basket()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot clear empty basket.')

    def test_should_clear_a_filled_purchase_basket(self):
        self.assertTrue(self.shopping.purchase_basket.is_empty())

        self.shopping.purchase_product('ipd')

        self.assertFalse(self.shopping.purchase_basket.is_empty())

        self.shopping.clear_basket()

        self.assertTrue(self.shopping.purchase_basket.is_empty())

    def test_should_not_checkout_when_basket_is_empty(self):
        with self.assertRaises(BaseError) as catched:
            self.shopping.checkout()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot checkout with an empty basket.')

    def test_should_checkout_and_return_an_invoice(self):
        self.shopping.purchase_product('ipd')
        self.shopping.purchase_product('ipd')
        self.shopping.purchase_product('ipd')
        self.shopping.purchase_product('ipd')
        self.shopping.purchase_product('ipd')

        invoice = self.shopping.checkout()

        self.assertIsNotNone(invoice)
        self.assertIn('items', invoice)
        self.assertIsInstance(invoice['items'], dict)
        self.assertIn('ipd', invoice['items'])
        self.assertIsInstance(invoice['items']['ipd'], dict)
        self.assertEqual(invoice['items']['ipd']['name'], 'Super iPad')
        self.assertEqual(invoice['items']['ipd']['units'], 5)
        self.assertEqual(invoice['items']['ipd']['price'], '2749.95')
        self.assertIn('promotions', invoice)
        self.assertIsInstance(invoice['promotions'], dict)
        self.assertIn('ipd50', invoice['promotions'])
        self.assertIsInstance(invoice['promotions']['ipd50'], dict)
        self.assertEqual(invoice['promotions']['ipd50']['price'], '-250.00')
        self.assertIn('total_price', invoice)
        self.assertIn(invoice['total_price'], '2499.95')
