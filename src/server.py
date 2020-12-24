from abc import ABC

from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter


class GunicornFlaskApplication(BaseApplication, ABC):

    def __init__(self, _app, _options=None):
        self.options = _options or {}
        self.options.update({'when_ready': when_ready, 'on_exit': on_exit})
        self.application = _app
        super(GunicornFlaskApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def on_exit(server: Arbiter):
    server.log.info('Stop server')


def when_ready(server: Arbiter):
    server.log.info("Server is ready. Spawning workers")
    server.app.application.setup()
