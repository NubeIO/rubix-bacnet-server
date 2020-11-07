from flask_restful import Resource


def getCurrentMemoryUsage():
    """ Memory usage in kB """
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    return int(memusage.strip())


class GetSystemMem(Resource):
    def get(self):
        mem = getCurrentMemoryUsage()
        print(mem)
        return {'networks': mem}
