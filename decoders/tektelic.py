
from IoTCrMetrics import *

def _tektelic_decode(data, startIdx):
        
    offset = 0
    rawValue = 0
    retValue = 0
    measType = data[startIdx:startIdx+2]
        
    if measType == "00":

        #Battery voltage: 00 ff 01 40
        #00 := Battery voltage
        #FF := Data type
        #01 40 := Value
        v = int(data[startIdx+4:startIdx+8], 16) * 0.01
        offset = 8;
        return (offset, MN_BATTERY_V, v)

    elif measType == "01":
        #Magnetic switch: 01 00 ff
        #01 := Reed switch
        #00 := Data type
        #FF := Value (0x00: Magnet present, 0xFF: Magnet absent)
        rawValue = int(data[startIdx+4:startIdx+6], 16)
        retValue = 0
        if rawValue > 0:
            retValue = 1
        offset = 6
        return (offset, MN_OPEN_CLOSE, retValue)

    elif measType == "03":
        #Temperature: 03 67 00 DF
        #03 := Temperature
        #67 := Data type
        #00 DF := Value
        rawValue = int(data[startIdx+4:startIdx+8], 16)
        retValue = rawValue * 0.1
        offset = 8;
        return (offset, MN_TEMPERATURE, retValue)

    elif measType == "04":
        #Relative humidity: 04 68 73
        #04 := Relative humidity
        #68 := Data type
        #73 := Value
        rawValue = int(data[startIdx+4:startIdx+6], 16)
        retValue = rawValue * 0.5
        offset = 6
        return (offset, MN_HUMIDITY, retValue)        

    elif measType == "08":
        #Reed switch count:  08 04 00 02
        #08 := Reed switch count
        #04 := Data type
        #00 02 := Value
        # Currently not supported. Just skip the bytes.
        offset = 8;
        return (offset, None, None)

    elif measType in ["0a", "0A"]:
        #Motion detected (PIR): 0a 00 ff
        #0a := Motion detected
        #00 := Data type
        #FF := Value
        rawValue = int(data[startIdx+4:startIdx+6], 16)
        retValue = 0
        if rawValue > 0:
            retValue = 1
        offset = 6
        
        return (offset, MN_OCCUPANCY, retValue)        

    elif measType in ["0d", "0D"]:
        #Motion count (PIR):0D 04 00 02
        #0D := Motion count
        #04 := Data type
        #00 02 := Value
        rawValue = int(data[startIdx+4:startIdx+8], 16)
        retValue = rawValue
        offset = 8
        return (offset, MN_MOTION_COUNT, retValue)        

    else:
        #this type of measurement is not yet defined
        #so we force the exit from the parse
        offset = len(data) + 1
        return (offset, None, None)

def decode(type, data):

    # In case the function is called testwise, return None
    if not data:
        return None
       
    currentIdx = 0
    d = {}

    while currentIdx < len(data): 
        l = _tektelic_decode(data, currentIdx)
        if not l:
            break

        offset = l[0]
        name = l[1]
        value = l[2]

        if name:
            d[name] = value

        currentIdx = currentIdx + offset

    return d