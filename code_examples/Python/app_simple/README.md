Python example for a SemWES application
==========================================

This is the simplest possible example of a SemWES application service
written in Python.

It contains a Python-based SOAP service which exposes a single method called
`showDialog`. This method fits the workflow manager's expectations for a
SemWES application and can therefore be registered in the workflow editor.
When called, this method delivers a static HTML website which simply contains
a button to continue the workflow.

## Try it out
The application itself is registered on the CloudiFacturing platform under
`http://demo/apps/showDialog.owl#showDialog_Service`.

An example workflow using this application is registered under
`http://demo/workflow/Demo_Dialog.owl#Demo_Dialog`.

## Prerequisites
To build, run, and test this skeleton service, you only need to have Docker
installed on your machine. All required software is already bundled in Docker
containers.

For further development based on this skeleton, it is highly recommended to
use a local Python environment.

## Configure, build, and run the service
### Configuration
Prior to running the service, have a look at the file `env`. This file defines
environment variables which will be passed into the container. The first one,
`CONTEXT_ROOT`, defines the deployment path of the app relative to root.
Essentially, this needs to be set to the relative path under which the VM
hosting the service is reachable.

You can define further configuration variables which then can be used in the
application source code.

### Build and run
To compile service source code, pack it into a Docker container, and run the
container, run
```
./rebuildandrun.sh
```
The service will listen on port 80 of your machine.

On the first run, this might take a while since the base container images need
to be downloaded and dependencies need to be installed. Subsequent builds will
complete significantly faster.

This run script starts the container in daemon mode, meaning that the command
returns immediately and that logs are not immediately visible.

Alternatively, run the container interactively via:
```
docker run -p 80:80 --env-file=env calculator
```
Again, choose a fitting port number.

### Testing the service
Once the container is running, it can be tested by using its published wsdl
file to create a SOAP webclient and call methods with it.

This example includes a Python-based client application, found in the
`test_client/` folder. If you have a local Python 3.x environment, you can
simply run `python test_service.py` (make sure that all dependencies defined in
`requirements.txt`) are installed. Alternatively, the example includes a Python
Docker container for executing the test client.

To use the Python container, run
```
cd test_client
./build.sh      # run this only once
./run.sh        # run this every time you want to test
```
Note that for every run, you will be asked to enter your username, project, and
password.

The results of the test will be written into the file `test.html`, which you
can open in any browser. Note that the button on the HTML page will _not_ work,
since this test page has not been created from within a running workflow.

You can make changes to `test_dialog.py` to test other methods or other
deployment locations. Rebuilding the container is not necessary after such
changes.

## Use this example as a template
To use this example as a template for your own service development, simply copy
the source code to another location and start editing. To understand the
structure of the code, start with `main.py` and then read `Dialog.py`.
