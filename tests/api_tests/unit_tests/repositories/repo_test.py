from abc import ABC, abstractmethod
from typing import Type
from contextlib import nullcontext as does_not_raise

import pytest
import pytest_asyncio
from pydantic import BaseModel

from repositories.ladles import LadlesRepo
from schemas.ladles import LadlesCreateUpdateDTO, LadlesReadDTO
from utils.repositories_base import SqlAlchemyRepo


pytestmark = pytest.mark.asyncio(scope='package')


class AbstractRepoMethodsCheck(ABC):
    """Абстрактный класс тестирования репозитория"""

    @abstractmethod
    def test_create_one(self, *args, **kwargs):
        """Проверка метода create_one"""
        raise NotImplementedError

    @abstractmethod
    def test_retrieve_one(self, *args, **kwargs):
        """Проверка метода retrieve_one"""
        raise NotImplementedError

    @abstractmethod
    def test_retrieve_all(self, *args, **kwargs):
        """Проверка метода retrieve_all"""
        raise NotImplementedError

    @abstractmethod
    def test_update_one(self, *args, **kwargs):
        """Проверка метода update_one"""
        raise NotImplementedError

    @abstractmethod
    def test_delete_one(self, *args, **kwargs):
        """Проверка метода delete_one"""
        raise NotImplementedError

    @abstractmethod
    def test_delete_by_ids(self, *args, **kwargs):
        """Проверка метода delete_by_ids"""
        raise NotImplementedError


class BaseRepoMethodsCheck(AbstractRepoMethodsCheck):
    """
    Тестирование базовых методов репозитория.
    Это методы: create_one, delete_one, delete_by_ids,
    update_one, retrieve_one, retrieve_all
    """
    repository: SqlAlchemyRepo | None = None

    async def test_create_one(
            self,
            repo: SqlAlchemyRepo,
            data: BaseModel,
            answer: BaseModel
    ):
        """Проверка метода create_one"""
        repo_answer = await repo.create_one(data)
        assert repo_answer == answer

    async def test_retrieve_one(
            self,
            repo: SqlAlchemyRepo,
            read_schema: Type[BaseModel],
            answer: BaseModel,
            **filters
    ):
        """Проверка метода retrieve_one"""

        repo_answer = await repo.retrieve_one(read_schema, **filters)
        assert repo_answer == answer

    async def test_retrieve_all(
            self,
            repo: SqlAlchemyRepo,
            answer: list[BaseModel],
            offset: int = 0,
            limit: int = 100,
            **filters
    ):
        """Проверка метода retrieve_all"""
        repo_answer = await repo.retrieve_all(offset, limit, **filters)
        assert repo_answer == answer

    async def test_update_one(
            self,
            repo: SqlAlchemyRepo,
            data_schema: BaseModel,
            answer: BaseModel,
            **filters
    ):
        """Проверка метода update_one"""
        repo_answer = await repo.update_one(data_schema, **filters)
        assert repo_answer == answer

    async def test_delete_one(
            self,
            repo: SqlAlchemyRepo,
            answer,
            *args,
            **filters
    ):
        """Проверка метода delete_one"""
        repo_answer = await repo.delete_one(**filters)
        assert repo_answer == answer

    async def test_delete_by_ids(
            self,
            repo: SqlAlchemyRepo,
            ids: list[int],
            answer: list[int]
    ):
        """Проверка метода delete_by_ids"""
        repo_answer = await repo.delete_by_ids(ids)
        assert repo_answer == answer


@pytest_asyncio.fixture(scope='package')
async def repo(session):
    """
    Инициализация репозитория
    """
    repo: SqlAlchemyRepo = LadlesRepo(session)
    yield repo


class TestLadlesRepo(BaseRepoMethodsCheck):
    """Тестирование репозиториев происшествий"""
    # repository = LadlesRepo

    @pytest.mark.parametrize(
        'data_schema, answer, expectation',
        [
            (
                    LadlesCreateUpdateDTO(title="test_ladle_1", is_active=True, is_broken=False),
                    LadlesReadDTO(title="test_ladle_1", is_active=True, is_broken=False, id=11),
                    does_not_raise()
            ),
            (
                    LadlesCreateUpdateDTO(title="test_ladle_2", is_active=False, is_broken=True),
                    LadlesReadDTO(title="test_ladle_2", is_active=False, is_broken=True, id=12),
                    does_not_raise()
            ),
            (
                    LadlesCreateUpdateDTO(title="test_ladle_3", is_active=True, is_broken=False),
                    LadlesReadDTO(title="test_ladle_3", is_active=True, is_broken=True, id=13),
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_create_one(self, data_schema, answer, expectation, repo):
        """Тестирование метода create_one"""
        with expectation:
            await super().test_create_one(repo, data_schema, answer)

    @pytest.mark.parametrize(
        'obj_id, answer, read_schema, expectation',
        [
            (
                    11,
                    LadlesReadDTO(title="test_ladle_1", is_active=True, is_broken=False, id=11),
                    LadlesReadDTO,
                    does_not_raise()

            ),
            (
                    12,
                    LadlesReadDTO(title="test_ladle_2", is_active=False, is_broken=True, id=12),
                    LadlesReadDTO,
                    does_not_raise()
            ),
            (
                    13,
                    LadlesReadDTO(title="test_ladle_3", is_active=True, is_broken=True, id=13),
                    LadlesReadDTO,
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_retrieve_one(
            self, obj_id: int, answer, read_schema, expectation, repo
    ):
        """Тестирование метода retrieve_one"""
        with expectation:
            await super().test_retrieve_one(repo, read_schema, answer, id=obj_id)

    @pytest.mark.parametrize(
        'answer, expectation, offset, limit',
        [
            (
                    [
                        LadlesReadDTO(title="test_ladle_1", is_active=True, is_broken=False, id=11),
                        LadlesReadDTO(title="test_ladle_2", is_active=False, is_broken=True, id=12),
                        LadlesReadDTO(title="test_ladle_3", is_active=True, is_broken=False, id=13),
                    ],
                    does_not_raise(),
                    10,
                    3
            ),
            (
                    [
                        LadlesReadDTO(title="test_ladle_1", is_active=True, is_broken=False, id=11),
                    ],
                    does_not_raise(),
                    10,
                    1
            ),
            (
                    [
                        LadlesReadDTO(title="test_ladle_1123", is_active=True, is_broken=False, id=11),
                    ],
                    pytest.raises(AssertionError),
                    10,
                    1
            ),
        ]
    )
    async def test_retrieve_all(
            self,
            answer: list[BaseModel],
            expectation,
            offset: int,
            limit: int,
            repo
    ):
        """Проверка метода retrieve_all"""
        with expectation:
            await super().test_retrieve_all(repo, answer, offset, limit)

    @pytest.mark.parametrize(
        'data_schema, answer, updated_obj_id, expectation',
        [
            (
                    LadlesCreateUpdateDTO(title="test_ladle_123", is_active=True, is_broken=False),
                    LadlesReadDTO(title="test_ladle_123", is_active=True, is_broken=False, id=11),
                    11,
                    does_not_raise()
            ),
            (
                    LadlesCreateUpdateDTO(title="test_ladle_2", is_active=True, is_broken=False),
                    LadlesReadDTO(title="test_ladle_2", is_active=True, is_broken=False, id=12),
                    12,
                    does_not_raise()
            ),
            (
                    LadlesCreateUpdateDTO(title="test_ladle_31", is_active=True, is_broken=True),
                    LadlesReadDTO(title="test_ladle_32", is_active=True, is_broken=True, id=13),
                    13,
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_update_one(
            self,
            data_schema: BaseModel,
            answer: BaseModel,
            expectation,
            updated_obj_id: int,
            repo
    ):
        """Проверка метода update_one"""
        with expectation:
            await super().test_update_one(repo, data_schema, answer, id=updated_obj_id)

    @pytest.mark.parametrize(
        'deleted_obj_id, answer, expectation',
        [
            (
                    11,
                    11,
                    does_not_raise()
            ),
            (
                    12321312,
                    13,
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_delete_one(
            self,
            answer,
            expectation,
            deleted_obj_id: int,
            repo
    ):
        """Проверка метода delete_one"""
        with expectation:
            await super().test_delete_one(repo, answer, id=deleted_obj_id)

    @pytest.mark.parametrize(
        'ids, answer, expectation',
        [
            (
                    [12, 13],
                    [12, 13],
                    does_not_raise()
            ),
            (
                    [12321312, 12321312],
                    [12, 13],
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_delete_by_ids(
            self,
            ids: list[int],
            answer,
            expectation,
            repo
    ):
        """Проверка метода delete_by_ids"""
        with expectation:
            await super().test_delete_by_ids(repo, ids, answer)
