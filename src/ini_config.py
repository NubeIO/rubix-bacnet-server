"""Load configuration from .ini file."""
import configparser

import os

config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = '/settings/config.ini'
else:
    filename = f'{os.environ.get("data_dir")}/config.ini'

config.read(filename)
