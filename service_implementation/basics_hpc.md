# HPC access through the SemWES platform
One of the caveats when it comes to the access and utilization of HPC resources
is vendor specificity. HPC providers usually allow login via SSH with personal
user credentials, have specific queueing systems and specific locations for
file storage. Migrating computations from one HPC provider to another thus
involves substantial adaptations, but usually not so much to the exciting
computation code but rather to the boring managing framework.

The SemWES platform, on the other hand, allows the utilization of HPC
resources through a _generic_ interface, without the need to adapt to the
environment and configuration of a specific HPC provider. The basic concept of
this simplification comprises two main ideas:

1. "Containerization" of the computation software

   On the SemWES platform, all software which should be executed on an HPC
   cluster has to be wrapped into a Singularity image. Similar to Docker (but
   tailored specifically with application in an HPC environment in mind),
   Singularity allows to package software together with all its required
   dependencies into self-contained images, which can be executed anywhere where
   Singularity is installed. Instead of registering a software with each HPC
   provider it should run on (including the adaptations required for each
   specific provider), it is enough to create a Singularity image once and then
   simply run it on several HPC resources.

   Read more on how to [create and register Singulariy images](basics_singularity.md)

2. HPC access through a generic HPC service

   The SemWES platform offers a generic HPC service which serves as an
   interface to an arbitrary HPC resource provider. This completely eliminates
   the need to learn several queueing systems, storage solutions, and acquire
   login credentials for each HPC provider to be used. Instead, all this is
   taken over by the HPC service.

   Learn more how to [integrate the HPC service](../workflow_creation/HPC_service.md)
   in your workflows.
