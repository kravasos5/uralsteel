from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, AccServiceDEP, \
    is_author_and_accident_object, make_object_broken
from schemas.accidents import AccidentReadDTO, AccidentsUpdatePatchDTO, \
    AccidentReadShortDTO, AccidentsCreateUpdateDTO


router = APIRouter(
    prefix='/accident',
)


@router.get('/accidents', response_model=list[AccidentReadShortDTO])
def get_accidents(uow: UOWDep, service: AccServiceDEP, offset: int = 0, limit: int = 100):
    """Получение отчётов инцидентов"""
    accidents = service.retrieve_all(uow, offset, limit)
    return accidents


@router.post('/create', response_model=AccidentReadDTO)
def create_accident(uow: UOWDep, service: AccServiceDEP, accident_data: AccidentsCreateUpdateDTO):
    """Создание происшествия"""
    # проверка есть ли такой автор и агрегат
    is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    new_accident = service.create_one(uow, accident_data)
    # отметить объект отчёта сломанным
    make_object_broken(uow, service, accident_data.object_id)
    return new_accident


@router.get('/{object_id}', response_model=AccidentReadDTO)
def get_crane(uow: UOWDep, service: AccServiceDEP, object_id: GetIdDEP):
    """Получение происшествия"""
    accident = service.retrieve_one_by_id(uow, object_id)
    error_raiser_if_none(accident)
    return accident


@router.put('/update/{object_id}', response_model=AccidentReadDTO)
def update_crane_put(
        uow: UOWDep,
        service: AccServiceDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsCreateUpdateDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    updated_acc = service.update_one(uow, accident_data, id=object_id)
    error_raiser_if_none(updated_acc)
    return updated_acc


@router.patch('/update/{object_id}', response_model=AccidentReadDTO)
def update_crane_patch(
        uow: UOWDep,
        service: AccServiceDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsUpdatePatchDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    updated_acc = service.update_one(uow, accident_data, id=object_id)
    error_raiser_if_none(updated_acc)
    return updated_acc


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_crane(uow: UOWDep, service: AccServiceDEP, crane_id: GetIdDEP):
    """Удаление происшествия по id"""
    deleted_acc = service.delete_one(uow, id=crane_id)
    error_raiser_if_none(deleted_acc)
