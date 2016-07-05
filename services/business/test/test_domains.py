"""Automated tests for module `app.domains`.
"""


import unittest
from decimal import Decimal

from app.domains import Product, ProductError, Purchase, PurchaseError, PurchaseBasket
from app.domains import PurchaseBasketError, Invoice


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.sku = 'ipd'
        self.name = 'Super iPad'
        self.price = '549.99'

    def test_should_not_create_a_product_with_price_in_wrong_format(self):
        with self.assertRaises(ProductError) as catched:
            Product(self.sku, self.name, '1.9')

        error = catched.exception
        self.assertEqual(error.message, 'Amount 1.9 is not in the correct format.')

    def test_should_create_a_product(self):
        product = Product(self.sku, self.name, self.price)

        self.assertEqual(product.sku, self.sku)
        self.assertEqual(product.name, self.name)
        self.assertEqual(product.price.amount, Decimal(self.price))

    def test_should_describe_a_product(self):
        product = Product(self.sku, self.name, self.price)

        self.assertEqual(product.describe(), '%s %s $%s' % (self.sku, self.name, self.price))


class PurchaseTestCase(unittest.TestCase):

    def setUp(self):
        self.product = Product('ipd', 'Super iPad', '549.99')

    def test_should_not_purchase_less_than_one_product_item(self):
        with self.assertRaises(PurchaseError) as catched:
            purchase = Purchase(self.product, 0)

        error = catched.exception
        self.assertEqual(error.message, 'Must purchase at least 1 item.')

    def test_should_purchase_a_product(self):
        purchase = Purchase(self.product, 3)

        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.amount, 3)

    def test_should_increase_product_amount_by_one(self):
        purchase = Purchase(self.product, 3)

        self.assertEqual(purchase.amount, 3)

        purchase.increase_amount()

        self.assertEqual(purchase.amount, 4)

    def test_should_not_decrease_product_amount_to_less_than_one(self):
        with self.assertRaises(PurchaseError) as catched:
            purchase = Purchase(self.product, 1)
            purchase.decrease_amount()

        error = catched.exception
        self.assertEqual(error.message, 'Product amount cannot be less than 1.')

    def test_should_decrease_product_amount_by_one(self):
        purchase = Purchase(self.product, 3)

        self.assertEqual(purchase.amount, 3)

        purchase.decrease_amount()

        self.assertEqual(purchase.amount, 2)

    def test_should_purchase_calculate_price(self):
        purchase = Purchase(self.product, 3)

        self.assertEqual(purchase.calculate_price(), Decimal('1649.97'))


class PurchaseBasketTestCase(unittest.TestCase):

    def setUp(self):
        self.purchase_basket = PurchaseBasket()
        self.product = Product('ipd', 'Super iPad', '549.99')

    def test_should_add_a_new_product_item(self):
        self.assertNotIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)
        self.assertIsNotNone(self.purchase_basket.purchases[self.product.sku])
        self.assertEqual(self.purchase_basket.purchases[self.product.sku].amount, 1)

    def test_should_increment_amount_by_one_of_existing_product_in_basket(self):
        self.purchase_basket.purchases[self.product.sku] = Purchase(self.product, 1)
        self.assertEqual(self.purchase_basket.purchases[self.product.sku].amount, 1)

        self.purchase_basket.add_product(self.product)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].amount, 2)

    def test_should_not_remove_an_item_for_non_existing_given_sku(self):
        self.assertNotIn(self.product.sku, self.purchase_basket.purchases)

        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.remove_product(self.product.sku)

        error = catched.exception
        self.assertEqual(error.message, 'Cannot remove non-existing product item.')

    def test_should_delete_product_when_removing_purchase_of_amount_one(self):
        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.remove_product(self.product.sku)

        self.assertNotIn(self.product.sku, self.purchase_basket.purchases)

    def test_should_decrease_product_amount_when_removing_purchase_of_amount_higher_than_one(self):
        self.purchase_basket.add_product(self.product)

        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].amount, 2)

        self.purchase_basket.remove_product(self.product.sku)

        self.assertEqual(self.purchase_basket.purchases[self.product.sku].amount, 1)

    def test_should_not_clear_empty_purchase_basket(self):
        with self.assertRaises(PurchaseBasketError) as catched:
            self.purchase_basket.clear()

        error = catched.exception
        self.assertEqual(error.message, 'Cannot clear empty basket.')

    def test_should_clear_purchase_basket(self):
        self.assertFalse(self.purchase_basket.purchases)

        self.purchase_basket.add_product(self.product)

        self.assertTrue(self.purchase_basket.purchases)
        self.assertIn(self.product.sku, self.purchase_basket.purchases)

        self.purchase_basket.purchases.clear()

        self.assertFalse(self.purchase_basket.purchases)

    def test_should_be_considered_empty_if_has_no_purchase(self):
        self.assertTrue(self.purchase_basket.is_empty())

        self.purchase_basket.add_product(self.product)

        self.assertFalse(self.purchase_basket.is_empty())

    def test_should_calculate_basket_total_value(self):
        self.assertTrue(self.purchase_basket.is_empty())

        self.purchase_basket.add_product(self.product)
        self.purchase_basket.add_product(self.product)

        self.assertEqual(self.purchase_basket.calculate_price(), Decimal('1099.98'))


class InvoiceTestCase(unittest.TestCase):

    def setUp(self):
        self.purchase_basket = PurchaseBasket()

        ipd = Product('ipd', 'Super iPad', '549.99')
        mbp = Product('mbp', 'MacBook Pro', '1399.99')
        atv = Product('atv', 'Apple TV', '109.50')
        vga = Product('vga', 'VGA adapter', '30.00')

        self.purchase_basket.add_product(atv)
        self.purchase_basket.add_product(atv)
        self.purchase_basket.add_product(atv)

        self.purchase_basket.add_product(ipd)
        self.purchase_basket.add_product(ipd)
        self.purchase_basket.add_product(ipd)
        self.purchase_basket.add_product(ipd)
        self.purchase_basket.add_product(ipd)

        self.purchase_basket.add_product(mbp)

        self.purchase_basket.add_product(vga)

    def test_should_process_invoice_correctly(self):
        invoice = Invoice(self.purchase_basket)

        for (sku, amount, price) in invoice.items:
            self.assertIn(sku, self.purchase_basket.purchases)

            purchase = self.purchase_basket.purchases[sku]

            int_amount = int(amount)
            self.assertEqual(int_amount, purchase.amount)

            expected_price = (int_amount * purchase.product.price).amount
            self.assertEqual(Decimal(price[1 : ]), expected_price)

        basket_price = self.purchase_basket.calculate_price()
        self.assertEqual(invoice.total_price, basket_price)