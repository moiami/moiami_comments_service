from flask import Flask
from src.core.config import config
from src.core.db import db
from src.core.exceptions import handle_errors
from src.api.comments import bp as comments_bp
from src.api.likes import bp as likes_bp
from flask_smorest import Api


def init_app():
    app = Flask(__name__)

    app.config["DEBUG"] = config.DEBUG
    app.config["RESOURCE_SERVICE_URL"] = config.RESOURCE_SERVICE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    app.config["API_TITLE"] = "moiami_comment_service"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    api = Api(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.register_blueprint(comments_bp)
    api.register_blueprint(likes_bp)

    handle_errors(app)

    return app


if __name__ == "__main__":
    app = init_app()
    app.run(host="0.0.0.0", port=8007, debug=True)
