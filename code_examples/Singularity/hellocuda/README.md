# Full-featured Singularity example: Hello Cuda
This code example shows how to prepare a Singularity image to execute a very
simple Cuda application. Note that it will most probably not work if the
application uses the driver API of Cuda.  The Singularity image is based on
Ubuntu 18.04 and does not contain anything else than the compiled application.
In order to simplify the build process, the example also contains a
Docker-based build environment, based on the same Linux version.  This will
ensure that the Singularity images contains compatible C libraries.  The
application does not take any arguments, and when executed as a part of a
SemWes workflow, the output from standard out will be reported as the result of
the HPC service.

## Preparing the application
The application folder contains two files:
* `app/startup.sh`: Starts the application and writes to `/service/status.html`
  and `/service/result.txt`
* `app/hellocuda.cu`: Source code of the Cuda application

The startup script is the main entrypoint for executing the Singularity image,
and has the main purpose of redirecting the standard out and standard err of
the application to the service result.  For convenience, it also reports the
output of `nvidia-smi` to the results file.  For more realistic examples of
such scripts, please refer to [abortable demo
example](../abortable_demo_job/README.md).

## Building the image
To build the containers, run `buildSingularityUsingDocker.sh`.  The first step
of the build process is to build the build environment as a Docker image named
cudabuildenv.  This Docker image is in turn used to build the Cuda application.
This build image is rather large, as it contains the full Cuda SDK, and is
therefore not suitable to be used in production.  The next step is therefore to
create the Singularity image from a small image and only copy the needed files
into the Singularity image.  So far, it has been tested with Singularity 2.6.1
locally, and 2.6.0 at IT4I's Anselm cluster.

## Testing the image
Run `test.sh` to execute the container locally.  By default, the container will
be executed without the "--nv" option to Singularity, which may cause it to
execute wrongly.  Execute the test scrip with the "--nv" option to pass it to
singularity.

## Registering the image
Use the [clfpy library's](https://github.com/SemWES/clfpy) command-line
interface to upload and register the image on the SemWES platform.

## Container execution through the HPC service
To execute this image through the HPC service, provide the following parameters:

* `commandline`: `"/app/startup.sh"`

* `parameters`: `""`

* `SingularityVersion`: `"2.6.0"`

Provide also the other required parameters as explained in
[the HPC service documentation](../../../workflow_creation/HPC_service.md).
