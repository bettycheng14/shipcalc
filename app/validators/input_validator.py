from decimal import Decimal, InvalidOperation

VALID_REGIONS = {"australia", "usa", "europe"}
VALID_SHIPPING_TYPES = {"standard", "express"}


def validate_inputs(price_str, weight_str, region, shipping_type):
    return True, None
