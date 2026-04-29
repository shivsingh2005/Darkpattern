"""
Database configuration and initialization.
"""

import logging
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from backend.app.core.config import settings


logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.database.url,
    echo=settings.database.echo,
    poolclass=QueuePool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    connect_args={
        "check_same_thread": False
    } if "sqlite" in settings.database.url else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Enable query logging in debug mode
if settings.debug:
    @event.listens_for(Engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        logger.debug(f"Query: {statement}")


def init_db() -> None:
    """Initialize database tables."""
    from backend.app.models.base import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
