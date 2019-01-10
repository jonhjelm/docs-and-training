## ========================================================================= ##
##                                                                           ##
## Filename: sessionHelper.py                                                ##
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

from suds.client import Client


def validateSession(token, wsdlurl):
    client = Client(wsdlurl)
    return client.service.validateSessionToken(sessionToken=token)


def sessionsWatcher(sessions, wsdlurl, closeSessionFunc):
    while True:
        for token in sessions:
            if not validateSession(token, wsdlurl):
                for service in sessions[token]:
                    closeSessionFunc(service=service, token=token)
        time.sleep(3600)  # wait an hour and check again
