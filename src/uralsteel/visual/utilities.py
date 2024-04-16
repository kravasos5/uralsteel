import json
import os
from enum import Enum
from uralsteel.settings import BASE_DIR

import glob2

from visual.redis_interface import RedisCacheMixin


class LadleOperationTypes(str, Enum):
    """Перечисление операций над ковшами"""
    TRANSPORTING = 'transporting'
    STARTING = 'starting'
    ENDING = 'ending'


class CraneMixin(RedisCacheMixin):
    """
    Миксин методов для операций над Cranes
    Вынесен сюда потому что будет использоваться в FastAPI также.
    """

    @staticmethod
    def get_cranes_pos() -> dict:
        """
        Функция, распаковывующая json-данные в рамках модуляции
        с помощью pygame интерфейса
        """
        # ключ для redis
        key_name = 'cranes_pos:1'
        # проверяю нет ли этой информации в redis
        result: dict | None = CraneMixin.get_key_redis_json(key_name)
        if result is not None:
            return result
        path = os.path.join(BASE_DIR, 'visual\\static\\visual\\jsons')
        files = glob2.glob(path + '\\*.json')
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
        CraneMixin.set_key_redis_json(key_name, data, 10)
        return data
