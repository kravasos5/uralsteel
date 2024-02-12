from typing import Annotated

from fastapi import Depends

from utils.unitofwork import AbstractUnitOfWork, UnitOfWork


UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


# def get_db():
#     """Получить сессию БД"""
#     db = session_factory()
#     try:
#         yield db
#     finally:
#         db.close()
