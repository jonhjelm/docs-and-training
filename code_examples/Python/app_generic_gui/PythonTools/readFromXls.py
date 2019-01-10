#!/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: readFromXLs.py                                                  ##
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

import xlrd
from collections import OrderedDict
import simplejson as json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def xls2JSON(filename):
    # Open the workbook
    wb = xlrd.open_workbook(str(filename))

    # Get the first sheet either by index or by name
    sh = wb.sheet_by_index(0)

    # Gettting labels
    labels = sh.row_values(0)

    storeRowEntry = []

    # Creating JSON Objects
    for rownum in range(1, sh.nrows):
        # Templist stores value of each row as a list
        templist = sh.row_values(rownum)
        createObj = OrderedDict()
        if (len(labels) == len(templist)):
            for itr in range(len(templist)):
                createObj[labels[itr]] = str(templist[itr]).encode('ascii', errors='xmlcharrefreplace')

            storeRowEntry.append(createObj)

    # JSON obj
    jsonData = json.dumps(storeRowEntry)

    return jsonData


def filter(inp):
    if (inp == 'n/a'):
        return ''
    elif (inp == '--'):
        return ''
    elif (inp == 'na'):
        return ''
    else:
        return inp


def getNameValuePair(filename):
    getJSON_Obj = xls2JSON(filename)
    makeDict = json.loads(getJSON_Obj)
    genKVPair = {}
    for ob in makeDict:
        genKVPair[ob['Name']] = filter(ob['Default Value'])
    return genKVPair
