from decimal import Decimal, ROUND_HALF_UP

TAX_RATES = {
    "australia": Decimal("0.10"),
    "usa": Decimal("0.08"),
    "europe": Decimal("0.20"),
}

BASE_FEE = Decimal("5.00")
RATE_STANDARD = Decimal("1.50")
RATE_HEAVY = Decimal("2.50")
WEIGHT_THRESHOLD = Decimal("20.0")
EXPRESS_SURCHARGE_RATE = Decimal("0.15")

CENTS = Decimal("0.01")


def _quantize(value):
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


def calculate_shipping_fee(weight, shipping_type, item_price):
    weight = Decimal(str(weight))
    item_price = Decimal(str(item_price))

    if weight <= WEIGHT_THRESHOLD:
        fee = BASE_FEE + weight * RATE_STANDARD
    else:
        fee = (BASE_FEE + WEIGHT_THRESHOLD * RATE_STANDARD) + (weight - WEIGHT_THRESHOLD) * RATE_HEAVY

    if shipping_type.lower() == "express":
        fee += item_price * EXPRESS_SURCHARGE_RATE

    return _quantize(fee)


def calculate_tax(item_price, region):
    item_price = Decimal(str(item_price))
    rate = TAX_RATES[region.lower()]
    return _quantize(item_price * rate)


def calculate_total(item_price, shipping_fee, tax_amount):
    return _quantize(Decimal(str(item_price)) + Decimal(str(shipping_fee)) + Decimal(str(tax_amount)))


def estimate(price_str, weight_str, region, shipping_type):
    item_price = _quantize(Decimal(price_str))
    weight = _quantize(Decimal(weight_str))
    shipping_fee = calculate_shipping_fee(weight, shipping_type, item_price)
    tax_amount = calculate_tax(item_price, region)
    total = calculate_total(item_price, shipping_fee, tax_amount)

    return {
        "item_price": item_price,
        "shipping_fee": shipping_fee,
        "tax_amount": tax_amount,
        "total": total,
        "region": region.lower(),
        "shipping_type": shipping_type.lower(),
        "weight": weight,
    }
