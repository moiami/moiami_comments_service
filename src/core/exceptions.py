from flask import jsonify


class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ValidationError(ServiceError):
    def __init__(self, message):
        super().__init__(message, 400)


def handle_errors(app):
    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({
            "error": "service_error",
            "message": e.message,
        }), e.status_code

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "error": "not_found",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            "error": "internal_error",
            "message": "Internal server error"
        }), 500