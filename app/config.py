from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, root_validator
from sqlalchemy.pool import NullPool


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None  

    @root_validator(pre=True) 
    def set_database_url(cls, values):
        db_url = f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        values['DATABASE_URL'] = db_url
        return values

    SECRET_KEY: str
    ALGORIHTM: str
    RANDOM_USER_API_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
