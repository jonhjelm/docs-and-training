# CloudFlow servicectl
CloudFlow servicectl is a service offering a REST API to control third-party
services on the CloudFlow platform. It is used to create and deploy auxiliary
services on the CloudFlow platform such as HPC pre-processors or graphical
input-parameter masks. Services are deployed as Docker containers, the images
of which are pushed to repositories created for each service.

## API reference

### Assumptions
1. `<URL>` is the deployment URL of servicectl
2. All requests are performed with an `X-Auth-Token` header and a valid
   CloudFlow session token.

### Generic status codes
All API calls return error 400 if no authentication token was provided and
error 403 if a token was provided but its validation failed.

## `GET <URL>/v0/services`: List all services
Returns a minimal list of all currently defined services including their
deployment paths. Note that in the deployment paths, the user's project appears
again, whereas the API URLs do not contain it.

### Response
#### Response body
Example response body:
```json
[
	{
		"name": "my-service",
		"links": [
		    {
		    "rel": "self",
		    "href": "/v0/services/my-service"
		    },
		    {
		    "rel": "deployment",
		    "href": "https://.../my-project-my-service"
		    }
		]
	},
	{
		"name": "great-service",
		"links": [
		    {
		    "rel": "self",
		    "href": "/v0/services/great-service"
		    },
		    {
		    "rel": "deployment",
		    "href": "https://.../my-project-great-service"
		    }
		]
	}
]
```

#### Status codes
* 200 - OK: Request was successful

## `POST <URL>/v0/services`: Create a new service
Creates a new, "empty" and inactive service.

### Request
#### Minimal request body
As a minimum, you need to provide the name of a new service. In this case, a
standard health check is configured for the service, which is to check
connectivity on the deployment path (see below in the response body), but
accepting any HTTP response code between 200 and 499.
```json
{
    "name": "<service-name>"
}
```

#### Request body with custom health check
The following request body creates a new service with a custom health-check
definition. In this example, the health check makes sure the wsdl file of a
SOAP service can be reached. `interval` is the interval in seconds between
consecutive health checks. 

The `status_codes` string can take single values (`"200"`, `"201"` etc.),
several values (`"200,201,204"`) or ranges (`"200-299"`).
```json
{
    "name": "<service-name>",
    "health_check": {
        "rel_path": "MyService?wsdl",
        "status_codes": "200",
        "interval": 30,
    }
}
```

### Response
#### Response body
```json
{
    "name": "<service-name>",
    "links": [
        {
        "rel": "self",
        "href": "/v0/services/<service-name>"
        },
        {
        "rel": "deployment",
        "href": "https://.../<project>-<service-name>"
        }
    ]
}
```

#### Status codes
* 201 - Created: Service created successfully
* 400 - Bad Request: Request body was malformed or requested service name is 
  not allowed
* 405 - Method Not Allowed: Service already exists

## `GET <URL>/v0/services/<service_name>[?view=status]`: Query a service's status
Returns detailed status information for a single service. The status is base64
encoded and meant to be human-readable, not necessarily machine-readable.

### Response
#### Response body for a not yet started service
This first example is a response body for `GET
<URL>/v0/services/my-service?view=status` for the case where the service has
never been started/updated before. The status report contains only placeholders
for status information. The report contains extensive status information on all
running service instances (tasks) as well as event messages.
```json
{
  "name": "brand-new",
  "links": [
    {
    "rel": "self",
    "href": "/v0/services/my-new-service"
    },
    {
    "rel": "deployment",
    "href": "https://.../my-project-my-new-service"
    }
  ],
  "status": {
    "service_status": "unknown",
    "count_desired": "unknown",
    "count_running": "unknown",
    "count_pending": "unknown",
    "tasks": [],
    "events": [],
    "target_health": []
  }
}
```

#### Response body for a running service
This second example shows the status report for a running service, where all
the placeholders from the example above are filled.
```json
{
  "name": "my-new-service",
  "links": [
    {
    "rel": "self",
    "href": "/v0/services/my-new-service"
    },
    {
    "rel": "deployment",
    "href": "https://.../my-project-my-new-service"
    }
  ],
  "status": {
    "service_status": "ACTIVE",
    "count_desired": 1,
    "count_running": 1,
    "count_pending": 0,
    "tasks": [
      {
        "task_name": "d958131a-eb36-4efa-81e6-387e2cf6be8b",
        "created_at": "2018-12-05 14:34:16",
        "desired_status": "RUNNING",
        "last_status": "RUNNING",
        "task_definition": {
          "name": "cloudifacturing-my-new-service",
          "revision": 18,
          "status": "ACTIVE",
          "container_image": "400389127564.dkr.ecr.eu-central-1.amazonaws.com/cloudifacturing-my-new-service:latest",
          "container_memory_reservation": 100,
          "container_memory_limit": 125,
          "container_port": 80
        }
      }
    ],
    "events": [
      {
        "created_at": "2018-12-05 14:35:58",
        "message": "(service cloudifacturing-my-new-service) has reached a steady state."
      },
      {
        "created_at": "2018-12-05 14:35:35",
        "message": "(service cloudifacturing-my-new-service) has stopped 1 running tasks: (task 12c11518-130e-461f-b18a-2e57a7951f41)."
      },
      {
        "created_at": "2018-12-05 14:35:02",
        "message": "(service cloudifacturing-my-new-service) has begun draining connections on 1 tasks."
      },
      {
        "created_at": "2018-12-05 14:35:02",
        "message": "(service cloudifacturing-my-new-service) deregistered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      },
      {
        "created_at": "2018-12-05 14:34:28",
        "message": "(service cloudifacturing-my-new-service) registered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      },
      {
        "created_at": "2018-12-05 14:34:16",
        "message": "(service cloudifacturing-my-new-service) has started 1 tasks: (task d958131a-eb36-4efa-81e6-387e2cf6be8b)."
      },
      {
        "created_at": "2018-12-05 13:18:59",
        "message": "(service cloudifacturing-my-new-service) has reached a steady state."
      },
      {
        "created_at": "2018-12-05 13:18:36",
        "message": "(service cloudifacturing-my-new-service) has stopped 1 running tasks: (task 2fcebbb7-f535-4c50-9acc-ee83b9c38589)."
      },
      {
        "created_at": "2018-12-05 13:18:02",
        "message": "(service cloudifacturing-my-new-service) has begun draining connections on 1 tasks."
      },
      {
        "created_at": "2018-12-05 13:18:02",
        "message": "(service cloudifacturing-my-new-service) deregistered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      },
      {
        "created_at": "2018-12-05 13:17:28",
        "message": "(service cloudifacturing-my-new-service) registered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      },
      {
        "created_at": "2018-12-05 13:17:16",
        "message": "(service cloudifacturing-my-new-service) has started 1 tasks: (task 12c11518-130e-461f-b18a-2e57a7951f41)."
      },
      {
        "created_at": "2018-12-05 13:15:35",
        "message": "(service cloudifacturing-my-new-service) has started 1 tasks: (task 8cf41319-0b8d-461d-8d60-73188d5ac6ec)."
      },
      {
        "created_at": "2018-12-05 13:14:51",
        "message": "(service cloudifacturing-my-new-service) has started 1 tasks: (task 5602f2d4-afde-4638-a552-f25f6a904e2e)."
      },
      {
        "created_at": "2018-12-05 13:13:57",
        "message": "(service cloudifacturing-my-new-service) has started 1 tasks: (task e6a686f0-c11d-4a9b-b326-8085bd017b35)."
      },
      {
        "created_at": "2018-12-05 11:21:41",
        "message": "(service cloudifacturing-my-new-service) has reached a steady state."
      },
      {
        "created_at": "2018-12-05 11:21:19",
        "message": "(service cloudifacturing-my-new-service) has stopped 1 running tasks: (task e1e2e634-7a1c-4d20-bc1e-f314ac93a60a)."
      },
      {
        "created_at": "2018-12-05 11:20:46",
        "message": "(service cloudifacturing-my-new-service) has begun draining connections on 1 tasks."
      },
      {
        "created_at": "2018-12-05 11:20:46",
        "message": "(service cloudifacturing-my-new-service) deregistered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      },
      {
        "created_at": "2018-12-05 11:20:13",
        "message": "(service cloudifacturing-my-new-service) registered 1 targets in (target-group arn:aws:elasticloadbalancing:eu-central-1:400389127564:targetgroup/cloudifacturing-my-new-service/459743ee4d5f520d)"
      }
    ],
    "target_health": [
      {
        "target": "i-08e5f0237d99e018d",
        "port": 32819,
        "health": "healthy"
      }
    ]
  }
}
```

#### Status codes
* 200 - OK: Request was successful
* 404 - Not found: Service unknown

## `GET <URL>/v0/services/<service_name>?view=logs`: Query a service's logs 
Returns log messages for a single service. By default, log messages for the
last active _log stream_ are returned, where each log stream corresponds to
one running task. Except during update phases, where more than one task can
run in parallel, there exists only a single task per service and thus only a
single active log stream.

### Request
#### Further query parameters:
* `tail=<n>`: Returns the last `n` log entries (default is 20)
* `streams=<n>`: Returns logs of the last `n` log streams (default is 1)

### Response
#### Response body
Example response for `GET <URL>/v0/services/my-service?view=logs&tail=2`:
```json
{
    "name": "my-service",
    "links": [
        {
        "rel": "self",
        "href": "/v0/services/my-new-service"
        },
        {
        "rel": "deployment",
        "href": "https://.../my-project-my-new-service"
        }
    ],
    "logs": [{
        "stream_name": "<stream name>",
        "logs": [{
            "time": "<time stamp>",
            "message": "<log message>"
        },{
            "time": "<time stamp>",
            "message": "<log message>"
        }]
    }]
}
```

#### Status codes
* 200 - OK: Request was successful
* 404 - Not found: Service unknown

## `GET <URL>/v0/services/<service_name>?view=docker`: Get service's Docker details
Returns information on how to access the Docker repository for a specific
service, which is necessary for uploading a new Docker image. The returned
parameters should be used for tagging and uploading an image as follows
(assuming that the current directory contains a `Dockerfile`):

```sh
docker login -u <user> -p <password> <proxy_endpoint>
docker build -t somename:sometag .
docker tag somename:sometag <repo_uri>:sometag
docker push <repo_uri>:<sometag>
docker logout <proxy_endpoint>
```
`somename` and `sometag` can be chosen by the user.

### Response
#### Response body
Example response body for `GET <URL>/v0/services/my-service?view=docker`:
```json
{
    "name": "my-service",
    "links": [
        {
        "rel": "self",
        "href": "/v0/services/my-service"
        },
        {
        "rel": "deployment",
        "href": "https://.../my-project-my-service"
        }
    ],
    "repo_uri": "<URI for the repository>",
    "proxy_endpoint": "<Endpoint for push commands>",
    "user": "<user name for Docker login command>",
    "password": "<password for Docker login command>",
}
```

#### Status codes
* 200 - OK: Request was successful
* 404 - Not found: Service unknown

## `PUT <URL>/v0/services/<service-name>`: Update a service
Updates a service to use a new Docker container and/or new task configuration.

### Request
#### Request body
```json
{
    "container-tag": "1.3.0",
    "memory-reservation": 125,
    "memory-limit": 150,
    "container-port": 80,
    "environment": [
        {
            "name": "MY_CONFIG_VAR",
            "value": 123
        }
    ]
}
```
Required parameters are:

* `container-tag`: Docker tag of the image to use for the service
* `memory-reservation`: Amount of memory to reserve on the VM for the container.
  The container is allowed to allocate more memory than this limit, which is
  why this number should be the minimum that the container requires.
* `memory-limit`: Hard memory limit. If the container tries to allocate more,
  it will be killed.
* `container-port`: The port under which the container listens for incoming
  requests. Note that the container port is fixed after the first PUT
  operation and cannot be changed afterwards. Specifying a different port in
  later updates will lead to an error. If you want to change the container
  port, fully delete and re-create the service.
* `environment`: Definition of environment variables, used to configure the
  container. Must be either a single json object with the elements `name` and
  `value` or a list of such objects.

### Response
#### Response body
```json
{
  "Success": "Successfully issued update command, check the status for details",
  "links": [
    {
      "rel": "self",
      "href": "/v0/services/my-new-service"
    },
    {
      "rel": "deployment",
      "href": "https://srv.hetcomp.org/cloudifacturing-my-new-service"
    }
  ]
}
```

#### Status codes
* 200 - OK: Service updated successfully
* 400 - Bad Request: Request body was malformed, e.g., because the Docker tag
  was not found, a parameter had the wrong format, or the container port did
  not match the initially defined one
* 404 - Not Found: Service doesn't exist

## `DELETE <URL>/v0/services/<service-name>`: Delete a service
Stops any running instance of the service and deletes all associated resources,
such as the Docker repository and all images therein.

### Response
#### Status codes
* 204 - No Content: Service deleted successfully
* 404 - Not Found: Service does not exist

