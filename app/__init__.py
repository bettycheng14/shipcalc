from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.calculator_routes import calculator
    app.register_blueprint(calculator)

    return app
