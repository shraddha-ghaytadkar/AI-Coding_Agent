"""
Shopping Cart implementation.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CartItem:
    item_id: str
    name: str
    price: float
    quantity: int = 1

    @property
    def total(self) -> float:
        return self.price * self.quantity


class ShoppingCart:
    def __init__(self, currency: str = "USD"):
        self.items: List[CartItem] = []
        self.currency: str = currency
        self.applied_coupon: Optional[str] = None

    def add_item(self, item_id: str, name: str, price: float, quantity: int = 1) -> CartItem:
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        for item in self.items:
            if item.item_id == item_id:
                item.quantity += quantity
                return item

        new_item = CartItem(item_id=item_id, name=name, price=price, quantity=quantity)
        self.items.append(new_item)
        return new_item

    def remove_item(self, item_id: str) -> bool:
        initial_len = len(self.items)
        self.items = [i for i in self.items if i.item_id != item_id]
        return len(self.items) < initial_len

    def get_subtotal(self) -> float:
        return sum(item.total for item in self.items)

    def apply_coupon(self, coupon_code: str) -> bool:
        if not coupon_code or not isinstance(coupon_code, str):
            return False
        self.applied_coupon = coupon_code.strip().upper()
        return True

    def clear(self) -> None:
        self.items.clear()
        self.applied_coupon = None
