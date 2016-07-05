"""Automated tests for module `app.logic`.
"""


import unittest

from app.logic import Shopping, ShoppingError


class ShoppingTestCase(unittest.TestCase):

    def setUp(self):
        self.shopping = Shopping()

    def test_should_not_purchase_an_item_when_status_is_not_SHOPPING(self):
        self.shopping.state = 'PAYMENT'

        with self.assertRaises(ShoppingError) as catched:
            self.shopping.purchase_item('ipd')

        error = catched.exception
        self.assertEqual(error.message, 'Purchases are allowed only when state is SHOPPING.')

    def test_should_not_purchase_an_item_with_invalid_sku(self):
        with self.assertRaises(ShoppingError) as catched:
            self.shopping.purchase_item('smsng')

        error = catched.exception
        self.assertEqual(error.message, 'Cannot purchase an invalid item.')

    def test_should_purchase_an_item(self):
        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.purchase_item('ipd')

        self.assertIn('ipd', self.shopping.purchase_basket.purchases)

    def test_should_not_return_an_item_when_status_is_not_SHOPPING(self):
        self.shopping.state = 'PAYMENT'

        with self.assertRaises(ShoppingError) as catched:
            self.shopping.return_item('ipd')

        error = catched.exception
        self.assertEqual(error.message, 'Returns are allowed only when state is SHOPPING.')

    def test_should_not_return_an_item_with_invalid_sku(self):
        with self.assertRaises(ShoppingError) as catched:
            self.shopping.return_item('smsng')

        error = catched.exception
        self.assertEqual(error.message, 'Cannot return an invalid item.')

    def test_should_return_an_item(self):
        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.purchase_item('ipd')

        self.assertIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.return_item('ipd')

        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

    def test_should_return_all_items_of_same_type(self):
        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

        self.shopping.purchase_item('ipd')
        self.shopping.purchase_item('ipd')
        self.shopping.purchase_item('ipd')

        self.assertEqual(self.shopping.purchase_basket.purchases['ipd'].amount, 3)

        self.shopping.return_item('ipd', return_all=True)

        self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

    def test_should_not_checkout_when_state_is_not_SHOPPING(self):
        self.shopping.state = 'PAYMENT'

        with self.assertRaises(ShoppingError) as catched:
            self.shopping.checkout()

        error = catched.exception
        self.assertEqual(error.message, 'Checkouts are allowed only when state is SHOPPING.')

    def test_should_not_checkout_when_basket_is_empty(self):
        with self.assertRaises(ShoppingError) as catched:
            self.shopping.checkout()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot checkout with an empty basket.')

    def test_should_checkout(self):
        self.assertEqual(self.shopping.state, 'SHOPPING')

        self.shopping.purchase_item('ipd')
        self.shopping.purchase_item('mbp')

        self.shopping.checkout()

        self.assertEqual(self.shopping.state, 'PAYMENT')

    def test_should_not_pay_when_state_is_not_PAYMENT(self):
        with self.assertRaises(ShoppingError) as catched:
            self.shopping.charge()

        error = catched.exception
        self.assertEqual(error.message, 'Payments are allowed only when state is PAYMENT.')

    def test_should_pay(self):
        self.shopping.state = 'PAYMENT'

        self.assertEqual(self.shopping.state, 'PAYMENT')

        invoice = self.shopping.charge()

        self.assertEqual(self.shopping.state, 'CHARGED')
        self.assertIsNotNone(invoice)
        # TODO detalhar invoice (app.domains.Invoice) com itens pedidos,
        #      descontos (criar "item desconto") e valor total