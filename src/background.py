import logging
from threading import Thread

from src.bacnet_server.bac_server import BACServer
from src.bacnet_server.mqtt_client import MqttClient
from src.ini_config import *

logger = logging.getLogger(__name__)


class Background:
    @staticmethod
    def run():
        logger.info("Running Background Task...")
        if settings__enable_mqtt:
            mqtt_thread = Thread(target=MqttClient.get_instance().start, daemon=True)
            mqtt_thread.start()

        if settings__enable_bacnet_server:
            bacnet_thread = Thread(target=BACServer.get_instance().start_bac, daemon=True)
            bacnet_thread.start()
