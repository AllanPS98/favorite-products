from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger

from src.configurations import Configurations
configurations = Configurations()

@contextmanager
def get_session():
    engine = create_engine(configurations.DB_STRING_URI)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.exception(f"Database session error: {e}")
        session.rollback()
        raise
    finally:
        session.close()