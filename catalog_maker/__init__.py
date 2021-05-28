__author__ = """Eleanor Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.1.0"

import logging
import os

from roocs_utils.config import get_config

import catalog_maker

CONFIG = get_config(catalog_maker)

LOG_LEVEL = "INFO"
logging.basicConfig(level=LOG_LEVEL)


for env_var, value in CONFIG["environment"].items():
    os.environ[env_var.upper()] = value
