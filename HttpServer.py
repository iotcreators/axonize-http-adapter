#####################################################################
# Copyright (c) 2019 T-Systems International GmbH                   #
# All rights reserved                                               #
#####################################################################
import http.server
import threading
import traceback
import time
import json
import requests
from datetime import datetime

from http.server import HTTPServer

from HttpRequestHandler import HttpRequestHandler

import logging
log = logging.getLogger(__name__)

class HttpServer(threading.Thread):
    
    def __init__(self, serviceName, port, cfg):
        threading.Thread.__init__(self)
        self._serviceName = serviceName 
        self._port = port
        self._cfg = cfg

    def run(self):        
        server = None
        
        try:
            server = HTTPServer(('', self._port), HttpRequestHandler)
            log.info("Starting HTTP server on port %d for service %s" % (self._port, self._serviceName))
            server.serve_forever()
            
        except Exception as ex:
            print("Caught exception: %s" % (str(ex)))
            pass
        
        finally:
            if server is not None:
                server.socket.close()
        
            