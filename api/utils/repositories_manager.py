from sqlalchemy.orm import Session

from repositories.accidents import LadlesAccidentRepo, CranesAccidentRepo, AggregatesAccidentRepo
from repositories.aggregates import AggregatesGMPRepo, AggregatesUKPRepo, AggregatesUVSRepo, AggregatesMNLZRepo, \
    AggregatesLRepo, AggregatesBurnerRepo, AggregatesAllRepo
from repositories.brandsteel import BrandSteelRepo
from repositories.cranes import CranesRepo
from repositories.dynamic import ArchiveDynamicTableRepo, ActiveDynamicTableRepo
from repositories.employees import EmployeesRepo
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
    }

    def __init__(self, session: Session, other, other_repositories):
        """Инициализация всех репозиториев в другом классе"""
        for repo in other_repositories.keys():
            other.repositories[repo] = self.repositories[repo](session)
        # other.repositories['ladles_accident_repo'] = self.repositories['ladles_accident_repo'](session)
        # other.repositories['cranes_accident_repo'] = self.repositories['cranes_accident_repo'](session)
        # other.repositories['aggregates_accident_repo'] = self.repositories['aggregates_accident_repo'](session)
        # other.repositories['aggregates_all'] = self.repositories['aggregates_all'](session)
        # other.repositories['aggregates_gmp_repo'] = self.repositories['aggregates_gmp_repo'](session)
        # other.repositories['aggregates_ukp_repo'] = self.repositories['aggregates_ukp_repo'](session)
        # other.repositories['aggregates_uvs_repo'] = self.repositories['aggregates_uvs_repo'](session)
        # other.repositories['aggregates_mnlz_repo'] = self.repositories['aggregates_mnlz_repo'](session)
        # other.repositories['aggregates_l_repo'] = self.repositories['aggregates_l_repo'](session)
        # other.repositories['aggregates_burner_repo'] = self.repositories['aggregates_burner_repo'](session)
        # other.repositories['brandsteel_repo'] = self.repositories['brandsteel_repo'](session)
        # other.repositories['cranes_repo'] = self.repositories['cranes_repo'](session)
        # other.repositories['archived_dyn_repo'] = self.repositories['archived_dyn_repo'](session)
        # other.repositories['active_dyn_repo'] = self.repositories['active_dyn_repo'](session)
        # other.repositories['employees_repo'] = self.repositories['employees_repo'](session)
        # other.repositories['ladles_repo'] = self.repositories['ladles_repo'](session)
        # other.repositories['routes_repo'] = self.repositories['routes_repo'](session)
