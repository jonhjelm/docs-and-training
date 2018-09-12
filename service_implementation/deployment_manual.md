# Manual container deployment for development use
During development, being "close to the code" is important for easy debugging
and quick development cycles. Therefore, each partner developing services for
the CloudFlow platform will have a dedicated virtual machine set up for this
purpose. On this machine, Docker containers can be built and run manually at
will.

## How to get access to a deployment environment?
During development, each partner will receive access to a small dedicated 
virtual machine (VM). To have a VM set up for you, please contact Robert from
SINTEF (robert.schittny@sintef.no).

You will receive SSH access credentials and the following bits of information:
* `CONTEXT_ROOT`: The URL sub-path path under which the VM will be reachable.
  
  Example: For "Partner A", the context root could be `"partner-a"`, and the VM
  would then be reachable under the URL https://srv.hetcomp.org/partner-a/...

  Note that the context root path needs to be made known to the containers as
  well. All code examples on this documentation center have this path
  configurable.

* `PORT`: Port number under which the platform expects communication to and from
  the VM. This is usually port 8080.

These two definitions will be used as placeholders in the descriptions further
below.

## How to run a single container?
Your VM will have Docker installed and prepared already, so all you have to do
is start a container in the correct way. It is highly recommended to read the
[Docker documentation](https://docs.docker.com/) when doing this manual
deployment.

1. *Get the container image to the VM*

   To copy the container image to the VM, there are two options. Either use a
   public or private [DockerHub](https://hub.docker.com/) repository to push to
   and pull from, or [save, scp, and load the image](https://stackoverflow.com/questions/23935141/how-to-copy-docker-images-from-one-host-to-another-without-via-repository) without a repository.

2. *Run the container*
   
   Assuming the image `myimg:1.0.0` is available on the VM, ssh into the VM and
   run
   ```
   docker run -d -p <PORT>:<ctr_port> [--env-file=env] myimg:1.0.0
   ```
   Here, `<ctr_port>` is the *internal* port of the container (e.g., port 80 for
   a standard webserver) to be forwarded to the *external* `PORT` which is
   routed to the platform domain. The optional `--env-file=env` argument
   specifies an environment-variable file to be used for the container
   environment. `-d` lets the container start in the background.

3. *Check container status*
   
   Use `docker ps` and `docker logs <ID>` to check that the container started
   up properly.

4. *Check service availability*

   Open a browser and open the following URL:
   ```
   https://srv.hetcomp.org/<CONTEXT_ROOT>/<service_name>?wsdl
   ```
   
If everything is configured correctly, you should receive an xml description of
the web service you just deployed (in the web service description language or
wsdl). The wsdl URL can then be used in the workflow editor to [register the
service](../tutorials/workflows/basics_service_registration.md). Once this is
done, the service can be used inside a workflow.

## What if my service cannot be executed as part of a workflow?
It can happen (for services using Python with the Spyne library) that even
though you see a seemingly valid wsdl under an URL similar to the one mentioned
above, the service is not working when being used as part of a workflow. In such
a case, check the wsdl for a section like the following:
```xml
<wsdl:service name="WaiterService">
  <wsdl:port name="WaiterService" binding="tns:WaiterService">
    <soap:address location="http://localhost:8080/nabladot/waiter/Waiter"/>
  </wsdl:port>
</wsdl:service>
```
The SOAP address (pointing to localhost) is obviously wrong, it should begin
with `https://srv.hetcomp./org/...`. The reason for this error is that the
Python Spyne library creates the wsdl from the very first request it receives,
and caches it afterwards. If that request commes from the VM itself (for 
example by using `cURL` to manually test if the service is available), localhost
will be used for creating the SOAP port address.

The simple fix for this problem is to:
1. Kill the container on the VM
2. Restart the container with the same settings as before
3. Open the wsdl URL `https://srv.hetcomp.org/...` in the browser _before_
   making any other requests to the service.

Once this first request using the correct address is made, the correct wsdl will
be cached and available for service execution in a workflow.

## How to run more than one container behind a single port?
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