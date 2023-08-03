from src.utils.config import get_config
from src.utils.database import get_engine
from src.utils.paths import paths

engine = get_engine(**get_config(paths.config_db))
