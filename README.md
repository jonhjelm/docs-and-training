# Service and workflow development in CAxMan
Welcome to the CAxMan service-development resources!

This repository is meant to be a center for CAxMan documentation relevant for
everyone who develops services and workflows in the CAxMan project. Here, you
will find everything from high-level descriptions of the concepts behind the
CAxMan infrastructure to step-by-step tutorials for advanced topics in CAxMan
service development.

## Infrastructure overview
New to the CAxMan project? Read all about its concepts and background here.

* [Workflows and services in the CAxMan cloud – an overview](infrastructure_overview/workflows_and_services.md):
  Gives a compact overview over the concepts behind CAxMan and what services and workflows are and how they are
  executed. Also explains the nomenclature used in CAxMan.

* [The CAxMan service types](infrastructure_overview/service_types.md): 
  Description and requirements of synchronous services, asynchronous services,
  and applications. Read this if you're wondering what kind of service you 
  need to develop for a certain use case.

* [Deployment strategy](infrastructure_overview/deployment_strategy.md): 
  Why do we recommend Docker for service deployment? How should I set up my
  VM(s)? How do I deploy several Docker containers when I have only a single
  available port? Learn about the CAxMan deployment strategy here.

## Service implementation: concepts, examples, tutorials
All workflows in CAxMan are basically a series of calls to individual web 
services. This section provides information on how to develop such web
services in a way that they can be registered in the CAxMan cloud.

All documentation here deals with things done "in code" (as opposed to via
the graphical tools provided on the portal).

### Basics
* **Synchronous services:**
  * Check out the [CAxMan service types](infrastructure_overview/service_types.md)
    for a high-level description of synchronous services.
  * [Code example (Python): synchronous service](code_examples/Python/sync_calculator):
    A very simple synchronous calculator service implemented in Python
  * [Code example (Java): synchronous-service skeleton](code_examples/Java/skeleton_syncservice):
    Bare-bone skeleton of a synchronous service
  * [Tutorial: Deploy and modify synchronous calculator webservice](tutorials/services/python_sync_calculator.md):
    This tutorial teaches you how to deploy and modify one of the code examples,
    namely the synchronous Calculator webservice implemented in Python. Good as a
    starting point in the service development.


* **Aynchronous services:**
  * Check out the [CAxMan service types](infrastructure_overview/service_types.md)
    for a high-level description of asynchronous services.
  * [Code example (Python): Waiter](code_examples/Python/async_waiter):
    An asynchronous service which does nothing but waiting
  * [Tutorial: Create a simple asynchronous service](tutorials/services/python_async_waiter.md):
    This tutorial guides you through the deployment steps of a simple
    asynchronous service. Starting from a simply Python script representing a
    long-running computation, we will wrap an asynchronous web service around it
    which can be deployed in the CAxMan infrastructure stack.


* **Applications:**
  * Check out the [CAxMan service types](infrastructure_overview/service_types.md)
    for a high-level description of applications.
  

* [Testing SOAP services](service_implementation/basics_testing.md):
  Explains how deployed SOAP services can be tested without having to go
  through the workflow manager.


* **File access:**
  * [Tutorial: Low-level file access (showcased via a simple image converter)](tutorials/services/python_imageconverter.md):
    Learn how to programmatically access files via GSS by implementing a simple
    synchronous image conversion service. This tutorial also teaches you an
    understanding of how GSS works, but it won't show you production-quality
    code.
  * [High-level file access using GSS libraries](service_implementation/basics_gss_libraries.md):
    In practice, one most likely wants to hide the interplay of SOAP and REST
    calls when accessing GSS behind some kind of library. This article gives
    an overview over existing libraries and their usage.
    

* [Using the HPC service: pre- and post-processor services](service_implementation/basics_HPC_service.md):
  Explains how one can interface with the generic HPC service by writing
  pre- and post-processor services.

### Advanced topics

* [Error handling in SOAP services](service_implementation/advanced_error_handling.md):
  Explains how to gracefully handle errors inside SOAP services such that the
  outside world can process them.

* [Beyond files: Using PLM for versioning and metadata](service_implementation/advanced_plm.md):
  Sometimes simple files just don't cut it. PLM offers versioning, metadata,
  and much more. Find out how to interface with PLM in your services.

* [Using authentication services inside a service](service_implementation/advanced_authentication.md):
  When a service is executed inside a workflow, the portal takes care that
  proper user authentication. If necessary, however, the authentication
  manager can also be used inside services.

## Workflow creation, execution, and monitoring
Once all required web services are developed, they need to be registered and
hooked up to make a workflow. This section deals with all things done
"graphically" via the tools provided on the portal.

### Basic workflow editing
* [Tutorial: Overview over the portal GUI](tutorials/workflows/basics_portal_overview.md):
  In this tutorial you will get to know the portal GUI, start a workflow and
  inspect its results.
  
* [Tutorial: Basic workflow editing](tutorials/workflows/basics_editing.md):
  In this tutorial you will load, modify, and save an existing workflow using the
  graphical workflow editor.
  
* [Tutorial: Publishing workflows](tutorials/workflows/basics_publishing.md):
  To make workflows available for execution, you need to *publish* them. This
  tutorial teaches you how.
  
* [Tutorial: Registration of new services](tutorials/workflows/basics_service_registration.md):
  Any newly created service needs to be registered properly to be usable in
  CAxMan. Learn about all details and caveats of service registration here.

### Available utility services
* [File selection using the FileChooser service](workflow_creation/utilities_filechooser.md):
  The FileChooser service is one of two ways to easily let the user upload and
  select files for a workflow. Learn how to integrate the file chooser into
  your workflows.

* [Using the PLM web client](workflow_creation/utilities_plm_webclient.md):
  While the FileChooser service can access all storage locations in CAxMan, only
  the PLM web client offers the extended functionality of versioning, metadata, etc.
  Read here how to integrate it in your workflows.

* [Automatic creation of graphical interfaces for user input](workflow_creation/utilities_auto_gui.md):
  Want an HTML form for user input at the start of a workflow? Then use this
  tool which automatically creates one for you with minimal input on your side.

* [DFKI’s utility services](workflow_creation/utilities_dfki.md):
  Want to show some HTML during a workflow? Need a user decision somewhere inside
  the workflow? DFKI's utility suite offers ready-made services just for that.

### Advanced topics
* [Using workflows inside workflows](workflow_creation/advanced_workflow_nesting.md):
  One of the great strengths of the CAxMan workflow concepts is that one can
  use complete workflows as services inside another workflow. Learn about this
  workflow nesting here.

* [Branching and looping](workflow_creation/advanced_branching_looping.md):
  Read how you can implement basic branches and loops using only the workflow
  editor.

## Reference documentation of infrastructure services
If you need information on a specific method of one of the infrastructure
services, have a look at our API references:
* [Workflow manager](service_APIs/api_wfm.md)
* [Workflow editor](service_APIs/api_wfe.md)
* [Authentication manager](service_APIs/api_authentication.md)
* [GSS](service_APIs/api_gss.md)