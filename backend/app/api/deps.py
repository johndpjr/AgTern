from typing import Generator

from sqlalchemy.orm import Session

from backend.app.database import DatabaseSession


def get_db() -> Generator[Session, None, None]:
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()
