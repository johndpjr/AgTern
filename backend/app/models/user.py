from sqlalchemy import Boolean, Column, Integer, String

from backend.app.database import DatabaseModel


class User(DatabaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String)
    made_password = Column(Boolean)
    username = Column(String)
    password = Column(String)
    full_name = Column(String)
    email = Column(String)
    disabled = Column(String)

    def __str__(self):
        return str(
            {
                column: getattr(self, column)
                for column in User.__table__.columns.keys()
                if hasattr(self, column)
            }
        )
