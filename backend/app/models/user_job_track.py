from sqlalchemy import Column, ForeignKey, Integer

from backend.app.database import DatabaseModel


class UserJobTrack(DatabaseModel):
    __tablename__ = "user_job_track"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    def __str__(self):
        return str(
            {
                column: getattr(self, column)
                for column in UserJobTrack.__table__.columns.keys()
                if hasattr(self, column)
            }
        )
