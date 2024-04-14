import pytest_asyncio

from utils.repositories_manager import RepoCollector


@pytest_asyncio.fixture(scope='package')
async def repo_collector(session):
    """
    Инициализация коллектора репозиториев
    """
    repo_collector = RepoCollector(session)
    yield repo_collector
