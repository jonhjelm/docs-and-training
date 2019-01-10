## ========================================================================= ##
##                                                                           ##
## Filename: serviceSetupUtil.py                                             ##
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

from spyne.model.primitive import Unicode
from spyne.model.primitive import Integer
from spyne.model.primitive import Float

import os
import sys

additionalPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PageGenerator'))
sys.path.append(additionalPath)

import generator

# Parse output types tuple from xls dict
def getTypesList(dict):
    types = []
    radiobutton_groups = []
    for key in dict:
        if key['Type'] == generator.types.INTEGER_FIELD:
            types.append(Integer)
        elif key['Type'] == generator.types.STRING_FIELD:
            types.append(Unicode)
        elif key['Type'] == generator.types.DECIMAL_FIELD:
            types.append(Float)
        elif key['Type'] == generator.types.DECIMAL_VEC_6:
            for _ in range(6):
                types.append(Float)
        elif key['Type'] == generator.types.DECIMAL_VEC_3:
            for _ in range(3):
                types.append(Float)
        elif key['Type'] == generator.types.RADIOBUTTON:
            if key['Unit of measurement'] in radiobutton_groups:
                continue
            else:
                radiobutton_groups.append(key['Unit of measurement'])
                types.append(Unicode)
        elif key['Type'] == generator.types.CHECKBOX:
            types.append(Unicode)
    return types


# Parse output parameter names from xls dict
def getOutputNamesList(dict):
    output_names = []
    for key in dict:
        if key['Type'] == generator.types.RADIOBUTTON:
            if key['output parameter'] in output_names:
                continue
            else:
                output_names.append(key['output parameter'])
        elif key['Type'] == generator.types.DECIMAL_VEC_3:
            output_names.append(key['output parameter'] + '_1')
            output_names.append(key['output parameter'] + '_2')
            output_names.append(key['output parameter'] + '_3')
        elif key['Type'] == generator.types.DECIMAL_VEC_6:
            output_names.append(key['output parameter'] + '_1')
            output_names.append(key['output parameter'] + '_2')
            output_names.append(key['output parameter'] + '_3')
            output_names.append(key['output parameter'] + '_4')
            output_names.append(key['output parameter'] + '_5')
            output_names.append(key['output parameter'] + '_6')
        elif key['Type'] == generator.types.TITLE or key['Type'] == generator.types.HEADING:
            continue
        else:
            output_names.append(key['output parameter'])
    return output_names

# Parse standard vals for output parameter types
def getStandardValsList(dict):
    standard_vals = []
    radiobutton_groups = []
    for key in dict:
        if key['Type'] == generator.types.INTEGER_FIELD:
            standard_vals.append(0)
        elif key['Type'] == generator.types.STRING_FIELD:
            standard_vals.append('')
        elif key['Type'] == generator.types.DECIMAL_FIELD:
            standard_vals.append(0.0)
        elif key['Type'] == generator.types.DECIMAL_VEC_6:
            for _ in range(6):
                standard_vals.append(0.0)
        elif key['Type'] == generator.types.DECIMAL_VEC_3:
            for _ in range(3):
                standard_vals.append(0.0)
        elif key['Type'] == generator.types.RADIOBUTTON:
            if key['Unit of measurement'] in radiobutton_groups:
                continue
            else:
                radiobutton_groups.append(key['Unit of measurement'])
                standard_vals.append('')
        elif key['Type'] == generator.types.CHECKBOX:
            standard_vals.append('unchecked')
    return standard_vals