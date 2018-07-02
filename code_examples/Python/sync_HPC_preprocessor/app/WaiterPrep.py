"""HPC preprocessor for the Waiter HPC example

Example of an HPC preprocessor which takes human-readable input and creates all
parameters the HPC launcher requires.
"""
import os

from spyne import Application, srpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11

# Define the target namespace
TNS = "waiterprep.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "WaiterPrep"


class WaiterPrep(ServiceBase):
    """The waiter preprocessor service

    Implements a single method which will act as the HPC preprocessor for the
    waiter example.

    Note that the class name is _not_ important for the endpoint URL of the
    service (that's defined by __service_url_path__), but it will show up in
    the service WSDL as the service name.
    """
    @srpc(Unicode, # time to wait in seconds
          _returns=(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode),
          _out_variable_names=(
              "imageName", "commandline", "parameters", "queue", "numNodes",
              "numCores", "maxDurationInMinutes"
          ))
    def waiter_prep(seconds_to_wait):
        """Creates all parameters required as input by the HPC launcher.

        Most parameters are hard-coded here, but in other scenarios (for example
        with user-defined input), some more string handling will happen here.
        """
        image_name = "waiter.simg"
        commandline = "python"
        parameters = "/app/wait_a_while.py {}".format(seconds_to_wait)
        queue = "qexp"
        numNodes = os.environ["N_NODES"]
        numCores = os.environ["N_CORES"]
        maxDurationInMinutes = 5

        return (image_name, commandline, parameters, queue, numNodes, numCores,
                maxDurationInMinutes)


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([WaiterPrep], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app
