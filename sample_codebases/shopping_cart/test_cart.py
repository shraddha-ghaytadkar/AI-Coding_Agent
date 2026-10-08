"""
Unit tests for Shopping Cart system.
"""
import unittest
from cart import ShoppingCart
from discounts import calculate_discount
from tax_calculator import calculate_tax


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("item-1", "Laptop", 1000.00, 1)
        self.cart.add_item("item-2", "Mouse", 50.00, 2)

    def test_subtotal_calculation(self):
        self.assertEqual(self.cart.get_subtotal(), 1100.00)

    def test_item_quantity_merge(self):
        self.cart.add_item("item-2", "Mouse", 50.00, 1)
        self.assertEqual(len(self.cart.items), 2)
        mouse_item = next(i for i in self.cart.items if i.item_id == "item-2")
        self.assertEqual(mouse_item.quantity, 3)

    def test_discount_calculation(self):
        subtotal = self.cart.get_subtotal()
        discount = calculate_discount(subtotal, "WELCOME10")
        self.assertEqual(discount, 110.00)

    def test_tax_calculation(self):
        tax = calculate_tax(1000.0, "CA")
        self.assertEqual(tax, 72.50)

    def test_invalid_coupon(self):
        subtotal = self.cart.get_subtotal()
        discount = calculate_discount(subtotal, "INVALID_CODE")
        self.assertEqual(discount, 0.0)


if __name__ == "__main__":
    unittest.main()
