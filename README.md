# axonize-http-adapter
Axonize HTTP adapter for IoT Creators (iotcrators.com) is a simple HTTP server which URL can be registered as application URL in the projects of the IoT Creators portal.
The HTTP adapter implements the following main functions
- Decode device specific sensor data into the Axonize format.
- Forward the decoded messages to your Axonize tenant.

# How to start the HTTP server
To start the HTTP server change into the root directory axonize-http-adapter and execute the script main.py.

# How to add sensor decodings
To add a new messages decoder to the adapter perform the following steps
- Create a Python file in the directory axonize-http-adapter/decoders.
- Add the function "def decode(type, data)" to the Python file.
- Register your decoder in the configuration file "CONFIG.py" with a symbolic name.

