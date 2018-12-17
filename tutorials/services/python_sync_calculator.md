# Tutorial: Extend the synchronous calculator webservice
In this tutorial, you will start with the pre-implemented
[Calculator](../../code_examples/Python/sync_calculator) webservice, deploy it,
and extend it with further functionality.

## Step 1: Prepare the example code
This tutorial starts from the code example
[Calculator](../../code_examples/Python/sync_calculator). To begin with, copy
this folder to a new location or alternatively create a new, local git branch
to work on.

Now, change into the folder containing your copy of the calculator service and
open a terminal there.

### Adapt the webservice's context root
The first thing to do is to adapt the existing code so that the calculator will
run and be reachable after you have deployed it on the CloudFlow platform.
Therefore, you have to tell the service its _relative deployment path_ or
_context root_. In CloudFlow, this path is always made up of two elements:
```
CONTEXT_ROOT=/<project>-<service_name>
```
Here, `<project>` is the project name you log in with, and `<service_name>` is
for you to choose. Please note that `<project>-<service_name>` must have a
maximum length of 32 characters and must consist only of lowercase letters,
digits, and hyphens.

After choosing a suitable service name (you can very well stick to
`calculator`), edit the environment-definition file `env` in the service source
folder and change the context-root definition accordingly.

The Calculator webservice is now deployable.

## Step 2: Build and deploy the webservice locally
To build and deploy the calculator webservice's Docker container on your local
machine, run:
```bash
./rebuildandrun.sh <port>
```
`<port>` defines the port the container will listen on for incoming
connections. If you don't specify a port number, port 80 will be used. The
build script will read the `env` file you adapted in the last step to deploy
the webservice with the correct deployment path.

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
ee605f4c0997        calculator          "/entrypoint.sh /sta…"   2 minutes ago       Up About a minute   443/tcp, 0.0.0.0:80->80/tcp   calculator
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
have a Python 3 environment and the necessary packages (see
`test_client/requirements.txt`) installed. Alternatively, the test client also
comes wrapped in a Docker container.

To build and run this test-client container, execute:
```bash
cd test_client
./build.sh
./run.sh <port>
```
Use the same port number for `<port>` as you used when building the webservice
container above. If you don't specify a port, port 80 will again be used.

You should see output similar to this:
```bash
$ ./run.sh 80
Using port 80
wsdl URL is http://localhost:80/demo-calculator/Calculator?wsdl
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

## Conclusion and further reading
Congratulations! You successfully deployed a synchronous webservice locally and
extended it by a new webmethod.

If you want to, you can now deploy the service on the CloudFlow platform and
afterwards integrate it into a workflow. Head over to the [deployment
manual](../../service_implementation/deployment_automated.md)

For further development, take a look at other tutorials. To learn
more about SOAP development in Python using the Spyne module, head over to the
[Spyne documentation](http://spyne.io/docs/2.10/).
