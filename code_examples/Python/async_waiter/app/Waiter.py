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
from flask import Flask
from flask import request
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, Boolean
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
spyne = Spyne(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


# Read environment variables to obtain configuration values
WAITER_LOG_FOLDER = os.environ["WAITER_LOG_FOLDER"]


@app.route('/')
def root():
    """Static page on root to avoid error 404"""
    return 'Nothing to see here.'


class WaiterService(spyne.Service):
    """The actual waiter asynchronous service."""
    __service_url_path__ = '/Waiter'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Integer, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "output_file"))
    def startWaiter(serviceID, sessionToken, secondsToWait=300):
        """Starts a waiter script as a separate process and returns immediately.

        In a more realistic scenario, this is where a longer computation etc.
        would be started as a separate process. Here, we simply start a process
        which waits for a while while regularly updating a status file.
        """

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

        # Spawn new process running the waiter script.
        # We pass the status and result file to the script to ensure that the
        # waiter logs to the correct place.
        command = ['python', 'wait_a_while.py', str(secondsToWait),
                   statusfile, resultfile]
        subprocess.Popen(command)

        # We now create a first status page to be displayed while the
        # workflow is executed. Since the waiter process was only just started,
        # we don't have a proper status yet. So we simply start with an empty
        # progress bar.
        # The status page needs to be base64 encoded.
        status = base64.b64encode(create_html_progressbar(0))
        output_file = "UNSET"

        return (status, output_file)

    @spyne.srpc(Unicode, Unicode, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "output_file"))
    def getServiceStatus(serviceID, sessionToken):
        """Status-query method which is called regularly by WFM.

        Here, a more realistic service would query the status of a calculation
        etc. and process its log files to create a status page. Here, the log
        contains only a single number, which we convert to an html progress
        bar.
        """
        # Create correct file paths from service ID. By using the unique
        # service ID, we can address the right waiter process in case this
        # service is called several times in parallel.
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')

        # Read the current status from the waiter logs. Here, that is only a
        # single number between 0 and 100.
        with open(statusfile) as f:
            current_status = f.read().strip()

        if current_status == "100":
            status = "COMPLETED"
            # Read result page from waiter
            with open(resultfile) as f:
                output_file = f.read()
            return (status, output_file)

        # Note that the interface definition of getServiceStatus() specifies
        # "UNCHANGED" as another option for the return value of
        # 'status_base64'. In this case, the workflow manager will simply
        # continue to display the last status page transmitted. This can be
        # used when the status-page generation in itself is costly.

        # If not finished, create a status page from the current status
        # This could include more post-processing etc. in a more realistic
        # service
        output_file = "UNSET"
        status = base64.b64encode(create_html_progressbar(int(current_status)))
        return (status, output_file)

    @spyne.srpc(Unicode, Unicode, _returns=Boolean,
                _out_variable_name="success")
    def abortService(serviceID, sessionToken):
        """Aborts the currently running service (not implemented, returns false)
        """

        # This method offers the option to abort long-running asynchronous
        # services. In this example, we do not implement this functionality
        # and thus always return False.
        # In a more realistic scenario, this method would terminate the
        # background computation process gracefully.

        return False


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
