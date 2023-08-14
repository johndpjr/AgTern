import os
from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database import engine
from backend.app.models import User as UserModel

from ..deps import get_db

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_db = get_db()

router = APIRouter()


def hash_password(password: str):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


hashing_function = hash_password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


class User(BaseModel):
    username: str
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
    encoded_password = password.encode("utf-8")
    if not bcrypt.checkpw(encoded_password, user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.post("/users/register")
async def register_user(
    username: str,
    full_name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    """Registers a user"""
    users = crud.search_users(db, username)
    hashed_password = hashing_function(password)
    if len(users) > 0:
        raise HTTPException(status_code=400, detail="Username already exists!")
    new_user = UserModel(
        **{
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": hashed_password.decode("utf-8"),
            "disabled": False,
        }
    )
    user_list = [new_user]
    crud.create_users(db, *user_list)
    return {"status": "success"}


@router.post("/users/delete")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    """Deletes a user. Requires password confirmation"""
    if authenticate_user(username, password, db):
        crud.delete_user(db, username)
        return {"deleted": True}
    else:
        return {"deleted": False}


# This should be restricted to administrators only - useful for debugging
@router.get("/get_users")
async def get_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return crud.get_all_users(db)
