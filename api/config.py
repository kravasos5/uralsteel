import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class AuthSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / 'api' / 'auth' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'api' / 'auth' / 'public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    # access_token_expire_minutes: int = 3
    refresh_token_expire_minutes: int = 1440
    RESET_KEY: str
    reset_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file="auth/password_reset_key.env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    BASE_DIR: Path = BASE_DIR
    MEDIA_ROOT: str = os.path.join(BASE_DIR, 'uralsteel', 'media')
    MEDIA_URL: str = '/media/'
    TIME_ZONE: str = 'Asia/Yekaterinburg'
    AUTH: AuthSettings = AuthSettings()

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
