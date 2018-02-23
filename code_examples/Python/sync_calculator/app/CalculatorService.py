"""A very simple calculator SOAP service written in Python.

This simple service utilizes the "flask_spyne" package to create a SOAP service
with just a few lines of code.
"""
from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Float
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def root():
    """Static page on root to avoid error 404"""
    return 'Nothing to see here.'


class CalculatorService(spyne.Service):
    """The actual spyne calculator service

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    __service_url_path__ = '/Calculator'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @spyne.srpc(Float, Float, _returns=Float)
    def add(a, b):
        return a+b

    @spyne.srpc(Float, Float, _returns=Float)
    def subtract(a, b):
        return a-b

    @spyne.srpc(Float, Float, _returns=Float)
    def multiply(a, b):
        return a*b
