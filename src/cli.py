import click
from sqlalchemy import Connection
from sqlalchemy.orm import Session
from streamlit.web import bootstrap

from deps import engine
from repositories import CategoriesRepository
from src.jobs.add_source_data import AddSourceDataCommand
from src.jobs.create_tables import CreateTableCommand
from src.jobs.insert_categories import InsertCategoriesCommand
from src.repositories import FinancesRepository
from src.utils.paths import GUI as GUI_PATH
from utils.database import with_connection, with_session


@click.group()
def cli():
    pass


@cli.command()
@with_session(engine)
@click.argument("file", type=str)
def add_source_data(session: Session, file: str):
    repository = FinancesRepository(session)
    AddSourceDataCommand(repository, file).execute()


@cli.command()
@with_connection(engine)
def create_tables(connection: Connection):
    CreateTableCommand(connection).execute()


@cli.command()
@with_session(engine)
def insert_categories(session: Session):
    repo_categories = CategoriesRepository(session)
    repo_finances = FinancesRepository(session)
    InsertCategoriesCommand(repo_categories, repo_finances).execute()


@cli.command()
def launch_gui():
    bootstrap.run(main_script_path=GUI_PATH, command_line="", args=[], flag_options={})


if __name__ == "__main__":
    cli()
