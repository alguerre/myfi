from src.utils.config import get_config
from src.utils.database import get_engine
from src.utils.paths import CONFIG_DB

engine = get_engine(**get_config(CONFIG_DB))
