from datetime import datetime
from enum import Enum

import pytz

from config import settings
from utils.repositories_base import RedisRepo
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class LadleOperationTypes(str, Enum):
    """Перечисление операций над ковшами"""
    TRANSPORTING = 'transporting'
    STARTING = 'starting'
    WAITING = 'waiting'


class ActiveDynamicTableService(ServiceBase):
    """Сервис для работы с активной динамической таблицей"""
    repository = 'active_dyn_repo'
    archive_repo = 'archive_dyn_repo'

    async def from_active_to_archive(self, uow: AbstractUnitOfWork, dyn_ids: list[int]):
        """Перенос данных из активной динамической таблицы в архивную"""
        async with uow:
            answer: list[tuple] = []
            for dyn_id in dyn_ids:
                # получаю информацию для трансфера из одной таблицы в другую
                transfer_info = await uow.repositories[self.repository].retrieve_one(id=dyn_id)
                # преобразую эту информацию в нужную схему создания
                create_schema = await uow.repositories[self.repository].convert_to_create_schema(transfer_info)
                # удаляю из активной динамической таблицы
                deleted_one = await uow.repositories[self.repository].delete_one(id=dyn_id)
                # добавляю в архивную
                created_one = await uow.repositories[self.archive_repo].create_one(create_schema)
                answer.append((deleted_one, created_one))
            # провожу транзакцию
            await uow.commit()
            return answer

    async def time_convert(self, hours: int, minutes: int) -> datetime:
        """Метод, переводящий время в удобный формат без использования django timezone"""
        # записываю время в redis-cache
        RedisRepo.set_key_redis('ltimeform', f'{hours}:{minutes}', 120)
        # получаю "наивную дату"
        naive_datetime = datetime(2023, 12, 11, hours, minutes)
        # преобразую её в "осведомлённую", то есть знающую часовой пояс
        aware_datetime = pytz.timezone(settings.TIME_ZONE).localize(naive_datetime)
        ############
        # в будущем здесь может быть любая дата, но будет текущий день
        # получаю текущий часовой пояс
        # current_timezone = pytz.timezone(TIME_ZONE)
        # получаю сегодняшнюю дату
        # today = current_timezone.localize(datetime.now())
        ############
        return aware_datetime

    async def is_end_time_gt_start_time(self, start_time: datetime, end_time: datetime) -> bool:
        """Сравнивает время конца и начала операции"""
        if end_time > start_time:
            return True
        return False

    async def get_ladle_operation_id(
            self,
            uow: AbstractUnitOfWork,
            operation_id: int,
            operation_type: LadleOperationTypes,
            hours: int,
            minutes: int
    ):
        async with uow:
            """Запрос с операцией над ковшом"""
            data: dict = {}
            # получаю объект операции
            operation = await uow.repositories[self.repository].retrieve_one(id=operation_id)
            # получаю время
            time = await self.time_convert(hours, minutes)
            # удаляю старые ключи из хранилища redis
            RedisRepo.delete_keys_redis('*ltime:*')
            match operation_type.value:
                case LadleOperationTypes.TRANSPORTING.value:
                    # если ковш "транспортируемый"
                    # перезаписываю запись в архивную таблицу
                    await self.from_active_to_archive(uow, [operation.id])
                    data['st'] = 'Ladle moved into archive dynamic table'
                case LadleOperationTypes.STARTING.value:
                    # если ковш "начинающий"
                    # перезаписываю дату в операции Активной Таблицы,
                    # то есть теперь ковш стаёт "ожидающим"
                    operation.actual_start = time
                    await uow.repositories[self.repository].update_one(operation, id=operation_id)
                    data['st'] = 'Now ladle is waiting'
                case LadleOperationTypes.WAITING.value:
                    # если ковш "ожидающий"
                    # перезаписываю дату в операции Активной Таблицы,
                    # то есть теперь ковш стаёт "транспортируемым"
                    operation.actual_end = time
                    await uow.repositories[self.repository].update_one(operation, id=operation_id)
                    data['st'] = 'Now ladle is transporting'
                case _:
                    # в таком случае status=400, то есть пользователь
                    # клиент неверно указал operation_type
                    data['st'] = 'Invalid operation_type'
            await uow.commit()
            return data

    async def get_ladle_timeform(self):
        """
        Получение информации о времени в форме времени на странице ковшей.
        Проходит проверка наличия значения времени в кэше, оно будет передано
        странице и там обработано
        """
        ladle_timeform = RedisRepo.get_key_redis('ltimeform')
        if ladle_timeform:
            return {'timeformvalue': ladle_timeform}
        return {}

    async def get_ladles_info(self, uow: AbstractUnitOfWork, date: datetime) -> tuple[dict, list[int]] | None:
        """Получение информации о положении ковшей на странице"""
        async with uow:
            ladles_info: dict = {}
            deletion_ids: list[int] = []
            # получаю имя ключа, которое используется при кэшировании
            key_name: str = f"ltime:{date.strftime('%H-%M')}"
            # проверка наличия ключа в redis-cache
            result: dict | None = RedisRepo.get_key_redis_json(key_name)
            if result is not None:
                return result, deletion_ids
            # если ключа нет, то брать информацию из базы данных,
            # она автоматически добавится в кэш в конце этого метода, перед return
            # Извлекаю "транспортируемые" ковши и
            # добавляю всю нужную информацию в словарь
            ladles_info, deletion_ids = await uow.repositories[self.repository].retrieve_transporting(
                date=date,
                ladles_info=ladles_info,
                deletion_ids=deletion_ids
            )
            # Извлекаю "ожидающие" ковши и
            # добавляю всю нужную информацию в словарь
            ladles_info, deletion_ids = await uow.repositories[self.repository].retrieve_waiting(
                date=date,
                ladles_info=ladles_info,
                deletion_ids=deletion_ids
            )
            # Извлекаю "начинающие" ковши и
            # добавляю всю нужную информацию в словарь
            ladles_info, deletion_ids = await uow.repositories[self.repository].retrieve_starting(
                date=date,
                ladles_info=ladles_info,
                deletion_ids=deletion_ids
            )
            # добавление ключа в redis
            RedisRepo.set_key_redis_json(key_name, ladles_info, 300)
            return ladles_info, deletion_ids


class ArchiveDynamicTableService(ServiceBase):
    """Сервис для работы с активной динамической таблицей"""
    repository = 'archive_dyn_repo'
