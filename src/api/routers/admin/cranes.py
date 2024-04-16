from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, UploadFile, File

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, CraneFieldsDEP, CraneFieldsPatchDEP
from schemas.cranes import CranesReadDTO, CranesCreateUpdateDTO, CranesUpdatePatchDTO
from services.cranes import CranesService
from utils.utilities import Base64Converter, PhotoAddToSchema

router = APIRouter(
    prefix='/crane',
)


path: str = 'photos/cranes/'


@router.get('/cranes', response_model=list[CranesReadDTO], description='photo кодируется с помощью base64')
async def get_cranes(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение кранов"""
    cranes = await CranesService().retrieve_all(uow, offset, limit)
    answer_data = Base64Converter.key_to_base64(cranes, is_list=True)
    return answer_data


@router.post('/create', response_model=CranesReadDTO)
async def create_crane(
    uow: UOWDep,
    crane_data: CraneFieldsDEP,
    photo: Annotated[UploadFile, File()]
):
    """Создание крана"""
    create_data = await PhotoAddToSchema.file_add(photo, path, crane_data, CranesCreateUpdateDTO)
    new_crane = await CranesService().create_one(uow, create_data)
    answer_data = Base64Converter.key_to_base64(new_crane)
    return answer_data


@router.get('/{object_id}', response_model=CranesReadDTO)
async def get_crane(uow: UOWDep, object_id: GetIdDEP):
    """Получение крана"""
    crane = await CranesService().retrieve_one_by_id(uow, object_id)
    await error_raiser_if_none(crane, 'Crane')
    answer_data = Base64Converter.key_to_base64(crane)
    return answer_data


@router.put('/update/{object_id}', response_model=CranesReadDTO)
async def update_crane_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        crane_data: CraneFieldsDEP,
        photo: Annotated[UploadFile, File()]
):
    """Обновление крана методом put"""
    update_data = await PhotoAddToSchema.file_add(photo, path, crane_data, CranesCreateUpdateDTO)
    updated_crane = await CranesService().update_one(uow, update_data, id=object_id)
    await error_raiser_if_none(updated_crane, 'Crane')
    answer_data = Base64Converter.key_to_base64(updated_crane)
    return answer_data


@router.patch('/update/{object_id}', response_model=CranesReadDTO)
async def update_crane_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        crane_data: CraneFieldsPatchDEP,
        photo: Annotated[UploadFile, File()] = None
):
    """Обновление крана методом patch"""
    crane_data = {key: value for key, value in crane_data.items() if value is not None}
    if photo:
        update_data = await PhotoAddToSchema.file_add(photo, path, crane_data, CranesUpdatePatchDTO)
    else:
        update_data = CranesUpdatePatchDTO(**crane_data)
    updated_crane = await CranesService().update_one(uow, update_data, id=object_id)
    await error_raiser_if_none(updated_crane, 'Crane')
    answer_data = Base64Converter.key_to_base64(updated_crane)
    return answer_data


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_crane(uow: UOWDep, object_id: GetIdDEP):
    """Удаление крана по id"""
    deleted_crane = await CranesService().delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_crane, 'Crane')
