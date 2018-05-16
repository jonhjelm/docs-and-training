"""Simple application example

TODO: Write something here!
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

    @srpc(Unicode, Unicode, _returns=(Unicode, Unicode),
          _out_variable_names=("status_base64", "result"))
    def startDialog(serviceID, sessionToken):
        """
        TODO: Write something here!
        """
        logging.info("startDialog() called with service ID {}".format(serviceID))

        status = base64.b64encode(create_html_dialog(serviceID, sessionToken).encode()).decode()
        result = "UNSET"

        return (status, result)

def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([DialogService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app


DIALOG = """<html>
<head>
<script type="text/javascript">
var request = new XMLHttpRequest();
function cont_wf() {{
    request.open("POST", "https://api.hetcomp.org/dfki/WorkflowManager2Service/services/SOAP", false);
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
RES = "<ServiceOutputs><result>Dialog finished</result></ServiceOutputs>"
RES_B64 = base64.b64encode(RES.encode()).decode()


def create_html_dialog(serviceID, sessionToken):
    """Creates a very simple html dialog."""
    html = DIALOG.format(
        sid=serviceID,
        stk=sessionToken,
        result=RES_B64,
    )

    return html