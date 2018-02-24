# Tutorial 3-2: Creating a simple asynchronous service
In this tutorial, you will take an existing piece of software (in this case,
it's a very simply Python script which doesn't do anything else but to wait
for a while) and wrap a simple asynchronous service around it, so that the
waiter script can be used on the CloudFlow infrastructure stack.

## Step 1: Prepare the example code
This tutorial starts from the code example
[Waiter tutorial](../../code_examples/Python/async_waiter_tutorial). To begin
with, copy this folder to a new location or alternatively create a new, local
git branch to work on.

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

## Step 2: Code overview
The example directory already contains a full service skeleton and a Docker
container to wrap the service in. For now, have a look at
`app/wait_a_while.py`. In this tutorial, this script is a placeholder for a
long-running complex calculation. The script expects three input parameters
when executed: the number of seconds to wait, the path to a statusfile, and the
path to a results file. In that respect, this script is not different from 
a long-running software package: Consider the first argument as an input to a
complex calculation, while the status file is like a calculation log file. The
results file, finally, is where the "calculation's" results shall be stored. 

The main part of the pre-implemented webservice skeleton is `app/Waiter.py`.
Open that file in a text editor and have a quick look around. You will see an
almost empty definition of a `WaiterService` class as well as a function
`create_html_progresspage()`, which takes a number in percent and creates a
very simple html status page from it.

In the following, we will add two webmethods to the so far empty `WaiterService`
class: one to start the webservice, and one to obtain its current exection
status.

## Step 3: Add a start method to the webservice skeleton
Before we implement the method to start the waiter service, let's think shortly
about the method interface. Every asynchronous service needs to accept at least
two input parameters: The `serviceID` (a unique identifier assigned by the
workflow manager) and the `sessionToken` (an authentication token that can be
used to verify user credentials). In this example, we also want to have the
number of seconds to wait as an input, which leaves us with three input
parameters.

Furthermore, every asynchronous service at least needs to have one output 
parameter, namely `status_base64`, a base64-encoded status string. Additionally,
we want to have another output parameter representing the result of the long-
running program (= the waiter in this case) we start from the service.

### The function definition
With this in mind, add the following method definition to the `WaiterService`
class:
```
    @spyne.srpc(Unicode, Unicode, Integer, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "result"))
    def startWaiter(serviceID, sessionToken, secondsToWait=300):
```
The function decorator `@spyne.srpc(...)` marks the following function
definition as a Spyne SOAP method, which will be made available via the
service's wsdl file. In this decorator, we define the function signature,
specifying two strings (`Unicode`) and one integer input value as well as two
string output values. The input values map directly to the arguments of the
function definition in the next line (`serviceID`, `sessionToken`, and
`secondsToWait`). Since in Python, return arguments are never named, we also
explicitly define the names the return variables will have in the SOAP service
definition.

### The function implementation
The start method needs to do exactly three things:
1. Prepare a unique environment (meaning a location for input, status, and
   output data) for the waiter script to run in.
2. Start the waiter script.
3. Create a first status report to send back to the workflow manager via the
   start method's return arguments.

_Important:_ Note that a CloudFlow service can be run several times in parallel.
It is therefore important that subsequent status-query calls to the service
return information from the correct long-running background process (the waiter
script in this example). Use the unique `serviceID` to distinguish between these
different service executions.

Add the following lines to the method you just created:
```
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        if not os.path.exists(waiterdir):
            os.mkdir(waiterdir)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')
```
We create a temporary folder named after the service ID (`WAITER_LOG_FOLDER`)
is read from an environment variable at the top of `Waiter.py`) to have a
unique environment for the waiter script to run in. We furthermore define paths
for the status and results files.

Now, add the following lines to the function:
```
        command = ['python', 'wait_a_while.py', str(secondsToWait),
                   statusfile, resultfile]
        subprocess.Popen(command)
```
These lines start the waiter script `wait_a_while.py` as a detached subprocess.
It is crucial here that the `startWaiter` method does _not_ wait for this process
to return, which would ruin the idea of an asynchronous service. Instead, the
`subprocess.Popen()` call returns immediately.

Finally, add the following lines to conclude the `startWaiter` method:
```
        status = base64.b64encode(create_html_progresspage(0))
        result = "UNSET"

        return (status, result)
```
We call `create_html_progresspage()` with an initial progress of 0 % (which is
our "best guess" since we actually don't know the stats yet). We then
base64-encode the result page to make it digestable for the workflow manager.
We furthermore set the result value to some value indicating that it is not
assigned yet. (We have to supply this output value, but it won't have any
meaningful content as long as the waiter script is still running.)

_Note:_ The status page we return can be anything from a very simple text file to
a full-fledged html page including, for example, pictures. This way, we can
create a rich feedback for the user during the execution of asynchronous 
services. Have a look at the [level-3 tutorial page](.) for tutorials on the
creation of such status pages.

## Step 4: Implement getServiceStatus()
The second function missing in our service has the pre-defined name
`getServiceStatus()`. This function is called every few seconds by the workflow
manager to query the current execution status of the service until the service
terminates.

Add the following function definition to the `WaiterService` class:
```
    @spyne.srpc(Unicode, Unicode, _returns=(Unicode, Unicode),
                _out_variable_names=("status_base64", "result"))
    def getServiceStatus(serviceID, sessionToken):
```
The function signature is similar to that of the `startWaiter` method. The two
input arguments `serviceID` and `sessionToken` are again mandatory for 
asynchronous services. Note that the output arguments are identical to those of
the start method.

First, our function needs to make sure to query the correct background waiter
script. Therefore, add the following lines to the function:
```
        waiterdir = os.path.join(WAITER_LOG_FOLDER, serviceID)
        statusfile = os.path.join(waiterdir, 'status.txt')
        resultfile = os.path.join(waiterdir, 'result.txt')
```
You can see that this again creates directory and file names using the unique
service ID.

Next, the function should read the status file (which is periodically updated
by the waiter script) and act depending on its content. Add the following lines
to your code:
```
        with open(statusfile) as f:
            current_status = f.read().strip()
```

The waiter script simply writes a number between 0 and 100 into the status file
to indicate its progress, so we can use this number to decide how to proceed.
We first add the logic for when the waiter script has finished to the code:
```
        if current_status == "100":
            status = "COMPLETED"
            # Read result page from waiter
            with open(resultfile) as f:
                result = base64.b64encode(f.read())
            return (status, result)
```
In this case, we report the pre-defined status string `"COMPLETED"`, which tells
the workflow manager that the service has finished and that the next element in
the workflow can now be executed. We furthermore read the waiter script's result
file (which should at this state be filled with something meaningful),
base64-encode it and send it back to the workflow manager together with the
status string.

Finally, we add the logic for when the waiter script has _not_ yet finished its
work:
```
        result = "UNSET"
        status = base64.b64encode(create_html_progressbar(int(current_status)))
        return (status, result)
```
In that case, we use the current status value to again create a html status
page and once again return "UNSET" as the result output.
