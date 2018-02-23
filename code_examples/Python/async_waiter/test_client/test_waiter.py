#!/usr/bin/env python
"""Simple test client to call the waiter SOAP service"""

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
    # URL of the SOAP service to test. Modify this if the deployment location
    # changes.
    url = "http://localhost:8080/sintef/docker_services/waiter/Waiter?wsdl"

    if sys.argv[1] == 'start':
        start(url)
    elif sys.argv[1] == 'status':
        status(url)
    else:
        pass


if __name__ == "__main__":
    main()
