import pytest


@pytest.fixture(scope='session', autouse=True)
def flush_redis_cache():
    """Очистить Redis-кэш"""
    ...
