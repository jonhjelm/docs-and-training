Java skeleton for a synchronous service
=======================================

This is a bare-bone skeleton of a Java synchronous-service application, wrapped
in a Docker container.

## Prerequisites
You only need to have Docker installed on your machine, all the rest is handled by Docker containers.

## Build, configure, and run the service
### Build
To compile service skeleton's source code and pack it into a Docker container, run
```
./build.sh
```

This will trigger a Java maven Docker container which compiles the source code.
On the first run, this will take a while, since first the container has to be
downloaded and then all necessary Java dependencies need to be installed.
Afterwards, build times will be reduced tremendously.

Afterwards, docker is called to build an image out of the compiled source code.

### Configuration
Prior to running the service, have a look at `env_template`. This file defines
environment variables which will be passed into the container. The first one,
`CONTEXT_ROOT`, defines the deployment path of the app relative to root. This
service defines the webservice `SyncExample` and has a default configuration of
`CONTEXT_ROOT=/sintef/examples/syncservice`. This means that the web service
will later be reachable under
`<hostname>/sintef/examples/syncservice/SyncExample?wsdl`.

The rest of the file contains further configuration variables which will can be
used in the application source code.

### Running
To run the container locally, simply execute
```
./run.sh
```

Alternatively, run
```
docker run -p 8080:8080 --env-file=env_template skeleton_syncservice
```

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
./run.sh
```

You can make changes to `test_service.py` to test other methods or other
deployment locations. Rebuilding the container is not necessary after such
changes.
