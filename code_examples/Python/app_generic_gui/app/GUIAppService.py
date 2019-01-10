#!/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: GUIAppService.py                                                ##
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
import base64
import time
from spyne import Application, srpc, ServiceBase, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode
from spyne.model.primitive import Integer

import os
import sys

additionalPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PythonTools'))
sys.path.append(additionalPath)

import sessionHelper as sh
import fileHelper as fh
import util as utl
import guiServiceBase as guiSrvc
import serviceBase as srvc

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s')

# Define the target namespace
TNS = "tns"


class GUIAppService(ServiceBase):
    __service_url_path__ = srvc.serviceURLPath
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @srpc(Unicode, Unicode, Unicode, _returns=guiSrvc.return_type_tuple,
          _out_variable_names=guiSrvc.return_names_tuple)
    def startInputGUI(serviceID, sessionToken, extraParameters):
        logging.info('#################')
        logging.info('\tsessionToken: ' + sessionToken)
        logging.info('\tserviceID: ' + serviceID)
        logging.info('#################')

        extraParametersDict = utl.parseExtraParameters(extraParameters)

        authURL = extraParametersDict['auth']

        logging.info('Validating request...')

        if sh.validateSession(token=sessionToken, wsdlurl=authURL):

            logging.info('Request is valid')

            logging.info('Reading web page header')
            readPageHeader = utl.returnFileAsString('pageHeader.dat')
            logging.info('Reading web page body')
            readPageData = utl.returnFileAsString('pageBody.dat')
            logging.info('Reading web page footer')
            readPageFooter = utl.returnFileAsString('pageFooter.dat')

            logging.info('Constructing final web page')

            addServiceID = '<input type="hidden"  id="servID" value="' + serviceID + '" />'
            addSessionToken = '<input type="hidden"  id="sessToken" value="' + sessionToken + '" />'
            addWFMURL = '<input type="hidden"  id="WFM" value="' + extraParametersDict['WFM'] + '" />'

            outputPage = readPageHeader + readPageData + addServiceID + addSessionToken + addWFMURL + readPageFooter

            outputs = [base64.b64encode(outputPage)] + guiSrvc.standard_vals_list

            logging.info('Returning web page with standard values')

            return tuple(outputs)
        else:
            logging.critical("Invalid Request")
            outputs = [base64.b64encode("UNCHANGED")] + guiSrvc.standard_vals_list
            return tuple(outputs)


def create_app():
    """Creates an Application object containing the gui app service."""
    app = Application([GUIAppService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
