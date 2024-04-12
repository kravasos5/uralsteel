from datetime import timedelta, datetime

import jwt
import pytz
from passlib.context import CryptContext

from config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTH.private_key_path.read_text(),
    algorithm: str = settings.AUTH.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.AUTH.access_token_expire_minutes,
    expire_minutes_refresh=settings.AUTH.refresh_token_expire_minutes,
    is_refresh: bool = False,
):
    """Кодировать JWT"""
    to_encode = payload.copy()
    now = datetime.now(pytz.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        if is_refresh:
            expire_minutes = expire_minutes_refresh
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded, expire


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTH.public_key_path.read_text(),
    algorithm: str = settings.AUTH.algorithm,
):
    """Раскодировать JWT"""
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded


def validate_password(
    password: str,
    hashed_password: str
) -> bool:
    """Валидация пароля"""
    password_context = CryptContext(
        schemes=['django_pbkdf2_sha256', 'django_bcrypt', 'django_argon2', 'pbkdf2_sha256'],
        deprecated='auto'
    )
    return password_context.verify(password, hashed_password)
