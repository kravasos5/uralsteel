from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, GetAccTypeDEP, AccidentType, error_raiser_if_none, is_author, is_object
from schemas.accidents import AccidentReadDTO, AccidentsUpdatePatchDTO, \
    AccidentReadShortDTO, AccidentsCreateUpdateDTO
from services.accidents import CranesAccidentService, LadlesAccidentService, AggregatesAccidentService


router = APIRouter(
    prefix="/admin/accident",
    tags=["admin"],
)


@router.get('/accidents', response_model=list[AccidentReadShortDTO])
def get_accidents(uow: UOWDep, acc_type: GetAccTypeDEP, offset: int = 0, limit: int = 100):
    """Получение отчётов инцидентов"""
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    accidents = service.retrieve_all(uow, offset, limit)
    return accidents


@router.post('/create', response_model=AccidentReadDTO)
def create_accident(uow: UOWDep, acc_type: GetAccTypeDEP, accident_data: AccidentsCreateUpdateDTO):
    """Создание происшествия"""
    # проверка есть ли такой автор и агрегат
    is_author(uow, accident_data.author_id)
    is_object(uow, accident_data.object_id, acc_type)
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    new_accident = service.create_one(uow, accident_data)
    return new_accident


@router.get('/{object_id}', response_model=AccidentReadDTO)
def get_crane(uow: UOWDep, acc_type: GetAccTypeDEP, object_id: GetIdDEP):
    """Получение происшествия"""
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    accident = service.retrieve_one_by_id(uow, object_id)
    error_raiser_if_none(accident)
    return accident


@router.put('/update/{object_id}', response_model=AccidentReadDTO)
def update_crane_put(
        uow: UOWDep,
        acc_type: GetAccTypeDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsCreateUpdateDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    is_author(uow, accident_data.author_id)
    is_object(uow, accident_data.object_id, acc_type)
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    updated_acc = service.update_one(uow, accident_data, id=object_id)
    error_raiser_if_none(updated_acc)
    return updated_acc


@router.patch('/update/{object_id}', response_model=AccidentReadDTO)
def update_crane_patch(
        uow: UOWDep,
        acc_type: GetAccTypeDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsUpdatePatchDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    is_author(uow, accident_data.author_id)
    is_object(uow, accident_data.object_id, acc_type)
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    updated_acc = service.update_one(uow, accident_data, id=object_id)
    error_raiser_if_none(updated_acc)
    return updated_acc


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_crane(uow: UOWDep, acc_type: GetAccTypeDEP, crane_id: GetIdDEP):
    """Удаление происшествия по id"""
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    deleted_acc = service.delete_one(uow, id=crane_id)
    error_raiser_if_none(deleted_acc)
