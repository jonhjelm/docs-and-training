Python example for an asynchronous service
==========================================

This is a very simple example of an asynchronous service written in Python. It
does nothing but to wait for a specified amount of time, but uses the same
concepts and techniques required for wrapping a longer-running calculation in
a SemWES asynchronous service.

It also protects all methods by checking that the supplied session token is
valid.

For details on the implementation, also read the [corresponding
tutorial](../../tutorials/services/python_async_waiter.md).

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
`CONTEXT_ROOT`, defines the deployment path of the app relative to root. In
SemWES, this path is always made up of two elements:
```
CONTEXT_ROOT=/<project>-<service_name>
```
Here, `<project>` is the project name you log in with, and `<service_name>` is
for you to choose. Please note that `<project>-<service_name>` must have a
maximum length of 32 characters and must consist only of lowercase letters,
digits, and hyphens.

You can define further configuration variables which then can be used in the
application source code.

### Build and run
To compile service source code, pack it into a Docker container, and run the
container, run
```
./rebuildandrun.sh
```
The container will listen on port 80 of your machine.

On the first run, this might take a while since the base container images need
to be downloaded and dependencies need to be installed. Subsequent builds will
complete significantly faster.

This run script starts the container in daemon mode, meaning that the command
returns immediately and that logs are not immediately visible.

Alternatively, run the container interactively via:
```
docker run -p 80:80 --env-file=env calculator
```
Again, choose a fitting port number

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
./build.sh                # run only once
./run.sh [start|status]   # run every time you want to test
```

You can make changes to `test_service.py` to test other methods or other
deployment locations. Rebuilding the container is not necessary after such
changes.

Note that you will have to enter your username, project, and password for each
test run in order to obtain a valid session token.

## Use this example as a template
To use this example as a template for your own service development, simply copy
the source code to another location and start editing. To understand the
structure of the code, start with `main.py` and then read `Waiter.py`.
