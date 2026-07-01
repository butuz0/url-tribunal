"""Global API error handlers."""

from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """Convert HTTP exceptions to JSON format."""

        return jsonify({'error': e.description}), e.code

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError):
        """Format Pydantic validation errors."""

        errors = {str(err['loc'][0]): err['msg'] for err in error.errors()}
        return jsonify({
            'error': 'Validation failed',
            'details': errors,
        }), 400
