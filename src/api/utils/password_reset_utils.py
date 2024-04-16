import datetime

import pytz
from cryptography.fernet import Fernet
import json

from config import settings


cipher_suite = Fernet(settings.AUTH.RESET_KEY)


def generate_token(
    payload: dict,
    expire_minutes: int = settings.AUTH.reset_token_expire_minutes,
    expire_delta: datetime.timedelta | None = None,
) -> str:
    """Сгенерировать токен для сброса пароля"""
    encoded_data = payload.copy()
    now = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)
    expire = int(expire.timestamp())
    encoded_data['exp'] = expire
    json_payload = json.dumps(encoded_data)
    token = cipher_suite.encrypt(json_payload.encode('UTF-8')).decode('UTF-8')
    return token


def decode_token(token: str) -> dict:
    """Декодировать токен"""
    token_text = cipher_suite.decrypt(bytes(token, 'UTF-8')).decode()
    payload = json.loads(token_text)
    return payload
