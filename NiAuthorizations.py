
import requests
import json
import base64
import time
import logging

log = logging.getLogger(__name__)

class _NiAuthorizations():

    def __init__(self):
        self._cfg = None
        self._appl = None
        self._auths = {}

    def init(self, cfg):
        if not self._cfg:
            self._cfg = cfg

    def _testInit(self):
        if not self._cfg:
            raise Exception("NiAuthorization not initialized.")

    def _buildNokiaImpactAuthHeaderString(self, username, password):
        s = "%s:%s" % (username, password)
        return base64.b64encode(s.encode("utf-8")).decode('utf-8')

    def _buildIndexKey(self, tenantName, username):
        return "%s_%s" % (tenantName, username)

    def requiresAuth(self, tenantName, username):
        self._testInit()

        key = self._buildIndexKey(tenantName, username)

        # If we don't have a cached auth for tenantName and username 
        # a authorization is required.
        if key not in self._auths.keys():
            return True

        # Test if the authorization is still valid

        auth = self._auths[key]
        now = time.time()
        
        if now - auth["timestamp"] > self._cfg["authValidSecs"]:
            return True
        
        #  We reach this point if we have a valid authorization
        return False


    def doAuth(self, tenantName, username, password):
        self._testInit()

        indexKey = self._buildIndexKey(tenantName, username)

        # Try to get the profile of the user

        url = "https://%s:%d/rest/me" % (self._cfg["niApiHost"], self._cfg["niApiPort"])
        log.debug("URL: %s" % (url))

        headers = {}    
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Basic %s" % self._buildNokiaImpactAuthHeaderString(username, password)

        log.debug("HEADERS: %s" % (str(headers)))

        response = requests.get(url, headers=headers)
        
        if not response.ok:
            response.raise_for_status()

        self._auths[indexKey] = {
            "timestamp":int(time.time())
        }

# Public singelton instance 
NiAuthorizations = _NiAuthorizations()

