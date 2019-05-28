"""A very simple calculator SOAP service written in Python.

This simple service utilizes the "flask_spyne" package to create a SOAP service
with just a few lines of code.
"""
from spyne import Application, srpc, ServiceBase, Float, Unicode
from spyne.protocol.soap import Soap11
import base64
from urllib.request import urlopen


# Define the target namespace
TNS = "cat.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Cat"

def htmlHeader():
    ret =  "<html>\n" 
    ret += "<header><title>This is title</title></header>\n"
    ret += "<body>\n"
    ret += "<h1><center>Cat delivered as a service</center></h1>"
    return(ret)

def htmlFooter():
    ret =  "</body>\n"
    ret += "</html>\n"
    return(ret)

class Cat(ServiceBase):
    """The actual spyne calculator service

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    @srpc(_returns=Unicode)
    def getCat():
        data_uri = base64.b64encode(urlopen('https://cataas.com/cat/gif/says/Perfect execution').read()).decode('utf-8').replace('\n','')
        img_tag = '<img src="data:image/png;base64,%s">' % data_uri
        returnString = htmlHeader() + img_tag + "\n"+ htmlFooter()
        return returnString

def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([Cat], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
