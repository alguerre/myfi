from dependency_injector import containers, providers

from src.jobs.add_source_data import AddDataService, AddDataUow
from src.jobs.insert_categories import InsertCategoriesService, InsertCategoriesUow
from src.utils.config import get_config
from src.utils.database import get_engine
from src.utils.paths import paths


class Container(containers.DeclarativeContainer):
    # Gateways
    engine = providers.Singleton(get_engine, **get_config(paths.config_db))

    # Units of work
    add_data_uow = providers.Singleton(
        AddDataUow,
        engine=engine,
    )

    categories_uow = providers.Singleton(
        InsertCategoriesUow,
        engine=engine,
    )

    # Services
    add_data_service = providers.Factory(
        AddDataService,
        uow=add_data_uow,
    )

    categories_service = providers.Factory(
        InsertCategoriesService,
        uow=categories_uow,
    )
