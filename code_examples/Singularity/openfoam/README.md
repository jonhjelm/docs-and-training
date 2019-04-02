# Full-featured Singularity example: Openfoam calculation

This code example shows how to prepare a Singularity image to carry out
Openfoam MPI calculations.
Following this tutorial, you'll be able to launch an Openfoam calculation
choosing the case folder and the number of processors to be used, check the
advancement in a webpage and abort the calculation if needed.

## Preparing the application

The logic of the application is similar to the abortable waiter example.
Before starting the simulation, the log_crawler and the notifications monitor
are started, along the domain decomposition.

The code of this example is structured as follows:

* `app/log_crawler.py`: processes the solver log file

* `app/notifications_monitor.py`: interface for incoming messages

* `app/startup.py`: main entrypoint for the Singularity image

  This is the main entrypoint for executing the Singularity image. This script
  performs the following main steps:
  1. It starts the log-crawler script as a background process.
  2. It starts the notification monitor as a background process.
  3. It executes the domain decomposition, the main calculation and the domain
     reconstruction.

Since N instances of `startup.py` are executed, the rank has to be retrieved. This
is done by retrieving the value of the environment variable `PMIX_RANK`.
The rank is necessary since a few tasks are accomplished only by the root process,
while only the actual calculation is executed by all the instances launched.

For details, read the code directly, it comes with detailed in-code documentation.

## Building the image

To build the container, run `build.sh`.

The recipe is contained in the file `openfoam.def`.
The container is built with Singularity 2.5; it is based on Ubuntu 18.04 and includes
OpenFoam 5.

Keep in mind that to make Openfoam work inside the container, three files of
Openfoam and Singularity installation are to be modified. That's why the files in the
folder `openfoam_mod` are included in the container.

Eventually, Openfoam image can be pulled from the official Openfoam Docker hub.
You can choose, for example, a newer Openfoam version.

If you want to test this image, modify the recipe. Keep in mind that, possibly,
you won't need to update files in the `openfoam_mod` folder.

## Testing the image

Run `test.sh` to execute the container locally, after adding the required parameters
as shown in the file.

Note that the complete command line to execute an MPI Openfoam calculation through a
Singularity container is shown.

## Registering the image

Run `python register.py` (after adding your credentials in the file) to upload
and register the image on the CloudFlow platform. Make sure that you have the
[clfpy library](https://github.com/CloudiFacturing/clfpy) installed.

## Container execution through the HPC service

To execute this image through the HPC service, provide the following parameters:

* `commandline`: `"python3"`

* `parameters`: `"/app/startup.py SOLVER FOLDER NP"`

* `MPILibrary`: `"OpenMPI/2.1.1.-GCC-6.3.0-2.27"`

* `SingularityVersion`: `"2.5.1"`

Provide also the other required parameters as explained in
[the HPC service documentation](../../../workflow_creation/HPC_service.md).

Parameters listed above give a working configuration if your container is built with
the given version of Singularity, Ubuntu and Openfoam. You could change one  or all of
these settings, but in this case is up to you to verify that your container is compatible
with the cluster environment.
