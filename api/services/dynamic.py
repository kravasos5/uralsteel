from schemas.dynamics import DynamicTableCreateUpdateDTO
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class ActiveDynamicTableService(ServiceBase):
    """Сервис для работы с активной динамической таблицей"""
    repository = 'active_dyn_repo'
    active_repo = 'active_dyn_repo'
    archive_repo = 'archive_dyn_repo'

    def from_active_to_archive(self, uow: AbstractUnitOfWork, dyn_id: int):
        """Перенос данных из активной динамической таблицы в архивную"""
        with uow:
            # получаю информацию для трансфера из одной таблицы в другую
            transfer_info = uow.repositories[self.active_repo].retrieve_one(id=dyn_id)
            # преобразую эту информацию в нужную схему создания
            create_schema = uow.repositories[self.active_repo].convert_to_create_schema(transfer_info)
            # удаляю из активной динамической таблицы
            deleted_one = uow.repositories[self.active_repo].delete_one(id=dyn_id)
            # добавляю в архивную
            created_one = uow.repositories[self.archive_repo].create_one(create_schema)
            return deleted_one, created_one


class ArchiveDynamicTableService(ServiceBase):
    """Сервис для работы с активной динамической таблицей"""
    repository = 'archive_dyn_repo'
