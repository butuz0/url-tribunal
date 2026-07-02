"""Flask application dependencies module."""

from flask import g
from sqlalchemy.orm import Session

from url_tribunal.db.session import create_db_session

DB_SESSION = 'db_session'


def get_flask_db_session() -> Session:
    """Get or create a request-scoped database session."""

    if DB_SESSION not in g:
        g.db_session = create_db_session()

    return g.db_session


def close_flask_db_session(exception: BaseException | None = None) -> None:
    """Close the request-scoped database session."""

    session = g.pop(DB_SESSION, None)

    if session is not None:
        if exception is not None:
            session.rollback()

        session.close()
