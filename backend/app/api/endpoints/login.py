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

from backend.app.api.login_base import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    CLIENT_ID,
    User,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    hashing_function,
    router,
)
from backend.app.core import settings
from backend.app.crud import crud
from backend.app.database import engine
from backend.app.models import User as UserModel

from ..deps import get_db


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
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            CLIENT_ID,
            clock_skew_in_seconds=1000000,
        )
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
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        # Invalid token
        return {"Error": e}
