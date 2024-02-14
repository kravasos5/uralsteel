from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class AccidentsBaseService(ServiceBase):
    """Сервис инцидентов и отчётов"""
    repository = None

    def retrieve_one_by_id(self, uow: AbstractUnitOfWork, accident_id: int):
        return self.retrieve_one(uow, id=accident_id)


class AggregatesAccidentService(AccidentsBaseService):
    """Сервис инцидентов и отчётов с агрегатами"""
    repository = 'aggregates_accident_repo'


class LadlesAccidentService(AccidentsBaseService):
    """Сервис инцидентов и отчётов с ковшами"""
    repository = 'ladles_accident_repo'


class CranesAccidentService(AccidentsBaseService):
    """Сервис инцидентов и отчётов с кранами"""
    repository = 'cranes_accident_repo'
