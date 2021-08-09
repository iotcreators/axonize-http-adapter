
import json
from IoTCrMetrics import *

from decoders.nkewatteco.Decoding_Functions import *
from decoders.nkewatteco.Scroll_Decoding_Functions import *

'''
{
 "EndPoint": 0,
 "Report": "Standard",
 "CommandID": "ReportAttributes",
 "ClusterID": "SimpleMetering",
 "AttributeID": "CurrentMetering",
 "AttributeType": "ByteString",
 "Data": {
  "ActiveEnergy": 0,
  "ReactiveEnergy": 0,
  "NbMinutes": 237,
  "ActivePower": 0,
  "ReactivePower": 0
 },
 "Cause": []
}
'''

def decode(type, data):

    # In case the function is called testwise, return None
    if not data or len(data.strip()) == 0:
         return None

    d = json.loads(Decoding_JSON(data, False))

    if "Data" not in d.keys():
        return None
    else:
        d = d["Data"]

    values = {}
    
    for i in [["ActiveEnergy", MN_ACTIVE_ENERGY],
              ["ReactiveEnergy", MN_REACTIVE_ENERGY],
              ["CurrentPowerMode",MN_POWER_MODE],
              ["ActivePower", MN_ACTIVE_POWER],
              ["ReactivePower", MN_REACTIVE_POWER]]:

        if i[0] in d.keys():
            values[i[1]] = d[i[0]]            
   
    return values




    
