from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.app_env.lower() == "production" and settings.database_url.startswith("sqlite"):
    raise RuntimeError("production requires PostgreSQL")

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine_kwargs = {"pool_pre_ping": True}
if not settings.database_url.startswith("sqlite"):
    engine_kwargs.update(pool_size=settings.db_pool_size, max_overflow=settings.db_max_overflow, pool_timeout=settings.db_pool_timeout_seconds)
engine = create_engine(settings.database_url, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Compatibility helper: schema creation is test/development only; production uses Alembic."""
    if settings.app_env.lower() == "production":
        return
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
