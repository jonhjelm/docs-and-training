refissh: RESTful storage via SSH
================================
refissh is a web service which provides management of files, Singularity
images, and HPC jobs through an SSH server (typically an HPC provider's login
node), hidden behind a REST API.

refissh is part of the CloudFlow infrastructure stack and was developed with
the CloudiFacturing project in mind. It therefore relies on the CloudFlow
authentication services for user authentication.


# API overview
refissh consists of a files API, a jobs API, and an images API, which interplay
with each other to enable encapsulated multi-user file storage and HPC job
execution (via Singularity containers) on an HPC cluster, using only a single
user's login credentials.

All of the calls described in the following API overview assume that the
`"X-Auth-Token"` header is part of the call and contains a valid token obtained
from the authentication manager. All API calls return error 401 if no
authentication was given and error 403 if validation of the token failed.

It is further assumed that `$URL` contains the refissh deployment URL.

*Note:* For the development of non-infrastructure services in CloudiFacturing,
it is generally _not_ necessary to interact with any of the refissh APIs. 
Instead, high-level services such as GSS or the HPC service should be used.


## Files API

### `HEAD $URL/files/some/file/or/folder` : get resource type
Returns the resource type of the given path, which can be `FILE`, `FOLDER`, or
`NOTEXIST`.

#### Status codes:
* *200* if resource is a file
* *204* if resource is a folder
* *404* if resource doesn't exist

### `GET $URL/files/some/folder` : list directory contents
Returns a list of the contents of the given resource path, which must be a
folder. The returned list is a json representation of a list of GSS
ResourceInformation objects.

#### Status codes:
* *200* if successful
* *404* if resource doesn't exist

### `GET $URL/files/some/file.ext` : download a file
Performs a binary download of the file at the given path.

#### Status codes:
* *200* if successful
* *404* if resource doesn't exist

### `POST $URL/files/non/existing/folder` : create a new folder
Creates a new empty folder at the given path. Pass `"Content-Type:
application/directory"` as an additional header with the call.

#### Status codes:
* *201* if successful
* *400* if no `"Content-Type"` header was given
* *405* if folder already exists
* *405* if parent folder doesn't exist or if POST was attempted in root
  folder and root folder is configured immutable

### `POST $URL/files/non/existing/file` : upload a file
Expects the file to be uploaded as the request data in binary form. Also pass
a fitting `"Content-Type"` header with the call.

#### Status codes:
* *201* if successful
* *400* if no `"Content-Type"` header was given
* *405* if file already exists
* *405* if parent folder doesn't exist or if POST was attempted in root
  folder and root folder is configured immutable

### `PUT $URL/files/already/existing/file` : update a file
Like the POST request, but to update an existing file. Fails if the file
doesn't exist.

#### Status codes:
* *201* if successful
* *405* if file doesn't exist

### `DELETE $URL/files/already/existing/file/or/folder` : delete a file/folder
Deletes the file or folder at the given path. Will delete non-empty folders.

#### Status codes:
* *204* if successful
* *404* if resource doesn't exist


## Jobs API
The refissh jobs API allows to manage and monitor HPC jobs for multiple users
using a single user's HPC login-node credentials. The individual jobs are 
wrapped in Singularity containers which have access only to a restricted 
portion of the host file system.

### `GET $URL/jobs/` : list all known jobs
Returns a json representation of a list of job informations for all jobs
known to refissh. This includes finished jobs. Each job information contains
the job's service ID, queue ID, and associated project. Only allowed if the
token is connected to the admin project configured in refissh's environment
variables.

#### Status codes:
* *200* if successful
* *403* if token validation successful but connected project is not the admin
  project

### `POST $URL/jobs/<service_ID>` : start a new job
For a unique and not yet known service ID, a new job is started on the scheduler.
The request data has to contain the following json-formatted job specifications:
```
{
"image_name": "hetcomp/sing_test",
"commandline": "/runscript.sh",
"parameters": "nothing important",
"cluster": "anselm",
"N_nodes": 1,
"N_cores": 24,
"max_runtime": 5
}
```

#### Status codes:
* *200* if successful
* *400* if the payload is malformed (parameters missing etc.)
* *405* if a job is already registered with the service ID

### `GET $URL/jobs/<service_ID>` : get job status
Returns the status of a known job. Returns either "FINISHED", "UNKNOWN", or
the status html as produced by a running job. If no such html file exists,
returns "RUNNING".

#### Status codes:
* *200* if successful
* *404* if the service ID doesn't exist for the project connected to the
  authentication token

### `PUT $URL/jobs/<service_ID>` : send message to a job
NOTE: Not yet implemented!

Sends a message to a running job. The request data has to contain the message
in the following json format:
```
{
"message": "my message to the service"
}
```

#### Status codes:
to be defined

### `DELETE $URL/jobs/<service_ID>` : abort job
Stops execution of a running job.

#### Status codes:
* *200* if successful
* *405* if the service state is FINISHED, EXITING, or UNKNOWN


## Images API
The images API provides functionality to register Singularity which then can be
executed as HPC jobs.

Currently, only the registration of pre-built Singularity images which reside
on the refissh/files storage is supported. In future, support for image
creation from a Singularity recipe or a Docker image might be added.

Note that all images are project-bound. This means that an image registered by
as user with credentials connected to a certain project will only be visible
and usable by users from the same project.

### `GET $URL/images/` : list available images
Lists all images which are registered with the project the calling user is
authenticated with.

#### Status codes:
* *200* if successful

### `POST $URL/images/<image_name>` : register new image
Registers a new Singularity image with refissh. `<image_name>` is an arbitrary
name which must follow the formatting convention for Docker images. The request
must further contain a json string with the following content:

```
{
    "image": {
        "source_location": "<location_identifier>"
    }
}
```

Here, `<location_identifier>` is the URL of file stored on the HPC storage
accessible through refissh/files.

refissh will copy the image from the user's storage and register it as
available. `<image_name>` can then be used in a POST request of the jobs API
(see above).

#### Status codes:
* *204* if successful
* *400* if image name or source location path is illegal
* *404* if source file is not found
* *405* if image already exists

### `PUT $URL/images/<image_name>` : update image
Replaces an existing Singularity image with a new version. The request must
contain the same data payload as for the `POST` request.

#### Status codes:
* *204* if successful
* *400* if image name or source location path is illegal
* *404* if source file is not found
* *405* if image to be updated doesn't exists

### `GET $URL/images/<image_name>` : query image information
Returns information about an image, such as whether it exists and when it was
registered.

#### Status codes:
* *200* if successful
* *404* if image doesn't exist

### `DELETE $URL/images/<image_name>` : deregisters an existing image
De-registers and removes an existing image from refissh. The image won't be
usable for refissh jobs anymore.

#### Status codes:
* *204* if successful
* *404* if image doesn't exist

# Example calls implemented with `curl`
Below are examples of all available calls of the refissh API. All examples
below assume a locally running refissh container and that `$token` contains a
valid token provided by the authentication manager.

Example payloads for the calls can be found in the `resources_<API_part>`
folder.

## Files API
```
export URL=127.0.0.1:5000/refissh

# List files and folders
curl -H "X-Auth-Header: $token" -X GET $URL/files/
curl -H "X-Auth-Header: $token" -X GET $URL/files/some_folder

# Download a file
curl -H "X-Auth-Header: $token" -X GET -o out_file.file $URL/files/some_file.file

# Create a folder
curl -H "X-Auth-Header: $token" -X POST -H “Content-Type: application/directory” $URL/files/some/nonexisting/folder

# Upload a new file, here, a png image
curl -H "X-Auth-Header: $token" -X POST -H “Content-Type: image/png” --data-binary @image.png $URL/files/existing/folder/image.png

# Update an existing file
curl -H "X-Auth-Header: $token" -X PUT -H “Content-Type: image/png” --data-binary @image.png $URL/files/existing/folder/image.png

# Delete a file or folder
curl -H "X-Auth-Header: $token" -X DELETE $URL/files/existing/folder/or/file.file
```

## Jobs API
```
export URL=127.0.0.1:5000/refissh

# List all jobs known to refissh/jobs (only allowed when token is connected to the admin project)
curl -H "X-Auth-Token: $token" -X GET $URL/jobs/

# Start a new job with a new unique service ID
curl -H "X-Auth-Token: $token" -X POST -d @payload $URL/jobs/<service_ID>

# Get the status of a currently running job
curl -H "X-Auth-Token: $token" -X GET $URL/jobs/<service_ID>

# Abort a currently running job
curl -H "X-Auth-Token: $token" -X DELETE $URL/jobs/<service_ID>
```

## Images API
```
export URL=127.0.0.1:5000/refissh

# List all images registered with the current project
curl -H "X-Auth-Token: $token" -X GET $URL/images/

# Register a new image
curl -H "X-Auth-Token: $token" -X POST -d @payload $URL/image/<image_name>

# Update an existing image
curl -H "X-Auth-Token: $token" -X PUT -d @payload $URL/image/<image_name>

# Query information on an existing image
curl -H "X-Auth-Token: $token" -X GET $URL/images/<image_name>

# Delete an existing image
curl -H "X-Auth-Token: $token" -X DELETE $URL/images/<image_name>
```
