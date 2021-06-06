from src.bacnet_master.interfaces.object_property import ObjProperty


class ProtocolObjectTypesSupported:

    def get(self, address, object_type, object_instance):
        return f'{address} {object_type} {object_instance} {ObjProperty.protocolObjectTypesSupported.value}'
