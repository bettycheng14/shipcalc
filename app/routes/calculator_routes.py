from flask import Blueprint, render_template, request, jsonify
from app.validators.input_validator import validate_inputs
from app.services.shipping_calculator import estimate

calculator = Blueprint("calculator", __name__)


@calculator.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@calculator.route("/calculate", methods=["POST"])
def calculate():
    price_str = request.form.get("price", "")
    weight_str = request.form.get("weight", "")
    region = request.form.get("region", "")
    shipping_type = request.form.get("shipping_type", "")

    is_valid, error_message = validate_inputs(price_str, weight_str, region, shipping_type)

    if not is_valid:
        return jsonify({"error": error_message}), 400

    result = estimate(price_str, weight_str, region, shipping_type)
    return jsonify({
        "item_price": str(result["item_price"]),
        "shipping_fee": str(result["shipping_fee"]),
        "tax_amount": str(result["tax_amount"]),
        "total": str(result["total"]),
        "region": result["region"],
        "shipping_type": result["shipping_type"],
        "weight": str(result["weight"]),
    })
