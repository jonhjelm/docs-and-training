#!/usr/bin/env python
"""Simple test client to call the waiter SOAP service"""

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


def start(url, token):
    print("Starting service")
    response = soap_call(url, "startWaiter", ["serviceID1", token, extra_pars, "60"])
    print(response)


def status(url, token):
    print("Calling getServiceStatus:")
    response = soap_call(url, "getServiceStatus", ["serviceID1", token])
    print(response)


def main():
    port = 80

    try:
        context_root = os.environ["CONTEXT_ROOT"]
    except KeyError:
        print("Error: environment variable CONTEXT_ROOT not set.")
        exit(1)

    url = "http://localhost:{}{}/Waiter?wsdl".format(port, context_root)
    print("wsdl URL is {}".format(url))

    if len(sys.argv) != 2:
        print("Expected [start|status] as argument.")
        exit(1)

    print("Obtaining session token")
    user = input("Enter username: ")
    project = input("Enter project: ")
    password = getpass.getpass(prompt="Enter password: ")
    auth = AuthClient(auth_endpoint)
    token = auth.get_session_token(user, project, password)

    if sys.argv[1] == 'start':
        start(url, token)
    elif sys.argv[1] == 'status':
        status(url, token)
    else:
        print('Unknown argument.')


if __name__ == "__main__":
    main()
