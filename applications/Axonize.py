import requests
import json
from datetime import datetime
import time
import logging
from IoTCrMetrics import *

log = logging.getLogger(__name__)

# Names of http header fields
CFG_AXO_IOTHUBURL   = "axo-iothub-url"
CFG_AXO_GWDEVID     = "axo-gateway-device-id"
CFG_AXO_GWDEVSASTOK = "axo-gateway-sas-token"
CFG_AXO_APPID       = "axo-gateway-app-id"

IOTCR_2_AXONIZE_MAP = {
    MN_DATA            : ["Data", 43],
    MN_TEMPERATURE     : ["Temperature", 7],
    MN_HUMIDITY        : ["Humidity", 8],
    MN_ACCELERATION    : ["Acceleration", 9],
    MN_LIGHT_LUX       : ["Light LUX", 1069],
    MN_MOTION_COUNT    : ["Motion Counter", 997],
    MN_CO2             : ["CO2", 1008],
    MN_BATTERY_V       : ["Battery Volt", 5],
    MN_OCCUPANCY       : ["Occupancy", 998],
    MN_OPEN_COUNT      : ["Open Count", 996],
    MN_CLOSE_COUNT     : ["Close Count", 996],
    MN_OPEN_CLOSE      : ["Open Close", 1022],
    MN_ACTIVE_ENERGY   : ["ActiveEnergy", 15],
    MN_REACTIVE_ENERGY : ["ReactiveEnergy", 15],    
    MN_ACTIVE_POWER    : ["ActivePower", 15],
    MN_REACTIVE_POWER  : ["ReactivePower", 15],
    MN_COUNTER_A       : ["Count A", 1083],
    MN_COUNTER_B       : ["Count B", 1083],
    MN_RSSI_LEVEL      : ["RSSI Level", 1057],
    MN_PRESENCE        : ["Presence", 1026]
}

#('Batterypercentage', 5, batteryLevel));
#('Differential Open Count', 996, rawValue));
#('Differential Close Count', 996, rawValue));

def getConnectionFromHTTP(httpHeaders, httpBody):
    conn = {}

    # Verify if all required fields are present and build
    # the connnection disctionary

    for key in [CFG_AXO_IOTHUBURL, 
                CFG_AXO_GWDEVID, 
                CFG_AXO_GWDEVSASTOK, 
                CFG_AXO_APPID]:

        if not key in httpHeaders.keys():
            raise Exception("Configuration field %s not found." % (key))
        else:
            conn[key] = httpHeaders[key]

    return conn


'''
IoT Creators Messages:
{
    "serialNumber":"IMEI:866425033313638",
    "timestamp":1598887180734,
    "subscriptionId":"fa37d89c-a7e2-4f3d-b12f-6002a3642b4c",
    "resourcePath":"uplinkMsg/0/data",
    "value":"6920616d20616c697665",
    "customAttributes": {
        "deviceType":"ELSYS ERS-CO2"
    }
}

Axonize Message:
{
    "custom_id" : "IMEI:357518080195142",
    "app_id":"f74b005a-cda3-4b52-ac7e-1afdb27aceac",
    "dateTime":"2021-08-04T15:40:01Z",
    "type":991,
    "value":[
        {
            "type":1008,
            "value":1002,
            "name":"CO2"
        }    
    ]
}
'''
def transMsg2Appl(axoConn, report, decodedValues):

    if "timestamp" not in report.keys():
        report["timestamp"] = int(time.time()) * 1000

    # Convert the timestamp into ISO format stringp
    tsSecs = int(report["timestamp"]) / 1000
    tsDate = datetime.fromtimestamp(tsSecs)
    dateTime = tsDate.strftime("%Y-%m-%dT%H:%M:%S")        

    # Convert serial number
    customId = report["serialNumber"]
    if customId.startswith("IMEI:"):
        customId = customId[5:]

    # Translate decoded data model and values into the axo 
    values = []
    for decodedName in decodedValues.keys():
        if decodedName in IOTCR_2_AXONIZE_MAP.keys():
            a = IOTCR_2_AXONIZE_MAP[decodedName]
            axoName = a[0]
            axoCode = a[1]
            axoValue = decodedValues[decodedName]
            values.append({
                "type"  : axoCode,
                "value" : axoValue,
                "name"  : axoName})

    # Build the axo messages and return it
    axoMsg = {
        "custom_id" : customId,
        "app_id"    : axoConn[CFG_AXO_APPID],
        "dateTime"  : dateTime,
        "type"      : 991,        
        "value"     : values
    }

    return axoMsg

def sendMsg2Appl(axoConn, axoMsg):

    #https://prod-iot-axonize.azure-devices.net/devices/60feea857876a71148540f6f/messages/events?api-version=2018-04-01    

    url = "https://%s/devices/%s/messages/events?api-version=2018-04-01" % (
        axoConn[CFG_AXO_IOTHUBURL],str(axoConn[CFG_AXO_GWDEVID]))

    log.debug("POST %s" % (url))

    headers = {}    
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Authorization"] = axoConn[CFG_AXO_GWDEVSASTOK]

    log.debug("HEADERS: %s" % (str(headers)))

    log.debug("BODY: %s" % (str(axoMsg)))
    
    response = requests.post(url, headers=headers, data=json.dumps(axoMsg))
    
    if not response.ok:
        log.error(response.content)
        response.raise_for_status()

    print(response.content)


