from logging import Logger
from threading import Thread

from flask import current_app
from werkzeug.local import LocalProxy


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:
    @staticmethod
    def run():
        from src import AppSetting
        from src.bacnet_server import BACServer
        from src.mqtt import MqttClient
        setting: AppSetting = current_app.config[AppSetting.KEY]
        logger = LocalProxy(lambda: current_app.logger) or Logger(__name__)
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            FlaskThread(target=MqttClient().start, daemon=True,
                        kwargs={'logger': logger, 'config': setting.mqtt}).start()

        if setting.bacnet.enabled:
            FlaskThread(target=BACServer().start_bac, daemon=True,
                        kwargs={'logger': logger, 'config': setting.bacnet}).start()
