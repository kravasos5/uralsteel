from sqlalchemy.orm import Session

from repositories.accidents import LadlesAccidentRepo, CranesAccidentRepo, AggregatesAccidentRepo
from repositories.aggregates import AggregatesGMPRepo, AggregatesUKPRepo, AggregatesUVSRepo, AggregatesMNLZRepo, \
    AggregatesLRepo, AggregatesBurnerRepo, AggregatesAllRepo
from repositories.brandsteel import BrandSteelRepo
from repositories.cranes import CranesRepo
from repositories.dynamic import ArchiveDynamicTableRepo, ActiveDynamicTableRepo
from repositories.employees import EmployeesRepo
from repositories.jwt import RefreshTokenRepo, RefreshTokenBlacklistRepo
from repositories.ladles import LadlesRepo
from repositories.routes import RoutesRepo


class RepoManager:
    """Менеджер репозиториев"""
    repositories = {
        'ladles_accident_repo': LadlesAccidentRepo,
        'cranes_accident_repo': CranesAccidentRepo,
        'aggregates_accident_repo': AggregatesAccidentRepo,
        'aggregates_all': AggregatesAllRepo,
        'aggregates_gmp_repo': AggregatesGMPRepo,
        'aggregates_ukp_repo': AggregatesUKPRepo,
        'aggregates_uvs_repo': AggregatesUVSRepo,
        'aggregates_mnlz_repo': AggregatesMNLZRepo,
        'aggregates_l_repo': AggregatesLRepo,
        'aggregates_burner_repo': AggregatesBurnerRepo,
        'brandsteel_repo': BrandSteelRepo,
        'cranes_repo': CranesRepo,
        'archive_dyn_repo': ArchiveDynamicTableRepo,
        'active_dyn_repo': ActiveDynamicTableRepo,
        'employees_repo': EmployeesRepo,
        'ladles_repo': LadlesRepo,
        'routes_repo': RoutesRepo,
        'refresh_token_repo': RefreshTokenRepo,
        'refresh_token_bl_repo': RefreshTokenBlacklistRepo,
    }

    def __init__(self, session: Session, other, other_repositories):
        """Инициализация всех репозиториев в другом классе"""
        for repo in other_repositories.keys():
            other.repositories[repo] = self.repositories[repo](session)
