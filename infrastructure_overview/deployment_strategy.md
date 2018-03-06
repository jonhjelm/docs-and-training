# The CAxMan service-deployment strategy
In late 2017, the recommended service-deployment method in CAxMan changed from
direct deployment on a VM to a Docker-based solution. Here, we explain the
motivation for this change and answer some of the questions connected to it.

## Motivation to use Docker
The currently recommended way to deploy services in CAxMan is to use Docker
containers. Why that? Consider you're developing a service, and you use some of
the newest features of that fancy library Foo version 9. At the same time, the
VM your service should be deployed on has only Foo version 8.3 available
in its repositories. This leaves you with the choice of either rewriting your
service to fit to the older version of Foo, or manually install the right
version on the VM. So far so good. But what if you're developing not one but
two services which need two different, mutually exclusive versions of Foo or
another tool or library? Or if your local development environment has a
different Linux distribution (of course with slightly different paths,
configurations etc.) than your VM? You might end up spending much more time on
fiddling with the different environments than you do on what you really want:
developing a really cool service.

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

It is noteworthy that Docker is _not_ a virtualization solution. It directly
relies on the host operating system instead of emulating an entirely new host.
This makes it much fast than virtualizations, and starting a Docker container
is often as good as instantaneous.

Another obvious use case for (Docker) containers is load-balancing and
automatic scaling: When many instances of a service run in parallel with
traffic distributed dynamically among them and when these instances should be
automatically spawned or terminated depending on the current demand, a manual
deployment strategy inevitably fails. This is currently not relevant for
CAxMan, but developing (stateless) Docker containers gives compatibility with
such a design for free.

## How to configure a CAxMan VM for Docker?
Convinced that Docker is the way to go? Then the only thing you need to do is
to install Docker on your VM. Either from the host-OS's package repositories
or, if you want the newest version, following an installation guide on the
Docker website.

Once that is done, you're set. You don't need anything else. (You might want to
take a look at the [code examples(../code_examples)] where we keep a list of
up-to-date example services wrapped into fitting Docker containers.)

## How to run several containers behind a single port?
Consider you have a VM which has port 8080 open and available to the public
under `https://<host>/your_company/services`. You have services `Foo` and `Bar`
ready as Docker containers and want to deploy them under
`https://<host>/your_company/services/Foo` and
`https://<host>/your_company/services/Bar`, respectively. Yo start the `Foo`
container and map it to port 8080. But what about `Bar`? How can we make both
`Foo` and `Bar` available under that `.../services` path? If we want to avoid
having a separate path-to-port mapping for every single service we deploy, the
answer is to run a proxy server locally on the VM which takes care of routing
traffic based on the URL path to the correct container. In our example with
`Foo` and `Bar`, we could do the following:
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


        location /sintef/docker_services/waiter {
                proxy_set_header Host $host;
                proxy_pass http://127.0.0.1:8081;
        }
        location /sintef/docker_services/calculator {
                proxy_set_header Host $host;
                proxy_pass http://127.0.0.1:8082;
        }
   }
   ```

With the above in mind, we should always consider whether it's the right thing
at all to run several services on the same VM. For computationally demanding
services, running a single service per VM might often be the best options. For
smaller services which, for example, perform simple pre- or postprocessing
tasks, running them on the same machine can be completely justified.
