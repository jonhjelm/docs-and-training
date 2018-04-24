# Advanced HPC and Singularity topics
This section discusses some more advanced and intricate topics of the HPC and
Singularity usage on the CloudFlow platform. Make sure you have read the
basics on [HPC access](basics_hpc.md) and [Singularity images](basics_singularity.md)
before reading on.

## How to communicate with a running HPC job
Sometimes, communication with a running HPC job can be important. For example,
one might want to restart a simulation or gracefully cancel it when a certain
level of convergence has been reached. At the same time, one often does _not_
want to forcefully abort the whole workflow which contains the HPC job (which is
the only option available through the portal). To this end, the CloudFlow
platform allows to send string messages via the `notifyService()` method of the
workflow manager to a running service.

Since the "distance" of an HPC job running on an HPC cluster and the web browser
from where communication is initiated is quite large, this communication is a
bit more intricate to set up.

Communication with a running job involves mainly two concepts:
1. The HPC-job's status report (which is an html page generated within the 
   Singularity image) needs to provide controls (for example a "Cancel" button)
   which, when activated, call the webmethod `notifyService` from the CloudFlow
   workflow manager. This means that the generated status html needs to contain
   some JavaScript code which performs these calls.
2. The messages sent via this `notifyService` method will be written into a
   specific file inside the HPC-job's `/service` folder (which is also where the
   status and result files are being saved). Consequently, the HPC job needs to
   monitor this file and react to the changes made to it.

The following sections describe these two concepts in more detail.

### Create status reports with elements that talk to the workflow manager
to be written

* HPC service "injects" notification functionality into the status html code
* Injection works only if the code contains a `<head>` element
* Available java script method is `notify_running_job()`
* Link to example

### Make an HPC job react to messages that it receives
to be written

* notifications.txt
* messages are appended

## How to properly set up Singularity images for MPI applications
to be written

* MPI lib -> link to IT4I docs
* how to execute data-crawling processes only on one node (-> _MPI rank_)

## Using GPU acceleration
to be written