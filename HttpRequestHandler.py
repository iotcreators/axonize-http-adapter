import sys
import http.server
import traceback
import time
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import logging

from IoTDecoders import IoTDecoders as decoders
from IoTApplication import IoTApplication as appl
from NiAuthorizations import NiAuthorizations as auths

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

class HttpRequestHandler(BaseHTTPRequestHandler):

    def returnWithError(self, statusCode, message):
        self.send_response(statusCode)
        self.send_header('Content-type', "application/json")
        self.end_headers()

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

        try:        
            self.do_POST_Ex()

        except Exception as ex:
            traceback.print_exc()           
            self.returnWithError(500, "Caught exception: %s" % (str(ex)))

    def do_POST_Ex(self):
        log.info("###########################################################################")

        # Incr and print request counter
        global REQUEST_COUNT
        REQUEST_COUNT = REQUEST_COUNT + 1
        log.info("Request count: %d" % (REQUEST_COUNT))
        log.info("~~~")

        # Parse the header fields
        header = parseHttpHeader(str(self.headers))

        log.info("*** Header:")                
        for k in header.keys():
            log.info("%s:%s" % (k, header[k]))
        log.info("~~~")

        # Verify the authorization 
        # Expect an auth string of the form "<impact-tenant-name>:<username>:<password>" 
        # and verifies if it has been already successfully verified.

        if "authorization" not in header.keys():
            raise Exception("No Authorization header field defined.")

        a = splitString(header["authorization"], ":")

        if len(a) != 3:
            raise Exception("Authorization string has not valid format. Should be <tenantName>:<username>:<password>")

        if auths.requiresAuth(a[0], a[1]):
            log.info("... Authorizing %s:%s ..." % (a[0], a[1]))
            auths.doAuth(a[0], a[1], a[2])     
        else:
            log.info("%s:%s already authorized." % (a[0], a[1]))

        # Get the body and verify it
        
        content_len = int(header["content-length"]) if "content-length" in header.keys() else 0
        sBody = self.rfile.read(content_len).decode("utf8") if content_len > 0 else ""
        sBody = sBody.strip()

        log.info("*** Body:")
        log.info(str(sBody))
        log.info("~~~")
        
        if len(sBody) == 0:
            log.info("Body is empty.")
            return self.returnOk()

        '''
        {
            "reports":[{
               "serialNumber":"IMEI:866425033313638",
                "timestamp":1598887180734,
                "subscriptionId":"fa37d89c-a7e2-4f3d-b12f-6002a3642b4c",
                "resourcePath":"uplinkMsg/0/data",
                "value":"6920616d20616c697665",
                "customAttributes": {
                    "deviceType":"ELSYS ERS-CO2"
                }
            }],
            "registrations":[],
            "deregistrations":[],
            "updates":[],
            "expirations":[],
            "responses":[]
        }
        '''

        dBody = json.loads(sBody)
      
        # Get the application connection from the http header fields and the message
        applConn = appl.getConnectionFromHTTP(header, dBody)

        # Process all reports

        if "reports" not in dBody.keys() or len(dBody["reports"]) == 0:
            log.info("No reports in body.")
            return self.returnOk()

        # Process each report
        n = 0
        for report in dBody["reports"]:

            log.info("\n*** reports[%d]:\n%s\ņ~~~" % (n, json.dumps(report, sort_keys=False, indent=4)))
            n = n + 1 
            
            ###
            # Verify the value element
            if "value" not in report.keys() or report["value"] == None or len(report["value"]) == 0:
                log.error("No value element in report. Doing nothing.")
                continue

            ###
            # Determine the decoder which shall be used to decode the message
            decoderKey = None
            if "customAttributes" in report.keys() and "deviceType" in report["customAttributes"]:
                decoderKey = report["customAttributes"]["deviceType"].lower()


            ###
            # Call the decoder. If the key is not set or unknown the default decoder is called internally.
            decodedValues = decoders.decode(decoderKey, None, report["value"])

            if not decodedValues:
                log.error("No decoded values available.")
                continue

            decodedValues["Data"] = report["value"]

            log.info(json.dumps(decodedValues, sort_keys=False, indent=4))

            ###
            # Translate the decoded messages to the format of the receiving system
            applMsg = appl.transMsg2Appl(applConn, report, decodedValues)

            log.info(json.dumps(applMsg, sort_keys=False, indent=4))

            ###
            # Send the message to application
            appl.sendMsg2Appl(applConn, applMsg)

        return self.returnOk()    


