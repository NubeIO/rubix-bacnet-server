import BAC0



class BAC0_Device:
    def __init__(self, ip, instance_number, obj_name, model_name, vendor_id, vendor_name, description):
        self.ip = ip
        self.instance_number = instance_number
        self.obj_name = obj_name
        self.model_name = model_name
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.description = description

    def start_device(self, init_port):
        self.device = BAC0.lite(
            ip=self.ip,
            deviceId=self.instance_number,
            localObjName=self.obj_name,
            port=init_port,
            modelName=self.model_name,
            vendorId=self.vendor_id,
            vendorName=self.vendor_name,
            description=self.description,
        )