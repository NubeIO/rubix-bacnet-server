from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run

from bacpypes.basetypes import StatusFlags, PriorityArray

from bacpypes.app import BIPSimpleApplication
from bacpypes.object import register_object_type
from bacpypes.local.device import LocalDeviceObject
from bacpypes.local.object import BinaryOutputCmdObject

# some debugging
_debug = 0
_log = ModuleLogger(globals())

# register the classes
register_object_type(LocalDeviceObject, vendor_id=999)


@bacpypes_debugging
@register_object_type(vendor_id=999)
class BinaryOutputFeedbackObject(BinaryOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # listen for changes to the present value
        self._property_monitors["presentValue"].append(self.check_feedbacks)
        # self._property_monitors["presentValue"].append(self.check_feedbacks)

    def check_feedbacks(self, old_value, new_value):
        print(
            "check_feedback %r %r", old_value, new_value
        )
        print(12222, self._highest_priority_value())

        def highest_priority(iterable, default=None):
            if iterable:
                count = 0
                for item in iterable:
                    count += 1
                    if item.get('enumerated') == 0 or item.get('enumerated') == 1:
                        return {"item": item, "count": count}
            return default

        pnt_dict = self._dict_contents()
        priority_array = pnt_dict.get("priorityArray")
        priority_array = highest_priority(priority_array)
        print(priority_array)

        # event reporting, but it is here for illustration
        if new_value == self.presentValue:
            print(1111111)
            # self.eventState = "normal"
            # self.statusFlags["inAlarm"] = False
        else:
            print(222222)
            # self.eventState = "offnormal"
            # self.statusFlags["inAlarm"] = True


def main():
    global this_application

    # parse the command line arguments
    args = ConfigArgumentParser(description=__doc__).parse_args()

    print("initialization")

    print("    - args: %r", args)

    # make a device object
    this_device = LocalDeviceObject(ini=args.ini)
    print("    - this_device: %r", this_device)

    # make a sample application
    this_application = BIPSimpleApplication(this_device, args.ini.address)

    # make a commandable binary output object, add to the device
    boo1 = BinaryOutputFeedbackObject(
        objectIdentifier=("binaryOutput", 1),
        objectName="boo1",
        presentValue="inactive",
        eventState="normal",
        statusFlags=StatusFlags(),
        feedbackValue="inactive",
        relinquishDefault="inactive",
        priorityArray=PriorityArray(),
    )

    this_application.add_object(boo1)
    run()


if __name__ == "__main__":
    main()
