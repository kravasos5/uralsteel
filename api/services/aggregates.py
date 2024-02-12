from abc import ABC, abstractmethod

from schemas.aggregates import AggregatesBaseDTO
from utils.unitofwork import AbstractUnitOfWork


class AbstractAggregateService(ABC):
    """Абстрактный репозиторий агрегатов"""
    aggregate_type = None

    @abstractmethod
    def get_aggregate_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_all_aggregates(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update_aggregate(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_aggregate(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_aggregate(self, *args, **kwargs):
        raise NotImplementedError


class AggregatesAllService(AbstractAggregateService):
    """Сервис взаимодействия с Aggregates базовый"""
    aggregate_type = 'aggregates_all'

    def get_aggregate_by_id(self, uow: AbstractUnitOfWork, ag_id: int):
        """Получение агрегата по id"""
        with uow:
            result = uow.aggregates[self.aggregate_type].retrieve_one(id=ag_id)
            return result

    def get_all_aggregates(
        self,
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 100,
        **filters,
    ):
        """Получение агрегатов"""
        with uow:
            result = uow.aggregates[self.aggregate_type].retrieve_all(offset=offset, limit=limit, **filters)
            return result

    def update_aggregate(self, uow: AbstractUnitOfWork, data_schema: AggregatesBaseDTO, ag_id: int):
        """Обновление агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].update_one(data_schem=data_schema, id=ag_id)
            uow.commit()
            return result

    def delete_aggregate(self, uow: AbstractUnitOfWork, ag_id: int):
        """Обновление агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].delete_one(id=ag_id)
            uow.commit()
            return result

    def create_aggregate(self, uow: AbstractUnitOfWork, data_schema: AggregatesBaseDTO):
        """Создание нового агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].create_one(data_schema)
            uow.commit()
            return result


class AggregatesUtilityService(AggregatesAllService):
    aggregate_type = ''

    def get_aggregate_by_id(self, uow: AbstractUnitOfWork, ag_id: int):
        """Получение агрегата по id"""
        with uow:
            result = uow.aggregates[self.aggregate_type].retrieve_one(id=ag_id)
            ...
            return result

    def get_all_aggregates(
        self,
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 100,
        **filters,
    ):
        """Получение агрегатов"""
        with uow:
            result = uow.aggregates[self.aggregate_type].retrieve_all(offset=offset, limit=limit, **filters)
            ...
            return result

    def update_aggregate(self, uow: AbstractUnitOfWork, data_schema: AggregatesBaseDTO, ag_id: int):
        """Обновление агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].update_one(data_schem=data_schema, id=ag_id)
            uow.commit()
            ...
            return result

    def delete_aggregate(self, uow: AbstractUnitOfWork, ag_id: int):
        """Обновление агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].delete_one(id=ag_id)
            uow.commit()
            ...
            return result

    def create_aggregate(self, uow: AbstractUnitOfWork, data_schema: AggregatesBaseDTO):
        """Создание нового агрегата"""
        with uow:
            result = uow.aggregates[self.aggregate_type].create_one(data_schema)
            uow.commit()
            ...
            return result


class AggregatesGMPService(AggregatesUtilityService):
    aggregate_type = 'aggregates_gmp_repo'


class AggregatesUKPService(AggregatesUtilityService):
    aggregate_type = 'aggregates_ukp_repo'


class AggregatesUVSService(AggregatesUtilityService):
    aggregate_type = 'aggregates_uvs_repo'


class AggregatesMNLZService(AggregatesUtilityService):
    aggregate_type = 'aggregates_mnlz_repo'


class AggregatesLService(AggregatesUtilityService):
    aggregate_type = 'aggregates_l_repo'


class AggregatesBurnerService(AggregatesUtilityService):
    aggregate_type = 'aggregates_burner_repo'

