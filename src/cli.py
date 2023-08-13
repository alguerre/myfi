import click
from dependency_injector.wiring import Provide, inject
from streamlit.web import bootstrap

from src.containers import Container
from src.commands.add_data import (
    AddDataService,
    AddDataCommand,
)
from src.commands.insert_categories import (
    InsertCategoriesCommand,
    InsertCategoriesService,
)
from src.utils.paths import paths


@click.group()
def cli():
    pass


@cli.command()
@inject
@click.argument("file", type=str)
def add_data(
    service: AddDataService = Provide[Container.add_data_service],
    file: str = "",
    # only to be after injected service, but obligatory field
):
    AddDataCommand(service, file).execute()


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
