# Logging and debugging for HPC applications
Debugging HPC jobs running in SemWES can be difficult. The jobs run as
Singularity containers on a cluster not directly accessible, "hidden" behind
several abstraction layers of the SemWES platform.

To make the development and debugging of Singularity images as smooth as 
possible, here are a few hints:
1. When the SemWES HPC service executes a Singularity image on an HPC
   cluster, it pipes all stdout and stderr output to a log file which is written
   to the corresponding HPC storage. Via GSS, this file will be available under 
   `<storage_identifier>/home/hpc_logs/<timestamp>_<service_ID>.log`, where the
   timestamp marks the start time of the job execution. Use the file-browser
   workflow or a GSS library to access and view this file.

   Example for the IT4I Anselm cluster: `it4i_anselm://home/hpc_logs/2018-06-29_14_52_08_bff13094b0988e404713177921198f5f_0.log`

2. Test locally before deployment. When developing a Singularity image, make
   sure to locally test the image before uploading and registering it with the
   HPC service. See the [article on Singularity images](./basics_singularity.md)
   for details.

3. Get an IT4I account for testing and development. While you will have to
   register your image via the SemWES platform to include it in a workflow,
   it can be very helpful to be able to run the image directly on the cluster
   for testing purposes. Contact IT4I if you would like to have an account.
