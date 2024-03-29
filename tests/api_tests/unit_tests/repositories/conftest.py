import pytest

from sqlalchemy.orm import Session

from src.api.database import engine


@pytest.fixture(scope='package', autouse=True)
def session_factory():
    """Инициализация сессии"""
    with Session(engine) as session:
        yield
        session.commit()
