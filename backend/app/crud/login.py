from typing import List

from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.app.models import User as UserModel
from backend.app.schemas import User as UserSchema
from backend.app.utils import LOG

def create_users(db: Session, *users: UserModel) -> List[UserSchema]:
    if len(users) > 0:
        db.add_all(users)
        db.commit()
        # Maybe call db.refresh()?
    return convert_users(*users)

def get_all_users(db: Session) -> list[UserSchema]:
    """Gets all users."""
    return convert_users(*db.query(UserModel).all())

def convert_users(*db_users: UserModel) -> List[UserSchema]:
    """Converts UsersModels as stored in the database to a User."""
    users = []
    for db_user in db_users:
        try:
            data = {
                column: getattr(db_user, column)
                for column in UserSchema.__fields__.keys()
                if column in UserModel.__table__.columns.keys()
            }
            users.append(
                UserSchema(
                    **{
                        k: v
                        for k, v in data.items()
                        if v is not None
                        and len(str(v)) != 0  # Don't add Nones or empty strings
                    }
                )
            )
        except ValidationError as errors:
            LOG.error("Unable to create User!")
            LOG.error(f"UserModel: {db_user}")
            LOG.error(errors)
    return users

def search_users(db: Session, username: str, skip: int = 0, limit: int = 1000):
    """Searches for users by username"""
    results = (
        db.query(UserModel)
        .filter(UserModel.username == username)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return convert_users(*results)


def delete_user(db: Session, username: str):
    """Deletes a user with the given username"""
    user = db.query(UserModel).filter(UserModel.username == username).first()
    db.delete(user)
    db.commit()
    return True
