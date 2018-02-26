"""Simple synchronous service which converts png images to jpg images.

Note that this service is mainly intended to showcase file access via GSS. The
file access is coded explicitly here. In production code, one would rather wrap
the GSS access into a library and use that.
"""
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

        # Get gss location URL from extra parameters
        extra_pars = parse_extra_parameters(extra_pars_str)
        gss_location = extra_pars['gss']

        # obtain resource information for given GSS ID and check if read is
        # allowed
        res_info = get_resource_information(gss_location, gss_ID,
                                            sessionToken)
        read_desc = res_info.readDescription
        if not read_desc.supported:
            raise AttributeError('Read operation not allowed')

        # Create a temporary folder to store the file in
        tempdir = tempfile.mkdtemp()
        gss_folder, png_filename = os.path.split(gss_ID)
        png_filepath = os.path.join(tempdir, png_filename)

        # Formulate RESTful request to download the file
        # Therefore, we copy all headers defined in the requestDescription object
        # into the request headers.
        headers = {h.key: h.value for h in read_desc.headers}
        request = urllib2.Request(url=read_desc.url, headers=headers)
        with open(png_filepath, 'wb') as out_file:
            result = urllib2.urlopen(request)
            while True:
                buffer = result.read()
                if not buffer:
                    break
                out_file.write(buffer)

        # Convert the file using imagemagick
        jpg_filepath = convert_png2jpg(png_filepath)

        # Create a new GSS ID to store the converted file in
        _, jpg_filename = os.path.split(jpg_filepath)
        gss_ID_new = os.path.join(gss_folder, jpg_filename)

        # Make sure we are allowed to upload to this GSS ID.
        # Room for improvement: if 'create' is not allowed (because the file
        # already exists), use 'update' instead
        res_info = get_resource_information(gss_location, gss_ID_new,
                                            sessionToken)
        create_desc = res_info.createDescription
        if not create_desc.supported:
            raise AttributeError('Create operation not allowed')

        # Formulate RESTful request to upload the new file
        # We again copy the headers from the requestDescription object
        headers = {h.key: h.value for h in create_desc.headers}
        headers["Content-Length"] = "%d" % os.stat(jpg_filepath).st_size

        with open(jpg_filepath, "r") as in_file:
            request = urllib2.Request(url=create_desc.url, data=in_file,
                                      headers=headers)
            request.get_method = lambda: create_desc.httpMethod
            result = urllib2.urlopen(request)

        # Remove temporary folder and return new gss ID
        shutil.rmtree(tempdir)

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
