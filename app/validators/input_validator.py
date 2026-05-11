from decimal import Decimal, InvalidOperation

VALID_REGIONS = {"australia", "usa", "europe"}
VALID_SHIPPING_TYPES = {"standard", "express"}


def validate_inputs(price_str, weight_str, region, shipping_type):
    if not price_str or not price_str.strip():
        return False, "Price is required."
    if not weight_str or not weight_str.strip():
        return False, "Weight is required."
    if not region or not region.strip():
        return False, "Region is required."
    if not shipping_type or not shipping_type.strip():
        return False, "Shipping type is required."

    try:
        price = Decimal(price_str.strip())
    except InvalidOperation:
        return False, "Price must be a valid decimal number."

    try:
        weight = Decimal(weight_str.strip())
    except InvalidOperation:
        return False, "Weight must be a valid decimal number."

    if price < Decimal("0"):
        return False, "Price cannot be negative."

    if weight <= Decimal("0"):
        return False, "Weight must be greater than zero."

    if region.strip().lower() not in VALID_REGIONS:
        return False, "Unsupported region. Choose australia, usa, or europe."

    if shipping_type.strip().lower() not in VALID_SHIPPING_TYPES:
        return False, "Shipping type must be standard or express."

    return True, None
