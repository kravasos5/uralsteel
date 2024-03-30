from abc import ABC, abstractmethod
from typing import Type
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import BaseModel

from repositories.accidents import LadlesAccidentRepo
from schemas.ladles import LadlesCreateUpdateDTO, LadlesReadDTO
from utils.repositories_base import SqlAlchemyRepo


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
    repo: SqlAlchemyRepo | None = None

    def test_create_one(
            self,
            data: BaseModel,
            answer: BaseModel
    ):
        """Проверка метода create_one"""
        repo_answer = self.repo.create_one(data)
        print(repo_answer)
        assert repo_answer == answer

    def test_retrieve_one(
            self,
            read_schema: Type[BaseModel],
            answer: BaseModel,
            **filters
    ):
        """Проверка метода retrieve_one"""
        repo_answer = self.repo.retrieve_one(read_schema, **filters)
        print(repo_answer)
        assert repo_answer == answer

    def test_retrieve_all(
            self,
            answer: list[BaseModel],
            offset: int = 0,
            limit: int = 100,
            **filters
    ):
        """Проверка метода retrieve_all"""
        repo_answer = self.repo.retrieve_all(offset, limit, **filters)
        print(repo_answer)
        assert repo_answer == answer

    def test_update_one(
            self,
            data_schema: BaseModel,
            answer: BaseModel,
            **filters
    ):
        """Проверка метода update_one"""
        repo_answer = self.repo.update_one(data_schema, **filters)
        print(repo_answer)
        assert repo_answer == answer

    def test_delete_one(
            self,
            answer,
            *args,
            **filters
    ):
        """Проверка метода delete_one"""
        repo_answer = self.repo.delete_one(**filters)
        print(repo_answer)
        assert repo_answer == answer

    def test_delete_by_ids(
            self,
            ids: list[int],
            answer: list[int]
    ):
        """Проверка метода delete_by_ids"""
        repo_answer = self.repo.delete_one(ids)
        print(repo_answer)
        assert repo_answer == answer


class TestLadleAccidentRepo(BaseRepoMethodsCheck):
    """Тестирование репозиториев происшествий"""
    repo = LadlesAccidentRepo

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
    def test_create_one(self, data_schema, answer, expectation):
        """Тестирование метода create_one"""
        with expectation:
            super().test_create_one(data_schema, answer)

    @pytest.mark.parametrize(
        'obj_id, answer, expectation',
        [
            (
                    11,
                    LadlesReadDTO(title="test_ladle_1", is_active=True, is_broken=False, id=11),
                    does_not_raise()

            ),
            (
                    12,
                    LadlesReadDTO(title="test_ladle_2", is_active=False, is_broken=True, id=12),
                    does_not_raise()
            ),
            (
                    13,
                    LadlesReadDTO(title="test_ladle_3", is_active=True, is_broken=True, id=13),
                    pytest.raises(AssertionError)
            ),
        ]
    )
    def test_retrieve_one(
            self, data_schema, answer, expectation, obj_id: int
    ):
        """Тестирование метода retrieve_one"""
        with expectation:
            super().test_retrieve_one(data_schema, answer, id=obj_id)

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
    def test_retrieve_all(
            self,
            answer: list[BaseModel],
            expectation,
            offset: int = 0,
            limit: int = 100
    ):
        """Проверка метода retrieve_all"""
        with expectation:
            super().test_retrieve_one(answer, offset, limit)

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
    def test_update_one(
            self,
            data_schema: BaseModel,
            answer: BaseModel,
            expectation,
            updated_obj_id: int
    ):
        """Проверка метода update_one"""
        with expectation:
            super().test_update_one(data_schema, answer)

    @pytest.mark.parametrize(
        'deleted_obj_id, answer, expectation',
        [
            (
                    11,
                    11,
                    does_not_raise()
            ),
            (
                    123213124354234,
                    13,
                    pytest.raises(AssertionError)
            ),
        ]
    )
    def test_delete_one(
            self,
            answer,
            expectation,
            deleted_obj_id: int
    ):
        """Проверка метода delete_one"""
        with expectation:
            super().test_delete_one(answer, id=deleted_obj_id)

    @pytest.mark.parametrize(
        'ids, answer, expectation',
        [
            (
                    [12, 13],
                    [12, 13],
                    does_not_raise()
            ),
            (
                    [123213124354234, 123213124354235],
                    [12, 13],
                    pytest.raises(AssertionError)
            ),
        ]
    )
    def test_delete_by_ids(
            self,
            ids: list[int],
            answer,
            expectation
    ):
        """Проверка метода delete_by_ids"""
        with expectation:
            super().test_delete_by_ids(ids, answer)
