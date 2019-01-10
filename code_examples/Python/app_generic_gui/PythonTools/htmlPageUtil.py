## ========================================================================= ##
##                                                                           ##
## Filename: htmlPageUtil.py                                                 ##
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
import sys
from util import xls2Dict

additionalPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PageGenerator'))
sys.path.append(additionalPath)

import generator
from jsGenerator import generateJS

headerBegin = '<!DOCTYPE html>' \
                    '\n<html lang=\'en\'>' \
                    '\n<head>' \
                    '\n\t<meta charset=\'utf-8\'>' \
                    '\n\t<meta name=\'viewport\' content=\'width=device-width, initial-scale=1\'>' \
                    '\n\t<link rel=\'stylesheet\' href=\'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\'>' \
                    '\n\t<link rel=\"stylesheet\" type=\"text/css\" href=\"https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css\">' \
                    '\n\t<script type=\"text/javascript\" src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>' \
                    '\n\t<script type=\"text/javascript\" src=\"https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js\"></script>' \
                    '\n\t<script type=\"text/javascript\">\n\n'

headerEnd = '\n\t</script>' \
                  '\n\t</head>' \
                  '\n<body>' \
                  '\n<div class=\'jumbotron\' style=\'margin-top:-10px;padding-bottom:16px;padding-top:16px\'>' \
                  '\n\t<div class=\'row\' style=\'margin-left:10px;\' class=\'container\'>' \
                  '\n\t\t<img src=\'https://api.hetcomp.org/fraunhofer/resources/CFG_Logo_alpha.png\' style=\'width:7%;height:7%\'>' \
                  '\n\t\t<img src=\'https://www.igd.fraunhofer.de/sites/default/files/logos/igd.svg\' style=\'width:5%;height:3%;margin-left:15px;\'>' \
                  '\n\t</div>\n</div>\n<div class=\"row\"  style=\'position:relative;left:0.3%;\'>'


# Generation of Page Body
# Note that it writes result to output Filenames
def getPage(configFile, xlsDict, outputHeaderFilename, outputBodyFilename, outputPageFooterFilename):

    logging.info('Reading layout configuration file')
    generator.readConfigParam(configFile)

    logging.info('Constructing web page body elements')
    pageBody = ""
    for key in xlsDict:
        getType = key['Type']
        pageBody = generator.generate(getType, key, pageBody)

    try:
        # Removing existing file
        os.remove(outputBodyFilename)
        logging.info('Stale page body removed successfully')
    except OSError:
        pass
    with open(outputBodyFilename, 'a') as f:
        logging.info('Writing page body to file')
        f.write(pageBody)

    logging.info('Constructing web page header')

    pageHeader = headerBegin

    pageHeader += generateJS(xlsDict)

    pageHeader += headerEnd

    try:
        # Removing existing file
        os.remove(outputHeaderFilename)
        logging.info('Stale page header removed successfully')
    except OSError:
        pass
    with open(outputHeaderFilename, 'a') as f:
        logging.info('Writing page header to file')
        f.write(pageHeader)

    logging.info('Constructing web page footer')

    pageFooter = generator.createPageFooter()

    try:
        # Removing existing file
        os.remove(outputPageFooterFilename)
        logging.info('Stale page footer removed successfully')
    except OSError:
        pass
    with open(outputPageFooterFilename, 'a') as f:
        logging.info('Writing page footer to file')
        f.write(pageFooter)
