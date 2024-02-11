from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..sql import crud, schemas
from api.dependencies import get_db


router = APIRouter(
    prefix="/profile",
    tags=["users"],
)


dbDep = Annotated[Session, Depends(get_db)]


@router.get('/{slug}', response_model=schemas.EmployeesReadSchema)
def get_profile(slug: str, db: dbDep):
    """Получить данные профиля пользователя"""
    user_db = crud.get_user_by_slug(db, slug)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db
