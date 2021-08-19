
from IoTCrMetrics import *

IOTCR_2_AXONIZE_MAP = {
    # Mapped from IoT Creators metrics model to Axonize model
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
    MN_PRESENCE        : ["Presence", 1026],

    # Standard Axonize event types without name mapping
    "KeepAlive" : ["KeepAlive", 1],
    "Power" : ["Power", 2],
    "Reset" : ["Reset", 3],
    "Hello" : ["Hello", 4],
    "Battery" : ["Battery", 5],
    "Charging" : ["Charging", 6],
    "Temperature" : ["Temperature", 7],
    "Humidity" : ["Humidity", 8],
    "Accelerometer" : ["Accelerometer", 9],
    "Light" : ["Light", 10],
    "Sound" : ["Sound", 11],
    "Gps2D" : ["Gps2D", 12],
    "Gps" : ["Gps", 13],
    "HeartRate" : ["HeartRate", 14],
    "Energy" : ["Energy", 15],
    "Activation" : ["Activation", 21],
    "pH" : ["pH", 22],
    "OXYGEN" : ["OXYGEN", 23],
    "TURBIDITY" : ["TURBIDITY", 24],
    "SALINITY" : ["SALINITY", 25],
    "INK" : ["INK", 26],
    "PRINTED" : ["PRINTED", 27],
    "PRINTEDMETHOD" : ["PRINTEDMETHOD", 28],
    "OPENCLOSE" : ["OPENCLOSE", 29],
    "DISCONNECT" : ["DISCONNECT", 30],
    "Speed" : ["Speed", 31],
    "Direction" : ["Direction", 32],
    "Distance" : ["Distance", 33],
    "Ignition" : ["Ignition", 34],
    "Odometer" : ["Odometer", 35],
    "TotalFuel" : ["TotalFuel", 36],
    "IdleFuel" : ["IdleFuel", 37],
    "OilPressure" : ["OilPressure", 38],
    "EngineRPM" : ["EngineRPM", 39],
    "CruiseTime" : ["CruiseTime", 40],
    "EngineIdle" : ["EngineIdle", 41],
    "FuelEconomy" : ["FuelEconomy", 42],
    "Error" : ["Error", 43],
    "Utilization" : ["Utilization", 44],
    "MultiDimensional" : ["MultiDimensional", 991],
    "CustomInstantaneous" : ["CustomInstantaneous", 993],
    "CustomList" : ["CustomList", 995],
    "CustomSum" : ["CustomSum", 996],
    "CustomAvg" : ["CustomAvg", 997],
    "CustomCount" : ["CustomCount", 998],
    "Custom" : ["Custom", 999],
    "Complex" : ["Complex", 777],
    "Angle" : ["Angle", 1000],
    "Pressure" : ["Pressure", 1001],
    "Soil temperature" : ["Soil temperature", 1002],
    "Soil moisture" : ["Soil moisture", 1003],
    "anemometer" : ["anemometer", 1004],
    "wind vane" : ["wind vane", 1005],
    "pluviometer" : ["pluviometer", 1006],
    "CO" : ["CO", 1007],
    "CO2" : ["CO2", 1008],
    "O2" : ["O2", 1009],
    "CH4" : ["CH4", 1010],
    "LPG" : ["LPG", 1011],
    "NH3" : ["NH3", 1012],
    "Air Pollutans" : ["Air Pollutans", 1013],
    "Solvent Vapors" : ["Solvent Vapors", 1014],
    "NO2" : ["NO2", 1015],
    "Ozone" : ["Ozone", 1016],
    "Hydrocarbons" : ["Hydrocarbons", 1017],
    "Pressure atmospheric" : ["Pressure atmospheric", 1018],
    "Pressure/Weight" : ["Pressure/Weight", 1019],
    "Bend" : ["Bend", 1020],
    "Vibration" : ["Vibration", 1021],
    "Hall Effect" : ["Hall Effect", 1022],
    "Liquid Presence" : ["Liquid Presence", 1023],
    "Liquid Level" : ["Liquid Level", 1024],
    "Luminosity" : ["Luminosity", 1025],
    "Presence" : ["Presence", 1026],
    "Stretch" : ["Stretch", 1027],
    "Microphone" : ["Microphone", 1028],
    "Crack detection gauge" : ["Crack detection gauge", 1029],
    "Crack propagation gauge" : ["Crack propagation gauge", 1030],
    "Linear Displacement" : ["Linear Displacement", 1031],
    "Dust" : ["Dust", 1032],
    "Ultrasound" : ["Ultrasound", 1033],
    "Magnetic Field" : ["Magnetic Field", 1034],
    "Parking Spot Status" : ["Parking Spot Status", 1035],
    "Air Temperature" : ["Air Temperature", 1036],
    "Air Humidity" : ["Air Humidity", 1037],
    "Soil Temperature" : ["Soil Temperature", 1038],
    "Soil Humidity" : ["Soil Humidity", 1039],
    "Leaf Wetness" : ["Leaf Wetness", 1040],
    "Solar Radiation" : ["Solar Radiation", 1041],
    "Ultraviolet Radiation" : ["Ultraviolet Radiation", 1042],
    "Trunk Diameter" : ["Trunk Diameter", 1043],
    "Stem Diameter" : ["Stem Diameter", 1044],
    "Fruit Diameter" : ["Fruit Diameter", 1045],
    "Anemometer" : ["Anemometer", 1046],
    "Wind Vane" : ["Wind Vane", 1047],
    "Watermark" : ["Watermark", 1048],
    "Dendrometer" : ["Dendrometer", 1049],
    "Vane" : ["Vane", 1050],
    "Pluviometer" : ["Pluviometer", 1051],
    "Geiger tube" : ["Geiger tube", 1052],
    "Current" : ["Current", 1053],
    "Water Consumption" : ["Water Consumption", 1054],
    "Load cell" : ["Load cell", 1055],
    "Distance foil" : ["Distance foil", 1056],
    "RSSI" : ["RSSI", 1057],
    "MAC Address" : ["MAC Address", 1058],
    "Network Address" : ["Network Address", 1059],
    "Network Identifier origin" : ["Network Identifier origin", 1060],
    "Date" : ["Date", 1061],
    "Time" : ["Time", 1062],
    "GMT" : ["GMT", 1063],
    "RAM" : ["RAM", 1064],
    "Internal temperature" : ["Internal temperature", 1065],
    "Millis" : ["Millis", 1066],
    "String" : ["String", 1067],
    "LDR" : ["LDR", 1068],
    "Light LUX" : ["Light LUX", 1069],
    "Mass Flow" : ["Mass Flow", 1070],
    "Gas" : ["Gas", 1071],
    "Water Flow" : ["Water Flow", 1072],
    "Availability" : ["Availability", 1073],
    "Health" : ["Health", 1074],
    "Logical Disk" : ["Logical Disk", 1075],
    "Network Adapter" : ["Network Adapter", 1076],
    "Operating System" : ["Operating System", 1077],
    "Motion" : ["Motion", 1078],
    "Pressure" : ["Pressure", 1079],
    "Movement" : ["Movement", 1080],
    "Door OpenClose" : ["Door OpenClose", 1081],
    "Flood" : ["Flood", 1082],
    "Counter" : ["Counter", 1083],
    "Zone" : ["Zone", 1084],
    "Battery OK" : ["Battery OK", 1085],
    "Supervision" : ["Supervision", 1086],
    "Tamper" : ["Tamper", 1087],
    "Tyco Temp Hot" : ["Tyco Temp Hot", 1088],
    "Tyco Temp Cold" : ["Tyco Temp Cold", 1089],
    "Tyco Temp Freezing" : ["Tyco Temp Freezing", 1090],
    "Tyco Temp Freezer" : ["Tyco Temp Freezer", 1091],
    "Gas OK" : ["Gas OK", 1092],
    "Fire OK" : ["Fire OK", 1093],
    "Lift" : ["Lift", 1094],
    "GarbageBin" : ["GarbageBin", 1095],
    "SoupLevel" : ["SoupLevel", 1096],
    "ToiletPapaer" : ["ToiletPapaer", 1097],
    "SolerEnergy" : ["SolerEnergy", 1098],
    "CameraAngle" : ["CameraAngle", 1099],
    "LastCleaned" : ["LastCleaned", 1100],
    "WiFiMB" : ["WiFiMB", 1101],
    "Hight" : ["Hight", 1102],
    "Panic Button" : ["Panic Button", 1103],
    "Impact" : ["Impact", 1104],
    "Occupancy" : ["Occupancy", 1105],
    "Voltage" : ["Voltage", 1106],
    "KiloWatt Power" : ["KiloWatt Power", 1107],
    "Load" : ["Load", 1108],
    "Efficiency" : ["Efficiency", 1109],
    "COP" : ["COP", 1110],
    "Steam Flow" : ["Steam Flow", 1111],
    "Compressor KPI" : ["Compressor KPI", 1112],
    "Savings" : ["Savings", 1113],
    "OnOff" : ["OnOff", 1114],
    "Gas Flow" : ["Gas Flow", 1115],
    "Air Flow" : ["Air Flow", 1116],
    "Volume" : ["Volume", 1117],
    "CO2 Alarm" : ["CO2 Alarm", 1118],
    "Alarm" : ["Alarm", 1119],
    "Tilt" : ["Tilt", 1120],
    "Sewage" : ["Sewage", 1121],
    "Leakage" : ["Leakage", 1122],
    "Rapid Flow" : ["Rapid Flow", 1123],
    "Reverse Flow" : ["Reverse Flow", 1124],
    "Broken Glass" : ["Broken Glass", 1125],
    "Threshold Capacity" : ["Threshold Capacity", 1126],
    "Accelerometer G" : ["Accelerometer G", 1127],
    "Irrigation Status" : ["Irrigation Status", 70029],
    "Water Conservation Percentage" : ["Water Conservation Percentage", 70030],
    "Percentage" : ["Percentage", 70031],
    "InternalRuleEngineProperties" : ["InternalRuleEngineProperties", 70000],
    "Wind Direction" : ["Wind Direction", 1128],
    "Water Degrees" : ["Water Degrees", 1129],
    "Wind Speed" : ["Wind Speed", 1130],
    "Rainfall" : ["Rainfall", 1131],
    "Power Factor" : ["Power Factor", 1132],
    "Picture Link" : ["Picture Link", 1133],
    "Bypass" : ["Bypass", 1134],
    "VOC" : ["VOC", 1135],
    "Cumulative Counter" : ["Cumulative Counter", 1136]
}
