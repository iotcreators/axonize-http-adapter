
from IoTCrMetrics import *

def _decode(type, data, startIndex):
    offset = 0
    rawValue = 0
    endIndex = startIndex + 2
    measType = data[startIndex:endIndex]  #take the first 2 hex chars as type of measurement

    if measType == "01": # Temperature
        s = data[endIndex:endIndex+4]
        v = int(s, 16) / 10.0
        offset = 6
        return (offset, MN_TEMPERATURE, v)

    elif measType == "02": # Humidity
        s = data[endIndex:endIndex+2]
        v = int(s, 16)
        offset = 4
        return (offset, MN_HUMIDITY, v)

    elif measType == "03": # Acceleration
        s = data[endIndex:endIndex+6]
        v = int(s, 16)
        offset = 8
        return (offset, MN_ACCELERATION, v)

    elif measType == "04": # Light LUX
        s = data[endIndex:endIndex+4]
        v = int(s, 16)
        offset = 6
        return (offset, MN_LIGHT_LUX, v)

    elif measType == "05": # Motion Counter
        s = data[endIndex:endIndex+2]
        v = int(s, 16)
        offset = 4
        return (offset, MN_MOTION_COUNT, v)

    elif measType == "06": # CO2
        s = data[endIndex:endIndex+4]
        v = int(s, 16)
        offset = 6
        return (offset, MN_CO2, v)

    elif measType == "07": # Battery in mV
        s = data[endIndex:endIndex+4]
        v = int(s, 16) / 1000.
        offset = 6
        return (offset, MN_BATTERY_V, v)

    elif measType == "11": # Occupancy
        s = data[endIndex:endIndex+2]
        v = int(s, 16)
        offset = 4
        return (offset, MN_OCCUPANCY, v)

    elif measType.lower() == "Ob": # Pulse ABS used for Open Count
        s = data[endIndex:endIndex+8]
        v = int(s, 16)
        offset = 10
        return (offset, MN_OPEN_COUNT, v)

    elif measType == "17": # Pulse ABS used for Close Count
        s = data[endIndex:endIndex+8]
        v = int(s, 16)
        offset = 10
        return (offset, MN_CLOSE_COUNT, v)

    elif measType.lower() == "Od": # OpenClose, 0:=Open, 1:=Close
        s = data[endIndex:endIndex+2]
        v = int(s, 16)
        offset = 4
        return (offset, MN_OPEN_CLOSE, v)

    elif measType.lower() in ["12", "0f"]: # Ignore some 
        offset = 4
        return (offset, None, None)

    else:
        return None

def decode(type, data):
    
    # In case the function is called testwise, return None
    if not data:
        return None
    
    currentIndex = 0

    d = {}

    while currentIndex < len(data): 
        l = _decode(type, data, currentIndex)
        if not l:
            break

        offset = l[0]
        name = l[1]
        value = l[2]

        if name:
            d[name] = value

        currentIndex = currentIndex + offset

    return d