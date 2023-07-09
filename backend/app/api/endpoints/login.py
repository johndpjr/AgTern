from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database import engine
from backend.app.models import User as UserModel

from ..deps import get_db

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
users_db = get_db()

router = APIRouter()


def fake_hash_password(password: str):
    return "fakehashed" + password


hashing_function = fake_hash_password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    users = crud.search_users(db, form_data.username)
    if len(users) == 0:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = users[0]
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


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
    if len(users) > 0:
        raise HTTPException(status_code=400, detail="Username already exists!")
    new_user = UserModel(
        **{
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": hashing_function(password),
            "disabled": False,
        }
    )
    user_list = [new_user]
    crud.create_users(db, *user_list)
    return {"status": "success"}


@router.post("users/delete")
async def delete_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    """Deletes a user. Requires password confirmation"""
    users = crud.search_users(db, username)
    deleted = False
    for user in users:
        if hashing_function(password) == user.password:
            crud.delete_user(db, username)
            deleted = True
        else:
            print(user.password, password)
    return {"deleted": deleted}


# This should be restricted to administrators only - useful for debugging
@router.get("/get_users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(
        "ALTER TABLE %s ADD COLUMN %s %s" % (table_name, column_name, column_type)
    )


@router.post("/update_columns")
def update_columns():
    """Updates the user model"""
    columns = []
    columns.append(Column("full_name", String(100)))
    columns.append(Column("email", String(100)))
    columns.append(Column("disabled", Boolean))
    errors = []
    for col in columns:
        try:
            add_column(engine, "user", col)
        except Exception as e:
            errors.append(str(e))
    return {"errors": errors}


@router.post("/init_user_db")
def init_database(db: Session = Depends(get_db)):
    """Initializes the user model in the database"""
    init_user_list = []
    init_user_list.append(
        UserModel(
            **{
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "password": "fakehashedsecret",
                "disabled": False,
            }
        )
    )
    crud.create_users(db, *init_user_list)
    print("Saving to database succeeded!")
    return {"status": "success"}
