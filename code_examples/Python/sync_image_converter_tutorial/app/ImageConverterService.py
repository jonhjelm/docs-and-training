import os
import shutil
import tempfile
import subprocess
import urllib2
from flask import Flask
from flask_spyne import Spyne
from suds.client import Client
from suds.cache import NoCache
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


class ImageConverterService(spyne.Service):
    """Spyne SOAP service to convert png images to jpg images.

    This service's purpose is to showcase file access via GSS.

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    __service_url_path__ = '/ImageConverter'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Unicode, _returns=Unicode,
                _out_variable_name="file_content")
    def imageconvert_png2jpg(sessionToken, extra_pars_str, gss_ID):
        """Converts a png image specified by a gss ID to a jpg image."""

        # Implementation starts here ...
        gss_ID_new = 'fake!'
        # ... and ends here

        return gss_ID_new


def get_resource_information(gss_location, gss_ID, session_token):
    """Returns a GSS resourceInformation object for the given gss ID."""
    client = Client(gss_location, cache=NoCache())
    return client.service.getResourceInformation(gss_ID, session_token)


def convert_png2jpg(png_filepath):
    '''Converts a png image to jpg and returns the jpg filepath.'''
    folder, png_filename = os.path.split(png_filepath)
    filebase, _ = os.path.splitext(png_filename)
    jpg_filepath = os.path.join(folder, filebase + '.jpg')

    command = ['convert', png_filepath, jpg_filepath]
    subprocess.call(command)
    return jpg_filepath


def parse_extra_parameters(extra_pars):
    """Parses an extra-parameters string into a dict.

    The extra parameters as delivered from the workflow manager are encoded in
    a single string of the format "key1=value1,key2=value2,key3=value3,...".
    """
    return {pair.split('=')[0]: pair.split('=')[1] for pair in
            extra_pars.split(',')}
