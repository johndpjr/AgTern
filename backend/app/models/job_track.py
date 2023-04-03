from sqlalchemy import Column, ForeignKey, Integer, String

from backend.app.database import DatabaseModel


class JobTrack(DatabaseModel):
    __tablename__ = "job_track"

    id = Column(Integer, primary_key=True, index=True)
    job_status_id = Column(Integer, ForeignKey("job_status.id"))
    user_job_track_id = Column(Integer, ForeignKey("user_job_track.id"))
    timestamp = Column(String, index=True)

    def __str__(self):
        return str(
            {
                column: getattr(self, column)
                for column in JobTrack.__table__.columns.keys()
                if hasattr(self, column)
            }
        )
