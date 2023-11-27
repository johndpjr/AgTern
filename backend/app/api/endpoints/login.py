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

from backend.app.crud import crud
from backend.app.database import engine
from backend.app.models import User as UserModel

from ..deps import get_db

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Google Client ID
CLIENT_ID = "710734565405-3nkf5plf0m4p460osals94rnksheoh93.apps.googleusercontent.com"

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
            "made_password": True,
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


@router.post("/users/google-login")
async def google_login(token: str, db: Session = Depends(get_db)):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        print("testing:", token)
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            CLIENT_ID,
            clock_skew_in_seconds=1000000,
        )
        print("Success")
        # print("ID_info:", idinfo)
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # print("Getting user info")
        userid = idinfo["sub"]
        name = idinfo["name"]
        # print(userid)
        email = idinfo["email"]
        # print(email)
        user = crud.search_users_by_google_id(db, userid)
        if user is None or len(user) == 0:
            # Register a new user
            new_user = UserModel(
                **{
                    "username": "{}.{}".format(email, userid),
                    "google_id": userid,
                    "made_password": False,
                    "full_name": name,
                    "email": email,
                    "password": "",
                    "disabled": False,
                }
            )
            user_list = [new_user]
            crud.create_users(db, *user_list)
            user = new_user
        else:
            user = user[0]
        print(user.username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        # Invalid token
        print("Invalid token:", token)
        print(e)
        return {"Error!"}
