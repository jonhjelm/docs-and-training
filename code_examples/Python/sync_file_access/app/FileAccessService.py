from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def root():
    """Static page on root to avoid error 404"""
    return 'Nothing to see here.'


class FileAccessService(spyne.Service):
    """The actual spyne service

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    __service_url_path__ = '/FileAccess'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Unicode, _returns=Unicode,
                _out_variable_name="file_content")
    def read_file(sessionToken, extra_pars_str, gss_ID):
        extra_pars = parse_extra_parameters(extra_pars_str)

        gss_location = extra_pars['gss']



def parse_extra_parameters(extra_pars):
    """Parses an extra-parameters string into a dict.

    The extra parameters as delivered from the workflow manager are encoded in
    a single string of the format "key1=value1,key2=value2,key3=value3,...".
    """
    return {pair.split('=')[0]: pair.split('=')[1] for pair in
            extra_pars.split(',')}
