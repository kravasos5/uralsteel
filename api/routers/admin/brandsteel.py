from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none
from schemas.brandsteel import BrandSteelReadDTO, BrandSteelCreateUpdateDTO, BrandSteelUpdatePatchDTO
from services.brandsteel import BrandSteelService

router = APIRouter(
    prefix='/brandsteel',
)


error_raiser_message: str = 'Brand steel'


@router.get('/brands', response_model=list[BrandSteelReadDTO])
def get_brands(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение марок стали"""
    brandsteel = BrandSteelService().retrieve_all(uow, offset, limit)
    return brandsteel


@router.post('/create', response_model=BrandSteelReadDTO)
def create_brandsteel(uow: UOWDep, brandsteel_data: BrandSteelCreateUpdateDTO):
    """Создание марки стали"""
    new_brandsteel = BrandSteelService().create_one(uow, brandsteel_data)
    return new_brandsteel


@router.get('/{object_id}', response_model=BrandSteelReadDTO)
def get_brandsteel(uow: UOWDep, object_id: GetIdDEP):
    """Получение марки стали"""
    brandsteel = BrandSteelService().retrieve_one(uow, id=object_id)
    error_raiser_if_none(brandsteel, error_raiser_message)
    return brandsteel


@router.put('/update/{object_id}', response_model=BrandSteelReadDTO)
def update_brandsteel_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        brandsteel_data: BrandSteelCreateUpdateDTO
):
    """Обновление марки стали методом put"""
    updated_brandsteel = BrandSteelService().update_one(uow, brandsteel_data, id=object_id)
    error_raiser_if_none(updated_brandsteel, error_raiser_message)
    return updated_brandsteel


@router.patch('/update/{object_id}', response_model=BrandSteelReadDTO)
def update_brandsteel_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        brandsteel_data: BrandSteelUpdatePatchDTO
):
    """Обновление марки стали методом patch"""
    updated_brandsteel = BrandSteelService().update_one(uow, brandsteel_data, id=object_id)
    error_raiser_if_none(updated_brandsteel, error_raiser_message)
    return updated_brandsteel


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_brandsteel(uow: UOWDep, object_id: GetIdDEP):
    """Удаление марки стали по id"""
    deleted_brandsteel = BrandSteelService().delete_one(uow, id=object_id)
    error_raiser_if_none(deleted_brandsteel, error_raiser_message)
