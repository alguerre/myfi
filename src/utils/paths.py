from dataclasses import dataclass
from pathlib import Path


@dataclass(repr=False, frozen=True)
class Paths:
    this: Path = Path(__file__).resolve().parent
    src: Path = this.parent
    finances: Path = src.parent
    commands: Path = src / "commands"
    gui: Path = src / "gui" / "gui.py"
    config: Path = finances / "config"
    config_db: Path = config / "database.yml"
    config_categories: Path = config / "categories.yml"
    config_rules: Path = config / "rules.yml"


paths = Paths()
