from flask import Flask
from flasgger import Swagger

from controllers.welcome import welcome_bp
from controllers.calculator import calculator_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(welcome_bp)
    app.register_blueprint(calculator_bp, url_prefix="/calculator")
    Swagger(
        app,
        template={
            "info": {
                "title": "Web Python API",
                "description": "Приветственная страница и калькулятор (сумма)",
                "version": "1.0.0",
            }
        },
    )
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
