import logging
from IoTCrMetrics import *

log = logging.getLogger(__name__)

# North:  ./decode.py 0401110100050207000000
# Eeast:  ./decode.py 0401220200050209000000
# South:  ./decode.py 040144030005020a000000
# West:   ./decode.py 040188040005020c000000
# Center: ./decode.py 0401aa050005020e000000
# Center: ./decode.py 0401a20600050212000000
# N, W:   ./decode.py 0401980700050214000000

FIRSTCLICK_MASK = 1 + 2 + 4 + 8
ALLCLICK_MASK   = 16 + 32 + 64 + 128 
NORTHCLICK_MASK = 1
EASTCLICK_MASK  = 2
SOUTHCLICK_MASK = 4
WESTCLICK_MASK  = 8

def decode(deviceType, hexString):
    
    # In case the function is called testwise, return None
    if not hexString:
        return None

    d = {}

    hexData = bytearray.fromhex(hexString)

    L = int(hexData[0])  # Length
    T = int(hexData[1])  # Type

    # Button pushed
    if L == 4 and T == 1:
        bits = int(hexData[2]) # BitMask

        if (NORTHCLICK_MASK & bits) > 0:
            d[MN_FIRST_CLICK] = MV_NORTH
        elif (EASTCLICK_MASK & bits) > 0:
            d[MN_FIRST_CLICK] = MV_EAST
        elif (SOUTHCLICK_MASK & bits) > 0:
            d[MN_FIRST_CLICK] = MV_SOUTH
        elif (WESTCLICK_MASK & bits) > 0:
            d[MN_FIRST_CLICK] = MV_WEST

        # Determin which of buttons have been clicked els
        bits = (bits & ALLCLICK_MASK) >> 4
        
        for (mask, key) in [(NORTHCLICK_MASK, MN_NORTH_CLICK),
                            (EASTCLICK_MASK,  MN_EAST_CLICK),
                            (SOUTHCLICK_MASK, MN_SOUTH_CLICK),
                            (WESTCLICK_MASK,  MN_WEST_CLICK)]:
            if (mask & bits) > 0:
                d[key] = True
            else:
                d[key] = False

    else:
        log.error("Unknown event type.")

    return d