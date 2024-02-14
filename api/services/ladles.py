from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class LadlesService(ServiceBase):
    """Сервис для работы с ковшами"""
    repository = 'ladles_repo'

    def retrieve_one_by_id(self, uow: AbstractUnitOfWork, ladle_id: int, **filters):
        """Получение ковша по id"""
        return self.retrieve_one(uow, id=ladle_id, **filters)
