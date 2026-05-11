 from flask import Blueprint, render_template, request, jsonify

  calculator = Blueprint("calculator", __name__)

  @calculator.route("/", methods=["GET"])                                                                                          
  def index():
      return render_template("index.html")                                                                                         
                                                            
  @calculator.route("/calculate", methods=["POST"])
  def calculate():
      return jsonify({
          "item_price": "0.00", "shipping_fee": "0.00",
          "tax_amount": "0.00", "total":        "0.00",                                                                            
          "region": "australia", "shipping_type": "standard", "weight": "1.00",                                                    
      }) 