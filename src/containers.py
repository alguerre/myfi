from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from src.gui.painter import (
    CategoricalExpensesAnalysisPainter,
    CategoricalExpensesEvolutionPainter,
    SavingsEvolutionPainter,
    YearlySalaryPainter,
    YearlySavingsPainter,
)
from src.gui.service import DataService, DataUow
from src.commands.add_data import AddDataService, AddDataUow
from src.commands.insert_categories import InsertCategoriesService, InsertCategoriesUow
from src.utils.config import get_config
from src.utils.database import get_engine
from src.utils.paths import paths


class Container(containers.DeclarativeContainer):
    # Gateways
    engine = providers.Singleton(get_engine, **get_config(paths.config_db))

    session_factory = providers.Factory(sessionmaker, engine)

    # Units of work
    add_data_uow = providers.Singleton(
        AddDataUow,
        session_factory=session_factory,
    )

    categories_uow = providers.Singleton(
        InsertCategoriesUow,
        session_factory=session_factory,
    )

    data_uow = providers.Singleton(
        DataUow,
        session_factory=session_factory,
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

    data_service = providers.Factory(
        DataService,
        uow=data_uow,
    )

    # Painters
    painters = providers.Dict(
        categorical_expenses_analysis=providers.Factory(
            CategoricalExpensesAnalysisPainter,
            data_service=data_service,
        ),
        categorical_expenses_evolution=providers.Factory(
            CategoricalExpensesEvolutionPainter,
            data_service=data_service,
        ),
        salary_evolution=providers.Factory(
            YearlySalaryPainter,
            data_service=data_service,
        ),
        savings_evolution=providers.Factory(
            SavingsEvolutionPainter,
            data_service=data_service,
        ),
        yearly_savings=providers.Factory(
            YearlySavingsPainter,
            data_service=data_service,
        ),
    )
