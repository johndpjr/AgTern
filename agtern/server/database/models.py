
"""This file contains SQLAlchemy and/or Pydantic models that are used ONLY on the server (ex: stored in a database)"""

from sqlalchemy import Column, Integer, String

from .database import DatabaseModel


class DatabaseInternship(DatabaseModel):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    title = Column(String, index=True)
    year = Column(String, index=True)
    period = Column(String, index=True)
    link = Column(String)
    location = Column(String, index=True)
    description = Column(String)
