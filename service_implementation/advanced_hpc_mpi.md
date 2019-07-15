# How to properly set up Singularity images for MPI applications
_Note:_ This section can greatly benefit from the users. Did you gain some
experience on the topic? Then please consider sharing your insights.

For executing MPI-enabled HPC jobs, you need to call the SemWES HPC service
in the right way (see corresponding documentation
[here](../workflow_creation/HPC_service.md)) and also make proper use of MPI
inside your Singularity container.

For general documentation of using MPI with Singularity, please head over to the
[official Singularity documentation](http://singularity.lbl.gov/docs-hpc).

In an MPI-enabled job execution, your Singularity container will be started
multiple times. To avoid executing the same thing over and over again, your
container will have to make proper use of the environment created by MPI. 
Most importantly, MPI will set environment variables for each process which 
indicate its so-called _rank_ in the entirety of processes. Depending on this
rank, let your container do the different things it has to do.

The [OpenFoam code example](../code_examples/Singularity/openfoam) makes use of
these rank variables to execute the right commands on the right nodes. Have a
look at its source code to see how to access the rank from within a Python
script. Note that even though the code example uses OpenFoam, the MPI mechanics
can easily be adapted for other use cases.

Please also have a look at [How to communicate with a running HPC
job](./advanced_hpc_notifications.md) and the [abortable-waiter code
example](../code_examples/Singularity/abortable_waiter). This should give you a
good first overview of what your container needs beside the MPI functionality.
