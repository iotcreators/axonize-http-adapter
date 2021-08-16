#!/usr/bin/env python3
import sys
import os
import time
import argparse
import traceback
import logging

import utils

from HttpServer import HttpServer
from IoTDecoders import IoTDecoders as decoders
from IoTApplication import IoTApplication as application
from NiAuthorizations import NiAuthorizations as auths

log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.debug("*** START ***")

    cmdlineParser = argparse.ArgumentParser(prog="app.py", description="Programs main entry point.")

    cmdlineParser.add_argument("-config", metavar='<config>', default="./CONFIG.py",
                               help="Python file which contains the configuration.")

    cmdlineParser.add_argument("-loglevel", metavar='<loglevel>', 
                               choices = ["INFO", "WARN", "DEBUG"], default="INFO",
                               help="Log level.Possible values  are INFO, WARN, DEBUG.")

    ns = cmdlineParser.parse_args()
    
    if ns.loglevel is not None:
        logging.basicConfig(force=True, level=ns.loglevel, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")                                

    # Debug the command line options
    for e in dir(ns):
        if not e.startswith("_"):
            log.debug("%-20s = %s" % (e, str(getattr(ns, e))))

    try:

        # Load configuration
        CFG = utils.loadConfig(ns.config)

        # Initialize the application
        application.init(CFG.ApplicationCfg)

        # Initialize the decoder
        decoders.init(CFG.DecoderCfg)

        # Initialize the authorizations
        auths.init(CFG.ScsAuthorizationsCfg)

        # Start the http server
        httpServer = HttpServer(CFG.ServiceName, CFG.HttpServerCfg["port"], CFG.HttpServerCfg)
        httpServer.start()

        # Sleep this thread and let the container restart it 
        if CFG.ExitAfterSecs > 0:
            time.sleep(CFG.ExitAfterSecs)
            os._exit(0)
       
    except Exception as ex:
        print("ERROR: %s" % (str(ex)))
        traceback.print_exc()

