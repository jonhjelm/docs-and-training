# Packaging software in Singularity images
Singularity is a container solution similar to Docker, but with the specific
needs of HPC environments in mind. For example, while Docker containers always 
run with root privileges (which cannot be allowed on an HPC cluster for obvious
security reasons), Singularity containers run only with the rights of the user
that executes the container.

On the SemWES platform, all software that should be run on an HPC cluster
_has to be packaged in a Singularity image_. This packaging involves the
following steps:

1. Write a _Singularity build recipe_ (analogously to a Dockerfile) which
   * contains all required computation software,
   * creates paths where HPC file storage will be mounted,
   * writes progress information into a certain pre-defined text file

2. Build a Singularity image from the recipe

3. (Optional) Test the Singularity image manually on the HPC login node

4. Upload the Singularity image to the HPC storage using GSS

5. Register the Singularity image with the HPC service

Once these steps are complete, the image can be used by the HPC service. In the
following, we will give a detailed tutorial-style description of all the above
steps.

## Writing a Singularity recipe
A _Singularity recipe_ is very similar to a Dockerfile: it contains all
instructions which are necessary to build a Singularity image. Singularity
images can actually be based on Docker images, which is what we will be using
in this example.

Have a look at the [waiter folder of the Singularity code
examples](../code_examples/Singularity/waiter). It contains a minimal example of
a Python application to be packaged in a Singularity image. The Singularity
recipe itself is contained in the file `Singularity` and looks like this:
```
Bootstrap: docker
From: python

# Set up mandatory mount points:
# /scratch will link to the HPC scratch drive
# /service will be used for status and result reporting
# (/home) will be mapped automatically
%setup
    mkdir -p ${SINGULARITY_ROOTFS}/scratch
    mkdir -p ${SINGULARITY_ROOTFS}/service

%files
    app /
```
The first two lines tell Singularity to use the Docker image `python`
(translates to `python:latest` from https://hub.docker.com/_/python/) as the
basis for building the Singularity image. 

Under `%setup`, two directories are created: `/scratch` and `/service`. These
together with `/home` serve as mount points for HPC file storage paths when the
image is executed on the HPC cluster by the SemWES HPC service. `/home` and
`/scratch` will be mounted to the `home` and `scratch` folders on the HPC
storage which are accessible also by GSS (using, for example, the File Browser
workflow). They thus allow your packaged application to access all files on the
HPC storage which are available via GSS. `/service` will be used by your
packaged application to communicate status reports to the HPC service. It can
furthermore be used for cross-node communication and temporary files which are
_not_ supposed to be visible to the user, since `/service` is not exposed via
GSS.

**Important:** In your own recipes, you _always have to create these
mountpoints_. If you don't, your image will _not_ work on the SemWES
platform.

Finally, the `%files` section of the recipe tells to copy the local folder `app`
into the root folder (`/`) of the Singularity image. In this example, this local
folder contains a Python script which is a placeholder for a more complex
simulation/calculation software.

For more information on Singularity recipes, refer to the [official Singularity
documentation](http://singularity.lbl.gov/docs-recipes).

## Building Singularity images
**Note:** In order to build Singularity images, you have to have Singularity
installed (see http://singularity.lbl.gov/ for downloads) and you have to have
root privileges. This can therefore _not_ be done on an HPC login node.

To build an image from the above recipe, open a console in the folder containing
the recipe and execute the following command:
```
sudo singularity build waiter.simg Singularity
```
Singularity will then download the Docker base image, package the Python
application in `app/`, and save the image as `waiter.simg`.

_Note:_ Make sure to use the `.simg` file extension for your images.

_Important:_ In contrast to Docker, Singularity will _not_ overwrite but rather
extend an existing image in the build process. Therefore, make sure to always
delete an existing image before rebuilding.

## Communicating back to the HPC service: status and result files
Before we describe how to execute and test our Singularity image, let's have a
look at how to communicate status and result reports back to the HPC service.

When a Singularity image is executed as part of a SemWES workflow, it is the
SemWES HPC service which actually logs in to the HPC login node and executes
the Singularity image (more on that later). While the HPC service will use the
HPC cluster's queueing system to monitor the execution status of the Singularity
image, the application running inside this image still needs to communicate
with the HPC service, for the following reasons:
1. During the (possibly long-lasting) execution of the simulation/calculation,
   status information should be displayed to the user who is running the
   workflow.
2. Once the simulation/calculation is finished, its results need to be forwarded
   further in the workflow.

In order to do so, your application needs to write to two text files in the
mounted `/service` folder. Have a look at the example application
[`app/wait_a_while.py`](../code_examples/Singularity/waiter/app/wait_a_while.py)
to see how this is done:

```python
# ...

STATUSFILE = "/service/status.html"
RESULTFILE = "/service/result.txt"

PROGRESS = '''<html>
  <head>
    <title>HPC job progress</title>
  </head>

  <body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>This is a waiter. It's waiting on the HPC cluster. It has waited {}/{} seconds.</h3>
    </div>
  </body>
</html>
'''


def main():
    seconds_to_wait = int(sys.argv[1])

    with open(RESULTFILE, 'w') as f:
        f.write('UNSET')

    for current_time in range(seconds_to_wait):
        status = make_progressbar(current_time, seconds_to_wait)
        with open(STATUSFILE, 'w') as f:
            f.write(str(status))
        time.sleep(1)

        if current_time == seconds_to_wait - 1:
            with open(RESULTFILE, 'w') as f:
                f.write('Done. I have waited {} seconds.'.format(seconds_to_wait))

def make_progressbar(current_time, total_time):
    return PROGRESS.format(current_time, total_time)

# ...
```
**Status updates:**
This example application is a simple Python script which does nothing but to
wait for a certain amount of seconds. Every second, a simple html progress page
(as defined in the `PROGRESS` variable) is written to the status file, which is
hard-coded to `/service/status.html`. While the application is running, the HPC
service regularly reads this file and displays its contents to the user.

**Results:**
In addition, a predefined result file (hard-coded to `/service/result.txt`) is
written at the very beginning of the execution and once more when the waiter has
done its work. This file will be read (only once) by the HPC service when the
HPC job running the Singularity image is finished. The contents of the file will
then be forwarded to the output node of the HPC service and can from there be
accessed by other services in the workflow.

This back-communication with the HPC service is relatively straightforward to
set up. However, a few things should be kept in mind:
* As demonstrated above, the status report can be anything from simple text to
  elaborate html pages. Also images are no problem as long as they are embedded
  into the html page.
* If the status report requires some processing of simulation logs etc. (in
  other words, if the actual application does _not_ already output status
  messages which can be directly shown to the user), the simulation/calculation
  and the creation of status pages most likely have to happen in separate
  threads/processes, making the communication a little bit more involved. For an
  example of how this can work, see the [abortable waiter code
  example](../code_examples/Singularity/abortable_waiter).
* If the end result of an HPC job is a non-text file or a large amount of text,
  save the result in a file somewhere in `/home` or `/scratch` and only write
  GSS references to those files into the results file.

## Testing Singularity images locally or on the HPC login node
Before registering a built Singularity image for usage on the SemWES
platform, it is advised to test locally that it works as expected. Therefore,
you can either execute the image locally or copy it onto a HPC login node using
your personal credentials and execute it there.

### Local testing
To test an image under circumstances as close as possible to those when running
as part of a SemWES workflow, please use the following call command:
```bash
singularity exec \
    -H <HOME>:/home -B <SCRATCH>:/scratch -B <SERVICE>:/service \
    <IMAGE> <COMMAND> <PARAMETERS>
```
In this command, replace the following placeholders:
* `<HOME>` by an absolute folder path which will be mounted to `/home` inside
  the Singularity image
* `<SCRATCH>` by an absolute folder path which will be mounted to `/scratch` 
  inside the Singularity image
* `<SERVICE>` by an absolute folder path which will be mounted to `/service` 
  inside the Singularity image
* `<IMAGE>` by the image name
* `<COMMAND>` by the bash command to execute _inside_ the Singularity image
* `<PARAMETER>` by any parameters to pass to the command to be executed

_Side note:_ When you later use your Singularity image inside a SemWES 
workflow, the SemWES HPC service will execute the exact same command for 
you. Some of the parameters listed above will be automatically set for you 
(such as the home and scratch directories), some you will have to provide as
input to the HPC service.

In our waiter example, the command to be executed would be `python`, while the
parameters would be whatever we want to pass to Python, which in this case are
the script name and the number of seconds to wait. The following shows a
complete call command (in the form of a bash script for convencience, also
available as `test.sh` in the [code
example](../code_examples/Singularity/waiter)) which tests the waiter image:

```bash
#! /bin/bash
mkdir temp_home
mkdir temp_scratch
mkdir temp_service

singularity exec \
    -H $(pwd)/temp_home:/home \
    -B $(pwd)/temp_scratch:/scratch \
    -B $(pwd)/temp_service:/service \
    waiter.simg \
    python \
    /app/wait_a_while.py 10
```
Running this bash script will execute the Python application inside the
Singularity image. Since the application does nothing but waiting (in this case
for 10 seconds), you won't see any further output. You will, however, see the
status and result files being created and updated in the newly created
`temp_service` folder.

It is advisable to always perform such local tests before registering an image
with the HPC service, since debugging will be considerably harder once the
image execution is hidden behind several further abstraction layers. See [HPC 
debugging and logs](./basics_hpc_logs.md) for details.

### Testing on an HPC cluster
If you'd like to test an image directly on an HPC cluster, upload it to the
login node and execute `ml Singularity/<version>` to load the Singularity module
before making the above calls. Make sure that the loaded version fits to your
image. You can list all available modules via `ml av`.

## Uploading and registering a Singularity image
Once you have successfully developed and tested a Singularity image, you need
to register it with the SemWES HPC service before you can start using it in
a SemWES workflow. As registration can only happen from files which are
already saved on an HPC cluster's file storage, you need to upload your image
via GSS first.

_Note:_ For each HPC cluster available in CloudiFacturing (currently, the Anselm
and the Salomon cluster operated by IT4I), an individual instance of the
SemWES HPC service is running. This allows it to restrict
simulations/calculations to certain clusters by means of the workflow editor.
However, it also means that you need to upload and register your image with
every HPC service it should be run on.

### Uploading your image
To upload your image to GSS, you can use one of the following methods:
* Start one of the FileBrowser workflows available on the [CloudiFacturing
  portal](https://api.hetcomp.org) and upload via the file chooser application
* Use one of the platform client libraries
  (https://github.com/CloudiFacturing/client_libs)

### Registering your image
#### ... with the clfpy CLI
The easiest way of registering your image is by using the command-line
interface (CLI) of the [`clfpy` Python
library](https://github.com/CloudiFacturing/clfpy). Make sure you have the
latest version of the library installed (`pip install --upgrade clfpy`) and
start the CLI (`clfpy_cli` from anywhere in a console).

You now have two options for registering an image:
1. From within the GSS client (`client gss`), navigate to the GSS folder
   containing your image (make sure it has been uploaded to GSS) and execute
   `img_register FILENAME`. The image will then be registered under the same
   name as the source file name.
2. Make sure you have uploaded your image via the GSS client. From within the
   images client (`client images`), execute `register GSS_URI TARGET_NAME`.
   Here, `GSS_URI` is the GSS URI of the image saved on GSS
   (`it4i_anselm://home/my_image.simg` or similar) and `TARGET_NAME` is the
   name the registered image should have. Remember the `.simg` ending for the
   target name.

#### ... programmatically with the clfpy library
To programmatically register images, use the ImagesClient client of the clfpy
library. In `clfpy/tests/test_hpc.py` of the library source code, you'll find a
working example of how to upload and register an image.

#### ... with the Images SOAP API
To register an image which is available on the HPC-cluster storage, you need to
use the Images SOAP API of the SemWES HPC service(s). Descriptions of the
Images web services for the available clusters are found under the following
URLs:
* IT4I Anselm cluster: `https://api.hetcomp.org/hpc-4-anselm/Images?wsdl`
* IT4I Salomon cluster: `https://api.hetcomp.org/hpc-4-salomon/Images?wsdl`

Use these URLs to create SOAP clients and call their `registerImage()` method
with the following parameters:
* `token`: valid authentication token
* `image_name`: name to use for the registered image (use this for versioning)
* `image_source`: GSS URI of the image to register

## How to move on
Once you have successfully registered an image with the HPC service, you can use
it inside your SemWES workflows. Head over to the [HPC-service
overview](../workflow_creation/HPC_service.md) to learn how to do just that.

The waiter example shown here is very basic and probably won't be enough to
implement real-life HPC use cases. Specifically, one might want to run several
processes in parallel inside the Singularity image (the actual computation, a
job processing log files to create status output, etc.). For details and a more
involved example, have a look at the next article in the HPC series:
[Communicating with a running HPC job](./advanced_hpc_notifications.md).
