"""Asynchronous-service tutorial: a waiter service

"""
import os
import subprocess
import base64
import datetime
from flask import Flask
from flask import request
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, Boolean
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


# Read environment variables to obtain configuration values
WAITER_LOG_FOLDER = os.environ["WAITER_LOG_FOLDER"]


@app.route('/')
def root():
    """Static page on root to avoid error 404"""
    return 'Nothing to see here.'


class WaiterService(spyne.Service):
    """The actual waiter asynchronous service."""
    __service_url_path__ = '/Waiter'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()



def create_html_progresspage(progress):
    """Creates a very simple html progress page.
    """
    now_str = datetime.datetime.now().strftime('%H:%M:%S')

    html = "<html>\n" + \
        "<head>\n" + \
        "<title>Waiter status</title>\n" + \
        "</head>\n" + \
        "<body style=\"margin: 20px; padding: 20px;\">\n" + \
        "<h1>Waiter at " + str(progress) + " % at " + now_str + "</h1>\n" + \
        "</head>\n" + \
        "</body>"

    return html
