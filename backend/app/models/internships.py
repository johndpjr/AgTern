from sqlalchemy import Column, Integer, String

from backend.app.database import DatabaseModel


class Internship(DatabaseModel):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    company = Column(String, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    link = Column(String)
    apply_link = Column(String)
    period = Column(String, index=True)
    year = Column(String, index=True)
    post_date = Column(String)  # TODO: Store this as a date (date strings are all different formats right now)
    location = Column(String, index=True)
    description = Column(String)
    # TODO: Add tags to the model, see https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY
    # (we would have to use the PostgreSQL backend)
