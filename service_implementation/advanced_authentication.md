# Using authentication services inside a service
The web services you deploy in CloudFlow are by default accessible by the
"outside world". They are deployed under an available URL, and they expose a
SOAP interface that can be interacted with by anyone. For some auxiliary
services, that might be ok, but in most cases you will want to restrict access
to your services to logged-in users.

## Token validation with clfpy
It is highly recommended to use the `clfpy` Python library
(https://github.com/CloudiFacturing/clfpy) to interface with the CloudFlow
authentication manager for token validation. Most code examples available in
this repository do so.

In your service code, make sure to add a `sessionToken` and a `extraParameters`
input argument to your SOAP interface. Then, perform token validation as
follows:
```python
from clfpy import AuthClient, ExtraParameters

# ...

# Assumes that `sessionToken` and `extraParameters` are available as variables.
ep = ExtraParameters(extraParameters)
auth_endpoint = ep.get_auth_WSDL_URL()
auth = AuthClient(auth_endpoint)

if not auth.validate_session_token(sessionToken):
    # Report error here and return from the function
    return # ...

# Continue with the function as normal, everything from here on is protected
#by the token validation.
```
