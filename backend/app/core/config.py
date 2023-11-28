import os
from typing import Union

from pydantic import BaseSettings


class Base(BaseSettings):
    APP_NAME = "AgTern"
    API_V1_STR = ""
    HOST: str = None
    PORT: int = None
    JWT_SECRET_KEY: str = None
    ALGORITHM: str = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = None
    CLIENT_ID: str = None



class Dev(Base):
    class Config:
        env_file = os.path.join("envs", "dev.env")


class Prod(Base):
    class Config:
        env_file = os.path.join("envs", "prod.env")


config = dict(dev=Dev, prod=Prod)

settings: Union[Dev, Prod] = config[os.environ.get("ENV", "dev")]()
