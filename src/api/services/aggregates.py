from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class AggregatesAllService(ServiceBase):
    """Сервис взаимодействия с Aggregates базовый"""
    repository = 'aggregates_all'

    async def retrieve_one_by_id(self, uow: AbstractUnitOfWork, ag_id: int):
        """Получение агрегата по id"""
        async with uow:
            result = await uow.repositories[self.repository].retrieve_one(id=ag_id)
            return result


class AggregatesGMPService(AggregatesAllService):
    repository = 'aggregates_gmp_repo'


class AggregatesUKPService(AggregatesAllService):
    repository = 'aggregates_ukp_repo'


class AggregatesUVSService(AggregatesAllService):
    repository = 'aggregates_uvs_repo'


class AggregatesMNLZService(AggregatesAllService):
    repository = 'aggregates_mnlz_repo'


class AggregatesLService(AggregatesAllService):
    repository = 'aggregates_l_repo'


class AggregatesBurnerService(AggregatesAllService):
    repository = 'aggregates_burner_repo'
