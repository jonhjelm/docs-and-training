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

## How to deploy Docker containers in CloudiFacturing?
Service deployment in CloudiFacturing comes in two flavours: development
deployment and production deployment.

### Development deployment
During development, being "close to the code" is important for easy debugging
and quick development cycles. Therefore, each partner developing services for
the CloudFlow platform will have a dedicated virtual machine set up for this
purpose. On this machine, Docker containers can be built and run manually at
will.

#### How to run more than one container behind a single port?
The development VM will have one of its ports routed to a publicly available
path (currently `https://srv.hetcomp.org/<some_path>`). Consider your VM has
port 8080 open and available to the public under
`https://srv.hetcomp.org/your_company/services`. You have services `Foo` and
`Bar` ready as Docker containers and want to deploy them under
`https://srv.hetcomp.org/your_company/services/Foo` and
`https://srv.hetcomp.org/your_company/services/Bar`, respectively. You start
the `Foo` container and map it to port 8080. But what about `Bar`? How can we
make both `Foo` and `Bar` available under that `.../services` path? If we
want to avoid having a separate path-to-port mapping for every single service
we deploy, the answer is to run a proxy server locally on the VM which takes
care of routing traffic based on the URL path to the correct container. In
our example with `Foo` and `Bar`, we could do the following:
1. Deploy container `Foo` at port 8081, listening to
   `.../your_company/services/Foo`.
2. Deploy container `Bar` at port 8082, listening to
   `.../your_company/services/Bar`.
3. Run an nginx server on the VM which listens at port 8080 and routes traffic
   to `Foo` and `Bar` with the following configuration:
   ```
   server {
        listen 8080;
        listen [::]:8080;


        location /your_company/services/Foo {
                proxy_set_header Host $host;
                proxy_pass http://127.0.0.1:8081;
        }
        location /your_company/services/Bar {
                proxy_set_header Host $host;
                proxy_pass http://127.0.0.1:8082;
        }
   }
   ```

### Production deployment
Once service development is completed, deployment happens in a more
automated fashion including load balancing and automatic scaling of the
services. Also port handling is done automatically there.

**TODO** Add more content here
