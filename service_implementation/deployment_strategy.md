# The CloudFlow service-deployment strategy

## Motivation to use Docker
Services in the CloudFlow platform are deployed using Docker containers. Why
that? Consider you're developing a service, and you use some of the newest
features of that fancy library Foo version 9. At the same time, the VM your
service should be deployed on has only Foo version 8.3 available in its
repositories. This leaves you with the choice of either rewriting your service
to fit to the older version of Foo, or manually install the right version on the
VM. So far so good. But what if you're developing not one but two services which
need two different, mutually exclusive versions of Foo or another tool or
library? Or if your local development environment has a different Linux
distribution (of course with slightly different paths, configurations etc.) than
your VM? You might end up spending much more time on fiddling with the different
environments than you do on what you really want: developing a really cool
service.

Enter Docker. A Docker container simply encapsulates the complete environment
(libraries, software and their configuration in specific versions) a service
needs (and of course the service itself) into a single, portable image. This
image can run as-is and out of the box wherever Docker is installed. It can
easily be run several times in parallel, maybe with slightly different
configurations. Several versions of an image (with different library versions
etc.) can run in parallel just as well. It's a bring-your-own-environment
party, completely independent from the specifics of the host system. This also
encourages to develop local and only deploy remotely. If it runs locally, it
will run remotely just as well.

Another obvious use case for (Docker) containers is load-balancing and
automatic scaling: When many instances of a service run in parallel with
traffic distributed dynamically among them and when these instances should be
automatically spawned or terminated depending on the current demand, a manual
deployment strategy inevitably fails.

It is noteworthy that Docker is _not_ a virtualization solution. It directly
relies on the host operating system instead of emulating an entirely new host.
This makes it much fast than virtualizations, and starting a Docker container
is often as good as instantaneous.

## How to deploy
The exact deployment procedure is described in the [service-deployment
manual](./deployment_automated.md).
