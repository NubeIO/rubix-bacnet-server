from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.object_property import ObjProperty
from src.bacnet_server.utils.functions import to_bool


class BACnetCommon:

    @classmethod
    def type_mstp(cls, type_mstp):
        return to_bool(type_mstp)

    @classmethod
    def present_value(cls):
        return ObjProperty.presentValue.value

    @classmethod
    def obj_device(cls):
        return ObjType.DEVICE.id

    @classmethod
    def object_list(cls):
        return ObjProperty.objectList.value

    @classmethod
    def build_url(cls, ip, **kwargs):
        mask = kwargs.get('mask', None)
        port = kwargs.get('port', None)
        if mask is not None:
            if port is not None:
                return f"{ip}/{mask}:{port}"
            else:
                return f"{ip}/{mask}"
        else:
            return ip

    # device, obj, obj_instance, prop
    @classmethod
    def common_point(cls, device_ip, **kwargs):
        network_number = kwargs.get('network_number', None)
        type_mstp = kwargs.get('type_mstp', None)
        device_id = kwargs.get('device_id', None)
        device_mac = kwargs.get('device_mac', None)
        type_mstp = BACnetCommon.type_mstp(type_mstp)
        obj = kwargs.get('obj', None)  # analogInput
        obj_instance = kwargs.get('obj_instance', None)  # 1
        prop = kwargs.get('prop', None)  # 85 presentValue
        if type_mstp:
            return f'{network_number}:{device_mac} {obj} {obj_instance} {prop}'
        if network_number != 0:
            if 1 <= network_number <= 65534:
                return f'{network_number}:{device_ip} {obj} {obj_instance} {prop}'
        else:
            return f'{device_ip} {obj} {obj_instance} {prop}'

    @classmethod
    def common_device(cls, device_ip, device_id, **kwargs):
        network_number = kwargs.get('network_number', None)
        type_mstp = kwargs.get('type_mstp', None)
        device_mac = kwargs.get('device_mac', None)
        prop = kwargs.get('prop', None)
        type_mstp = BACnetCommon.type_mstp(type_mstp)
        obj = BACnetCommon.obj_device()
        if type_mstp:
            return f'{network_number}:{device_mac} {obj} {device_id} {prop}'
        if network_number is not None:
            if 1 <= network_number <= 65534:
                return f'{network_number}:{device_ip} {obj} {device_id} {prop}'
        else:
            return f'{device_ip} {obj} {device_id} {prop}'


class PointReadFunctions:

    @classmethod
    def read_present_value(cls, device_ip, **kwargs):
        device_mask = kwargs.get('device_mask', None)
        device_port = kwargs.get('device_port', None)
        network_number = kwargs.get('network_number', None)
        type_mstp = kwargs.get('type_mstp', None)
        device_mac = kwargs.get('device_mac', None)
        obj = kwargs.get('obj', None)  # analogInput
        obj_instance = kwargs.get('obj_instance', None)  # 1
        prop = BACnetCommon.object_list()  # 85 presentValue
        url = BACnetCommon.build_url(device_ip, mask=device_mask, port=device_port)
        return BACnetCommon.common_point(url, network_number=network_number, type_mstp=type_mstp, device_mac=device_mac,
                                         obj=obj, obj_instance=obj_instance,
                                         prop=prop)


class DeviceReadFunctions:

    @classmethod
    def read_object_list(cls, device_ip, device_id, **kwargs):
        device_port = kwargs.get('device_port', None)
        device_mask = kwargs.get('device_mask', None)
        network_number = kwargs.get('network_number', None)
        type_mstp = kwargs.get('type_mstp', None)
        device_mac = kwargs.get('device_mac', None)
        url = BACnetCommon.build_url(device_ip, mask=device_mask, port=device_port)
        return BACnetCommon.common_device(url, device_id,
                                          network_number=network_number, type_mstp=type_mstp, device_mac=device_mac,
                                          prop=BACnetCommon.object_list())

    @classmethod
    def supported_services(cls, address, object_type, object_instance, type_mstp):
        if type_mstp:
            return f'{address} {object_type} {object_instance} {ObjProperty.protocolServicesSupported.value}'
        else:
            return f'{address} {object_type} {object_instance} {ObjProperty.protocolServicesSupported.value}'
