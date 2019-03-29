# How to communicate with a running HPC job
Sometimes, communication with a running HPC job can be important. For example,
one might want to restart a simulation or gracefully cancel it when a certain
level of convergence has been reached. At the same time, one often does _not_
want to forcefully abort the whole workflow which contains the HPC job (which is
the only option available through the portal). To this end, the SemWES
platform allows to send notifications as string messages to a running service.

For a job running via the SemWES HPC service, this communication involves two
concepts:
1. The HPC-job's status report (which is an html page generated within the 
   Singularity image) needs to provide controls (for example a "Cancel" button)
   which, when activated, send messages back to the job itself.
2. These messages will be received by the HPC service and written into a
   specific file inside the HPC-job's `/service` folder (which is where also the
   status und result files are being saved). Consequently, the HPC job needs to
   monitor this file and react to the changes made to it.

The following sections describe these two concepts in more detail.

## Create status reports with elements that talk back to the running job
To create status reports which allow to "talk back" to the running HPC job,
simply create html elements such as buttons which call the
`notify_running_job()` JavaScript method.

Example:
```html
<html>
<head>
    <title>HPC job status</title>
    <script type="text/javascript">
        function abort() {
            notify_running_job("ABORT");
        }
    </script>
</head>
<body>
    <h1>HPC job status</h1>
    <div>
        <h3>Some info on the job status</h3>
        <input type="button" value="Abort this job" onclick="abort()">
    </div>
</body>
</html
```
This html snippet creates a button which, when clicked, calls the method
`notify_running_job()` with the message `"ABORT"`.

_Important:_ You do _not_ have to implement `notify_running_job()` yourself!
This JavaScript method is provided by the SemWES HPC service which runs your
job and is "injected" into the status html before it is forwarded to the
workflow manager. Note that this injection works only if your html status has a
`<head>` tag, so make sure to write valid html.

Obviously, you will have to define the specific message(s) ("ABORT" in the 
example above) sent via the status page such that they fit to what your job
"understands".

## Make an HPC job react to messages that it receives
With the simple html code presented above, your job's status page can be used to
send messages back to the job. Every such message is appended to the pre-defined
file `/service/notifications.txt` inside the job's Singularity container. (As
explained in the [basics of Singularity usage](basics_singularity.md), the
`/service` folder is also where your job needs to save status and result
reports.)

It is your responsibility (as a Singularity-image developer) to monitor changes
to this file and react accordingly. To this end, please keep in mind the 
following:
* On job startup, `/service/notifications.txt` does _not_ exist. It will be 
  created automatically with the first message sent to the job.
* This also means that it is ok for your job to _delete or move/rename_ this
  file whenever necessary or convenient. Once a new message arrives, the file 
  will be re-created.
* Each message is placed on _a new line at the end_ of `notifications.txt`.
  (Specifically, a newline character is appended to each message.) It is 
  _allowed_ to add further newline characters (`"\n"`) to the messages
  themselves if necessary.

## Examples
In general, be aware that the platform provides only a generic tool to send
messages to a running HPC service. The format of these messages and the way of
reacting to them is _entirely_ up to each individual Singularity image.

Nonetheless, we do provide a working example of how such a more complex
Singularity container can be designed. Head over the [abortable_waiter code 
example](../code_examples/Singularity/abortable_waiter) for details.



