"""A very simple calculator SOAP service written in Python.

This simple service utilizes the "flask_spyne" package to create a SOAP service
with just a few lines of code.
"""
from spyne import Application, srpc, ServiceBase, Float
from spyne.protocol.soap import Soap11

# Define the target namespace
TNS = "calculator.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Calculator"


class Calculator(ServiceBase):
    """The actual spyne calculator service

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    @srpc(Float, Float, _returns=Float)
    def add(a, b):
        return a+b

    @srpc(Float, Float, _returns=Float)
    def subtract(a, b):
        return a-b

    @srpc(Float, Float, _returns=Float)
    def multiply(a, b):
        return a*b


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([Calculator], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
