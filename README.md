# axonize-http-adapter
Axonize HTTP adapter for IoT Creators (iotcrators.com) is a simple HTTP server which URL can be registered as application URL in the projects of the IoT Creators portal.
The HTTP adapter implements the following main functions
- Decode device specific sensor data into the Axonize format.
- Forward the decoded messages to your Axonize tenant.

###
# How to start the HTTP server
To start the HTTP server change into the root directory `axonize-http-adapter` and execute the script `main.py`.

###
# How to register axonize-http-adapter as application URL in IoT Creators portal
Within your project in IoT Creators portal define the URL of your `axonize-http-adapter` web server as **CALLBACK URL** and configure the following header fields.

###Authorization
Authorization token of the IoT Creators project to which you assign `axonize-http-adapter` as **CALLBACK URL**. 
The format of the Authorization header field is:
```
Authorization: <GROUP_NAME>:<API USERNAME>:<API USER PASSWORD>
```

###
# How to add sensor decodings
To add a new messages decoder to the adapter perform the following steps
1. Create a Python file in the directory axonize-http-adapter/decoders.
2. Add the function "def decode(type, data)" to the Python file.
3. If your decoder introduces new metrics declar them in the file IoTCrMetrics and extend the Axonize mapping in the file applications/Axonize.py.
- Register your decoder in the configuration file "CONFIG.py" with a symbolic name.

###
# Infos to current integrated sensor decoders
###
## Efento CoAP NB-IoT sensors
See `decoders/efento/efento.py`.
###
## Elsys LoRaWAN sensors
See `decoders/elsys.py`.
###
## IMBUILDING NB-IoT sensors
See `decoders/imbuilding.py`.
###
## TekTelic LoRaWAN sensors
See `decoders/tektelic.py`.
###
## nke WATTECO LoRaWAN Smart Plug
See `decoders/nkewatteco/nkewatteco.py`.
To install required python packages perform:
```
pip3 install dicttoxml
pip3 install construct==2.8.12
```


