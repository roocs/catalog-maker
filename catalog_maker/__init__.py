import logging
import os

from roocs_utils.config import get_config

import catalog_maker

CONFIG = get_config(catalog_maker)

LOG_LEVEL = "INFO"
logging.basicConfig(level=LOG_LEVEL)


for env_var, value in CONFIG["environment"].items():
    os.environ[env_var.upper()] = value
