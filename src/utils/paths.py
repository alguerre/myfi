from pathlib import Path
from dataclasses import dataclass


@dataclass(repr=False, frozen=True)
class Paths:
    this: Path = Path(__file__).resolve().parent
    src: Path = this.parent
    finances: Path = src.parent
    jobs: Path = src / "jobs"
    gui: Path = src / "gui" / "gui.py"
    config: Path = finances / "config"
    config_db: Path = config / "database.yml"
    config_equivalences: Path = config / "equivalences.yml"
    config_rules: Path = config / "rules.yml"


paths = Paths()
