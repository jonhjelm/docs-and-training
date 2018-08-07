"""Simple application example

Extremely simple CloudFlow application example, implementing a graphical dialog
to request user input.
"""
import os
import subprocess
import base64
import datetime
import logging

from spyne import Application, srpc, ServiceBase, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11

# Define the target namespace
TNS = "app-dialog.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Dialog"


class DialogService(ServiceBase):
    # Note that the class name does not influence the deployment endpoint
    # under which the service will be reachable. It will, however, appear
    # in the wsdl file.

    @srpc(Unicode, Unicode, Unicode, _returns=(Unicode, Unicode),
          _out_variable_names=("status_base64", "result"))
    def startDialog(serviceID, sessionToken, extraParameters):
        """
        Starts the dialog application.
        """
        logging.info("startDialog() called with service ID {}".format(serviceID))

        eP_parsed = parse_extra_parameters(extraParameters)

        status = base64.b64encode(create_html_dialog(serviceID, sessionToken, eP_parsed).encode()).decode()
        result = "UNSET"

        return (status, result)

def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([DialogService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app

# HTML code which is delivered to the workflow manager. In this example, this
# HTML code contains the complete application.
DIALOG = """<html>
<head>
<script type="text/javascript">
var request = new XMLHttpRequest();
function cont_wf() {{
    request.open("POST", "{wfm_endpoint}", false);
    request.setRequestHeader("Content-Type", "text/xml");
    request.setRequestHeader("SOAPAction", "");
    var request_body = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:wor=\"http://www.eu-cloudflow.eu/dfki/WorkflowManager2/\">' +
                       '  <soapenv:Header />' +
                       '  <soapenv:Body>' +
                       '    <wor:serviceExecutionFinished>' +
                       '    <serviceID>{sid}</serviceID>' +
                       '    <sessionToken>{stk}</sessionToken>' +
                       '    <xmlOutputs_base64>{result}</xmlOutputs_base64>' +
                       '    </wor:serviceExecutionFinished>' +
                       '  </soapenv:Body>' +
                       '</soapenv:Envelope>';
	try {{
        request.send(request_body);
    }} catch (exception) {{
        alert(exception);
    }}
}}
</script>
</head>
<body>
    <div style="padding: 30px;">
    <h2>A simple dialog</h2>
    <input type="button" value="Click to continue" onclick="cont_wf()">
    </div>
</body>
</html>
"""

# The service outputs to be included in the SOAP request to the workflow manager
RES = "<ServiceOutputs><result>Dialog finished</result></ServiceOutputs>"
RES_B64 = base64.b64encode(RES.encode()).decode()


def create_html_dialog(serviceID, sessionToken, eP):
    """Creates a very simple html dialog."""
    html = DIALOG.format(
        sid=serviceID,
        stk=sessionToken,
        wfm_endpoint=eP["WFM"],
        result=RES_B64,
    )

    return html


def parse_extra_parameters(extra_pars):
    """Parses an extra-parameters string into a dict.

    The extra parameters as delivered from the workflow manager are encoded in
    a single string of the format "key1=value1,key2=value2,key3=value3,...".
    Important: The string contains another comma at the very end.
    """
    print(extra_pars)
    return {pair.split('=')[0]: pair.split('=')[1] for pair in
            extra_pars.split(',')[:-1]}