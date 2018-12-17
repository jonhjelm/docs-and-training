"""HPC preprocessor for the Abortable Waiter HPC example

Example of an HPC preprocessor which takes human-readable input and creates all
parameters the HPC launcher requires.
"""
import os
import logging

from spyne import Application, srpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.model.fault import Fault

from clfpy import AuthClient, ExtraParameters

# Define the target namespace
TNS = "waiterprep.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "WaiterPrep"


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class WaiterPrep(ServiceBase):
    """The waiter preprocessor service

    Implements a single method which will act as the HPC preprocessor for the
    waiter example.

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    @srpc(Unicode, Unicode, Unicode,
          _returns=(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode),
          _out_variable_names=(
              "imageName", "commandline", "parameters", "queue", "numNodes",
              "numCores", "maxDurationInMinutes", "SingularityVersion"
          ))
    def hpcprepWaiter(sessionToken, extraParameters, seconds_to_wait):
        """Creates all parameters required as input by the HPC launcher.

        Most parameters are hard-coded here, but in other scenarios (for example
        with user-defined input), some more string handling will happen here.
        """
        # Validate session token
        ep = ExtraParameters(extraParameters)
        auth = AuthClient(ep.get_auth_WSDL_URL())
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # Prepare parameters the HPC launcher needs
        image_name = "waiter_abortable.simg"
        commandline = "python"
        parameters = "/app/startup.py {} /app".format(seconds_to_wait)
        queue = "qexp"
        numNodes = os.environ["N_NODES"]
        numCores = os.environ["N_CORES"]
        maxDurationInMinutes = 5
        SingularityVersion = "2.4.2"

        return (image_name, commandline, parameters, queue, numNodes, numCores,
                maxDurationInMinutes, SingularityVersion)


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([WaiterPrep], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
