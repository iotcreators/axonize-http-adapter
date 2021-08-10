
print("Using configuration CONFIG.py ...")

ServiceName = "axonize-http-adapter-for-iotcreators"

# In case we run the service in managed cluster such as kubernetes we can kill
# the service to keep it clean by re-initialization.
# If you want to disable auto-termination set ExitAfterSecs=0
ExitAfterSecs = 60 * 60 * 24

HttpServerCfg = {
    "port" : 8080
}

ApplicationCfg = {
    "pyfile":"./applications/Axonize.py"
}

DecoderCfg = {
    "decoders" : {
        "elsys ers co2"      : {"pyfile":"./decoders/elsys.py"},
        "efento"             : {"pyfile":"./decoders/efento/efento.py"},
        "tektelic smartroom" : {"pyfile":"./decoders/tektelic.py"},
        "nke smartplug"      : {"pyfile":"./decoders/nkewatteco/nkewatteco.py"},
        "imbuilding co2"     : {"pyfile":"./decoders/imbuilding.py"}
    }
}

