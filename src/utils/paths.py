from os.path import abspath, dirname, join

PATHS = dirname(abspath(__file__))

SRC = dirname(PATHS)
FINANCES = dirname(SRC)

JOBS = join(SRC, "jobs")

GUI = join(SRC, "gui", "gui.py")

CONFIG = join(FINANCES, "config")
CONFIG_DB = join(CONFIG, "database.yml")
CONFIG_EQUIVALENCES = join(CONFIG, "equivalences.yml")
CONFIG_RULES = join(CONFIG, "rules.yml")
