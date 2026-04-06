from flask import Flask
from src.core.config import config
from src.core.db import db
from src.core.exceptions import handle_errors
from src.api.comments import bp as comments_bp
from src.api.likes import bp as likes_bp
from src.models.comment import Comment
from src.models.like import Like


def init_app():
    app = Flask(__name__)

    app.config["DEBUG"] = config.DEBUG
    app.config["RESOURCE_SERVICE_URL"] = config.RESOURCE_SERVICE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(comments_bp)
    app.register_blueprint(likes_bp)

    handle_errors(app)

    return app


if __name__ == "__main__":
    app = init_app()
    app.run(host="0.0.0.0", port=8007, debug=app.config["DEBUG"])
