# Tutorial 3-1: Extend the synchronous calculator webservice
In this tutorial, you will start with the pre-implemented
[Calculator](../../code_examples/Python/sync_calculator) webservice, deploy it,
and extend it with further functionality. You will then wrap the new 
functionality in a CAxMan service and include it into a workflow.

## Step 1: Prepare the example code
This tutorial starts from the code example
[Calculator](../../code_examples/Python/sync_calculator). To begin with, copy
this folder to a new location or alternatively create a new, local git branch
to work on.

Now, change into the folder containing your copy of the calculator service and
open a terminal there.

### Adapt the webservice's context root
The first thing to do is to adapt the existing code so that it runs smoothly on
your deployment setup. To be able to listen to the correct http requests, the
webservice needs to know its _relative deployment path_ or _context root_.

Example: If you aim to run the service on a VM which is reachable via
`<somehost>/mycompany/myvm` (`<somehost>` can, for example, be
`caxman.clesgo.net`), the context root needs to be set to `/mycompany/myvm`.

The code example we're working with is a Docker container which is configured
via environment variables defined in the `env` file in the source folder. Edit
this file and change the context-root definition to the string appropriate to
your deployment path.

The Calculator webservice is now deployable.

## Step 2: Build and deploy the webservice
To build and deploy the calculator webservice's Docker container, run:
```bash
./rebuildandrun.sh <port>
```
`<port>` defines the port the container will listen on for incoming connections
and must therefore be open to the public and correctly routed on the VM the
container will run on. If you don't specify a port number, port 8080 will be
used. The build script will read the `env` file you adapted in the last step 
to deploy the webservice at the right place.

_Note:_ The initial build process will take a while because the base container
image needs to be downloaded. Subsequent builds will perform much faster.

The script runs the container in daemon mode, meaning that once started, no 
container output will be displayed in the terminal. To confirm that the 
container is running, execute:
```bash
docker ps
```

You should see output similar to this:
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                           NAMES
ee605f4c0997        calculator          "/entrypoint.sh /sta…"   2 minutes ago       Up About a minute   443/tcp, 0.0.0.0:8882->80/tcp   calculator
```
In further docker commands, you can address the container either by its
container ID or by its name (last column of the output), which is `calculator`
in this example.

To inspect the container's startup log, execute:
```bash
docker logs calculator
```
You will see the startup log from nginx (the webserver hosting the webservice
inside the container) and uwsgi (the application server hosting the calculator
Python program).

## Step 3: Check that the webservice works
The code example comes with a simple test client which tests the locally
deployed calculator service. You find it in the `test_client/` folder.

The test client `test_calculator.py` is a simple Python script that calls a few
of the calculator's webmethods. You can either run it directly, given that you
have a Python 3 environment and the necessary packages (see `test_client/requirements.txt`) 
installed. Alternatively, the test client also comes wrapped in a Docker 
container.

To build and run this test-client container, execute:
```bash
cd test_client
./build.sh
./run.sh <port>
```
Use the same port number for `<port>` as you used when building the webservice
container above. If you don't specify a port, port 8080 will be used. 

You should see output similar to this:
```bash
$ ./run.sh 8080
Using port 8080
wsdl URL is http://localhost:8080/sintef/docker_services/calculator/Calculator?wsdl
Testing addition:
11 + 31 = 42.0
Testing subtraction:
11 - 31 = -20.0
Testing multiplication:
11 * 31 = 341.0
```

_Note:_ The run script executes the test client `test_calculator.py` inside a
Docker container which has the required packages installed. It furthermore also
uses the environment configuration you adapted in the last step (`env` file in
the code-example's main folder) to make sure that the correct context root is
used. Open `run.sh` to see the details of this.

_Note:_ You can modify `test_calculator.py` and run the run script without
having to rebuild the test-client container first.

If you again run `docker logs calculator`, you will see some http requests in
the logs which correspond to the function calls the test client made.

### Check that the webservice is reachable from outside
So far, we have accessed the deployed calculator webservice only from inside
the VM it is deployed on. To make sure that it is also reachable from the
outside, open a browser _outside_ of the VM and open the following URL:
```
https://caxman.clesgo.net/<your_context_root>/calculator/Calculator?wsdl
```
Replace `<your_context_root>` with the deployment path of your VM just as you
did in `env` when deploying the calculator service.

The browser should display an xml file. This file describes the interface of
the calculator webservice with all its callable methods. Pay special attention
to the following block:
```xml
<wsdl:portType name="CalculatorService">
  <wsdl:operation name="multiply" parameterOrder="multiply">
    <wsdl:input name="multiply" message="tns:multiply"/>
    <wsdl:output name="multiplyResponse" message="tns:multiplyResponse"/>
  </wsdl:operation>
  <wsdl:operation name="add" parameterOrder="add">
    <wsdl:input name="add" message="tns:add"/>
    <wsdl:output name="addResponse" message="tns:addResponse"/>
  </wsdl:operation>
  <wsdl:operation name="subtract" parameterOrder="subtract">
    <wsdl:input name="subtract" message="tns:subtract"/>
    <wsdl:output name="subtractResponse" message="tns:subtractResponse"/>
  </wsdl:operation>
</wsdl:portType>
```
Here you can see the three webmethods `add`, `subtract`, and `multiply` which
are currently implemented. When integrated into the CAxMan workflow editor,
exactly these webmethods will be available.

If you cannot obtain the wsdl file, check all paths and make sure that the
context root you set at deployment is identical to the path your VM is 
available at. Also check that you deployed the calculator at the port which
is routed to that context-root path.

## Step 4: Implement a division method for the calculator
We will now extend the calculator by implementing another calculation operation,
namely the division of two numbers.

To do so, edit `app/CalculatorService.py`. In the `CalculatorService` class 
definition, there are three methods implemented for the three operations `add`,
`subtract`, and `multiply`. Add another, very similar method below:
```python
    @spyne.srpc(Float, Float, _returns=Float)
    def divide(a, b):
        return a/b
```
_Note:_ It is the function decorator `@spyne.srpc(...)` which makes this
method a SOAP webmethod, defining its input and output signature.

Redeploy the modified webservice by running `./rebuildandrun.sh <port>` as
before. This will stop the running calculator container and replace it with an
updated version. Run `docker ps` to make sure that the modified container
started successfully.

Now, edit `test_client/test_calculator.py` and add the following code at the
end of the function `main()`:
```python
    print("Testing division:")
    response = soap_call(url, "divide", [a, b])
    print("{} * {} = {}".format(a, b, response))
```
Close the file and execute `./run.sh <port>` in the `test_client/` folder. You
should see the additional terminal output for the division.

Finally, refresh the wsdl-file browser page from the last step and confirm that
the newly implemented webmethod is available as another `<wsdl:operation>`
element.

## Step 5: Register the new method as a CAxMan service
You can now head over to the CAxMan portal and register the newly added
division operation as a CAxMan service and subsequently include it in a
workflow. Have a look at the [level-2
tutorials](../level_2_modifying_workflows) to learn how to do this using the
workflow-editor GUI.

## Conclusion and further reading
Congratulations! You successfully deployed a new webservice and extended it by
a new webmethod.

For further development, take a look at other [level-3 tutorials](./). To learn
more about SOAP development in Python using the Spyne module, head over to the
[Spyne documentation](http://spyne.io/docs/2.10/).
