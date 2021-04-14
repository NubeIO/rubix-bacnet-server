# def pnt_check_obj_type(self, network):

#     return self.networks.get(net_url, {}).get(network_device_id, {}).get(network_device_name)

# Object ObjectNumber
# analogInput	0
# analogOutput	1
# analogValue	2
# binaryInput	3
# binaryOutput	4
# binaryValue	5
# calendar	6
# command	7
# device	8
# Event Enrollment	9
# File	10
# Group	11
# Loop	12
# Multistate Input	13
# Multistate Output	14
# Notification Class	15
# Program	16
# Schedule	17


# BACNET_APPLICATION_TAG_NULL = 0,
# BACNET_APPLICATION_TAG_BOOLEAN = 1,
# BACNET_APPLICATION_TAG_UNSIGNED_INT = 2,
# BACNET_APPLICATION_TAG_SIGNED_INT = 3,
# BACNET_APPLICATION_TAG_REAL = 4,
# BACNET_APPLICATION_TAG_DOUBLE = 5,
# BACNET_APPLICATION_TAG_OCTET_STRING = 6,
# BACNET_APPLICATION_TAG_CHARACTER_STRING = 7,
# BACNET_APPLICATION_TAG_BIT_STRING = 8,
# BACNET_APPLICATION_TAG_ENUMERATED = 9,
# BACNET_APPLICATION_TAG_DATE = 10,
# BACNET_APPLICATION_TAG_TIME = 11,
# BACNET_APPLICATION_TAG_OBJECT_ID = 12,
# BACNET_APPLICATION_TAG_RESERVE1 = 13,
# BACNET_APPLICATION_TAG_RESERVE2 = 14,
# BACNET_APPLICATION_TAG_RESERVE3 = 15,
# MAX_BACNET_APPLICATION_TAG = 16


# device required property
deviceRequiredProperty = [
    'objectIdentifier',
    'objectName',
    'objectType',
    'systemStatus',
    'vendorName',
    'vendorIdentifier',
    'modelName',
    'firmwareRevision',
    'applicationSoftwareVersion',
    'firmwareRevision',
    'protocolVersion',
    'ProtocolConformanceClass',
    'protocolServicesSupported',
    'protocolObjectTypesSupported',
    'objectList',
    'maxAPDULengthSupported',
    'numberOfAPDURetries',
    'segmentationSupported',
    'APDUTimeout',
    'deviceAddressBinding',

]

# point required property
requiredProperty = [
    'objectIdentifier',
    'objectName',
    'objectType',
    'presentValue',
    'statusFlags',
    'eventState',
    'outOfService',
    'units'
]

# point/device object types
objectType = ['analogInput', 'analogOutput', 'analogValue', 'binaryInput', 'binaryOutput', 'binaryValue', 'device']

objectTypeAsNum = {
    'analogInput': 0,
    'analogOutput': 1,
    'analogValue': 2,
    'binaryInput': 3,
    'binaryOutput': 4,
    'binaryValue': 5,
    'device': 8

}
