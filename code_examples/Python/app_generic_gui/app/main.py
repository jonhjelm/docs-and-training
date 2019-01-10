# !/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: main.py                                                         ##
##                                                                           ##
##                                                                           ##
## Author: Fraunhofer Institut fuer Graphische Datenverarbeitung (IGD)       ##
## Competence Center Interactive Engineering Technologies                    ##
## Fraunhoferstr. 5                                                          ##
## 64283 Darmstadt, Germany                                                  ##
##                                                                           ##
## Rights: Copyright (c) 2018 by Fraunhofer IGD.                             ##
## All rights reserved.                                                      ##
## Fraunhofer IGD provides this product without warranty of any kind         ##
## and shall not be liable for any damages caused by the use                 ##
## of this product.                                                          ##
##                                                                           ##
## ========================================================================= ##

import logging
import os

from flask import Flask
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter
from werkzeug.serving import run_simple

import sys
from sys import argv

from spyne.model.primitive import Unicode

additionalPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PythonTools'))
sys.path.append(additionalPath)

import htmlPageUtil as htmlUtl
import fileHelper as fh
import guiServiceBase as guiSrvc
import serviceBase as srvc
import util as utl
import serviceSetupUtil as srvcUtl

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s')

location = 'localhost'
port = 8080

logging.info('Reading pathes to configuration files')
pageConfigDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.environ['PAGE_CONFIG']))
xlsFileDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.environ['XLS_PARAM_SHEET']))

srvc.serviceURLPath = '/' + os.environ['SERVICE_NAME']

# Convert xls html page specification to dictionary
xlsDict = utl.xls2Dict(xlsFileDir)

logging.info('Constructing web page components from specified input parameters and layout')

# Save page footer, body and header in specified file names
htmlUtl.getPage(pageConfigDir, xlsDict, 'pageHeader.dat', 'pageBody.dat', 'pageFooter.dat')

logging.info('Instantiating GUI Application')

# Prepare GUI application for gui components
guiSrvc.return_type_tuple = tuple([Unicode] + srvcUtl.getTypesList(xlsDict))
guiSrvc.return_names_tuple = tuple(['status_base64'] + srvcUtl.getOutputNamesList(xlsDict))
guiSrvc.standard_vals_list = srvcUtl.getStandardValsList(xlsDict)

# Import GUI application and instantiate app
import GUIAppService as GUIApp

GUIApp.TNS = os.environ['TNS']

application = WsgiMounter({
    os.environ['SERVICE_NAME']: WsgiApplication(GUIApp.create_app())
})

if __name__ == '__main__':
    # Start the web service
    run_simple(location, int(port), application, use_reloader=False)
