"""Simple asynchronous-service example: a waiter service

This example implements a very simple asynchronous CloudFlow service. When
called, it starts a background task which does nothing but waiting while
periodically updating a status file. The service's getServiceStatus()
method, which is called periodically by the workflow manager, reads this
status file and generates a status html page from it, which is displayed
during workflow execution.
"""
import os
import subprocess
import base64
import datetime
import logging

from spyne import Application, rpc, ServiceBase, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11
from spyne.model.fault import Fault

from clfpy import AuthClient, ExtraParameters

# Define the target namespace
TNS = "waiter.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Waiter"

# Read environment variables to obtain configuration values
WAITER_LOG_FOLDER = os.environ["WAITER_LOG_FOLDER"]


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class WaiterService(ServiceBase):
    """The actual waiter asynchronous service."""
    # Note that the class name does not influence the deployment endpoint
    # under which the service will be reachable. It will, however, appear
    # in the wsdl file.

    # We use the @rpc decorator here (instead of @srpc like in the Calculator
    # example) to have access to Spyne's context argument 'ctx'. Via that
    # context, we can access class properties (used here to save the
    # authentication-manager endpoint).
    @rpc(Unicode, Unicode, Unicode, Integer, _returns=(Unicode, Unicode),
          _out_variable_names=("status_base64", "result"),
          _throws=[TokenValidationFailedFault])
    def startWaiter(ctx, serviceID, sessionToken, extraParameters, secondsToWait):
        """Starts a waiter script as a separate process and returns immediately.

        In a more realistic scenario, this is where a longer computation etc.
        would be started as a separate process. Here, we simply start a process
        which waits for a while while regularly updating a status file.
        """
        logging.info("startWaiter() called with service ID {}".format(serviceID))

        # Check that the session token is valid and abort with a SOAP fault if
        # it's not. To that end, we use the clfpy library both to extract the
        # authentication endpoint from the extraParameters input argument and
        # to communicate with that endpoint. We also save the authentication-
        # manager endpoint in a class property which we can re-use in methods
        # that don't have the extraParameters as an argument.
        ep = ExtraParameters(extraParameters)
        auth = AuthClient(ep.get_auth_WSDL_URL())
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # Add default value for waiting time
        if secondsToWait is None:
            logging.info("Setting default value for waiting time")
            secondsToWait = 60

        # Create a temporary folder to store the status files in.
        # Note that we use the service ID as a unique identifier. Since this
        # service is stateless, subsequent calls to getServiceStatus() need to
        # be able to read the correct status files. (The service can be started
        # several times in parallel.)
        # In a more realistic setting, one would set up log directories for a
        # computation here.
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        if not os.path.exists(waiterdir):
            os.mkdir(waiterdir)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')

        # Store the auth-manager WSDL URL in a file for later use in
        # getServiceStatus()
        wsdlfile = os.path.join(waiterdir, 'wsdl.txt')
        with open(wsdlfile, 'w') as f:
            f.write(ep.get_auth_WSDL_URL())
        logging.info("Stored auth-manager WSDL URL: {}".format(ep.get_auth_WSDL_URL()))

        # Spawn new process running the waiter script.
        # We pass the status and result file to the script to ensure that the
        # waiter logs to the correct place.
        logging.info("Starting waiter script")
        command = ['python', 'wait_a_while.py', str(secondsToWait),
                   statusfile, resultfile]
        subprocess.Popen(command)

        # We now create a first status page to be displayed while the
        # workflow is executed. Since the waiter process was only just started,
        # we don't have a proper status yet. So we simply start with an empty
        # progress bar.
        # The status page needs to be base64 encoded.
        status = base64.b64encode(create_html_progressbar(0).encode()).decode()
        result = "UNSET"

        return (status, result)

    @rpc(Unicode, Unicode, _returns=(Unicode, Unicode),
          _out_variable_names=("status_base64", "result"))
    def getServiceStatus(ctx, serviceID, sessionToken):
        """Status-query method which is called regularly by WFM.

        Here, a more realistic service would query the status of a calculation
        etc. and process its log files to create a status page. Here, the log
        contains only a single number, which we convert to an html progress
        bar.
        """
        logging.info("getServiceStatus() called with service ID {}".format(serviceID))

        # Create correct file paths from service ID. By using the unique
        # service ID, we can address the right waiter process in case this
        # service is called several times in parallel.
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')

        # Read wsdl URL from a file
        wsdlfile = os.path.join(waiterdir, 'wsdl.txt')
        with open(wsdlfile) as f:
            auth_wsdl = f.read().strip()

        logging.info("Read WSDL: {}".format(auth_wsdl))

        # Check that the session token is valid
        auth = AuthClient(auth_wsdl)
        logging.info("AuthClient created, validating session token")
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)
        logging.info("Token validation succeeded")

        # Read the current status from the waiter logs. Here, that is only a
        # single number between 0 and 100.
        with open(statusfile) as f:
            current_status = f.read().strip()
        logging.info("Status file read")

        if current_status == "100":
            logging.info("Waiting completed")
            status = "COMPLETED"
            # Read result page from waiter
            with open(resultfile) as f:
                result = f.read()
            return (status, result)

        # Note that the interface definition of getServiceStatus() specifies
        # "UNCHANGED" as another option for the return value of
        # 'status_base64'. In this case, the workflow manager will simply
        # continue to display the last status page transmitted. This can be
        # used when the status-page generation in itself is costly.

        # If not finished, create a status page from the current status
        # This could include more post-processing etc. in a more realistic
        # service
        logging.info("Waiting not done yet")
        result = "UNSET"
        status = base64.b64encode(create_html_progressbar(int(current_status)).encode()).decode()
        return (status, result)

    @rpc(Unicode, Unicode, _returns=Boolean, _out_variable_name="success")
    def abortService(ctx, serviceID, sessionToken):
        """Aborts the currently running service (not implemented, returns false)
        """
        logging.info("abortService() called with service ID {}".format(serviceID))

        # We obtain the authentication-manager endpoint from a class property
        # and check that the session token is valid
        # Read wsdl URL from a file
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        wsdlfile = os.path.join(waiterdir, 'wsdl.txt')
        with open(wsdlfile) as f:
            auth_wsdl = f.read().strip()

        auth = AuthClient(auth_wsdl)
        if not auth.validate_session_token(sessionToken):
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # This method offers the option to abort long-running asynchronous
        # services. In this example, we do not implement this functionality
        # and thus always return False.
        # In a more realistic scenario, this method would terminate the
        # background computation process gracefully.

        return False


def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([WaiterService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app


def create_html_progressbar(progress):
    """Creates a very simple html progress bar.

    In a more realistic scenario, any kind of log/calculation status processing
    could happen here.
    """
    max_width = 800
    relative_progress = progress/100.0 * max_width

    html = "<html>\n" + \
        "<head>\n" + \
        "<title>Waiter status</title>\n" + \
        "</head>\n" + \
        "<body style=\"margin: 20px; padding: 20px;\">\n" + \
        "<h1>Waiter status at " + datetime.datetime.now().strftime('%H:%M:%S') + "</h1>\n" + \
        "<div style=\"border-radius: 5px; border-color: lightblueblue; border-style:dashed; width: " + str(max_width) + "px; height: 80px;padding:0; margin: 0; border-width: 3px;\">\n" + \
        "<div style=\"position: relative; top: -3px; left: -3px; border-radius: 5px; border-color: lightblue; border-style:solid; width: " + str(relative_progress) + "px; height: 80px;padding:0; margin: 0; border-width: 3px; background-color: lightblue;\">\n" + \
        "<h1 style=\"margin-left: 20px;\" >" + str(progress) + "%</h1>\n" + \
        "</div>\n" + \
        "</div>\n" + \
        "</head>\n" + \
        "</body>"

    return html
