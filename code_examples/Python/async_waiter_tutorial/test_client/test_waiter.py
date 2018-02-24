#!/usr/bin/env python
"""Simple test client to call the waiter SOAP service"""

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


def start(url):

    print("Starting service")
    response = soap_call(url, "startWaiter", ["serviceID1", "sessionToken", "60"])
    print(response)


def status(url):

    print("Calling getServiceStatus:")
    response = soap_call(url, "getServiceStatus", ["serviceID1", "sessionToken"])
    print(response)


def main():
    try:
        port = int(sys.argv[1])
        print("Using port {}".format(port))
    except:
        print("Couldn't get port from commandline argument, using 8080.")
        port = 8080

    try:
        context_root = os.environ["CONTEXT_ROOT"]
    except KeyError:
        print("Error: environment variable CONTEXT_ROOT not set.")
        exit(1)

    url = "http://localhost:{}{}/waiter/Waiter?wsdl".format(port, context_root)
    print("wsdl URL is {}".format(url))

    if len(sys.argv) != 2:
        print("Expected [start|status] as argument.")
        exit(1)

    if sys.argv[1] == 'start':
        start(url)
    elif sys.argv[1] == 'status':
        status(url)
    else:
        print('Unknown argument.')


if __name__ == "__main__":
    main()
