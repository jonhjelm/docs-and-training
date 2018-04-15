# The GSS API

## SOAP webmethods

### `getResourceInformation(fileID, session_id)`
Queries the type and other information for an arbitrary GSS URI.

Arguments:
* `fileID (string)`: GSS URI (file, folder, or non-existent resource)
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns a `ResourceInformation` object.

### `containsFile(fileID, session_id)`
Checks if a file or folder exists on a GSS storage.

_Note:_ An alternative to using `containsFile()` is to call
`getResourceInformation()` and check the `type` field of the returned
`ResourceInformation` object.

Arguments:
* `fileID (string)`: GSS URI of a (file, folder, or non-existent resource)
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns `true` if the resource exists, `false` otherwise.


### `listFiles(fileID, session_id)`
Lists the content of a folder.

Arguments:
* `fileID (string)`: GSS URI of a folder to list the contents of
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns a list of `ResourceInformation` objects (one for each element in the
folder). 

### `listFilesMinimal(fileID, session_id)`
Lists the content of a folder without request descriptions. For some storage
types, this method requires fewer calls to the storage backend and is therefore
faster than `listFiles()`.

Arguments:
* `fileID (string)`: GSS URI of a folder to list the contents of
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns a list of `ResourceInformation` objects (one for each element in the
folder).

### `createFolder(folderID, session_id)`
Creates a new folder.

Arguments:
* `folderID (string)`: Valid GSS URI of a non-existent folder. (Use 
  `getResourceInformation()` to verify that a folder URI does not yet exist.)
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns a `ResourceInformation` object for the created folder.

### `deleteFolder(folderID, session_id)`
Deletes an existing folder and all of its files/subfolders. 

Arguments:
* `folderID (string)`: GSS URI of an existing folder.
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns `true` if the folder was deleted successfully, `false` otherwise.

### `getDirectInteractionEndpoint(gssID, session_id)`
Returns the storage-specific endpoint addresses for a GSS URI.

In some cases, it might be required to interact directly with the specific
storage endpoint of a certain GSS resource. For example, some storage providers
might functionality (such as versioning) which goes beyond what GSS itself
offers. For such cases, this method can be used to obtain the endpoint address
to interact with.

Arguments:
* `gssID (string)`: GSS URI of a file or folder.
* `session_id (string)`: Valid authentication token (obtained from the
  authentication manager, is also available as an automatic service input in a
  workflow)

Returns a list of `EndpointInformation` objects.

## Structured return types of GSS webmethods

### The `ResourceInformation` object
The `ResourceInformation` object is used to encapsulate all required information
on a GSS resource which is necessary to interact with that particular resource.

A `ResourceInformation` object contains the following fields:
* `visualName (string)`: the name of a resource (such as the file name)
* `uniqueName (string)`: the full GSS URI of a resource
* `type (string)`: one of `["FILE", "FOLDER", "NOTEXIST"]`
* `queryForName (boolean)`: `true` if a new resource's file name cannot be 
  "predicted" (for non tree based storage systems)
* `createDescription (RequestDescription)`: "recipe" for an HTML request which
  creates the resource 
* `readDescription (RequestDescription)`: "recipe" for an HTML request which
  downloads the resource
* `updateDescription (RequestDescription)`: "recipe" for an HTML request which
  updates the resource with new data
* `deleteDescription (RequestDescription)`: "recipe" for an HTML request which
  deletes the resource
* `metaReadDescription (RequestDescription)`: "recipe" for an HTML request which
  returns meta information on the resource (such as file size, date of last
  modification, etc.)

The webmethods listed above return textual representations (in the form of json
strings) of these objects.

Example (full request descriptions not shown):
```
(resourceInformation){
   createDescription = 
      (requestDescription){
         supported = False
      }
   deleteDescription = ...
   metaReadDescription = ...
   queryForName = False
   readDescription = ...
   type = "FILE"
   uniqueName = "it4i_anselm://home/testfile.file"
   updateDescription = ...
   visualName = "testfile.file"
 }
```

### The `RequestDescription` object
A `RequestDescription` object contains all necessary information to make an
HTML request to read, update, delete, or create a resource in direct interaction
with its storage endpoint. `RequestDescription` objects are provided from GSS as
part of `ResourceInformation` objects and contain the following fields:

* `supported (boolean)`: `true` if this specific request is allowed
* `url (string)`: URL to make the request to
* `httpMethod (string)`: HTTP method ot use (GET, POST, PUT, ...)
* `headers (list of key-value pairs)`: list of headers to add to the request
  (contains authentication information)
* `sessionTokenField (string)`: deprecated

Example of a read description object (as part of a resource information):
```
uniqueName = "it4i_anselm://home/testfile.file"
...
readDescription = 
      (requestDescription){
         headers[] = 
            (httpHeaderField){
               key = "X-Auth-Token"
               value = ... (token removed for sake of brevity)
            },
         httpMethod = "GET"
         supported = True
         url = "https://api.hetcomp.org/refissh_anselm/files/home/testfile.file"
      }
```

### The `EndpointInformation` object
An `EndpointInformation` object describes the specific storage-provider endpoint
for a GSS resource and contains the following fields:

* `url (string)`: endpoint URL
* `type (string)`: endpoint type, one of `["SOAP", "REST"]`