from werkzeug.contrib.fixers import ProxyFix

from flask import Flask
from flask import request
from flask_spyne import Spyne
from flask import send_from_directory
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Float
from spyne.model.complex import Iterable

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/sintef/docker_services/calculator")
def hello():
    response = "<h1>Hello World</h1>\n<h2>Request headers</h2>"
    for header in request.headers:
        response += "%s: %s<br/>" % (header[0], header[1])
    return response


@app.route("/sintef/docker_services/calculator/log/<path:filename>")
def get_log(filename):
    print (filename)
    return send_from_directory("/var/log/", filename, as_attachment=True)


class SomeSoapService(spyne.Service):
    __service_url_path__ = '/sintef/docker_services/calculator/Calculator'
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
