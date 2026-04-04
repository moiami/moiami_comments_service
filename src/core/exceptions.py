from http import HTTPStatus

from flask import jsonify


class ServiceError(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ValidationError(ServiceError):
    def __init__(self, message):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


def handle_errors(app):
    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({
            "error": "service_error",
            "message": e.message,
        }), e.status_code

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def handle_not_found(e):
        return jsonify({
            "error": "not_found",
            "message": "Resource not found"
        }), HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_internal_error(e):
        return jsonify({
            "error": "internal_error",
            "message": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR