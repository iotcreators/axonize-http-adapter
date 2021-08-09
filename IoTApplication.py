import importlib
import logging

log = logging.getLogger(__name__)

global _APPL
_APPL = None

def init(cfg):
    global _APPL
    _APPL = _IoTApplication(cfg)

def getApplication():
    global _APPL
    return _APPL

class _IoTApplication():

    def __init__(self, cfg):
        self._cfg = cfg
        self._appl = None

        # Load the application implementation
        log.info("Loading application implementation from %s..." % (cfg["pyfile"]))

        spec = importlib.util.spec_from_file_location("application", cfg["pyfile"])
        self._appl = importlib.util.module_from_spec(spec)
        spec = spec.loader.exec_module(self._appl)

    def getConnectionFromHTTP(self, httpHeaders, httpBody):
        '''
        Builds the connection object to the application from the passed
        HTTP header fields and body.a
        '''
        return self._appl.getConnectionFromHTTP(httpHeaders, httpBody)

    def transMsg2Appl(self, conn, report, decodedValues):
        '''
        Transforms the data messages from the internal and decoded
        IoT Creators format into the format of the target IoT application.
        '''
        return self._appl.transMsg2Appl(conn, report, decodedValues)

    def sendMsg2Appl(self, conn, applMsg):     
        '''
        Sends the message to the application
        '''
        return self._appl.sendMsg2Appl(conn, applMsg)
