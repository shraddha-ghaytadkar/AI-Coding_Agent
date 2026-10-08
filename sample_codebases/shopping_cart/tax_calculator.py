"""
Sales tax calculation module.
"""

TAX_RATES = {
    "CA": 0.0725,
    "NY": 0.08875,
    "TX": 0.0625,
    "FL": 0.060,
    "DEFAULT": 0.05,
}


def calculate_tax(taxable_amount: float, region: str = "DEFAULT") -> float:
    """Calculate tax for a given amount and region."""
    if taxable_amount <= 0:
        return 0.0

    rate = TAX_RATES.get(region.upper(), TAX_RATES["DEFAULT"])
    return round(taxable_amount * rate, 2)
