import json

import glob2

from utils.repositories_base import RedisRepo
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class CranesService(ServiceBase):
    """Сервис для работы с кранами"""
    repository = 'cranes_repo'

    async def retrieve_one_by_id(self, uow: AbstractUnitOfWork, crane_id: int):
        """Получение крана по id"""
        return await self.retrieve_one(uow, id=crane_id)

    async def get_cranes_info(self, uow: AbstractUnitOfWork, **filters):
        """Получить фото кранов и кареток"""
        # имя ключа в redis
        key_name = 'cranes_info:1'
        # проверяю нет ли этой информации в redis
        result: dict | None = RedisRepo.get_key_redis_json(key_name=key_name)
        if result is not None:
            return result
        # получаю информацию
        cranes = await self.retrieve_all(uow, **filters)
        cranes_dict: dict = {}
        # формирую словарь
        # информация ниже это размеры фото и само фото,
        # корпуса или каретки крана например
        for elem in cranes:
            cranes_dict[f'{elem.title}'] = {
                'size_x': elem.size_x,
                'size_y': elem.size_y,
                'photo': f'{elem.photo}'
            }
        # если в redis нет такого ключа, то запишу его, время жизни 10 секунд
        RedisRepo.set_key_redis_json(key_name=key_name, data=cranes_dict, ttl=360)
        return cranes_dict

    async def get_cranes_pos(self):
        """
        Функция, распаковывующая json-данные в рамках модуляции
        с помощью pygame интерфейса
        """
        # ключ для redis
        key_name: str = 'cranes_pos:1'
        # проверяю нет ли этой информации в redis
        result: dict | None = RedisRepo.get_key_redis_json(key_name=key_name)
        if result is not None:
            return result
        path = 'K:/python/python/uralsteel/uralsteel/visual/static/visual/jsons'
        files = glob2.glob(path + '/*.json')
        data: dict = {}
        for file in files:
            with open(file, 'r') as f:
                crane_data = json.load(f)
            for key, value in crane_data.items():
                new_value = {
                    'x': value[0][0],
                    'y': value[0][-1],
                    'is_ladle': value[1],
                }
                data[str(key)] = new_value
        # если в redis нет такого ключа, то запишу его, время жизни 10 секунд
        RedisRepo.set_key_redis_json(key_name=key_name, data=data, ttl=10)
        return data

    async def get_cranes_pos_info(self, uow: AbstractUnitOfWork, **filters):
        """Получение информации о кранах"""
        cranes_pos = await self.get_cranes_pos()
        cranes_info = await self.get_cranes_info(uow, **filters)
        data: dict = {
            'cranes_pos': cranes_pos,
            'cranes_info': cranes_info
        }
        return data
