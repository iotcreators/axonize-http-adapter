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
from http.server import BaseHTTPRequestHandler

from HttpRequestHandler import HttpRequestHandler as reqHandler

import logging
log = logging.getLogger(__name__)

def splitString(str, sepChar):
    a = []
    for s in str.split(sepChar):
        a.append(s.strip())
    return a

def parseHttpHeader(s):
    d = {}
    for line in splitString(s.strip(), "\n"):
        idx = line.find(":")
        if idx > -1:
            key = line[0:idx].strip().lower()
            val = line[idx+1:].strip()
            d[key] = val

    return d

global REQUEST_COUNT
REQUEST_COUNT = 0

class RequestHandler(BaseHTTPRequestHandler):
    
    def returnWithError(self, statusCode, message):
        self.send_response(statusCode)
        self.send_header('Content-type', "application/json")
        self.end_headers()

        if not message:
            message = ""

        s = json.dumps({"message":message})
        log.error("Returning with error: %d %s" % (statusCode, s))

        self.wfile.write(s.encode("utf8"))
        log.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def returnOk(self):
        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()
        log.info("Returning with ok: %d" % (200))
        log.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return

    def do_POST(self):
        global REQUEST_COUNT

        try:        
            log.info("###########################################################################")

            # Incr and print request counter
            REQUEST_COUNT = REQUEST_COUNT + 1
            log.info("Request count: %d" % (REQUEST_COUNT))
            log.info("~~~")

            # Get the header fields from the request
            header = parseHttpHeader(str(self.headers))

            # Get the body from the request
            content_len = int(header["content-length"]) if "content-length" in header.keys() else 0
            sBody = self.rfile.read(content_len).decode("utf8") if content_len > 0 else ""
            sBody = sBody.strip()

            # Process the http request
            (code, msg) = reqHandler.doHandle(header, sBody)

            if code == 200:
                self.returnOk()
            else:
                self.returnWithError(code, msg)

        except Exception as ex:
            traceback.print_exc()           
            self.returnWithError(500, "Caught exception: %s" % (str(ex)))



class HttpServer(threading.Thread):
    
    def __init__(self, serviceName, port, cfg):
        threading.Thread.__init__(self)
        self._serviceName = serviceName 
        self._port = port
        self._cfg = cfg

    def run(self):        
        server = None
        
        try:
            server = HTTPServer(('', self._port), RequestHandler)
            log.info("Starting HTTP server on port %d for service %s" % (self._port, self._serviceName))
            server.serve_forever()
            
        except Exception as ex:
            print("Caught exception: %s" % (str(ex)))
            pass
        
        finally:
            if server is not None:
                server.socket.close()
        
            