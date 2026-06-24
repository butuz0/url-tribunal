"""API layer dependency provider."""

from contextlib import contextmanager
from typing import Generator

from flask import current_app
from sqlalchemy.orm import Session


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Yield a database session from the app session factory."""

    session_factory = current_app.config['DB_SESSION_FACTORY']

    session: Session = session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
