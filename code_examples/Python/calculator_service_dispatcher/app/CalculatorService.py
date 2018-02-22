from werkzeug.contrib.fixers import ProxyFix

from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Float

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


class SomeSoapService(spyne.Service):
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
