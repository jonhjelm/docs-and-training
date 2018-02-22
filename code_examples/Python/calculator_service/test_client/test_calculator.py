#!/usr/bin/env python

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
    url = "http://localhost:5000/sintef/examples/calculator/Calculator?wsdl"

    a = 11
    b = 31
    response = soap_call(url, "add", [a, b])
    print("{} + {} = {}".format(a, b, response))

    response = soap_call(url, "subtract", [a, b])
    print("{} - {} = {}".format(a, b, response))

    response = soap_call(url, "multiply", [a, b])
    print("{} * {} = {}".format(a, b, response))

if __name__ == "__main__":
    main()

