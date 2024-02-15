import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    BASE_DIR: str = os.getcwd()
    MEDIA_ROOT: str = 'K:/python/python/uralsteel/uralsteel/media'
    MEDIA_URL: str = '/media/'
    TIME_ZONE: str = 'Asia/Yekaterinburg'

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
