from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/sql_app.db"
# NOTE: to move database engines, we simply need
#   to change our URL (SQLAlchemy handles it all!)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DatabaseModel = declarative_base(name="DatabaseModel")


def get_db() -> Generator[Session, None, None]:
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()
