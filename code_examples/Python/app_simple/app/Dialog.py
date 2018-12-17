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
from spyne.model.fault import Fault

from clfpy import AuthClient, ExtraParameters

# Define the target namespace
TNS = "dialog-app.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Dialog"


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class DialogService(ServiceBase):
    # Note that the class name does not influence the deployment endpoint
    # under which the service will be reachable. It will, however, appear
    # in the wsdl file.

    @srpc(Unicode, Unicode, Unicode, _returns=(Unicode, Unicode),
          _out_variable_names=("status_base64", "result"))
    def showDialog(serviceID, sessionToken, extraParameters):
        """
        Starts the dialog application.
        """
        logging.info("startDialog() called with service ID {}".format(serviceID))

        # Check that the session token is valid and abort with a SOAP fault if
        # it's not. To that end, we use the clfpy library both to extract the
        # authentication endpoint from the extraParameters input argument and
        # to communicate with that endpoint.
        ep = ExtraParameters(extraParameters)
        auth = AuthClient(ep.get_auth_WSDL_URL())
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # The entire application, which will be visible to the user running the
        # workflow, is packed in the status report created in this method.
        # Here, we create a simple HTML page with a button to continue the
        # workflow.
        status = base64.b64encode(create_html_dialog(serviceID, sessionToken,
                                  ep.get_WFM_endpoint()).encode()).decode()
        result = "UNSET"

        return (status, result)

def create_app():
    """Creates an Application object containing the waiter service."""
    app = Application([DialogService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app

# HTML code which is delivered to the workflow manager. In this example, this
# HTML code contains the complete application.
# Important is the JavaScript part with a SOAP request to the workflow
# manager's serviceExecutionFinished() method. With this request, the user
# tells the workflow manager to continue in the workflow.
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


def create_html_dialog(serviceID, sessionToken, wfm_endpoint):
    """Creates a very simple html dialog.
    
    We pack the required parameters for making the request to the workflow
    manager's serviceExecutionFinished method right into this html dialog.
    """
    html = DIALOG.format(
        sid=serviceID,
        stk=sessionToken,
        wfm_endpoint=wfm_endpoint,
        result=RES_B64,
    )

    return html
