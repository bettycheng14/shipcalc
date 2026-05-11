import pytest
from decimal import Decimal
from app.services.shipping_calculator import (
    calculate_shipping_fee,
    calculate_tax,
    calculate_total,
    estimate,
)


# BVA weight boundaries for shipping fee
def test_fee_at_19point9kg():
    fee = calculate_shipping_fee(Decimal("19.9"), "standard", Decimal("0"))
    # 5 + 19.9 * 1.5 = 5 + 29.85 = 34.85
    assert fee == Decimal("34.85")


def test_fee_at_20point0kg():
    fee = calculate_shipping_fee(Decimal("20.0"), "standard", Decimal("0"))
    # 5 + 20 * 1.5 = 5 + 30 = 35.00
    assert fee == Decimal("35.00")


def test_fee_at_20point1kg_heavy_surcharge():
    fee = calculate_shipping_fee(Decimal("20.1"), "standard", Decimal("0"))
    # (5 + 20*1.5) + (0.1 * 2.5) = 35 + 0.25 = 35.25
    assert fee == Decimal("35.25")


def test_heavy_surcharge_25kg():
    fee = calculate_shipping_fee(Decimal("25.0"), "standard", Decimal("0"))
    # (5 + 20*1.5) + (5 * 2.5) = 35 + 12.5 = 47.50
    assert fee == Decimal("47.50")


# Tax calculations
def test_tax_australia_10_percent():
    tax = calculate_tax(Decimal("100.00"), "australia")
    assert tax == Decimal("10.00")


def test_tax_usa_8_percent():
    tax = calculate_tax(Decimal("100.00"), "usa")
    assert tax == Decimal("8.00")


def test_tax_europe_20_percent():
    tax = calculate_tax(Decimal("100.00"), "europe")
    assert tax == Decimal("20.00")


def test_tax_zero_price():
    tax = calculate_tax(Decimal("0.00"), "australia")
    assert tax == Decimal("0.00")


def test_tax_case_insensitive():
    tax = calculate_tax(Decimal("100.00"), "AUSTRALIA")
    assert tax == Decimal("10.00")


# Express fee: adds 15% of item price on top of standard
def test_express_adds_15_percent_of_price():
    standard_fee = calculate_shipping_fee(Decimal("5.0"), "standard", Decimal("100.00"))
    express_fee = calculate_shipping_fee(Decimal("5.0"), "express", Decimal("100.00"))
    assert express_fee - standard_fee == Decimal("15.00")


def test_express_fee_value():
    fee = calculate_shipping_fee(Decimal("5.0"), "express", Decimal("100.00"))
    # standard: 5 + 5*1.5 = 12.50; express surcharge: 100 * 0.15 = 15.00; total = 27.50
    assert fee == Decimal("27.50")


# Express + heavy combined: 25kg express at $200 price
def test_express_heavy_combined():
    fee = calculate_shipping_fee(Decimal("25.0"), "express", Decimal("200.00"))
    # heavy standard: 35 + 5*2.5 = 47.50; express: 200 * 0.15 = 30.00; total = 77.50
    assert fee == Decimal("77.50")


# Right-BICEP cross-check: total - shipping_fee - tax_amount == item_price
def test_right_bicep_cross_check_standard():
    result = estimate("150.00", "10.0", "australia", "standard")
    total = result["total"]
    shipping = result["shipping_fee"]
    tax = result["tax_amount"]
    price = result["item_price"]
    assert total - shipping - tax == price


def test_right_bicep_cross_check_express():
    result = estimate("250.00", "25.0", "europe", "express")
    total = result["total"]
    shipping = result["shipping_fee"]
    tax = result["tax_amount"]
    price = result["item_price"]
    assert total - shipping - tax == price


# Decision table: all 6 region x shipping_type combos, verifying tax rate
@pytest.mark.parametrize("region,shipping_type,expected_tax_rate", [
    ("australia", "standard", Decimal("0.10")),
    ("australia", "express", Decimal("0.10")),
    ("usa", "standard", Decimal("0.08")),
    ("usa", "express", Decimal("0.08")),
    ("europe", "standard", Decimal("0.20")),
    ("europe", "express", Decimal("0.20")),
])
def test_decision_table_tax_rates(region, shipping_type, expected_tax_rate):
    price = Decimal("100.00")
    result = estimate(str(price), "5.0", region, shipping_type)
    expected_tax = (price * expected_tax_rate).quantize(Decimal("0.01"))
    assert result["tax_amount"] == expected_tax
