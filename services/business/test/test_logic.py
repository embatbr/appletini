# """Automated tests for module `app.logic`.
# """


# import unittest

# from logic import Shopping, ShoppingError
# from domains import Product


# class ShoppingTestCase(unittest.TestCase):

#     def setUp(self):
#         products = {
#             'ipd' : Product('ipd', 'Super iPad', '549.99'),
#             'mbp' : Product('mbp', 'MacBook Pro', '1399.99'),
#             'atv' : Product('atv', 'Apple TV', '109.50'),
#             'vga' : Product('vga', 'VGA adapter', '30.00')
#         }

#         self.shopping = Shopping(products)

#     def test_should_not_purchase_a_product_when_status_is_not_SHOPPING(self):
#         self.shopping.state = 'PAYMENT'

#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.purchase_product('ipd')

#         error = catched.exception
#         self.assertEqual(error.message, 'Purchases are allowed only when state is SHOPPING.')

#     def test_should_not_purchase_a_product_with_invalid_sku(self):
#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.purchase_product('smsng')

#         error = catched.exception
#         self.assertEqual(error.message, 'Cannot purchase an invalid product.')

#     def test_should_purchase_a_product(self):
#         self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

#         self.shopping.purchase_product('ipd')

#         self.assertIn('ipd', self.shopping.purchase_basket.purchases)

#     def test_should_not_return_a_product_when_status_is_not_SHOPPING(self):
#         self.shopping.state = 'PAYMENT'

#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.return_product('ipd')

#         error = catched.exception
#         self.assertEqual(error.message, 'Returns are allowed only when state is SHOPPING.')

#     def test_should_not_return_a_product_with_invalid_sku(self):
#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.return_product('smsng')

#         error = catched.exception
#         self.assertEqual(error.message, 'Cannot return an invalid product.')

#     def test_should_return_a_product(self):
#         self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

#         self.shopping.purchase_product('ipd')

#         self.assertIn('ipd', self.shopping.purchase_basket.purchases)

#         self.shopping.return_product('ipd')

#         self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

#     def test_should_return_all_items_of_same_product(self):
#         self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

#         self.shopping.purchase_product('ipd')
#         self.shopping.purchase_product('ipd')
#         self.shopping.purchase_product('ipd')

#         self.assertEqual(self.shopping.purchase_basket.purchases['ipd'].amount, 3)

#         self.shopping.return_product('ipd', return_all=True)

#         self.assertNotIn('ipd', self.shopping.purchase_basket.purchases)

#     def test_should_not_checkout_when_state_is_not_SHOPPING(self):
#         self.shopping.state = 'PAYMENT'

#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.checkout()

#         error = catched.exception
#         self.assertEqual(error.message, 'Checkouts are allowed only when state is SHOPPING.')

#     def test_should_not_checkout_when_basket_is_empty(self):
#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.checkout()

#         error = catched.exception
#         self.assertEqual(error.message, 'Cannot checkout with an empty basket.')

#     def test_should_checkout(self):
#         self.assertEqual(self.shopping.state, 'SHOPPING')

#         self.shopping.purchase_product('ipd')
#         self.shopping.purchase_product('mbp')

#         self.shopping.checkout()

#         self.assertEqual(self.shopping.state, 'PAYMENT')

#     def test_should_not_pay_when_state_is_not_PAYMENT(self):
#         with self.assertRaises(ShoppingError) as catched:
#             self.shopping.charge()

#         error = catched.exception
#         self.assertEqual(error.message, 'Payments are allowed only when state is PAYMENT.')

#     def test_should_pay(self):
#         self.shopping.purchase_product('ipd')
#         self.shopping.purchase_product('ipd')
#         self.shopping.purchase_product('mbp')

#         self.shopping.checkout()
#         invoice = self.shopping.charge()

#         self.assertEqual(self.shopping.state, 'INVOICE')
#         self.assertIsNotNone(invoice)

#         # TODO detalhar invoice (app.domains.Invoice) com itens pedidos,
#         #      descontos (criar "product desconto") e valor total


# if __name__ == '__main__':
#     unittest.main()