import os
from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core import settings
from backend.app.crud import crud
from backend.app.database import engine
from backend.app.models import User as UserModel

from backend.app.api.deps import get_db


load_dotenv()
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Google Client ID
CLIENT_ID = settings.CLIENT_ID

users_db = get_db()

router = APIRouter()


def hash_password(password: str):
    bytes_ = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_ = bcrypt.hashpw(bytes_, salt)
    return hash_


hashing_function = hash_password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


class User(BaseModel):
    username: str
    google_id: str | None = None
    made_password: bool | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db, username: str):
    users = crud.search_users(db, username)
    if len(users) > 0:
        return users[0]
    return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.made_password:
        raise HTTPException(
            status_code=400,
            detail="This account didn't make a password. Please login via Google.",
        )
    encoded_password = password.encode("utf-8")
    if not bcrypt.checkpw(encoded_password, user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user