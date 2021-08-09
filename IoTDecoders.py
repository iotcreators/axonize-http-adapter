import importlib
import logging

log = logging.getLogger(__name__)

global _DECODERS
_DECODERS = None

def init(cfg):
    global _DECODERS
    _DECODERS = _IoTDecoders(cfg)

def getDecoders():
    global _DECODERS
    return _DECODERS

class _IoTDecoders():
    
    def __init__(self, cfg):
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

    def decode(self, key, type, data):
        if key not in self._cfg["decoders"].keys():
            raise Exception("No decoder for >%s< available." % (key))

        # Get the  decoder and call it
        module = self._cfg["decoders"][key]["pymodule"]
        return module.decode(type, data)
