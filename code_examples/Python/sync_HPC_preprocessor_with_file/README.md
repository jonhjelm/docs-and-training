Python example for an HPC pre-processor
========================================
This is a sample preprocessor service for the HPC launcher.

## Prerequisites
To build, run, and test this  service, you only need to have Docker
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

The other configuration variables are the number of nodes and number of cores to
reserve on the HPC cluster. You can of course define further configuration 
values if needed.

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
docker run -p 80:80 --env-file=env waiterprep
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
./build.sh      # run only once
./run.sh        # run every time you want to test
```

You can make changes to `test_service.py` to test other methods or other
deployment locations. Rebuilding the container is not necessary after such
changes.
