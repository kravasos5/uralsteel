import datetime
from abc import ABC, abstractmethod
from typing import Type
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import BaseModel

from schemas.accidents import AccidentsCreateUpdateDTO, AccidentReadShortDTO
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
    repository: str | None = None

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


class TestLadlesRepo(BaseRepoMethodsCheck):
    """Тестирование репозиториев происшествий"""
    repository = 'ladles_repo'

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
    async def test_create_one(self, data_schema, answer, expectation, repo_collector):
        """Тестирование метода create_one"""
        with expectation:
            await super().test_create_one(repo_collector.repositories[self.repository], data_schema, answer)

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
            self, obj_id: int, answer, read_schema, expectation, repo_collector
    ):
        """Тестирование метода retrieve_one"""
        with expectation:
            await super().test_retrieve_one(repo_collector.repositories[self.repository], read_schema, answer,
                                            id=obj_id)

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
            repo_collector
    ):
        """Проверка метода retrieve_all"""
        with expectation:
            await super().test_retrieve_all(repo_collector.repositories[self.repository], answer, offset, limit)

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
            repo_collector
    ):
        """Проверка метода update_one"""
        with expectation:
            await super().test_update_one(repo_collector.repositories[self.repository], data_schema, answer,
                                          id=updated_obj_id)

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
            repo_collector
    ):
        """Проверка метода delete_one"""
        with expectation:
            await super().test_delete_one(repo_collector.repositories[self.repository], answer, id=deleted_obj_id)

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
            repo_collector
    ):
        """Проверка метода delete_by_ids"""
        with expectation:
            await super().test_delete_by_ids(repo_collector.repositories[self.repository], ids, answer)


class TestAccidentRepos(BaseRepoMethodsCheck):
    """
    Микин для тестирования репозиториев
    происшествий
    """
    # async def test_retrieve_all(
    #         self,
    #         repo: SqlAlchemyRepo,
    #         answer: list[BaseModel],
    #         offset: int = 0,
    #         limit: int = 100,
    #         **filters
    # ):
    #     """Проверка метода retrieve_all"""
    #     repo_answer = await repo.retrieve_all(offset, limit, **filters)
    #     assert repo_answer == answer

    @pytest.mark.parametrize(
        'creation_data, answer, repo_name, expectation',
        [
            (
                    AccidentsCreateUpdateDTO(author_id=1, report='test_report_1', object_id=10),
                    AccidentReadShortDTO(id=1, author_id=1, report='test_report_1', object_id=10, created_at=datetime.datetime.utcnow()),
                    'ladles_accident_repo',
                    does_not_raise()
            ),
            (
                    AccidentsCreateUpdateDTO(author_id=1, report='test_report_2', object_id=9),
                    AccidentReadShortDTO(id=2, author_id=1, report='test_report_2', object_id=9,
                                         created_at=datetime.datetime.utcnow()),
                    'ladles_accident_repo',
                    does_not_raise()
            ),
            (
                    AccidentsCreateUpdateDTO(author_id=1, report='test_report_3_error', object_id=10),
                    AccidentReadShortDTO(id=3, author_id=1, report='test_report_3', object_id=10,
                                         created_at=datetime.datetime.utcnow()),
                    'ladles_accident_repo',
                    pytest.raises(AssertionError)
            ),
        ]
    )
    async def test_create_one(
            self,
            creation_data: BaseModel,
            answer: BaseModel,
            repo_name: str,
            expectation,
            repo_collector
    ):
        """Проверка метода create_one ladles_accident"""
        with expectation:
            repo_answer = await repo_collector.repositories[repo_name].create_one(creation_data)
            answer.created_at = repo_answer.created_at
            assert repo_answer == answer

    # async def test_retrieve_one(
    #         self,
    #         repo: SqlAlchemyRepo,
    #         read_schema: Type[BaseModel],
    #         answer: BaseModel,
    #         **filters
    # ):
    #     """Проверка метода retrieve_one"""
    #
    #     repo_answer = await repo.retrieve_one(read_schema, **filters)
    #     assert repo_answer == answer
    #
    # async def test_update_one(
    #         self,
    #         repo: SqlAlchemyRepo,
    #         data_schema: BaseModel,
    #         answer: BaseModel,
    #         **filters
    # ):
    #     """Проверка метода update_one"""
    #     repo_answer = await repo.update_one(data_schema, **filters)
    #     assert repo_answer == answer
    #
    # async def test_delete_one(
    #         self,
    #         repo: SqlAlchemyRepo,
    #         answer,
    #         *args,
    #         **filters
    # ):
    #     """Проверка метода delete_one"""
    #     repo_answer = await repo.delete_one(**filters)
    #     assert repo_answer == answer
    #
    # async def test_delete_by_ids(
    #         self,
    #         repo: SqlAlchemyRepo,
    #         ids: list[int],
    #         answer: list[int]
    # ):
    #     """Проверка метода delete_by_ids"""
    #     repo_answer = await repo.delete_by_ids(ids)
    #     assert repo_answer == answer