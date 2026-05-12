import pytest
from app.validators.input_validator import validate_inputs


# ECT valid classes
def test_valid_australia_standard():
    ok, err = validate_inputs("100.00", "5.0", "australia", "standard")
    assert ok is True
    assert err is None


def test_valid_usa_express():
    ok, err = validate_inputs("250.99", "10.5", "usa", "express")
    assert ok is True
    assert err is None


def test_valid_europe_standard():
    ok, err = validate_inputs("0.00", "0.01", "europe", "standard")
    assert ok is True
    assert err is None


# ECT invalid region
def test_invalid_region_canada():
    ok, err = validate_inputs("100.00", "5.0", "canada", "standard")
    assert ok is False
    assert "Unsupported region" in err


# ECT empty fields
def test_empty_price():
    ok, err = validate_inputs("", "5.0", "australia", "standard")
    assert ok is False
    assert err is not None


def test_empty_weight():
    ok, err = validate_inputs("100.00", "", "australia", "standard")
    assert ok is False
    assert err is not None


def test_empty_region():
    ok, err = validate_inputs("100.00", "5.0", "", "standard")
    assert ok is False
    assert err is not None


# ECT negative values
def test_negative_price():
    ok, err = validate_inputs("-1.00", "5.0", "australia", "standard")
    assert ok is False
    assert err is not None


def test_negative_weight():
    ok, err = validate_inputs("100.00", "-1.0", "australia", "standard")
    assert ok is False
    assert err is not None


# BVA weight boundaries
def test_weight_zero_invalid():
    ok, err = validate_inputs("100.00", "0", "australia", "standard")
    assert ok is False


def test_weight_point01_valid():
    ok, err = validate_inputs("100.00", "0.01", "australia", "standard")
    assert ok is True


def test_weight_19point9_valid():
    ok, err = validate_inputs("100.00", "19.9", "australia", "standard")
    assert ok is True


def test_weight_20point0_valid():
    ok, err = validate_inputs("100.00", "20.0", "australia", "standard")
    assert ok is True


def test_weight_20point1_valid():
    ok, err = validate_inputs("100.00", "20.1", "australia", "standard")
    assert ok is True


# BVA price boundaries
def test_price_zero_valid():
    ok, err = validate_inputs("0.00", "5.0", "australia", "standard")
    assert ok is True


def test_price_point01_valid():
    ok, err = validate_inputs("0.01", "5.0", "australia", "standard")
    assert ok is True


def test_price_large_valid():
    ok, err = validate_inputs("999999.99", "5.0", "australia", "standard")
    assert ok is True


def test_price_negative_invalid():
    ok, err = validate_inputs("-0.01", "5.0", "australia", "standard")
    assert ok is False


# Invalid decimals
def test_price_non_numeric():
    ok, err = validate_inputs("abc", "5.0", "australia", "standard")
    assert ok is False
    assert err is not None


def test_weight_non_numeric():
    ok, err = validate_inputs("100.00", "abc", "australia", "standard")
    assert ok is False
    assert err is not None


# Invalid shipping type
def test_invalid_shipping_type():
    ok, err = validate_inputs("100.00", "5.0", "australia", "overnight")
    assert ok is False
    assert err is not None

def test_empty_shipping_type():
    ok, err = validate_inputs("100.00", "5.0", "australia", "")
    assert ok is False
    assert "required" in err.lower()