#####################################################################
# Copyright (c) 2018 T-Systems International GmbH                   #
# All rights reserved                                               #
#                                                                   #
# Licensed under the MIT license. See LICENSE file in the project   # 
# root for full license information.                                #
#####################################################################
import importlib
import imp
import os
import sys

import logging
log = logging.getLogger(__name__)

def importModule(moduleName, moduleFile):
    """
    Imports a module from source code and returns the exected module
    @param moduleName Name of the module
    @param moduleFile File of the source code
    @return Excecuted module is returned 
    @throws Exception in case of an error
    """
    log.debug("=> importModule(moduleName=%s, moduleFile=%s)" % (moduleName, moduleFile))

    # Python 2.7
    #module = imp.load_source(moduleName, moduleFile)

    # Python 3.5
    spec = importlib.util.spec_from_file_location(moduleName, moduleFile)
    module = importlib.util.module_from_spec(spec)
    spec = spec.loader.exec_module(module)
    
    log.debug("<=")
    return module

def loadConfig(configFile = None):
    log.debug("=> loadConfig(%s)" % (str(configFile)))
    
    # If no configuration has been passed, test if a configuration file is
    # referenced by the environment
    if not configFile:
        raise Exception("No configuration file has been defined.")
        
    elif not os.path.exists(configFile):
        raise Exception("Configuration file %s does not exist." % (configFile))
    
    log.debug("importModule(\"CFG\", %s) ..." % (configFile))
    return importModule("CFG", configFile)

