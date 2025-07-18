import redis
from redis.commands.json.path import Path

from uralsteel.settings import REDIS_HOST, REDIS_PORT


class RedisCacheMixin:
    """
    Миксин, проверяющий есть ли в redis какой-то ключ
    и добавляющий новый
    """
    @staticmethod
    def get_key_redis_json(key_name: str) -> dict | None:
        """
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None. Работает только с json
        """
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            result = redis_client.json().get(key_name)
        if result is not None:
            return result

    @staticmethod
    def set_key_redis_json(key_name: str, data: dict, ttl: int) -> None:
        """Функция, задающая ключ в хранилище. Работает только с json"""
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.json().set(key_name, Path.root_path(), data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)

    @staticmethod
    def get_key_redis(key_name: str) -> str | None:
        """
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None
        """
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            result: bytes = redis_client.get(key_name)
        if result is not None:
            return result.decode()

    @staticmethod
    def set_key_redis(key_name: str, data: str, ttl: int) -> None:
        """Функция, задающая ключ в хранилище"""
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.set(key_name, data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)

    @staticmethod
    def delete_key_redis(key_name: str) -> None:
        """Функция, удаляющая ключ из хранилища"""
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            # удаляю ключ
            redis_client.delete(key_name)

    @staticmethod
    def delete_keys_redis(pattern: str) -> None:
        """Функция, удаляющая ключи из хранилища по паттерну"""
        with redis.Redis() as redis_client:
            # получаю все ключи по паттерну
            all_keys: list = redis_client.keys(pattern)
            for key in all_keys:
                # удаляю ключ
                redis_client.delete(key)
