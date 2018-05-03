# Full-featured Singularity example: an abortable waiter
This code example shows how a full-featured Singularity image can be designed,
where besides the actual simulation/calculation software, two more processes are
running in parallel: one log-processing job which creates status reports from
the main application's log files, and one notification monitor which receives
message sent from the outside to the running job and forwards them to the main
application.

The code of this example is structured as follows:
* `app/wait_a_while.py`: the main application
  
  This application does nothing but to wait for a specific amount of time,
  regularly writing a log file. It also checks for the existence of a specific
  file, which is interpreted as an abort command. Once this file exists, the
  application terminates even if the specified waiting time has not been
  reached.

* `app/log_crawler.py`: processes the main application's log files

  This script monitors the main application's log file and creates html status
  pages from them. These status pages are written to the pre-defined status file
  which is read by the HPC service and shown to the user running a workflow 
  through the workflow manager. These html status pages contain an abort button
  which, when clicked, sends the message "ABORT" back to the running job.

* `app/notifications_monitor.py`: interface for incoming messages

  This script acts as an interface to allow the application to react to 
  messages from the outside (sent via the HPC service's feature of posting
  messages to the currently running job). It reads the pre-defined notifications
  file and translates it into commands to the main application. In this example,
  only a command to abort the waiting is implemented. 

* `app/startup.py`: main entrypoint for the Singularity image

  This is the main entrypoint for executing the Singularity image. This script
  performs the following main steps:
  1. It starts the log-crawler script as a background process.
  2. It starts the notification monitor as a background process.
  3. It starts the main application as a foreground process and waits for it
     to finish.

For details, read the code directly, it comes with detailed in-code 
documentation.

## Building, testing, and registration
To build the container, run `build.sh`.

Run `test.sh` to execute the container locally.

Run `python register.py` (after adding your credentials in the file) to upload
and register the image on the CloudFlow platform. Make sure that you have the
[clfpy library](https://github.com/CloudiFacturing/clfpy) installed.

## Container execution through the HPC service
To execute this image through the HPC service, provide the following parameters:
* `commandline`: `"python"`
* `parameters`: `"/app/startup.py <no_of_seconds_to_wait> /app"`
  
  (The second parameter `/app` denotes the path to the application inside the
  container.)

## Example workflows
This code example is included in the following workflow examples:
* http://sintef/workflow/HpcWaiterAbortableAnselm.owl#HPC_Waiter_Abortable_Anselm