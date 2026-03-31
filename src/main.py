from flask import Flask
from src.core.config import config
from src.core.exceptions import handle_errors
from src.api.comments import bp as comments_bp


def init_app():
    app = Flask(__name__)

    app.config["DEBUG"] = config.DEBUG
    app.config["RESOURCE_SERVICE_URL"] = config.RESOURCE_SERVICE_URL

    #init_db(app)

    app.register_blueprint(comments_bp)

    handle_errors(app)

    return app


app = init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8007, debug=app.config["DEBUG"])