## ========================================================================= ##
##                                                                           ##
## Filename: jsGenerator.py                                                  ##
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
import elementTypes as types

CreateXMLHttpRequestFunc = '\tvar objXMLHttpRequest = CreateXMLHttpRequest();' \
                           '\n\n\tfunction CreateXMLHttpRequest() {' \
                           '\n\t\tif (typeof XMLHttpRequest != \"undefined\") {' \
                           '\n\t\t\treturn new XMLHttpRequest();' \
                           '\n\t\t} else if (typeof ActiveXObject != \"undefined\") {' \
                           '\n\t\t\treturn new ActiveXObject(\"Microsoft.XMLHTTP\");' \
                           '\n\t\t} else {' \
                           '\n\t\t\tthrow new Error(\"XMLHttpRequest not supported\");' \
                           '\n\t\t}' \
                           '\n\t}' \
                           '\n\n'

convertBase_64FuncBegin = '\t//convert inputs to base 64' \
                          '\n\tfunction convertBase_64() {\n\n'

soapMsgFunc = '\n\t//send soap msg' \
              '\n\tfunction soapMsg() {' \
              '\n\t\tvar WFM = document.getElementById(\'WFM\').value+\'?wsdl\';' \
              '\n\t\tobjXMLHttpRequest.open(\"POST\", WFM, false);' \
              '\n\t\t\n\t\tobjXMLHttpRequest.setRequestHeader(\'Content-Type\', \'text/xml\');' \
              '\n\t\tobjXMLHttpRequest.setRequestHeader(\"SOAPAction\", \"\\"\\"\");' \
              '\n\t\t\n\t\tvar servID = document.getElementById(\'servID\').value;' \
              '\n\t\tvar sessToken = document.getElementById(\'sessToken\').value;' \
              '\n\t\tvar b64_xmlOut = convertBase_64();' \
              '\n\t\t\n\t\t//Soap Request' \
              '\n\t\tvar sr =\'<?xml version=\"1.0\" encoding=\"utf-8\"?>\'+' \
              '\n\t\t\t\'<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:wor=\"https://caxman.clesgo.net/dfki/WorkflowManager2Service/\">\'+' \
              '\n\t\t\t\'<soapenv:Header/>\'+' \
              '\n\t\t\t\'<soapenv:Body>\'+' \
              '\n\t\t\t\t\'<wor:serviceExecutionFinished>\'+' \
              '\n\t\t\t\t\t\'<serviceID>\'+servID+\'</serviceID>\'+' \
              '\n\t\t\t\t\t\'<sessionToken>\'+sessToken+\'</sessionToken>\'+' \
              '\n\t\t\t\t\t\'<xmlOutputs_base64>\'+b64_xmlOut+\'</xmlOutputs_base64>\'+' \
              '\n\t\t\t\t\'</wor:serviceExecutionFinished>\'+' \
              '\n\t\t\t\'</soapenv:Body>\'+' \
              '\n\t\t\'</soapenv:Envelope>\';' \
              '\n\t\t\n\t\tobjXMLHttpRequest.onreadystatechange = function() {' \
              '\n\t\t\tif (objXMLHttpRequest.readyState == 4)' \
              '\n\t\t\t{\n\t\t\t\tif (objXMLHttpRequest.status != 200)' \
              '\n\t\t\t\t\t{' \
              '\n\t\t\t\t\t\talert(\'Error while Sending Request status: \'+objXMLHttpRequest.status+\' Response :\'+objXMLHttpRequest.responseText);' \
              '\n\t\t\t\t\t}' \
              '\n\t\t\t}' \
              '\n\t\t}' \
              '\n\n\t\t//For sending the Post Request' \
              '\n\t\tobjXMLHttpRequest.send(sr);' \
              '\n\t}' \
              '\n\n'

resetFieldsFuncBegin = '\tfunction resetfields() {\n'
resetFieldsFuncEnd = '\t}\n'

validationMsgBegin = '\n\t\tvar str = \'<service_outputs><status_base64>\'+btoa(\'Success\')+\'</status_base64>\'+\n'

validationMsgEnd = '\t\t\'</service_outputs>\';' \
                   '\n\t\treturn btoa(str);' \
                   '\n\t}' \
                   '\n\n'

validateFieldsFunc = '\t//Validation' \
                     '\n\tfunction validatefields() {' \
                     '\n\t\tsoapMsg();' \
                     '\n\t}' \
                     '\n'


def generateJS(dict):
    JSCode = CreateXMLHttpRequestFunc + convertBase_64FuncBegin

    radiobutton_groups_dict = {}

    logging.debug('Count radio button groups (if any) and construct java script source code to extract parameters.')

    # Count the amount of radiobuttons in one group (Unit of measurement) also identify groups
    for key in dict:
        name = key['Name']
        name = name.replace(" ", "_")
        if key['Type'] == types.RADIOBUTTON:
            output_param_name = key['output parameter']
            if key['Unit of measurement'] in radiobutton_groups_dict:
                if output_param_name != radiobutton_groups_dict[key['Unit of measurement']][1]:
                    raise NameError(
                        'Multiple radiobuttons for same unit but different output parameter names at radiobutton ' +
                        key['Name'] + ', expected output variable was \"' +
                        radiobutton_groups_dict[key['Unit of measurement']][1] +
                        '\" but found \"' + output_param_name + '\"')
                radiobutton_groups_dict[key['Unit of measurement']][0] += 1
            else:
                radiobutton_groups_dict[key['Unit of measurement']] = [1, output_param_name]
        elif key['Type'] == types.DECIMAL_VEC_3:
            JSCode += checkVectorCode(name, name + '_arr', 3)
        elif key['Type'] == types.DECIMAL_VEC_6:
            JSCode += checkVectorCode(name, name + '_arr', 6)
        elif key['Type'] == types.CHECKBOX:
            JSCode += checkCheckboxCode(name, name + '_var', key['Default Value'])

    validation_radio_buttons = ""

    # Check radio button groups
    for key in radiobutton_groups_dict:
        param_name = 'param_' + key
        optradio_set = 'optradio_' + key
        output_param_name = radiobutton_groups_dict[key][1]
        JSCode += checkRadioButtonsCode(optradio_set, param_name, radiobutton_groups_dict[key][0])
        validation_radio_buttons += outputXMLParameter(param_name, output_param_name)

    logging.debug('Forge validation message')

    JSCode += validationMsgBegin

    # Forge workflow execution finished msg
    for key in dict:
        name = key['Name']
        name = name.replace(" ", "_")
        output_param_name = key['output parameter']
        if key['Type'] in [types.INTEGER_FIELD, types.DECIMAL_FIELD, types.STRING_FIELD]:
            JSCode += outputXMLInputField(name, output_param_name)
        elif key['Type'] == types.DECIMAL_VEC_3:
            JSCode += outputXMLVector(name + '_arr', output_param_name, 3)
        elif key['Type'] == types.DECIMAL_VEC_6:
            JSCode += outputXMLVector(name + '_arr', output_param_name, 6)
        elif key['Type'] == types.CHECKBOX:
            JSCode += outputXMLParameter(name + '_var', output_param_name)

    JSCode += validation_radio_buttons

    JSCode += validationMsgEnd

    logging.debug('Add function to send soap message')

    JSCode += soapMsgFunc

    logging.debug('Add reset fields function')

    JSCode += resetFieldsFuncBegin

    # Reset fields and radiobuttons to default values
    for key in dict:
        name = key['Name']
        name = name.replace(" ", "_")
        if key['Type'] in [types.INTEGER_FIELD, types.DECIMAL_FIELD]:
            JSCode += resetInputFieldCode(name, key['Default Value'])
        elif key['Type'] == types.STRING_FIELD:
            JSCode += resetStringFieldCode(name, key['Default Value'])
        elif key['Type'] in [types.RADIOBUTTON, types.CHECKBOX]:
            JSCode += resetCheckableElementCode(name, 'YES' == key['checked'])
        elif key['Type'] == types.DECIMAL_VEC_3:
            JSCode += resetVectorCode(name, 3, key['Default Value'])
        elif key['Type'] == types.DECIMAL_VEC_6:
            JSCode += resetVectorCode(name, 6, key['Default Value'])

    JSCode += resetFieldsFuncEnd

    logging.debug('Add function for field validation')

    JSCode += validateFieldsFunc

    return JSCode


def outputXMLInputField(name, serviceOutputParamName):
    return '\t\t\t\'<' + serviceOutputParamName + '>\'+document.getElementById(\'' + name + '\').value+\'</' + \
           serviceOutputParamName + '>\'+\n'


def outputXMLParameter(name, serviceOutputParamName):
    return '\t\t\t\'<' + serviceOutputParamName + '>\'+' + name + '+\'</' + serviceOutputParamName + '>\'+\n'

def outputXMLVector(arrName, serviceOutputParamBaseName, dim):
    res = ''
    for i in range(dim):
        res += '\t\t\t\'<' + serviceOutputParamBaseName + '_' + str(i + 1) + '>\'+' + arrName + '[' + str(i) +\
               ']+\'</' + serviceOutputParamBaseName + '_' + str(i + 1) + '>\'+\n'
    return res


def checkRadioButtonsCode(radioBtnName, paramName, amount):
    return '\t\tvar ' + paramName + ';\n\t\tvar ' + radioBtnName + '_radio_buttons = document.getElementsByName(\'' + \
           radioBtnName + '\');\n\t\tfor (var i = 0; i < ' + str(
        amount) + '; ++i) {\n\t\t\tif (' + radioBtnName + '_radio_buttons[i].checked) {\n\t\t\t\t' + paramName + ' = ' + \
           radioBtnName + '_radio_buttons[i].value;\n\t\t\t\tbreak;\n\t\t\t}\n\t\t}\n\n'

def checkCheckboxCode(checkBoxName, paramName, defaultValue):
    return '\t\tvar ' + paramName + ';\n\t\tif (' + checkBoxName + '.checked) {\n\t\t\t' + paramName + ' = \'' +\
           defaultValue + '\';\n\t\t} else {\n\t\t\t' + paramName + ' = \'unchecked\';\n\t\t}\n\n'


def checkVectorCode(vectorBaseName, paramName, dim):
    return '\t\tvar ' + paramName + ' = [];\n\t\tfor (var i = 1; i <= ' + str(dim) + '; ++i) {\n\t\t\t' + paramName + \
           '[i - 1] = document.getElementById(\'' + vectorBaseName + '_\' + i).value;\n\t\t}\n\n'


def resetCheckableElementCode(name, checked):
    if checked:
        return '\t\tdocument.getElementById(\'' + name + '\').checked = true;\n'
    else:
        return '\t\tdocument.getElementById(\'' + name + '\').checked = false;\n'


def resetInputFieldCode(name, value):
    return '\t\tdocument.getElementById(\'' + name + '\').value = ' + str(value) + ';\n'


def resetStringFieldCode(name, value):
    return '\t\tdocument.getElementById(\'' + name + '\').value = \'' + str(value) + '\';\n'


def resetVectorCode(vectorBaseID, dim, value):
    res = ''
    for i in range(dim):
        res += '\t\tdocument.getElementById(\'' + vectorBaseID + '_' + str(i + 1) + '\').value = ' + str(value) + ';\n'
    return res
