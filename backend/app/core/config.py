from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ""
    PORT: int = 8000


settings = Settings()
