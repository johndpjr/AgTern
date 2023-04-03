from sqlalchemy import Column, Integer, String

from backend.app.database import DatabaseModel


class JobStatus(DatabaseModel):
    __tablename__ = "job_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    description = Column(String)

    def __str__(self):
        return str(
            {
                column: getattr(self, column)
                for column in JobStatus.__table__.columns.keys()
                if hasattr(self, column)
            }
        )
