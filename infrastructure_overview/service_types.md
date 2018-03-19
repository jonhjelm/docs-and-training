# Service types in the CloudFlow platform
The CloudFlow infrastructure stack currently knows three types of CloudFlow
services. It is important to understand the differences between those types
in order to choose the right type for a certain use case.

_Important:_ In this document, "service" generally refers to a CloudFlow
service rather than a webservice. A single webservice application may contain
several webmethods which can be used as different types of CloudFlow
services.

## TLDR (Too Long, Didn't Read)
For the impatient, here are a few general rules of thumb for choosing the right
type of service to develop.

* Make a **synchronous service** only when you can _guarantee_ that it will
  _always_ execute in a time of under 10 seconds.
  
  Do _not_ make a synchronous service if it requires file input or will need to
  do any network communication with other services.
  
  Do _not_ make a synchronous service if you want user interaction or show
  status reports to the user while the service is running.

* Make an **asynchronous service** or **application** when you cannot guarantee
  a short execution time (< 10 seconds). Make an asynchronous service or
  application when you need file input or output or any network communication
  during execution.

  * Make an **asynchronous service** if you want to have status reports
    delivered to the user during execution. These reports can be simple text or
    complex html pages.

    Do _not_ make an asynchronous service if you require user interaction
    during service execution.

  * Make an **application** if you want the user to _interact_ with your service
    during its execution.

Curious what distinguishes the three service types from each other and why the
rules above are as they are? Read on.

## Synchronous services
Synchronous services are the simplest types of CloudFlow services. They are
wrappers of single webservice methods which, when called, do something, and
then immediately return their results. They do not require any pre-defined
input or out values.

_Important:_ A synchronous service has to return its response within the HTTP
request timeout time. If it fails to do so, it is automatically terminated by
the workflow manager. This response time is not strictly defined but ranges
typically around 10 to 30 seconds, so synchronous services fit only for simple
tasks. They can be compared to simple command-line commands which take some
input and immediately return some output.

_Hint:_ If your service needs to upload and/or download files via GSS, it most
likely should _not_ be a synchronous service since file upload and download time
depends heavily on file size and the current network speed.

Below you see the execution schema of a synchronous service and its interplay
with the workflow manager during a workflow execution.
<p align="center">
  <img src="service_types_img/sync_service_execution.png"
   alt="Execution diagram of a synchronous service" width="400px"/>
</p>

## Asynchronous services
Asynchronous services are meant for operations which possibly take longer to
complete than the HTTP request timeout time. These are especially operations
which have file input or output, need to interact with other services over the
network or in general have completion times which depend significantly on their
specific input values. Examples are file converters, meshers, solvers, etc.

Asynchronous services are regularly queried by the workflow manager for their
current status. Via these queries, they can report their status in the form
of an html page which will be displayed to the user executing the workflow.
These pages can also include images, but they do not allow user interaction.

Below you see the execution schema of a synchronous service and its interplay
with the workflow manager during a workflow execution.
<p align="center">
  <img src="service_types_img/async_service_execution.png"
   alt="Execution diagram of an asynchronous service" width="600px"/>
</p>

## Applications
Applications are very similar to asynchronous services, but with a slightly
different scope. While an asynchronous service, once started, runs without any
further user input (it only shows output to the user regularly), applications
are designed to interact with the user while they are being executed. Instead
of being queried for their status by the workflow manager, they have to
actively report to the workflow manager once their execution is finished.

Below you see the execution schema of a synchronous service and its interplay
with the workflow manager during a workflow execution.
<p align="center">
  <img src="service_types_img/application_execution.png"
   alt="Execution diagram of an application" width="600px"/>
</p>
