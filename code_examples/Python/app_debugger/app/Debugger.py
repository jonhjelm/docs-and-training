"""Application for debugging service outputs

CloudFlow application which takes in a bunch of inputs and outputs them without
any changes. Introduces a "breakpoint" in a workflow where all inputs are
displayed.
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
TNS = "app-debugger.sintef.no"
# Define the name under which the service will be deployed
SERVICENAME = "Debugger"


class TokenValidationFailedFault(Fault):
    """Raised when validation of the session token fails"""
    pass


class DebuggerService(ServiceBase):
    # Note that the class name does not influence the deployment endpoint
    # under which the service will be reachable. It will, however, appear
    # in the wsdl file.

    @srpc(
        Unicode, # serviceID
        Unicode, # sessionToken
        Unicode, # extraParameters
        Unicode, # Input 1
        Unicode, # Label 1
        Unicode, # Input 2
        Unicode, # Label 2
        Unicode, # Input 3
        Unicode, # Label 3
        Unicode, # Input 4
        Unicode, # Label 3
        Unicode, # Input 5
        Unicode, # Label 5
        _returns=Unicode,
        _out_variable_name="status_base64")
    def parameterDebugger(serviceID, sessionToken, extraParameters,
        in1="", label1="in1", 
        in2="", label2="in2", 
        in3="", label3="in3", 
        in4="", label4="in4", 
        in5="", label5="in5"):
        """
        Starts the debugger application.
        """
        logging.info("parameterDebugger() called with service ID {}".format(serviceID))

        # Validate token
        ep = ExtraParameters(extraParameters)
        auth = AuthClient(ep.get_auth_WSDL_URL())
        if not auth.validate_session_token(sessionToken):
            logging.error("Token validation failed")
            error_msg = "Session-token validation failed"
            raise TokenValidationFailedFault(faultstring=error_msg)

        # Create application HTML
        html = HTML.format(
            sid=serviceID,
            stk=sessionToken,
            wfm_endpoint=ep.get_WFM_endpoint(),
            eP=extraParameters,
            in1=in1,
            in2=in2,
            in3=in3,
            in4=in4,
            in5=in5,
            label1=label1,
            label2=label2,
            label3=label3,
            label4=label4,
            label5=label5,
            result=RES_B64,
        )

        status = base64.b64encode(html.encode()).decode()

        return status

def create_app():
    """Creates an Application object containing the debugger service."""
    app = Application([DebuggerService], TNS,
                      in_protocol=Soap11(validator='soft'), out_protocol=Soap11())

    return app

# HTML code which is delivered to the workflow manager. In this example, this
# HTML code contains the complete application.
HTML = """<html>
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
    <h2>Variable debugger</h2>
    <h3>General information</h3>
    Service ID: {sid}</br>
    Session Token: {stk}

    <h3>Extra parameters</h3>
    {eP}

    <h3>Variable contents</h3>
    <table>
        <tr>
            <th>Variable</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>{label1}</td>
            <td>{in1}</td>
        </tr>
        <tr>
            <td>{label2}</td>
            <td>{in2}</td>
        </tr>
        <tr>
            <td>{label3}</td>
            <td>{in3}</td>
        </tr>
        <tr>
            <td>{label4}</td>
            <td>{in4}</td>
        </tr>
        <tr>
            <td>{label5}</td>
            <td>{in5}</td>
        </tr>
    </table>
    <input type="button" value="Click to leave debugger and continue workflow" onclick="cont_wf()">
    </div>
</body>
</html>
"""

RES = """<ServiceOutputs>
<status_base64>Finished</status_base64>
</ServiceOutputs>
"""
RES_B64 = base64.b64encode(RES.encode()).decode()
