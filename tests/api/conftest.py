import pytest

from src.api.config import settings
from src.api.database import Base, engine


@pytest.fixture  # (scope='package', autouse=True)
def setup_db():
    """Инициализация БД"""
    assert settings.MODE == 'TEST'
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# @pytest.mark.usefixtures('setup_db')
@pytest.fixture(scope='package', autouse=True)
def add_db_info(setup_db):
    """Добавить данные в БД"""
    ...


@pytest.fixture
def get_auth_user():
    """Получить авторизованного пользователя, токены"""
    ...
