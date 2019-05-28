"""HPC preprocessor for an HPC demo job

Example of an HPC preprocessor which takes a file and a text input and creates
the necessary parameters for the HPC service.
"""
import os
import logging

from spyne import Application, srpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.model.fault import Fault

from clfpy import AuthClient, ExtraParameters

# Define the target namespace
TNS = "prepwithfile.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "PrepWithFile"


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class PrepWithFile(ServiceBase):
    """The preprocessor service

    Implements a single method which will act as the HPC preprocessor.

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    @srpc(Unicode, Unicode, Unicode, Unicode,
          _returns=(Unicode, Unicode, Unicode, Unicode, Unicode),
          _out_variable_names=(
              "commandline", "parameters", "queue", "numNodes",
              "numCores"
          ))
    def hpcPrepWithFile(sessionToken, extraParameters, filepath, textinput):
        """Creates parameters required as input by the HPC launcher.
        """
        # Validate session token
        ep = ExtraParameters(extraParameters)
        auth = AuthClient(ep.get_auth_WSDL_URL())
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # Prepare parameters the HPC launcher needs
        commandline = "python"
        parameters = "/app/startup.py {} {}".format(filepath, textinput)
        queue = "qexp"
        numNodes = os.environ["N_NODES"]
        numCores = os.environ["N_CORES"]

        return (commandline, parameters, queue, numNodes, numCores)


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([PrepWithFile], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
