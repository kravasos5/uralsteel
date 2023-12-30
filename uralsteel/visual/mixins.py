from typing import Optional

import redis
from redis.commands.json.path import Path
from django.middleware.csrf import get_token

from uralsteel.settings import REDIS_HOST, REDIS_PORT


class CsrfMixin:
    '''Миксин, добавляющий в контекст csrf_token'''
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        csrf_token = get_token(self.request)
        context['csrf_token'] = csrf_token
        return context

class RedisCacheMixin:
    '''
    Миксин, проверяющий есть ли в redis какой-то ключ
    и добавляющий новый
    '''
    @staticmethod
    def get_key_redis_json(key_name: str) -> Optional[dict]:
        '''
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None. Работает только с json
        '''
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            result = redis_client.json().get(key_name)
        if result is not None:
            return result

    @staticmethod
    def set_key_redis_json(key_name: str, data: dict, ttl: int) -> None:
        '''Функция, задающая ключ в храниилище. Работает только с json'''
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.json().set(key_name, Path.root_path(), data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)

    @staticmethod
    def get_key_redis(key_name: str) -> str:
        '''
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None
        '''
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            result = redis_client.get(key_name)
        if result is not None:
            return result

    @staticmethod
    def set_key_redis(key_name: str, data: str, ttl: int) -> None:
        '''Функция, задающая ключ в храниилище'''
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.set(key_name, data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)