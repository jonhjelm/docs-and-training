# Service-deployment manual
In CloudFlow, services are deployed in a highly automated fashion. As a
developer, you will not have to manually start and stop Docker containers. You
also won't have to (in fact, you cannot) log into the VM where your services
will be running. This manual describes all necessary steps for deploying and
monitoring your services.

## Prerequisites
### Where are services deployed?
While you won't have to manually deploy your services, you have to know _where_
they are deployed, such that you can register them in the workflow editor.
Once deployed, all services are available under the following deployment path:
```
https://srv.hetcomp.org/<project>-<service_name>
```
Here, `<project>` is the project name you log in with into the CloudFlow
portal. For experiment partners, this is most likely `"experiment_#"`.
`<service_name>` is a name that you choose when creating a new service.

### Do I have to configure my service for being deployed?
Yes, you do. You have to tell your service the `/<project>-<service_name>` bit
of the previous section, such that the service knows under which path it needs
to listen for incoming requests.

In all code examples in this repository, this sub-path is called the
`CONTEXT_ROOT`, and is configurable via an environment variable.

As an example, if you log in with the project name `experiment_2`, and you
create a service with the name `hpc-preprocessor`, your service would have to
listen under the path `/experiment_2-hpc-preprocessor`.

### Are there restrictions for the service names?
Yes. Service names have to
* begin with a lower-case letter,
* contain only lower-case letters (`a-z`), numbers (`0-9`), and hyphens,
* end with a lower-case letter or number (but not with a hyphen),
* have at most 32 characters, including the `<project>-` prefix.

### What is the interface for service deployment?
In CloudFlow, the platform service `servicectl` takes care of the automatic
service deployment. It is a RESTful web service deployed under:
```
https://api.hetcomp.org/servicectl-1/
```
Additionally, the CloudFlow Python library clfpy
(https://github.com/CloudiFacturing/clfpy) comes with a client for servicectl
for programmatic access as well as with an interactive command-line interface.
In the examples given here, usage of both the clfpy client and the command-line
interface (CLI) will be demonstrated.

### Where are code examples?
For a minimal example of creating, deploying, monitoring, and deleting a
service, check the test scripts in the clfpy library
(https://github.com/CloudiFacturing/clfpy):
* `test_services_create.py`: Creates and deploys a new service (requires
  Docker container source code to build from)
* `test_services_status_and_logs.py`: Prints status and log information for a
  running service
* `test_services_delete.py`: Deletes the created service

Alternatively, read the rest of this article for step-by-step instructions and
examples.

## Creating and starting a new service
The creation of a new service contains the following steps:
1. Create a new, empty, and non-active service. This will set up all the
   necessary "wiring" behind the scenes and also create a Docker repository for
   the service.
2. Obtain Docker login credentials for the service's repository
3. Push a Docker image to the service's repository
4. Update the service with a service definition. This will trigger the Docker
   image to be pulled and started.

Afterwards, the service's status and log files can be monitored, see the next
sections for details.

In the following sub-sections, the four steps above will be explained in
detail, with code stubs using the clfpy library for every step. For all API
calls, a valid CloudFlow session token is required which can also be acquired
using the clfpy library. Here, it is assumed that such a token is stored in the
environment variable `CFG_TOKEN`.

### 1 Create a new, empty service
#### clfpy services client
To create a new, empty service, one only needs to choose a name and call the
`create_new_service()` method of clfpy's services client:
```python
import os

import clfpy

interface_url = 'https://api.hetcomp.org/servicectl-1/'
token = os.environ['CFG_TOKEN']
name = 'test-service'

srv = clfpy.ServicesClient(interface_url)
r = srv.create_new_service(token, name)
```
The response object, `r`, is a Python `dict`:
```python
>>> pprint(r)
{'links': [{'href': '/services/test-service', 'rel': 'self'},
           {'href': 'https://srv.hetcomp.org/cloudifacturing-test-service',
            'rel': 'deployment'}],
 'name': 'test-service'}
```
The response object contains links to the service itself (as a relative link
within the services-client API) as well as to the deployment URL where the
service will be reachable once it's deployed.

#### clfpy CLI
Make sure you have the latest version of the clfpy library installed. (You can
execute `pip install --upgrade clfpy` to do so.) The library provides an
executable named `clfpy_cli` which should be available from the console after
installation.

Log into the CloudFlow platform bei either simply starting `clfpy_cli` (you
will be asked for your user credentials), or set the environment variables
`CFG_USER`, `CFG_PROJECT`, and `CFG_PASSWORD` before starting `clfpy_cli`.

Select the services client inside the CLI:
```
client services
```
The CLI prompt will change to `user@project – SERVICES: `.
Note that the CLI allows tab completion of most commands and provides help for
all commands. Execute `help` for details.

Then, create a new service with the following command:
```
create_new test-service
```
Answer with "N" to the question on a custom health check.

Afterwards, use the command `ls` (list) to see your currently registered
services and their deployment URLs.

### 2 Obtain Docker login credentials
#### clfpy services client
The following snippet assumes that it is run after the snippet in the previous
section.
```python
creds = srv.get_docker_credentials(token, name)
```
This returns a Python `dict` in `creds`, where Docker credentials are stored for the repository created
together with the new service. `creds` contains the following elements:
* `repo_uri`
* `proxy_endpoint`
* `user`
* `password`

#### clfpy CLI
In the CLI, this step is performed automatically when you push a Docker image
to a service's repository.

### 3 Push a Docker image to the service repository
#### clfpy services client
With the elements in the `creds` object mentioned above, you can perform the
following sequence of Docker commands to build, tag, and push a Docker image
to the service repository:
```
docker login -u <user> -p <password> <proxy_endpoint>
docker build -t somename:sometag .
docker tag somename:sometag <repo_uri>:sometag
docker push <repo_uri>:<sometag>
docker logout <proxy_endpoint>
```
We recommend, however, to use the convenience methods offered by the services
client, which will automatically perform the above steps for you:
```python
docker_source_folder = '/path/to/a/folder/containing/a/Dockerfile'
srv.build_and_push_docker_image(token, name, docker_source_folder, creds)
```
In case you want to assign a different Docker tag name than `latest` to your
image, add the tag as an optional keyword argument:
```python
docker_source_folder = '/path/to/a/folder/containing/a/Dockerfile'
srv.build_and_push_docker_image(token, name, docker_source_folder, creds, tag='1.1.0')
```

#### clfpy CLI
Execute the following command (replace the place holder with the path to the
Docker source folder):
```
push_docker_image test-service <docker_source_folder>
```
You will see the output of Docker within the CLI, which will automatically
build, tag, and push the Docker image in the folder you provided. Note that the
CLI currently always tags your images with `latest`. If you want to use custom
tags, you need to use the clfpy services client.

### 4 Update the service with a service definition
#### clfpy services client
The following snippet updates a service, which triggers currently running
instances of the service to be stopped and replaced by a new instance. This
new instance can have a new Docker image, or simply new configuration
parameters.
section.
```python
project = 'cloudifacturing'
service_definition = {
    "container-tag": "latest",
    "memory-reservation": 100,
    "memory-limit": 150,
    "container-port": 80,
    "environment": [
        {"name": "CONTEXT_ROOT", "value": "/{}-{}".format(project, name)}
    ]
}
pprint(srv.update_service(token, name, service_definition))
```
The service-definition object requires the following fields:
* `container-tag` (string): Which Docker image tag to use for the service. If
  no tag was given when pushing Docker images to the service repository, use
  `'latest'` here.
* `memory-reservation` (int): The amount of memory reserved for the service on
  the hosting VM. Make sure to set this to the lowest realistic number, as it
  affects how many services can be started on a single VM, and thus how many
  VMs need to be available for hosting CloudFlow services. (You as a user won't
  see anything of these VMs.) Use the `docker stats` command locally to
  determine how much your service needs. Note that this is not a hard limit, so
  the service will be allowed to allocate more memory.
* `memory-limit` (int): Hard memory limit. If the service tries to allocate
  more than this limit, it will be forcefully killed. Use this number to
  accomodate for memory-usage spikes your service might have.
* `container-port` (int): HTTP port the container listens to for incoming
  connections. For Python-based services using the spyne library (holds for all
  Python code examples), this is usually port 80. For the Java-based code
  examples, this is usually port 8080.
* `environment` (list of dicts): List of dicts with `name`-`value` pairs which
  define the environment variables set to configure the service. Corresponds to
  the `--env-file` argument to the `docker run` command. If you have
  environment files defined for your service (for example for local testing),
  you can also create the `environment` dict with the `read_env_file()` method
  of the services client:
  ```
  service_definition = {
      # ...
      'environment': srv.read_env_file(path_to_env_file)
  }
  # ...
  ```

Note: In the example above, the environment variable `CONTEXT_ROOT` is set to
`/<project>-<service-name>`. This corresponds directly to the deployment URL
returned when creating the service (section 1 above). It is important to tell
the Docker container to listen for connections on the same route as where the
service is deployed. Otherwise, no connections will ever reach the service.

#### clfpy CLI
The CLI performs the setup of the service definition for you after the
following command:
```
update test-service
```
You will be asked for memory reservation, memory limit, container port, and the
path to an environment-definition file. See section above for explanations of
these parameters.

## Listing available services
#### clfpy services client
The following method prints a list of all available services:
```
>>> srv.print_service_list(token)

2 services currently available:
newservice-5
  Deployment path: https://srv.hetcomp.org/cloudifacturing-newservice-5
test-service
  Deployment path: https://srv.hetcomp.org/cloudifacturing-test-service
```
Note that all services known to CloudFlow for the current project are listed,
even if these services have never been started or if their repositories don't
contain any Docker images.

If you want to have a service list which is programmatically processable, use
the following method instead to receive a list of Python objects instead of a
printed list:
```python
r = srv.list_services(token)
```

#### clfpy CLI
Execute the `ls` command.

## Monitoring a service's status
#### clfpy services client
To check whether a service has started correctly, you can obtain a detailed
status report:
```
>>> srv.print_service_status(token, name)

Status report for service newservice:
Service status: ACTIVE
Desired count: 1
Running count: 1
Pending count: 0

Tasks:
86b40ed8-ce68-4350-b2fd-80be3887c2dd
  Created: 2018-12-10 08:08:06
  Desired status: RUNNING
  Last status: RUNNING

  Task definition:
    Name: cloudifacturing-newservice
    Revision: 5
    Status: ACTIVE
    Container image: 400389127564.dkr.ecr.eu-central-1.amazonaws.com/cloudifacturing-newservice:latest
    Container memory reservation: 100
    Container memory limit: 150
    Container port: 80

Last events:
2018-12-10 08:08:43: (service cloudifacturing-newservice) has reached a steady state.
2018-12-10 08:08:18: (service cloudifacturing-newservice) registered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-newservice/0201b39a2bd062c1)
2018-12-10 08:08:06: (service cloudifacturing-newservice) has started 1 tasks: (task 86b40ed8-ce68-4350-b2fd-80be3887c2dd).

Target health:
Health-check path: https://srv.hetcomp.org//cloudifacturing-newservice/
Health-check interval: 30
Health-check status codes: 200-499
Target 1/1: i-08e5f0237d99e018d, Port: 32840, Health: healthy
```
CloudFlow uses Amazon Web Services (AWS) and their elastic container services
for service deployment. The status messages and events in this report are
therefore specific to AWS. Indicators for a successfully started service are:
* a running count of 1,
* a single task in the state `RUNNING`,
* a last event of "... has reached a steady state",
* and a single healthy target.

When updating a service and monitoring the status regularly, you will see that
more than one single task can run in such a transitionary time. A service's
status should, however, always end up in a similar state as displayed above.

If you call the method above for a service which has no running instances, you
will receive an empty status report:
```
>>> srv.print_service_status(token, name)

Status report for service test-service:
Service status: unknown
Desired count: unknown
Running count: unknown
Pending count: unknown

Tasks:

Last events:

Target health:
Health-check path: https://srv.hetcomp.org//cloudifacturing-test-service/
Health-check interval: 30
Health-check status codes: 200-499
```

For a status report that can be programmatically processed, use the following
method instead:
```python
r = srv.get_service_status(token, name)
```

#### clfpy CLI
Execute `status <service_name>`

## Monitoring a service's log files
In contrast to monitoring a service's _status_, which gives information about
the general health state of a service as seen from the outside, the _Docker
log files_ provide important information on what is happening inside a service
container.

#### clfpy services client
You can print log files with the following ServicesClient method:
```
>>> srv.print_service_logs(token, 'newservice')

Printing logs for service 'newservice'
Printing the last 20 log events for the last 1 log streams

Events for log stream 1/1 - cloudifacturing-newservice/cloudifacturing-newservice/86b40ed8-ce68-4350-b2fd-80be3887c2dd:
2018-12-10 08:25:29: 10.0.142.6 - - [10/Dec/2018:08:25:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:25:29: [pid: 14|app: 0|req: 66/69] 10.0.142.6 () {36 vars in 446 bytes} [Mon Dec 10 08:25:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:25:29: 10.0.154.158 - - [10/Dec/2018:08:25:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:25:29: [pid: 14|app: 0|req: 67/70] 10.0.154.158 () {36 vars in 448 bytes} [Mon Dec 10 08:25:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:25:59: 10.0.142.6 - - [10/Dec/2018:08:25:59 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:25:59: [pid: 14|app: 0|req: 68/71] 10.0.142.6 () {36 vars in 446 bytes} [Mon Dec 10 08:25:59 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:25:59: 10.0.154.158 - - [10/Dec/2018:08:25:59 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:25:59: [pid: 14|app: 0|req: 69/72] 10.0.154.158 () {36 vars in 448 bytes} [Mon Dec 10 08:25:59 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:26:29: 10.0.142.6 - - [10/Dec/2018:08:26:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:26:29: [pid: 14|app: 0|req: 70/73] 10.0.142.6 () {36 vars in 446 bytes} [Mon Dec 10 08:26:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:26:29: 10.0.154.158 - - [10/Dec/2018:08:26:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:26:29: [pid: 14|app: 0|req: 71/74] 10.0.154.158 () {36 vars in 448 bytes} [Mon Dec 10 08:26:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:26:59: 10.0.142.6 - - [10/Dec/2018:08:26:59 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:26:59: [pid: 14|app: 0|req: 72/75] 10.0.142.6 () {36 vars in 446 bytes} [Mon Dec 10 08:26:59 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:26:59: 10.0.154.158 - - [10/Dec/2018:08:26:59 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:26:59: [pid: 14|app: 0|req: 73/76] 10.0.154.158 () {36 vars in 448 bytes} [Mon Dec 10 08:26:59 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:27:29: 10.0.142.6 - - [10/Dec/2018:08:27:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:27:29: [pid: 14|app: 0|req: 74/77] 10.0.142.6 () {36 vars in 446 bytes} [Mon Dec 10 08:27:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
2018-12-10 08:27:29: 10.0.154.158 - - [10/Dec/2018:08:27:29 +0000] "GET /cloudifacturing-newservice/ HTTP/1.1" 404 5 "-" "ELB-HealthChecker/2.0" "-"
2018-12-10 08:27:29: [pid: 14|app: 0|req: 75/78] 10.0.154.158 () {36 vars in 448 bytes} [Mon Dec 10 08:27:29 2018] GET /cloudifacturing-newservice/ => generated 0 bytes in 0 msecs (HTTP/1.1 404) 0 headers in 26 bytes (0 switches on core 0)
```
If no further arguments are given, the services client prints the newest 20 log
events from the _log stream_ with the latest activity. For each service
instance, a separate log stream is created. Consequently, each new deployment
(triggered by a call to `srv.update_service()`) creates a new log stream.

`print_service_logs()` takes the following two optional arguments:
* `tail=50`: prints the last 50 log events for each log stream; corresponds to
  the `--tail` option for `docker logs`
* `streams=3`: prints log events for the last 3 log streams; use this for
  accessing logs from tasks that have been stopped and re-started (= updated)

The example above shows only log events triggered by the health checker which
pings each service regularly to make sure that it is still alive. This
sometimes can make it difficult to find more relevant log events. One option
around this is to increase the interval between two consecutive health checks.
See the section on "Defining custom health checks" below for details.

#### clfpy CLI
Execute `logs <service_name>`.

## Deleting a service
#### clfpy services client
Finally, to delete a service, call:
```python
srv.delete_service(name)
```
This stops any running service instances and deletes all resources associated
with the service. Note that this includes all logs and repository images. You
will have to re-push images if you re-create a service after deleting it.

#### clfpy CLI
Execute `remove <service_name>`.

## Defining custom health checks
When creating a new service, a standard health check is defined. In this
standard health check, a GET request is performed on the service's deployment
path (`https://srv.hetcomp.org/<project>-<service_name>`). The service is
considered healthy if the HTTP response code is anything between 200 and 499.
This means that as long as the service is alive and exposing a web server, even
"Not Found" errors (response code 404) are considered healthy. However, any
server-side errors (reponse codes 5xx) are considered unhealthy.

Note that unhealthy services will automatically be terminated and restarted. If
your container contains a bug causing consistent server-side errors, the
service will get stuck in a restart loop.

Upon service creation, you can also define a custom health check, where you can
define the health-check path, the accepted response codes, and the interval
between two consecutive health checks. For the SOAP services used in CloudFlow,
one can for example check if the wsdl service definition is available. To
define a custom health check, pass the `health_check` argument when creating a
new service:
```python
# ...
health_check = {
    'rel_path': '{}-{}/MyService?wsdl'.format(project, name),
    'status_codes': '200',
    'interval': 60
}
r = srv.create_new_service(token, name, health_check=health_check)
```
Notes
* The health-check path (`rel_path`) must always begin with the service's
  deployment path, which depends on the project the used token is associated
  with and the name of the service to be created.
* `status_codes` must be a string literal, not an integer. You can define lists
  (`'200,201'`) or ranges (`'200-299'`) as well.
* `interval` (must be an integer) is the number of seconds between two
  consecutive health checks.
* In the clfpy CLI, answer "y" to the question on a custom health check. The
  CLI will ask you for all necessary input afterwards.
