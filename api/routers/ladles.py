from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, Depends

from dependencies import UOWDep, GetIdDEP, GetOpTypeDEP, error_raiser_if_none, oauth2_scheme
from schemas.dynamics import DynamicLadleInfoAnswerNested
from services.dynamic import ActiveDynamicTableService, LadleOperationTypes
from utils.utilities import Base64Converter

router = APIRouter(
    prefix="/ladles",
    tags=["ladles"],
    dependencies=[Depends(oauth2_scheme)],
)


@router.get('/time')
async def get_time() -> dict:
    """Получение информации о времени в форме времени на странице ковшей."""
    # проверка на авторизацию
    # написать схему ответа
    data = await ActiveDynamicTableService().get_ladle_timeform()
    return data


@router.post('/ladles-info', response_model=dict[int, DynamicLadleInfoAnswerNested])
async def get_ladles_info(
    uow: UOWDep,
    hours: Annotated[int, Query(ge=0, le=23)],
    minutes: Annotated[int, Query(ge=0, le=60)]
) -> dict[int, DynamicLadleInfoAnswerNested]:
    """Получение информации о положении ковшей на странице"""
    # проверка на авторизацию
    # написать схему ответа
    service = ActiveDynamicTableService()
    date = await service.time_convert(hours, minutes)
    data, deletion_ids = service.get_ladles_info(uow, date)
    await service.delete_by_ids(uow, deletion_ids)
    data = Base64Converter.key_to_base64(data, is_nested=True)
    return data


@router.post('/ladle-operation/{object_id}')
async def ladle_operation(
    uow: UOWDep,
    object_id: GetIdDEP,
    operation_type: GetOpTypeDEP,
    hours: Annotated[int, Query(ge=0, le=23)],
    minutes: Annotated[int, Query(ge=0, le=60)],
) -> dict[str, str]:
    """Завершение операции над ковшами"""
    service = ActiveDynamicTableService()
    # проверяю есть ли такой объект
    operation = await service.retrieve_one(uow, id=object_id)
    await error_raiser_if_none(operation, 'Operation')
    # валидация соответствия типа операции и ковша в конкретной операции
    match operation_type.value:
        case LadleOperationTypes.TRANSPORTING.value:
            # если ковш транспортируемый, то у него должны быть
            # actual_start и actual_end
            if not (operation.actual_start and operation.actual_end):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Ladle in that operation isn't transporting"
                )
        case LadleOperationTypes.STARTING.value:
            # если ковш начинающий, то у него не должно быть
            # actual_start и actual_end
            if operation.actual_start or operation.actual_end:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Ladle in that operation isn't starting"
                )
        case LadleOperationTypes.WAITING.value:
            # если ковш "ожидающий", то нужно убедиться, что
            # фактическое время завершения операции больше,
            # чем фактическое время начала. А также, что оно есть вообще
            if not operation.actual_start or operation.actual_end:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Ladle in that operation isn't waiting"
                )
            end_date = await service.time_convert(hours, minutes)
            if not await service.is_end_time_gt_start_time(operation.actual_start, end_date):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Actual end time must be greater than actual start time"
                )
    data = await service.get_ladle_operation_id(uow, object_id, operation_type, hours, minutes)
    return data
