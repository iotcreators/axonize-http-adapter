
from IoTCrMetrics import *

# Default decode which just stores the data

def decode(type, data):

    # In case the function is called testwise, return None
    if not data:
        return None


    d = {
        MN_DATA : data
    }

    return d