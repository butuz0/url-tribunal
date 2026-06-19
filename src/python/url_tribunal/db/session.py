"""SQLAlchemy database setup."""

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from url_tribunal.core.config import DBSettings


def create_sync_db_engine(settings: DBSettings) -> Engine:
    """Create a synchronous SQLAlchemy engine configured for MySQL."""

    database_url = URL.create(
        drivername='mysql+pymysql',
        username=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.name,
    )

    timeout_seconds = settings.statement_timeout_ms / 1000
    init_command = f'SET max_execution_time = {int(settings.statement_timeout_ms)}'

    return create_engine(
        database_url,
        connect_args={
            'init_command': init_command,
            'connect_timeout': int(timeout_seconds),
        },
        pool_pre_ping=True,
    )


def create_sync_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a session factory for the provided engine."""

    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
        autoflush=False,
    )
