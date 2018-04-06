# Packaging software in Singularity images
Singularity is a container solution similar to Docker, but with the specific
needs of HPC environments in mind. For example, while Docker containers always 
run with root privileges (which cannot be allowed on an HPC cluster for obvious
security reasons), Singularity containers run only with the rights of the user
that executes the container.

On the CloudFlow platform, all software that should be run on an HPC cluster
_has to be packaged in a Singularity image_. This packaging involves the
following steps:

1. Write a _Singularity build recipe_ (analogously to a Dockerfile) which
   * 
   * contains all required computation software
   * 
2. 