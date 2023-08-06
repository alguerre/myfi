import click
from dependency_injector.wiring import Provide, inject
from sqlalchemy import Connection
from streamlit.web import bootstrap

from jobs.add_source_data import (
    AddDataService,
    AddSourceDataCommand,
)
from jobs.insert_categories import (
    InsertCategoriesCommand,
    InsertCategoriesService,
)
from src.containers import Container
from src.jobs.create_tables import CreateTableCommand
from src.utils.paths import paths
from utils.database import with_connection


@click.group()
def cli():
    pass


@cli.command()
@inject
@click.argument("file", type=str)
def add_source_data(
    service: AddDataService = Provide[Container.add_data_service],
    file: str = "",
    # only to be after injected service, but obligatory field
):
    AddSourceDataCommand(service, file).execute()


@cli.command()
@with_connection()
def create_tables(connection: Connection):
    CreateTableCommand(connection).execute()


@cli.command()
@inject
def insert_categories(
    service: InsertCategoriesService = Provide[Container.categories_service],
):
    InsertCategoriesCommand(service).execute()


@cli.command()
def launch_gui():
    bootstrap.run(
        main_script_path=str(paths.gui),
        command_line="",
        args=[],
        flag_options={},
    )


if __name__ == "__main__":
    # Enable the dependency-injector
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    cli()
