import logging
from IoTCrMetrics import *

log = logging.getLogger(__name__)

def decode(deviceType, data):

    # In case the function is called testwise, return None
    if not data:
        return None

    a = bytearray.fromhex(data)
    type = a[0]
    version = a[1]

    d = None
 
    if type == 1 and version == 1:
        d = {
            MN_DATA          : data,
            MN_DEVICE_STATUS : a[8],
            MN_BATTERY_V     : int.from_bytes(a[9:11], "big") / 100.,
            MN_TEMPERATURE   : int.from_bytes(a[12:14], "big") / 100.,
            MN_HUMIDITY      : int.from_bytes(a[14:16], "big") / 100.,
            MN_CO2           : int.from_bytes(a[16:18], "big"),
            MN_PRESENCE      : 1 if a[18] > 0 else 0
        }
        
    elif type == 2 and version == 4:
        d = {
            MN_DATA          : data,
            MN_DEVICE_STATUS : a[8],
            MN_BATTERY_V     : int.from_bytes(a[9:11], "big") / 100.,
            MN_COUNTER_A     : int.from_bytes(a[12:14], "big"),
            MN_COUNTER_B     : int.from_bytes(a[14:16], "big")
        }

    elif type == 2 and version == 6:

        d = {
            MN_DEVICE_STATUS: a[10]
        }

        c = int.from_bytes(a[13:15], "big")
        if c > 0:
            d[MN_COUNTER_A] = c

        c = int.from_bytes(a[15:17], "big")
        if c > 0:
            d[MN_COUNTER_B] = c

    else:
        log.warn("Unsupported type %d and version %d" % (type, version))

        d = {
            MN_DATA : data
        }

    return d

