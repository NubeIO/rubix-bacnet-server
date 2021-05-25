from src.pyinstaller import resource_path


def get_version() -> str:
    try:
        with open(resource_path('VERSION')) as version_file:
            version = f'v{version_file.read().strip()}'
    except FileNotFoundError:
        version = 'v0.0.0'
    return version
