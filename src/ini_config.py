"""Load configuration from .ini file."""
import configparser

# Read local file `config.ini`.
config = configparser.ConfigParser()
config.read('settings/config.ini')
