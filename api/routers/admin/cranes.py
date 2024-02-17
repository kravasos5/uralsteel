from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none
from schemas.cranes import CranesReadDTO, CranesCreateUpdateDTO, CranesUpdatePatchDTO
from services.cranes import CranesService

router = APIRouter(
    prefix="/admin/crane",
    tags=["admin"],
)


@router.get('/cranes', response_model=list[CranesReadDTO])
def get_cranes(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение кранов"""
    cranes = CranesService().retrieve_all(uow, offset, limit)
    return cranes


@router.post('/create', response_model=CranesReadDTO)
def create_crane(uow: UOWDep, crane_data: CranesCreateUpdateDTO):
    """Создание крана"""
    new_crane = CranesService().create_one(uow, crane_data)
    return new_crane


@router.get('/{object_id}', response_model=CranesReadDTO)
def get_crane(uow: UOWDep, object_id: GetIdDEP):
    """Получение крана"""
    crane = CranesService().retrieve_one_by_id(uow, object_id)
    error_raiser_if_none(crane, 'Crane')
    return crane


@router.put('/update/{object_id}', response_model=CranesReadDTO)
def update_crane_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        crane_data: CranesCreateUpdateDTO
):
    """Обновление крана методом put"""
    updated_crane = CranesService().update_one(uow, crane_data, id=object_id)
    error_raiser_if_none(updated_crane, 'Crane')
    return updated_crane


@router.patch('/update/{object_id}', response_model=CranesReadDTO)
def update_crane_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        crane_data: CranesUpdatePatchDTO
):
    """Обновление крана методом patch"""
    updated_crane = CranesService().update_one(uow, crane_data, id=object_id)
    error_raiser_if_none(updated_crane, 'Crane')
    return updated_crane


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_crane(uow: UOWDep, object_id: GetIdDEP):
    """Удаление крана по id"""
    deleted_crane = CranesService().delete_one(uow, id=object_id)
    error_raiser_if_none(deleted_crane, 'Crane')
