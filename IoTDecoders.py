import importlib
import logging

log = logging.getLogger(__name__)

class _IoTDecoders():

    def __init__(self):
        self._cfg = None
        self._decoders = None
    
    def init(self, cfg):
        self._cfg = cfg
        self._decoders = cfg["decoders"]

        log.info("Loading decoders ...")
        for key in cfg["decoders"]:
            d = cfg["decoders"][key]
            pyfile = d["pyfile"]
        
            log.info("  loading %s from %s ..." % (key, pyfile))        
            spec = importlib.util.spec_from_file_location(key, pyfile)
            module = importlib.util.module_from_spec(spec)
            spec = spec.loader.exec_module(module)

            log.info("  testing decoder ...")
            module.decode(None, None)

            d["pymodule"] = module

        log.info("Loading default decoder ...")
        spec = importlib.util.spec_from_file_location("defaultDecoder", cfg["defaultDecoder"]["pyfile"])
        module = importlib.util.module_from_spec(spec)
        spec = spec.loader.exec_module(module)

        log.info("  testing decoder ...")
        module.decode(None, None)

        cfg["defaultDecoder"]["pymodule"] = module

    def decode(self, key, type, data):

        if not key:
            log.warn("No decoder defined in messages. Using default decoder.")
            module = self._cfg["defaultDecoder"]["pymodule"]

        elif key not in self._cfg["decoders"].keys():
            log.warn("unknown deocder %s. Using default decoder ...")
            module = self._cfg["defaultDecoder"]["pymodule"]

        else:
            # Get the  decoder and call it
            module = self._cfg["decoders"][key]["pymodule"]
        
        return module.decode(type, data)

# Public singelton instance
IoTDecoders = _IoTDecoders()