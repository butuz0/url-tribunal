"""Global API error handlers."""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """Convert HTTP exceptions to JSON format."""

        return jsonify({'error': e.description}), e.code
