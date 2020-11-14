from flask_restful import Resource

from src.bacnet_server.bac_server import BACServer


class BACnetServerStatus(Resource):
    def get(self):
        return {'running': BACServer.get_instance().is_running()}, 200
