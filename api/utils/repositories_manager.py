from sqlalchemy.orm import Session

from repositories.accidents import LadlesAccidentRepo, CranesAccidentRepo, AggregatesAccidentRepo
from repositories.aggregates import AggregatesGMPRepo, AggregatesUKPRepo, AggregatesUVSRepo, AggregatesMNLZRepo, \
    AggregatesLRepo, AggregatesBurnerRepo
from repositories.brandsteel import BrandSteelRepo
from repositories.cranes import CranesRepo
from repositories.dynamic import ArchiveDynamicTableRepo, ActiveDynamicTableRepo
from repositories.employees import EmployeesRepo
from repositories.ladles import LadlesRepo
from repositories.routes import RoutesRepo


class RepoManager:
    """Менеджер репозиториев"""
    # ladles_accident_repo = LadlesAccidentRepo
    # cranes_accident_repo = CranesAccidentRepo
    # aggregates_accident_repo = AggregatesAccidentRepo
    # aggregates_gmp_repo = AggregatesGMPRepo
    # aggregates_ukp_repo = AggregatesUKPRepo
    # aggregates_uvs_repo = AggregatesUVSRepo
    # aggregates_mnlz_repo = AggregatesMNLZRepo
    # aggregates_l_repo = AggregatesLRepo
    # aggregates_burner_repo = AggregatesBurnerRepo
    # brandsteel_repo = BrandSteelRepo
    # cranes_repo = CranesRepo
    # archived_dyn_repo = ArchiveDynamicTableRepo
    # active_dyn_repo = ActiveDynamicTableRepo
    employees_repo = EmployeesRepo
    # ladles_repo = LadlesRepo
    # routes_repo = RoutesRepo

    def __init__(self, session: Session, other):
        """Инициализация всех репозиториев в другом классе"""
        # other.ladles_accident_repo = self.ladles_accident_repo(session)
        # other.cranes_accident_repo = self.cranes_accident_repo(session)
        # other.aggregates_accident_repo = self.aggregates_accident_repo(session)
        # other.aggregates_gmp_repo = self.aggregates_gmp_repo(session)
        # other.aggregates_ukp_repo = self.aggregates_ukp_repo(session)
        # other.aggregates_uvs_repo = self.aggregates_uvs_repo(session)
        # other.aggregates_mnlz_repo = self.aggregates_mnlz_repo(session)
        # other.aggregates_l_repo = self.aggregates_l_repo(session)
        # other.aggregates_burner_repo = self.aggregates_burner_repo(session)
        # other.brandsteel_repo = self.brandsteel_repo(session)
        # other.cranes_repo = self.cranes_repo(session)
        # other.archived_dyn_repo = self.archived_dyn_repo(session)
        # other.active_dyn_repo = self.active_dyn_repo(session)
        other.employees_repo = self.employees_repo(session)
        # other.ladles_repo = self.ladles_repo(session)
        # other.routes_repo = self.routes_repo(session)
