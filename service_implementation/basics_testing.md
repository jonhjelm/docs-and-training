# Testing SOAP services
When developing SOAP services for SemWES, one naturally wants to test the
services without having to deploy and integrate them in the SemWES platform
(especially since debugging through running workflows is _extremely_
cumbersome). One therefore needs tools for independent testing of the services.
This article portrays a few of those tools.

## The Python suds library
The Python `suds` library provides a very simple way to create SOAP clients
for your services.

_Requirements:_ Install the `suds-jurko` package, for example via pip:
```
pip install suds-jurko
```

### Minimum example without error handling
The following code example shows a very simply example client which
accesses the authentication manager and GSS. More complex clients can be
developed easily starting from here.
```python
from suds.client import Client

def main():
    auth_wsdl_url = "https://caxman.clesgo.net/sintef/auth/authManager/AuthManager?wsdl"
    gss_wsdl_url = "https://caxman.clesgo.net/sintef/infrastructure/gss-0.1/FileUtilities?wsdl"
    username = "myuser"
    project = "caxman"
    password = "mypassword"
    
    auth_client = Client(auth_wsdl_url)
    gss_client = Client(gss_wsdl_url)
    
    # Obtain a session token from the authentication manager
    token = auth_client.service.getSessionToken(username, password, project)
    
    # Use the token to get a file listing from GSS
    listing = gss_client.service.listFilesMinimal("swift://caxman/", token)
    print(listing)

if __name__ == "__main__":
    main()
```

Note that accessing SOAP methods is as easy as calling `client.service.<methodname>()`.

### Generic example with error handling
The following code block shows exactly the same functionality, but this time
implements and uses a more generic SOAP call method which also includes some
basic error handling.
```python
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
    auth_wsdl_url = "https://caxman.clesgo.net/sintef/auth/authManager/AuthManager?wsdl"
    gss_wsdl_url = "https://caxman.clesgo.net/sintef/infrastructure/gss-0.1/FileUtilities?wsdl"
    username = "myuser"
    project = "caxman"
    password = "mypassword"
    
    # Obtain a session token from the authentication manager
    token = soap_call(auth_wsdl_url, "getSessionToken", [username, password, project])
    
    # Use the token to get a file listing from GSS
    listing = soap_call(gss_wsdl_url, "listFilesMinimal", ["swift://caxman/", token])
    print(listing)

if __name__ == "__main__":
    main()
```
The `soap_call()` method as implemented above is usually the only building block to
build custom clients for your services.

## The Java jax-ws library
In the Java world, the `jax-ws` plugin can be used to create a client skeleton from
a wsdl file which then can be included in your Java code like any other class.

Read more here: https://javaee.github.io/metro-jax-ws/

## SoapUI – the graphical solution
If you prefer a graphical solution over writing your own test clients, have a look
at SoapUI: https://www.soapui.org/
