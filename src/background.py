import logging
from threading import Thread

from flask import current_app

from .setting import AppSetting

logger = logging.getLogger(__name__)


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
        from src.bacnet_server import BACServer
        from src.mqtt import MqttClient
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            MqttClient().start(setting.mqtt)

        if setting.bacnet.enabled:
            FlaskThread(target=BACServer().start_bac, daemon=True, kwargs={'config': setting.bacnet}).start()

        Background.sync_on_start()

    @staticmethod
    def sync_on_start():
        from rubix_http.request import gw_request

        """Sync mapped points values from LoRa > BACnet points values"""
        gw_request('/lora/api/sync/lp_to_bp')

        """Sync mapped points values from Modbus > BACnet points values"""
        gw_request('/ps/api/sync/mp_to_bp')

        """Sync mapped points values from BACnet > Generic points values"""
        from .bacnet_server.models.model_point_store import BACnetPointStoreModel
        BACnetPointStoreModel.sync_points_values_bp_to_gp_process()
