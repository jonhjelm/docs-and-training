import os
import subprocess
import base64
import datetime
from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer

app = Flask(__name__)
spyne = Spyne(app)


@app.route('/')
def root():
    """Static page on root to avoid error 404"""
    return 'Nothing to see here.'


class WaiterService(spyne.Service):
    __service_url_path__ = '/Waiter'
    __in_protocol__ = Soap11(validator='soft')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Integer, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "output_file"))
    def startWaiter(serviceID, sessionToken, secondsToWait=300):
        """Starts a waiter script as a separate process and returns immediately

        This is where a longer computation etc. would be started in a more
        realistic asynchronous service. Here, we simply start a process which
        waits for a while while updating a status file.
        """

        # Create a temporary folder to store the status files in
        waiterdir = os.path.join('/tmp', serviceID)
        if not os.path.exists(waiterdir):
            os.mkdir(waiterdir)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')

        # Spawn new process running the waiter script
        command = ['python', 'wait_a_while.py', str(secondsToWait),
                   statusfile, resultfile]
        subprocess.Popen(command)

        # The process doesn't have a proper status yet, so we start with an
        # empty status bar
        status = base64.b64encode(create_html_progressbar(0))
        output_file = "UNSET"

        return (status, output_file)

    @spyne.srpc(Unicode, Unicode, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "output_file"))
    def getServiceStatus(serviceID, sessionToken):

        # Create correct file paths from service ID
        waiterdir = os.path.join('/tmp', serviceID)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')

        # Read the current status from the waiter logs
        with open(statusfile) as f:
            current_status = f.read().strip()

        if current_status == "100":
            status = "COMPLETED"
            # Read result page from waiter
            with open(resultfile) as f:
                output_file = f.read()
            return (status, output_file)

        # If not finished, create a status page from the current status
        # This could include more post-processing etc. in a more realistic
        # service
        output_file = "UNSET"
        status = base64.b64encode(create_html_progressbar(int(current_status)))
        return (status, output_file)


def create_html_progressbar(progress):
    """Creates a very simple html progress bar"""
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

    return html;
