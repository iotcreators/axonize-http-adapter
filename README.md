# axonize-http-adapter
Axonize HTTP adapter for IoT Creators (iotcrators.com) is a simple HTTP server which URL can be registered as application URL in the projects of the IoT Creators portal.
The HTTP adapter implements the following main functions
- Decode device specific sensor data into the Axonize format.
- Forward the decoded messages to your Axonize tenant.

###
# Prepare Axonize to integrate with IoT Creators
Perform the following steps to prepare Axonize to integrate with IoT Creators via `axonize-http-adapter`:
1. In your Axonize tenant create a new product template with the name **IoT Creators Gateway**. Enable **Developer Mode** in the product template. Beside this you don't need to configure more.
2. In your Axonize tenant create a new device of product type **IoT Creators Gateway** with a name of your choice. 
3. In your new created device of type "IoT Creators Gateway" generate a **SAS token** which you will use to forward messages from `axonize-http-adapter` to Axonize.
###
# How to start the HTTP server
To start the HTTP server change into the root directory `axonize-http-adapter` and execute the script `main.py`.

###
# How to register axonize-http-adapter to IoT Creators
Within your project in IoT Creators portal define the URL of your `axonize-http-adapter` web server as **CALLBACK URL** and configure the following header fields.
###
```
axo-gateway-device-id: 60feea857871148540f6f
axo-gateway-sas-token: SharedAccessSignature sr=stg-ottokar.azure-devices.net%2Fdevices%2F60feea857876a71148540f6f&sig=ck6iv9dAZdUhEVjY4ZJ8wn2ZcYc54%3D&se=1654001125
axo-gateway-app-id: f74b005a-cda3-ac52-acbe-2fdb27aceac
Authorization: CON_0000048455:API_CON_0000048455_564442:XnHXa1+B+37hhs9o53.566
```
###
#### Authorization
Authorization token of the IoT Creators project to which you assign `axonize-http-adapter` as **CALLBACK URL**. 
The format of the Authorization header field is:
```
Authorization: <GROUP_NAME>:<API USERNAME>:<API USER PASSWORD>
```
###
#### axo-iothub-url
Azure IoT Hub url of your Axonize tenant. Before you enabled the **Developer Mode** of your product template **IoT Creators Gateway** you can find IoT Hub url in the connect string of your previously created "IoT Creator Gateway" device in Axonize.
```
axo-iothub-url: stg-ottokar.azure-devices.net
```
###
#### axo-gateway-device-id
Device id of your "IoT Creators Gateway" device. Before you enabled the **Developer Mode** of your product template **IoT Creators Gateway** you can find deviceId of your previously created "IoT Creator Gateway" device in Axonize.
```
axo-gateway-device-id: 60feea857876a711bac40f6f
```
###
#### axo-gateway-app-id
App id of your "IoT Creators Gateway" device. Before you enabled the **Developer Mode** of your product template **IoT Creators Gateway** you can find the appId of your previously created "IoT Creator Gateway" device in Axonize.
```
axo-gateway-app-id: f74b005a-baa3-4c52-ac7e-1afdb27aceac
```
###
#### axo-gateway-sas-token
SAS token of your "IoT Creators Gateway" device. Before you enabled the **Developer Mode** of your product template **IoT Creators Gateway** you can find and create the SAS token for your previously created "IoT Creator Gateway" device in Axonize.
```
axo-gateway-sas-token: SharedAccessSignature sr=stg-ottokar.azure-devices.net%2Fdevices%2F60feea857876a71148540&sig=ck6iv9dAZbkfg2eL2SWQjIhEVjY4ZJ8wn2ZcYc54%3D&se=1654001125
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


