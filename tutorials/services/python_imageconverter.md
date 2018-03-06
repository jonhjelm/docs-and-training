# Tutorial: Low-level file access (showcased via a simple image converter)
This tutorial will introduce the concepts of file access via GSS. You will
implement a synchronous service which downloads a png image file from a GSS
location, converts it to a jpg image file, and uploads the converted image to
the same GSS folder.

## Step 1: Prepare the example code
This tutorial starts from the code example
[sync_image_converter_tutorial](../../code_examples/Python/sync_image_converter_tutorial).
To begin, copy this folder to a new location or alternatively create a
new, local git branch to work on.

Now, change into the folder containing your copy of the calculator service and
open a terminal there.

### Adapt the webservice's context root
The first thing to do is to adapt the existing code so that it can run on
your deployment setup. To be able to listen to the correct http requests, the
webservice needs to know its _relative deployment path_ or _context root_.

Example: If you aim to run the service on a VM which is reachable via
`<somehost>/mycompany/myvm` (`<somehost>` can, for example, be
`caxman.clesgo.net`), the context root needs to be set to `/mycompany/myvm`.

The code example we're working with is a Docker container which is configured
via environment variables defined in the `env` file in the source folder. Edit
this file and change the context-root definition to the string appropriate to
your deployment path.

## Step 2: Code overview
The example directory already contains a full service skeleton and a Docker
container to wrap the service in. Have a look at
`app/ImageConverterService.py`, which is the main file we will be working on.
The main elements of this skeleton are:
* The SOAP service class `ImageConverterService`, which already has its main
  method `imageconvert_png2jpg()` defined but not implemented. You will finish
  the implementation of this method in this tutorial.
* The helper function `get_resource_information()`, which queries GSS for the
  resource information of a GSS ID. The resource information contains all
  details necessary to, for example, download or upload a file. The helper 
  function uses Python's `suds` module to issue a SOAP call to the GSS
  webservice.
* The helper function `convert_png2jpg()` which performs the actual image
  conversion using imagemagick's `convert` tool.
* The helper function `parse_extra_parameters()` which takes a special string
  given to our service by the workflow manager and creates a Python-friendly
  representation from it.

## Step 3: Implement `imageconvert_png2jpg()`
We will now implement the functionality of the service's main function
`imageconvert_png2jpg()`. As you can see, the function signature defines three
input arguments:
* `sessionToken` is used to authenticate the service when calling GSS
* `extra_pars_str` is a pre-defined workflow input which contains, among other
  things, the wsdl URL of the GSS service. We can therefore access GSS in our
  service without ever having to know or hard-code the exact location of GSS.
* `gss_ID` points to the image file to be converted

Eventually, the service needs to perform three main tasks:
1. Download the existing png file from GSS to a temporary local location
2. Convert the downloaded png file to a jpg file
3. Upload the converted image to a new GSS location

For step 2, we already have the helper function `convert_png2jpg()` defined. We
will therefore concentrate mainly on how to access GSS for downloading and
uploading files.

### Step 3.1: Download a file from GSS
The very first question we have to answer when we want to download a file from
GSS is where to find the GSS service. To avoid hardcoding a GSS deployment URL
or another resource location (which might change over time or for different
deployment setups), the workflow manager offers a special workflow input called
`extraParameters`. This input is a string containing comma-separated key-value
pairs, one of them being the URL where we can find the GSS service. To extract
the right key-value pair from the `extra_pars` input parameter, add the
following lines to your code:
```python
        extra_pars = parse_extra_parameters(extra_pars_str)
        gss_location = extra_pars['gss']
```

Since GSS is an abstraction layer of possibly many different storage locations,
downloading (and uploading) a file is a little more intricate than it might
seem at first: On the one hand, we do not want to download the file directly
from the GSS service (since that would mean that the file has to take a detour
from its original location via the machine hosting GSS to us, which will slow
things down especially for bigger files). This requires direct communication
with the storage location and its API. But on the other hand, GSS is all about
replacing the need to juggle different storage APIs with a single abstraction
API. In contrast, getting the `resourceInformation` object for a GSS ID is
nothing more than a simple SOAP call to the GSS webservice itself (see
`get_resource_information()`).The solution to this problem is simple: We only
ask GSS about _how_ to handle a certain file (i.e., what kind of request to
make to what URL), and then use GSS's response to perform the download directly
from the storage location. 

So let's ask GSS about the GSS ID we received in the input parameter `gss_ID`:
```python
        res_info = get_resource_information(gss_location, gss_ID,
                                            sessionToken)
        read_desc = res_info.readDescription
        if not read_desc.supported:
            raise AttributeError('Read operation not allowed')
```
We use the already defined helper function to obtain a `resourceInformation`
object describing the resource behind `gss_ID`. This object contains so-called
`requestDescription` objects for operations such as download, upload, update,
delete, etc. Here, since we want to download the file, we use the
`readDescription` object to confirm that downloading is a supported operation.

To be able to convert a file, we need to find a space to temporally store it on
the machine our service is deployed on. We do this using Python's `tempfile`
module and some path-manipulation functions:
```python
        tempdir = tempfile.mkdtemp()
        gss_folder, png_filename = os.path.split(gss_ID)
        png_filepath = os.path.join(tempdir, png_filename)
```

Now, we use the information provided in the `readDescription` field to create
a HTTP request to download the file to the filepath we defined:
```python
        headers = {h.key: h.value for h in read_desc.headers}
        request = urllib2.Request(url=read_desc.url, headers=headers)
        with open(png_filepath, 'wb') as out_file:
            result = urllib2.urlopen(request)
            while True:
                buffer = result.read()
                if not buffer:
                    break
                out_file.write(buffer)
```
Note that we first copy all headers defined in the read description into a
Python dictionary that we pass to the request object. These headers contain
mainly authentication information specific for the storage location of the GSS
ID the read description belongs to. We make a http request to the URL provided
in the read description and then perform a buffered download of the file.

### Step 3.2: Convert the image to jpg
We are now ready to perform the actual image conversion:
```python
        jpg_filepath = convert_png2jpg(png_filepath)
```
Have a look at the implementation of `convert_png2jpg` to learn more about how
to call the external convert tool with Python.

### Step 3.3: Upload the converted file
Before uploading the converted image back to GSS, we need to define the GSS ID
to upload to:
```python
        _, jpg_filename = os.path.split(jpg_filepath)
        gss_ID_new = os.path.join(gss_folder, jpg_filename)
```
We use the folder we downloaded the source image from and use the filename we
obtained from the conversion function.

Uploading the new file works almost exactly like downloading a file. We first
obtain a `resourceInformation` object (now with the new GSS ID we created) and
this time use its `createDescription` to make a fitting HTTP call. (Yes,
obtaining the resource information of a resource which doesn't exist is
perfectly valid and necessary if we want to create that resource.)
```python
        res_info = get_resource_information(gss_location, gss_ID_new,
                                            sessionToken)
        create_desc = res_info.createDescription
        if not create_desc.supported:
            raise AttributeError('Create operation not allowed')

        headers = {h.key: h.value for h in create_desc.headers}
        headers["Content-Length"] = "%d" % os.stat(jpg_filepath).st_size

        with open(jpg_filepath, "r") as in_file:
            request = urllib2.Request(url=create_desc.url, data=in_file,
                                      headers=headers)
            request.get_method = lambda: create_desc.httpMethod
            result = urllib2.urlopen(request)
```
Note that we also set the `"Content-Length"` header and that we change the
request's GET method to what is defined in the create description. The actual
upload is taken care of by Python's urllib2 module.

Finally, we shouldn't forget to remove the temporary folder we created and
to return the new GSS ID which will be the output argument of our service:
```python
        shutil.rmtree(tempdir)
        return gss_ID_new
```

If you are not sure whether you got all of the implementation right, you can
compare your code with the code example
[snyc_image_converter](../../code_examples/Python/sync_image_converter) which
contains a finished implementation.

## Step 4: Build and test the converter service
To build and deploy the image-conversion service as a Docker container, run the
included build script:
```bash
./rebuildandrun.sh <port>
```
As before, specify `<port>` if you want the container to listen on a port which
is _not_ 8080. Use `docker ps` and `docker logs imageconverter` to make sure
that your service is running.

For testing, the tutorial code comes with a small test client wrapped in a
Docker container, located in the `test_client/` folder. Run:
```bash
cd test_client
./build.sh
./run.sh <port> <username> <project> <password> <gss_ID>
```
`<username>`, `<project>`, and `<password>` are the same as those you use to
log into the CoudFlow portal. `<gss_ID>` is the file to convert; you can use
the FileBrowser workflow via the portal to upload and select a corresponding
file. Just make sure that it's a png file and that there is no jpg file with
the same name yet.

This test call is a bit more complicated than in the previous tutorials. Since
the converter service is not called in the context of a running workflow where
the workflow manager automatically passes the user's session token to each
service, we first have to obtain a session token from the authentication
services, which we then use to call our service. We also have to create the
extra-parameters input ourselves. Have a look at
`test_client/test_imageconverter.py` to learn more about how this is done.

The test call's output should be the same GSS ID as you defined as input, but
with a different file ending (jpg instead of png).

## Step 5: Create an image-conversion workflow
You can now head over to the portal and create your own image-conversion
workflow and integrate the image-converter service as a synchronous CloudFlow
service. You can either hard-code a GSS ID as input or, even better, use the
filechooser service
(`http://www.caxman.eu/apps/sintef/fileChooser03_new2.owl#fileChooser_Service`)
to have the user select a file during workflow execution. If you don't know how
to register and integrate your service in a workflow, refer to the 
[corresponding tutorial](../workflows/basics_service_registration.md).

## Conclusion
This tutorial showcased basic usage of GSS for file access. However, a few
important things are left to be said:
* The point of this tutorial is to create an understanding of how GSS works
  and how we can use it for file access without having any inside knowledge
  about the storage location and API of a specific file. That said, it is bad
  practice to directly use the above code every time you need to access a file.
  Instead, wrap the necessary code into a library in the language of your
  choice and use that library to reduce code duplication and make your code
  less prone to error.
* In this tutorial, we didn't care for error checking at all. For example, the
  service will fail if there is already a jpg file for a selected png file,
  since the create operation won't be supported. Also, no one stops us from
  trying to convert, say, an mp3 file to a jpg file with this service. It is
  quite likely that the service will crash, but we cannot say how. For such
  situations, each service should define appropriate SOAP faults and raise
  them as needed. Have a look at the 
  [error-handling documentation](../../service_implementation/advanced_error_handling.md)
  for more information.
