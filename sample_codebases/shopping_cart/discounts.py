"""
Discount calculation engine.
"""
from typing import Dict

VALID_COUPONS: Dict[str, float] = {
    "WELCOME10": 0.10,   # 10% off
    "SUPER20": 0.20,     # 20% off
    "HALFPRICE": 0.50,   # 50% off
}


def calculate_discount(subtotal: float, coupon_code: str = None) -> float:
    """
    Calculate discount amount based on coupon code.
    Returns the absolute dollar amount of discount.
    """
    if subtotal <= 0 or not coupon_code:
        return 0.0

    normalized_code = coupon_code.strip().upper()
    discount_rate = VALID_COUPONS.get(normalized_code, 0.0)
    return round(subtotal * discount_rate, 2)
