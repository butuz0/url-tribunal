"""Celery app configuration."""

from typing import Any, Optional

from celery import Celery
from celery.signals import worker_init

from url_tribunal.core.config import get_settings, Settings
from url_tribunal.db.session import init_database


def create_celery_app(settings: Optional[Settings] = None) -> Celery:
    """Create and configure a Celery application instance."""

    app = Celery('url-tribunal')

    if settings is None:
        settings = get_settings()

    app.conf.update(settings.celery.model_dump())
    app.autodiscover_tasks(['url_tribunal.tasks'])

    return app


@worker_init.connect
def configure_worker_db_connection(**kwargs: Any) -> None:
    """Initialize database connection."""

    settings = get_settings()
    init_database(settings.db)


app = create_celery_app(get_settings())
