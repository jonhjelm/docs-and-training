#!/usr/bin/env python

## ========================================================================= ##
##                                                                           ##
## Filename: generator.py                                                    ##
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

from xml.dom import minidom
from jsGenerator import generateJS
import elementTypes as types
import logging

# Used to count headings
headingCount = 0

# type of the element processed just before
lastElementType = ''

checkableElements = [types.CHECKBOX, types.RADIOBUTTON]

divClassForLayout = {
    'left2right': 'col-xs-4',
    'top2bottom': 'row'
}

formattingDivClassForNextElement = {
    'left2right': 'row',
    'top2bottom': 'col-xs-4'
}

# Page Congfig Elements
pageConfig = {}
pageLayout = 'left2right'
orientation = 'multiple'
margin = 0
margin_direction = 'none'
title_size = '3'
heading_size = '4'
font_size = '14px'


def readConfigParam(filename):
    global pageLayout
    global orientation
    global margin
    global margin_direction
    global title_size
    global heading_size
    global font_size

    xmldoc = minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('param')
    # Create dict
    for s in itemlist:
        pageConfig[str(s.attributes['name'].value)] = str(s.childNodes[0].nodeValue)
    pageLayout = pageConfig['layout']
    orientation = pageConfig['orientation']
    margin = pageConfig['margin']
    margin_direction = pageConfig['margin_direction']
    if 7 > int(pageConfig['title_size']) > 0:
        title_size = pageConfig['title_size']
    if 7 > int(pageConfig['heading_size']) > 0:
        heading_size = pageConfig['heading_size']
    font_size = pageConfig['font_size']


def generate(getType, key, page):
    global checkableElements
    global lastElementType
    global margin
    global margin_direction

    default_val = key['Default Value']

    # Filter Default value , ex. 'n/a' , '--', replaced by ''
    default_value = filter(default_val)

    min = key['Min Value']
    max = key['Max Value']
    unitRaw = key['Unit of measurement']
    # Filter Unit of measurement, ex. 'n/a' , '--', replaced by ''
    unit = filter(unitRaw)

    name = key['Name']

    getFunction = generationFunctions.get(str(getType), 'Not_Found')
    # if not found in the dataType list then generate a default text input field

    # If margins are specified, then create a section for them
    if (margin != 0 and margin_direction != 'none'):
        page += createMarginSection()

    # Starting new Section
    page += startNewSection()

    if getFunction == 'Not_Found':
        page += formattingforNextElement()
        value = createDefaultStringField(default_value, min, max, name, unit)
        page += value
        page += endSection()
    else:
        page += formattingforNextElement()
        if (getType in checkableElements and key['checked'] == 'YES'):
            value = getFunction(default_value, min, max, name, unit, True)
        else:
            value = getFunction(default_value, min, max, name, unit)
        page += value
        page += endSection()

    # End Current Section
    page += endSection()

    # If margins are specified, then end the section for the margin
    if (margin != 0 and margin_direction != 'none'):
        page += endSection()

    lastElementType = getType

    return page


# Filtering input util
def filter(inp):
    if (inp == 'n/a'):
        logging.debug('unit of measurement is  ' + str(inp))
        return ''
    elif (inp == '--'):
        logging.debug('unit of measurement is  ' + str(inp))
        return ''
    elif (inp == 'na'):
        logging.debug('unit of measurement is  ' + str(inp))
        return ''
    else:
        return inp


# Page Individual Elements Declared Below

def createDecimalField(default_value, min, max, name, unit):
    logging.debug("Number Field " + name)

    if (unit == ''):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + name + \
               "</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id=\"" + name.replace(" ", "_") + "\" type=\"number\" name=\"" + \
               name + "\" min=\"" + min + "\"  max=\"" + max + "\"class=\"form-control\" value=\"" + default_value + \
               "\"/>\n</div>\n" + horizontalLine()
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + name + "(" + \
               unit + ")</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id=\"" + name.replace(" ", "_") + "\" type=\"number\" name=\"" + \
               name + "\" min=\"" + min + "\" max=\"" + max + "\"class=\"form-control\" value=\"" + default_value + \
               "\"/>\n</div>\n" + horizontalLine()


def createIntegerField(default_value, min, max, name, unit):
    logging.debug("Integer Field " + name)

    if (unit == ''):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + name + \
               "</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id=\"" + name.replace(" ", "_") + \
               "\" type=\"number\" step=\"1\" name=\"" + name + "\" min=\"" + min + "\"  max=\"" + max + \
               "\"class=\"form-control\" value=\"" + default_value + "\"/>\n</div>\n" + horizontalLine()
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + name + \
               "(" + unit + ")</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id=\"" + name.replace(" ", "_") + \
               "\" type=\"number\" step=\"1\" name=\"" + name + "\" min=\"" + min + "\" max=\"" + max + \
               "\"class=\"form-control\" value=\"" + default_value + "\"/>\n</div>\n" + horizontalLine()


def create3DecimalField(default_value, min, max, name, unit):
    logging.debug("Decimal Field " + name + "_1")
    logging.debug("Decimal Field " + name + "_2")
    logging.debug("Decimal Field " + name + "_3")

    if (unit == ''):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + \
               name + "</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "_1" + \
               "\" type=\"number\" name=\"" + name + "\" min=\"" + min + "\"  max=\"" + max + \
               "\" class=\"form-control\" value=\"" + default_value + "\"/>\n\t<input id =\"" + \
               name.replace(" ", "_") + "_2" + "\" type=\"number\" name=\"" + name + "\" min=\"" + \
               min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_3" + "\" type=\"number\" name=\"" + \
               name + "\" min=\"" + min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + \
               default_value + "\"/>\n</div>\n" + horizontalLine()
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + \
               name + "(" + unit + ")</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "_1" + \
               "\" type=\"number\" name=\"" + name + "\" min=\"" + min + "\" max=\"" + max + \
               "\" class=\"form-control\" value=\"" + default_value + "\"/>\n\t<input id =\"" + \
               name.replace(" ", "_") + "_2" + "\" type=\"number\" name=\"" + name + "\" min=\"" + \
               min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_3" + "\" type=\"number\" name=\"" + \
               name + "\" min=\"" + min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + \
               default_value + "\"/>\n</div>\n" + horizontalLine()


def create6DecimalField(default_value, min, max, name, unit):
    logging.debug("Number Field " + name + "_1")
    logging.debug("Number Field " + name + "_2")
    logging.debug("Number Field " + name + "_3")
    logging.debug("Number Field " + name + "_4")
    logging.debug("Number Field " + name + "_5")
    logging.debug("Number Field " + name + "_6")

    if (unit == ''):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + \
               " for=\"usr\">" + name + "</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "_1" + \
               "\" type=\"number\" name=\"" + name + "\" min=\"" + min + "\"  max=\"" + max + \
               "\" class=\"form-control\" value=\"" + default_value + "\"/>\n\t<input id =\"" + \
               name.replace(" ", "_") + "_2" + "\" type=\"number\" name=\"" + name + "\" min=\"" + min + \
               "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_3" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_4" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_5" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_6" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\"  max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n</div>\n" + horizontalLine()
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + \
               name + "(" + unit + ")</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "_1" + \
               "\" type=\"number\" name=\"" + name + "\" min=\"" + min + "\" max=\"" + max + \
               "\" class=\"form-control\" value=\"" + default_value + "\"/>\n\t<input id =\"" + \
               name.replace(" ", "_") + "_2" + "\" type=\"number\" name=\"" + name + "\" min=\"" + \
               min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_3" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_4" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_5" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n\t<input id =\"" + name.replace(" ", "_") + "_6" + "\" type=\"number\" name=\"" + name + \
               "\" min=\"" + min + "\" max=\"" + max + "\" class=\"form-control\" value=\"" + default_value + \
               "\"/>\n</div>\n" + horizontalLine()


def createStringField(default_value, min, max, name, unit):
    logging.debug("String Field " + name)

    if (unit == ''):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + \
               name + "</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "\" type=\"text\" name=\"" + \
               name + "\" class=\"form-control\" value=\"" + default_value + "\"/>\n</div>\n" + horizontalLine()
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\" for=\"usr\">" + name + "(" + \
               unit + ")</label>\n</div>\n" + \
               "<div class=\"col-xs-12\">\n\t<input id =\"" + name.replace(" ", "_") + "\" type=\"text\" name=\"" + \
               name + "\" class=\"form-control\" value=\"" + default_value + "\"/>\n</div>\n" + horizontalLine()


def startNewSection():
    global pageLayout

    return "<div class=\"" + divClassForLayout[pageLayout] + "\">\n"


def endSection():
    return "</div>\n"


def createMarginSection():
    global margin
    global margin_direction

    return "<div style=\"margin-" + margin_direction + ":" + margin + "px\">\n"


def formattingforNextElement():
    global pageLayout

    return "<div class=\"" + formattingDivClassForNextElement[pageLayout] + "\">\n"


def createRadioButton(default_value, min, max, name, unit, checked=False):
    logging.debug("radiobutton " + name)

    if (checked):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\"><input id=\"" + \
               name.replace(" ", "_") + "\" class=\"" + unit + \
               "_radiobuttons\" type=\"radio\" checked=\"checked\" name=\"optradio_" + unit + "\" value=\"" + \
               default_value + "\"> " + name + "</label>\n</div>\n"
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + "\"><input id=\"" + \
               name.replace(" ", "_") + "\" class=\"" + unit + "_radiobuttons\" type=\"radio\" name=\"optradio_" + \
               unit + "\" value=\"" + default_value + "\"> " + name + "</label>\n</div>\n"


def createCheckbox(default_value, min, max, name, unit, checked=False):
    logging.debug("checkbox " + name)

    if (checked):
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + \
               "\"><input type=\"checkbox\" id=\"" + name.replace(" ", "_") + "\" name=\"" + name + "\" value=\"" + \
               default_value + "\" checked=\"checked\"> " + name + "</label>\n</div>\n"
    else:
        return "<div class=\"col-xs-12\">\n\t<label style=\"font-size:" + font_size + \
               "\"><input type=\"checkbox\" id=\"" + name.replace(" ", "_") + "\" name=\"" + name + "\" value=\"" + \
               default_value + "\"> " + name + "</label>\n</div>\n"


def createHeading(default_value, min, max, name, unit):
    global headingCount
    global lastElementType
    logging.debug("Heading " + name)

    ret = "<p><div class=\"col-xs-12\"><h" + heading_size + "><b>" + name + "</b></h" + heading_size + "></div></p>\n"
    if headingCount > 0 and (lastElementType == 'heading' or lastElementType in checkableElements):
        ret = horizontalLine() + ret
    headingCount += 1
    return ret


def createTitle(default_value, min, max, name, unit):
    return "<p><div class=\"col-xs-12\">\n\t<h" + title_size + "><b>" + name + "</b></h" + title_size + \
           ">\n</div></p>\n" + horizontalLine()


def horizontalLine():
    return "<div class=\"col-xs-12\"><hr/></div>\n"


def createPageFooter():
    if margin_direction == 'left' or margin_direction == 'right':
        return "</div><div style=\'position:relative;top:20px;" + margin_direction + ":" + margin + \
               "px;\'>\n\t<button type=\"reset\" class=\"btn btn-default\" onclick=\'resetfields()\'>Reset</button>" \
               "\n\t<button type=\"button\" class=\"btn btn-default\" onclick=\'validatefields()\'>" \
               "Submit</button>\n</div>\n</body>\n</html>"
    else:
        return "</div><div style=\'position:relative;top:20px;left:0.3%;\'>\n\t<button type=\"reset\" class=\"btn" \
               " btn-default\" onclick=\'resetfields()\'>Reset</button>\n\t<button type=\"button\" " \
               "class=\"btn btn-default\" onclick=\'validatefields()\'>Submit</button>\n</div>\n</body>\n</html>"


# Dictionary for the dataTypes
generationFunctions = {types.DECIMAL_FIELD: createDecimalField, types.INTEGER_FIELD: createIntegerField,
                       types.STRING_FIELD: createStringField, types.DECIMAL_VEC_3: create3DecimalField,
                       types.DECIMAL_VEC_6: create6DecimalField, types.RADIOBUTTON: createRadioButton,
                       types.HEADING: createHeading, types.TITLE: createTitle, types.CHECKBOX: createCheckbox}
