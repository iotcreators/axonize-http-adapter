
from IoTCrMetrics import *

import decoders.efento.proto_measurements_pb2 as proto_measurements_pb2
from google.protobuf.json_format import MessageToDict

import logging
log = logging.getLogger(__name__)

def decode(type, data):

    # In case the function is called testwise, return None
    if not data:
        return None

    d = {}
    
    d1 = MessageToDict(proto_measurements_pb2.ProtoMeasurements.FromString(bytes.fromhex(data)))

    if "channels" not in d1.keys():
        return None

    channelIdx = 0

    for e in d1["channels"]:
        if "type" not  in e.keys():
            continue

        # Log channel data
        for k in e.keys():
            log.info("Channel[%d][%s] = %s" % (channelIdx, k, str(e[k])))
        log.info("")
        channelIdx = channelIdx + 1 

        if e["type"] == "MEASUREMENT_TYPE_TEMPERATURE":
            d[MN_TEMPERATURE] = e["startPoint"] / 10.

        elif e["type"] == "MEASUREMENT_TYPE_HUMIDITY":
            d[MN_HUMIDITY] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_ATMOSPHERIC_PRESSURE":
            d["AtmosphericPressure"] = e["startPoint"] / 10.

        elif e["type"] == "MEASUREMENT_TYPE_DIFFERENTIAL_PRESSURE":
            d["DifferentialPressure"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_OK_ALARM":
            
            '''
            type          = MEASUREMENT_TYPE_OK_ALARM
            timestamp     = 1628585145
            sampleOffsets = [-1, 6, 81]
            '''
            d["OkAlarm"] = e["sampleOffsets"][0]

        elif e["type"] == "MEASUREMENT_TYPE_IAQ":
            d["IndoorAirQuality"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_FLOODING":
            d["Flooding"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_PULSE_CNT":
            d["PulseCount"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_ELECTRICITY_METER":
            d["ElectricityMeter"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_WATER_METER":
            d["WaterMeter"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_SOIL_MOISTURE":
            d["SoilMoisture"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_CO_GAS":
            d["CO"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_NO2_GAS":
            d["NO2"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_H2S_GAS":
            d["H2S"] = e["startPoint"] / 100.

        elif e["type"] == "MEASUREMENT_TYPE_AMBIENT_LIGHT":
            d["AmbientLight"] = e["startPoint"] / 10.

        elif e["type"] == "MEASUREMENT_TYPE_PM_1_0":
            d["MassConcentrationPM_1_0mu"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_PM_2_5":
            d["MassConcentrationPM_2_5mu"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_PM_10_0":
            d["MassConcentrationPM_10_0mu"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_NOISE_LEVEL":
            d["NoiseLevel"] = e["startPoint"] / 10.

        elif e["type"] == "MEASUREMENT_TYPE_NH3_GAS":
            d["NH3"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_CH4_GAS":
            d["CH4"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_HIGH_PRESSURE":
            d["HighPressure"] = e["startPoint"]

        elif e["type"] == "MEASUREMENT_TYPE_DISTANCE_MM":
            d["Distance"] = e["startPoint"]

    
    return d




    
