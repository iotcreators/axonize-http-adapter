import sys
import http.server
import traceback
import time
import json
import requests
from datetime import datetime
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

class _HttpRequestHandler():

    def doHandle(self, header, sBody):

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

        # Verify the body

        log.info("*** Body:")
        log.info(str(sBody))
        log.info("~~~")
        
        if len(sBody) == 0:
            log.info("Body is empty.")
            return (200, None)

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
            return (200, "No reports in body.")

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

        return (200, None)


# Public singelton instance 
HttpRequestHandler = _HttpRequestHandler()


