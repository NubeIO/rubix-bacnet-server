import toml

from src.pyinstaller import resource_path


def get_version():
    details = toml.load(resource_path("pyproject.toml"))
    version = details.get('tool', {}).get('poetry', {}).get('version')
    return f'v{version}' if version else None
