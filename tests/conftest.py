import pytest_asyncio


@pytest_asyncio.fixture(scope='session', autouse=True)
def flush_redis_cache():
    """Очистить Redis-кэш"""
    ...
