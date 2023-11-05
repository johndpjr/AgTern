import json

from sqlalchemy import Column, Integer, String

from backend.app.database import DatabaseModel


class Job(DatabaseModel):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    company_job_id = Column(String, index=True)
    company = Column(String, index=True)
    title = Column(String, index=True)
    type = Column(String, index=True)
    category = Column(String, index=True)
    posting_link = Column(String)
    apply_link = Column(String)
    period = Column(String, index=True)
    year = Column(String, index=True)
    post_date = Column(String)
    location = Column(String, index=True)
    description = Column(String)
    tags = Column(String)

    def __str__(self):
        return json.dumps(
            {
                column: getattr(self, column)
                for column in Job.__table__.columns.keys()
                if hasattr(self, column)
            },
            indent=2,
        )
