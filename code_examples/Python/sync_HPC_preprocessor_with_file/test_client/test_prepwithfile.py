#!/usr/bin/env python
"""Simple test client to call the waiter HPC preprocessor service"""

import os
import sys
import getpass

from suds.client import Client
from suds.cache import NoCache
from suds import WebFault, MethodNotFound

from clfpy import AuthClient

auth_endpoint = 'https://api.hetcomp.org/authManager/AuthManager?wsdl'
extra_pars = "auth={},".format(auth_endpoint)


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
    """Makes a series of test calls and prints their outputs."""

    port = 80

    try:
        context_root = os.environ["CONTEXT_ROOT"]
    except KeyError:
        print("Error: environment variable CONTEXT_ROOT not set.")
        exit(1)

    print("Obtaining session token")
    user = input("Enter username: ")
    project = input("Enter project: ")
    password = getpass.getpass(prompt="Enter password: ")
    auth = AuthClient(auth_endpoint)
    token = auth.get_session_token(user, project, password)

    # URL of the SOAP service to test. Modify this if the deployment location
    # changes.
    url = "http://localhost:{}{}/PrepWithFile?wsdl".format(port, context_root)
    print("wsdl URL is {}".format(url))

    filepath = "/tmp/somefile.txt"
    textinput = "'This is some text'"

    print("Calling preprocessor:")
    response = soap_call(url, "hpcPrepWithFile", [token, extra_pars, filepath, textinput])
    print(response)


if __name__ == "__main__":
    main()
