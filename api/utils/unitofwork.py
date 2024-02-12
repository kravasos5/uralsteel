from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import Session

from database import session_factory
from repositories.accidents import LadlesAccidentRepo, CranesAccidentRepo, AggregatesAccidentRepo
from repositories.aggregates import AggregatesGMPRepo, AggregatesUKPRepo, AggregatesUVSRepo, AggregatesMNLZRepo, \
    AggregatesLRepo, AggregatesBurnerRepo
from repositories.brandsteel import BrandSteelRepo
from repositories.cranes import CranesRepo
from repositories.dynamic import ArchiveDynamicTableRepo, ActiveDynamicTableRepo
from repositories.employees import EmployeesRepo
from repositories.ladles import LadlesRepo
from repositories.routes import RoutesRepo
from utils.repositories_manager import RepoManager


class AbstractUnitOfWork(ABC):
    """Абстрактный uow класс"""

    manager = Type[RepoManager]
    ladles_accident_repo: Type[LadlesAccidentRepo]
    cranes_accident_repo: Type[CranesAccidentRepo]
    aggregates_accident_repo: Type[AggregatesAccidentRepo]
    aggregates_gmp_repo: Type[AggregatesGMPRepo]
    aggregates_ukp_repo: Type[AggregatesUKPRepo]
    aggregates_uvs_repo: Type[AggregatesUVSRepo]
    aggregates_mnlz_repo: Type[AggregatesMNLZRepo]
    aggregates_l_repo: Type[AggregatesLRepo]
    aggregates_burner_repo: Type[AggregatesBurnerRepo]
    brandsteel_repo: Type[BrandSteelRepo]
    cranes_repo: Type[CranesRepo]
    archived_dyn_repo: Type[ArchiveDynamicTableRepo]
    active_dyn_repo: Type[ActiveDynamicTableRepo]
    employees_repo: Type[EmployeesRepo]
    ladles_repo: Type[LadlesRepo]
    routes_repo: Type[RoutesRepo]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """Uow класс, который управляет транзакциями с помощью SqlAlchemy"""

    def __init__(self):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()

        # объявление репозиториев
        self.manager = RepoManager
        self.manager(session=self.session, other=self)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
