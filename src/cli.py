import click
from sqlalchemy import Connection
from streamlit.web import bootstrap

from deps import engine
from jobs.add_source_data import AddDataService, AddDataUow, AddSourceDataCommand
from jobs.insert_categories import (
    InsertCategoriesCommand,
    InsertCategoriesService,
    InsertCategoriesUow,
)
from src.jobs.create_tables import CreateTableCommand
from src.utils.paths import GUI as GUI_PATH
from utils.database import with_connection


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file", type=str)
def add_source_data(file: str):
    uow = AddDataUow()
    service = AddDataService(uow)
    AddSourceDataCommand(service, file).execute()


@cli.command()
@with_connection(engine)
def create_tables(connection: Connection):
    CreateTableCommand(connection).execute()


@cli.command()
def insert_categories():
    uow = InsertCategoriesUow()
    service = InsertCategoriesService(uow)
    InsertCategoriesCommand(service).execute()


@cli.command()
def launch_gui():
    bootstrap.run(main_script_path=GUI_PATH, command_line="", args=[], flag_options={})


if __name__ == "__main__":
    cli()
