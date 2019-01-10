#!/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: util.py                                                         ##
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

import os
import signal
import sys
from readFromXls import xls2JSON
import json


def classifyType(input):
    try:
        if (eval(str(input)) is None):
            return str
        else:
            return type(eval(str(input)))
    except:
        return str


# For reading from Generated File
def returnFileAsString(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parseExtraParameters(extraParameters):
    extraParametersDict = {}
    if len(str(extraParameters)) > 0:
        paramsList = extraParameters.split(',')
        for param in paramsList:
            if len(param) is 0:
                continue
            keyVal = param.split('=')
            extraParametersDict[keyVal[0]] = keyVal[1]
    return extraParametersDict


def xls2Dict(xlsFilename):
    getJSONOBj = xls2JSON(xlsFilename)
    makeDict = json.loads(getJSONOBj)
    return makeDict