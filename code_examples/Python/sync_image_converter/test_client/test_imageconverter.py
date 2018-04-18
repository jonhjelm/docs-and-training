#!/usr/bin/env python
"""Simple test client to call the imageconverter SOAP service"""

import os
import sys

from suds.client import Client
from suds.cache import NoCache
from suds import WebFault, MethodNotFound


def soap_call(wsdl_url, methodname, method_args):
    """Calls a SOAP webmethod at a given URL with given arguments."""
    client = Client(wsdl_url, cache=NoCache())

    try:
        method = getattr(client.service, methodname)
    except MethodNotFound as error:
        return(error)

    try:
        response = method(*method_args)
    except WebFault as error:
        return(error)

    return response


def main():
    try:
        context_root = os.environ["CONTEXT_ROOT"]
    except KeyError:
        print("Error: environment variable CONTEXT_ROOT not set.")
        exit(1)

    if len(sys.argv) != 6:
        print("Expected arguments are: port username project password gss_ID")
        exit(1)

    port = sys.argv[1]
    username = sys.argv[2]
    project = sys.argv[3]
    password = sys.argv[4]
    gss_ID = sys.argv[5]

    # This test client also needs to obtain an authentication token from the
    # authentication-manager service to be able to access GSS afterwards.
    print('Obtaining session token')
    auth_url = "https://caxman.clesgo.net/sintef/auth/authManager/AuthManager?wsdl"
    session_token = soap_call(auth_url, 'getSessionToken', [username, password,
                                                            project])

    # Fake the extra-parameters string
    extra_pars = 'gss=https://caxman.clesgo.net/sintef/infrastructure/gss-0.1/FileUtilities?wsdl,'

    # Construct service URL
    url = "http://localhost:{}{}/imageconverter/ImageConverter?wsdl".format(port, context_root)
    print("wsdl URL is {}".format(url))

    # Make request
    print(soap_call(url, 'imageconvert_png2jpg', [session_token, extra_pars,
                                                  gss_ID]))


if __name__ == "__main__":
    main()
