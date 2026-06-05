"""
Conexión y sesión de SQLAlchemy para PostgreSQL remoto.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError
from app.config import get_settings

settings = get_settings()

def make_engine(db_url: str):
    connect_args = {}
    if db_url.startswith("sqlite:"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args=connect_args,
    )
    return engine

database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = make_engine(database_url)

# Fallback local: si no hay acceso a PostgreSQL, usa SQLite para desarrollo.
if database_url.startswith("postgresql+"):
    try:
        with engine.connect() as conn:
            pass
    except OperationalError:
        print("⚠️ No se pudo conectar a PostgreSQL. Usando SQLite local en ./local.db")
        engine.dispose()
        database_url = "sqlite:///./local.db"
        engine = make_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency injection de sesión de BD para los routers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
