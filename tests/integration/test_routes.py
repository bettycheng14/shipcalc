import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ShipCalc" in response.data


def test_valid_post_returns_correct_tax(client):
    # australia 10% of 100.00 AUD = 10.00
    response = client.post("/calculate", data={
        "price": "100.00",
        "weight": "5.0",
        "region": "australia",
        "shipping_type": "standard",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["tax_amount"] == "10.00"


def test_negative_price_returns_400_with_error(client):
    response = client.post("/calculate", data={
        "price": "-1.00",
        "weight": "5.0",
        "region": "australia",
        "shipping_type": "standard",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "negative" in data["error"].lower()


def test_empty_price_returns_400_with_required_error(client):
    response = client.post("/calculate", data={
        "price": "",
        "weight": "5.0",
        "region": "australia",
        "shipping_type": "standard",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "required" in data["error"].lower()


def test_unsupported_region_returns_400(client):
    response = client.post("/calculate", data={
        "price": "100.00",
        "weight": "5.0",
        "region": "canada",
        "shipping_type": "standard",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Unsupported region" in data["error"]


def test_heavy_shipping_25kg_returns_result(client):
    response = client.post("/calculate", data={
        "price": "100.00",
        "weight": "25.0",
        "region": "australia",
        "shipping_type": "standard",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "shipping_fee" in data
    assert "total" in data


def test_express_shipping_returns_express_in_result(client):
    response = client.post("/calculate", data={
        "price": "100.00",
        "weight": "5.0",
        "region": "australia",
        "shipping_type": "express",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["shipping_type"] == "express"
