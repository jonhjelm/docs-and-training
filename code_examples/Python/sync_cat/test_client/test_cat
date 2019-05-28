#!/usr/bin/env python
"""Simple test client to call the calculator SOAP service"""

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
    """Makes a series of test calls and prints their outputs."""

    try:
        port = int(sys.argv[1])
        print("Using port {}".format(port))
    except:
        print("Couldn't get port from commandline argument, using 80.")
        port = 80

    try:
        context_root = os.environ["CONTEXT_ROOT"]
    except KeyError:
        print("Error: environment variable CONTEXT_ROOT not set.")
        exit(1)

    # URL of the SOAP service to test. Modify this if the deployment location
    # changes.
    url = "http://localhost:{}{}/Calculator?wsdl".format(port, context_root)
    print("wsdl URL is {}".format(url))

    a = 11
    b = 31

    print("Testing addition:")
    response = soap_call(url, "add", [a, b])
    print("{} + {} = {}".format(a, b, response))

    print("Testing subtraction:")
    response = soap_call(url, "subtract", [a, b])
    print("{} - {} = {}".format(a, b, response))

    print("Testing multiplication:")
    response = soap_call(url, "multiply", [a, b])
    print("{} * {} = {}".format(a, b, response))


if __name__ == "__main__":
    main()
