"""Flask application factory."""

from typing import Optional

from flask import Flask

from url_tribunal.api.v1.errors import register_error_handlers
from url_tribunal.api.v1.views.url import url_bp
from url_tribunal.core.config import Settings, get_settings
from url_tribunal.db.session import (
    create_sync_db_engine,
    create_sync_session_factory,
)


def create_app(settings: Optional[Settings] = None) -> Flask:
    """Initialize and configure the Flask application."""

    app = Flask(__name__)

    if settings is None:
        settings = get_settings()

    app.config['SETTINGS'] = settings
    app.config['SECRET_KEY'] = settings.flask.secret_key

    engine = create_sync_db_engine(settings.db)
    session_factory = create_sync_session_factory(engine)

    app.config['DB_SESSION_FACTORY'] = session_factory

    @app.teardown_appcontext
    def shutdown_session(exception=None) -> None:
        pass

    @app.get('/health/')
    def health() -> tuple[dict, int]:
        return {'status': 'ok'}, 200

    register_error_handlers(app)

    app.register_blueprint(url_bp)

    return app
