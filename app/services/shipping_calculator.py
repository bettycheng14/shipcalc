from decimal import Decimal, ROUND_HALF_UP

def calculate_shipping_fee(weight, shipping_type, item_price):
    return Decimal("0.00")


def calculate_tax(item_price, region):
    item_price = Decimal(str(item_price))
    rate = TAX_RATES[region.lower()]
    return Decimal("0.00")


def calculate_total(item_price, shipping_fee, tax_amount):
    return Decimal("0.00")


def estimate(price_str, weight_str, region, shipping_type):
    return {
        "item_price":   Decimal(price_str),                                                                                      
        "shipping_fee": Decimal("0.00"),
        "tax_amount":   Decimal("0.00"),                                                                                         
        "total":        Decimal(price_str),               
        "region":       region.lower(),                                                                                          
        "shipping_type":shipping_type.lower(),
        "weight":       Decimal(weight_str),                                                                                     
    }
