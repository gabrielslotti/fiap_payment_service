from functools import lru_cache
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

SQLALCHEMY_DATABASE_URL = str(conf_settings.db_url)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    """
    Gets database session.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
