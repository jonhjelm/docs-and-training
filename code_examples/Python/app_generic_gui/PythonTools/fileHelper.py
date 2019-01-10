#!/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: fileHelper.py                                                   ##
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

import xmltodict
import dict2xml
import os.path


def parseXML(file):
    result = {}
    if (len(file) == 0):
        return result
    if not os.path.isfile(file):
        return result
    with open(file, 'r') as fd:
        result = xmltodict.parse(fd.read())
    return result


def writeXML(file, dict):
    result = {}
    if (len(dict) == 0):
        return
    with open(file, 'w') as fd:
        result = "<?xml version=\"1.0\"?>"
        result = result + dict2xml.dict2xml(dict, wrap="", indent="  ")
        fd.write(result)
