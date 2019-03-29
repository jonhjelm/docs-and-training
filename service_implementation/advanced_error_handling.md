# Error handling in SOAP services
On the SemWES platform, all workflows consist of a series of _SOAP calls_ to
the individual web services used in the workflow. If an error occurs during
processing these calls, the corresponding answer is a _SOAP fault_. This fault
message will arrive at the workflow manager and cause the workflow to fail.
Consequently, we should make sure that our SOAP faults are well defined and
contain valuable information for debugging.

**Important:** Currently, the workflow manager does _not_ respect SOAP faults.
Any failing workflow will simply result in an ugly stack trace from inside the
workflow manager without _any_ hint of what caused the error where. Thus, error
handling must be considered broken for now. 

That said, properly defined SOAP faults still help when debugging locally by 
making SOAP calls directly to a service.

## SOAP faults in Python Spyne
When using the `spyne` library in Python, do the following to implement proper
SOAP faults:
1. Create custom exceptions for possible errors based on 
   `spyne.model.fault.Fault`:
   ```python
   from spyne.model.fault import Fault
   
   class MySoapFault(Fault):
       """Nonsensical SOAP fault"""
       pass
   
   class AuthenticationFailedFault(Fault):
       """Raised when the authentication server is available but authentication fails."""
       pass
   ```

2. Add the `_throws` parameter to your function decorations:
   ```python
   @spyne.srpc(Unicode, _returns=Unicode, _out_variable_name="result", _throws=[AuthenticationFailedFault])
   def authenticate(user, password):
       # ... do authentication here ...
       if not authenticated:
           error_msg = "Unable to authenticate user '{}'".format(user)
           raise AuthenticationFailedFault(faultstring=error_msg)
   ```
Make sure to pass error messages to the `faultstring` argument of the 
custom exception (or modify the exception to pass the first parameter
to the `faultstring` parameter of its base class). See also 
http://spyne.io/docs/2.10/reference/model/fault.html.

A fault defined and raised as above will show up in the WSDL service 
description and can thus be handled gracefully by the calling entity.

## SOAP faults in Java EE
In Java, SOAP faults are defined in a very similar way.

1. Create custom exception classes for possible errors:
   ```java
   public class AuthenticationFailedException extends Exception {
    
       private final static String default_message = "403: Authentication failed";
    
       public AuthenticationFailedException() {
           super(default_message);
       }
    
       public AuthenticationFailedException(String message) {
           super(default_message + "; " + message);
       }
    
   }
   ```

2. Add the exceptions to the `throws` clause when defining web methods:
   ```java
   @WebMethod(operationName = "getImageInfo")
       public ImageInformation getImageInfo(
               @WebParam(name = "token", targetNamespace=namespace) String token,
               @WebParam(name = "image_name", targetNamespace=namespace) String image_name
       ) throws AuthenticationFailedException
       {
           // function code here
           if (!authenticated)
               throw AuthenticationFailedException();
       }
   ```
This also makes the fault(s) show up in the service's WSDL description.

## SOAP faults in other languages
Your favourite language is not in the examples above? Why don't you look up
how to create proper SOAP faults and submit example code to the core
platform team? ;-)
