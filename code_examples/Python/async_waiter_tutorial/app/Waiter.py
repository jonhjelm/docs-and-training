"""Asynchronous-service tutorial: a waiter service

"""
import os
import subprocess
import base64
import datetime
import logging

from spyne import Application, srpc, ServiceBase, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11
from spyne.model.fault import Fault

from clfpy import AuthClient, ExtraParameters

# Define the target namespace
TNS = "waiter.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Waiter"

# Read environment variables to obtain configuration values
WAITER_LOG_FOLDER = os.environ["WAITER_LOG_FOLDER"]


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class WaiterService(ServiceBase):
    """The actual waiter asynchronous service."""

    auth_wsdl = ''


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


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([WaiterService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
