# Available "global" parameters for CloudFlow services
When executing a workflow, the workflow manager automatically creates a set of
globally available parameters which can be accessed by any service – given that
corresponding input parameters are created and wired correclty in the workflow
editor.

## Available parameters
* `serviceID`: A unique string which is assigned to each service *per execution*.
  Use this string to unambiguously identify an individual execution of your
  service.

  Example: If your service needs to (locally) save some temporary files during
  its execution, the service ID can be used to name such files or a folder
  containing them.

* `sessionToken`: The session token is generated when you log onto the CloudFlow
  portal is the entity which grants you access to the CloudFlow platform. Use
  the session token if your service needs to access other services which require
  authentication (for example [GSS](../infrastructure_overview/storage.md) for 
  file access).

* `extraParameters`: This is a comma-separated string of key-value pairs which
  contains a few more parameters which are intended to help you avoid using
  hard-coded paths to platform services. Specifically, the string looks like
  this (note the trailing comma at the end):
  ```
  "key1=value1,key2=value2,...,keyN=valueN,"
  ```
  Currently, the following parameter keys are included:
  * `"WFM"`: Workflow-manager SOAP endpoint; use this in application-type 
    services which need to call the workflow manager. See the application code
    examples for details.
  * `"gss"`: WSDL URL for GSS. Note that this is not the same as the SOAP 
    endpoint, which is the same as the URL but without the trailing `"?wsdl"`.
    Use this for accessing GSS from within your services.
  * `"phpFileChooser"`: URL to the php file chooser service. Not commonly used
    in service development.
  * `"newWorkflowUrl"`: URL to the portal function which starts a new workflow.
    Not commonly used in service development.
  * `"auth"`: WSDL URL for the authentication manager. Necessary when session
    tokens should be validated inside a service.

## How to access them?
Simply create input parameters `serviceID`, `sessionToken`, and `extraParameters`
for your services. When adding them to a workflow inside the workflow manager,
`sessionToken` and `extraParameters` will be wired automatically. `serviceID`
must always remain unconnected in the workflow editor, the workflow manager will
automatically supply this parameter.
