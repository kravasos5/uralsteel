import base64
import os
from typing import Type

from fastapi import UploadFile
from pydantic import BaseModel

from config import settings


class Base64Converter:
    """Кодирует и декодирует информацию в/из base64"""
    @staticmethod
    def encode_to_base64(file_path: str) -> bytes:
        """Закодировать файл в base64 строку"""
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        file_base64 = base64.b64encode(file_bytes)
        return file_base64

    @staticmethod
    def decode_from_base64(file_base64: bytes) -> bytes:
        """Декодировать файл из base64 строки"""
        file_bytes = base64.b64decode(file_base64)
        return file_bytes

    @staticmethod
    def key_to_base64(data: BaseModel | dict, key_name: str = 'photo', is_nested: bool = False, is_list: bool = False):
        """Кодирует значение ключа из схемы объекта ответа в base64"""
        # если вложенные json
        if is_nested:
            is_dict = isinstance(list(data.values())[0], dict)
            for elem in data:
                data[elem] = Base64Converter.change_iter_data(data[elem], key_name=key_name, is_dict=is_dict)
            return data
        # если список json
        elif is_list:
            is_dict = isinstance(data[0], dict)
            for elem in data:
                data[data.index(elem)] = Base64Converter.change_iter_data(
                    elem, key_name=key_name, is_dict=is_dict
                )
            return data
        # если один объект
        else:
            is_dict = isinstance(data, dict)
            data = Base64Converter.change_iter_data(data, key_name=key_name, is_dict=is_dict)
            return data

    @staticmethod
    def change_iter_data(iter_data, key_name: str = 'photo', is_dict: bool = False, many: bool = False):
        """Цикл обработки iter_data, использующийся в key_to_base64"""
        # если нужно пройтись по списку словарей или схем
        if many:
            if is_dict:
                for elem in iter_data:
                    value = elem[key_name]
                    value_base64 = Base64Converter.encode_to_base64(f'{settings.MEDIA_ROOT}/{value}').decode('UTF-8')
                    elem[key_name] = value_base64
            else:
                for elem in iter_data:
                    value = getattr(elem, key_name)
                    value_base64 = Base64Converter.encode_to_base64(f'{settings.MEDIA_ROOT}/{value}').decode('UTF-8')
                    setattr(elem, key_name, value_base64)
        # если объект один
        else:
            if is_dict:
                value = iter_data[key_name]
                value_base64 = Base64Converter.encode_to_base64(f'{settings.MEDIA_ROOT}/{value}').decode('UTF-8')
                iter_data[key_name] = value_base64
            else:
                value = getattr(iter_data, key_name)
                value_base64 = Base64Converter.encode_to_base64(f'{settings.MEDIA_ROOT}/{value}').decode('UTF-8')
                setattr(iter_data, key_name, value_base64)
        return iter_data


class PhotoAddToSchema:
    """Класс для работы со схемами и схемами"""

    @staticmethod
    async def file_add(
        file: UploadFile,
        start_path: str,
        data: dict,
        schema: Type[BaseModel],
        key_name: str = 'photo',
        create_dir: bool = False,
        created_dir: str | None = None,
    ):
        """
        Метод, добавляющий путь к фото для сохраниния в БД,
        а также сохраняющий файл.
        """
        if create_dir:
            folder_path: str = f'{settings.MEDIA_ROOT}/{created_dir}'
            # Создаю папку, если она не существует
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        path: str = f'{start_path}{file.filename}'
        full_path = f'{settings.MEDIA_ROOT}/{path}'
        saved_data = await file.read()
        with open(full_path, 'wb') as new_file:
            new_file.write(saved_data)
        answer = schema(**data, **{f'{key_name}': path})
        return answer
