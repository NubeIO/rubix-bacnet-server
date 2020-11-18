"""Load configuration from .ini file."""
import configparser
import os
temp_path = os.path.dirname(os.path.abspath(__file__))
part_config = os.path.join(temp_path, "../settings/config.ini")
config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = '/settings/config.ini'
else:
    filename = f'{os.environ.get("data_dir")}/config.ini'

config.read(part_config)

