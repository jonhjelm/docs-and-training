# Service and workflow development for the CloudFlow infrastructure stack in CloudiFacturing
Welcome to the CloudFlow/CloudiFacturing service-development resources!

This repository is meant to be a center for documentation relevant for everyone
who develops services and workflows on the CloudFlow infrastructure stack in
the CloudiFacturing project. Here, you will find everything from high-level
descriptions of the concepts behind the infrastructure to step-by-step
tutorials for advanced topics in service development.

## Contents
- [Contents](#contents)
- [Infrastructure overview](#infrastructure-overview)
- [Service implementation: concepts, examples, tutorials](#service-implementation-concepts-examples-tutorials)
  - [CloudFlow Synchronous services](#cloudflow-synchronous-services)
  - [CloudFlow Aynchronous services](#cloudflow-aynchronous-services)
  - [CloudFlow Applications](#cloudflow-applications)
  - [SOAP services](#soap-services)
  - [File access](#file-access)
  - [Using HPC resources](#using-hpc-resources)
  - [Advanced topics](#advanced-topics)
- [Workflow creation, execution, and monitoring](#workflow-creation-execution-and-monitoring)
  - [Basic workflow editing](#basic-workflow-editing)
  - [Using the HPC service](#using-the-hpc-service)
  - [Available utility services](#available-utility-services)
  - [Advanced topics](#advanced-topics)
- [Reference documentation of infrastructure services](#reference-documentation-of-infrastructure-services)

## Infrastructure overview
New to the CloudFlow platform? Read all about its concepts and background here.

* [Workflows and services in the CloudFlow cloud – an overview](infrastructure_overview/workflows_and_services.md):
  Gives a compact overview over the concepts behind CloudFlow and what services
  and workflows are and how they are executed. Also explains the nomenclature
  used in this repository.

* [The CloudFlow service types](infrastructure_overview/service_types.md):
  Description and requirements of synchronous services, asynchronous services,
  and applications. Read this if you're wondering what kind of service you
  need to develop for a certain use case.

* [Accessing cloud storage: Generic Storage Services (GSS)](infrastructure_overview/storage.md):
  On the CloudFlow platform, different cloud storages can be accessed in a
  simple, unified way. Learn about the basic concepts of the CloudFlow
  Generic Storage Services and the available storage solutions in
  CloudiFacturing.

* [Service-deployment concept](infrastructure_overview/deployment_strategy.md):
  Learn about the CloudFlow deployment strategy here.

## Service implementation: concepts, examples, tutorials
All workflows in the CloudFlow platform are basically a series of calls to
individual web services. This section provides information on how to develop
such web services in a way that they can be registered in the CloudFlow
platform.

All documentation here deals with things done "in code" (as opposed to via
the graphical tools provided on the portal).

### CloudFlow Synchronous services
  * Check out the [CloudFlow service types](infrastructure_overview/service_types.md)
    for a high-level description of synchronous services.
  * [Code example (Python): synchronous service](code_examples/Python/sync_calculator):
    A very simple synchronous calculator service implemented in Python
  * [Code example (Java): synchronous-service skeleton](code_examples/Java/skeleton_syncservice):
    Bare-bone skeleton of a synchronous service
  * [Tutorial: Deploy and modify synchronous calculator webservice](tutorials/services/python_sync_calculator.md):
    This tutorial teaches you how to deploy and modify one of the code examples,
    namely the synchronous Calculator webservice implemented in Python. Good as a
    starting point in the service development.


### CloudFlow Aynchronous services
  * Check out the [CloudFlow service types](infrastructure_overview/service_types.md)
    for a high-level description of asynchronous services.
  * [Code example (Python): Waiter](code_examples/Python/async_waiter):
    An asynchronous service which does nothing but waiting
  * [Tutorial: Create a simple asynchronous service](tutorials/services/python_async_waiter.md):
    This tutorial guides you through the deployment steps of a simple
    asynchronous service. Starting from a simply Python script representing a
    long-running computation, we will wrap an asynchronous web service around it
    which can be deployed in the CloudFlow infrastructure stack.


### CloudFlow Applications
  * Check out the [CloudFlow service types](infrastructure_overview/service_types.md)
    for a high-level description of applications.


### SOAP services
* [Testing SOAP services](service_implementation/basics_testing.md):
  Explains how deployed SOAP services can be tested without having to go
  through the workflow manager.

### File access
  * [Tutorial: Low-level file access (showcased via a simple image converter)](tutorials/services/python_imageconverter.md):
    Learn how to programmatically access files via GSS by implementing a simple
    synchronous image conversion service. This tutorial also teaches you an
    understanding of how GSS works, but it won't show you production-quality
    code.
  * [High-level file access using GSS libraries](service_implementation/basics_gss_libraries.md):
    In practice, one most likely wants to hide the interplay of SOAP and REST
    calls when accessing GSS behind some kind of library. This article gives
    an overview over existing libraries and their usage.
    

### Using HPC resources
  * [HPC access through the CloudFlow platform](service_implementation/basics_hpc.md):
    The CloudFlow platform abstracts access of specific HPC resources with a
    generic API, making it possible to run computations on different HPC
    resources without any change to the computation code. This article explains
    the concepts and technical background of this solution.

  * [Packaging software in Singularity images](service_implementation/basics_singularity.md):
    All software that should be run on the HPC resources accessible through the
    CloudFlow platform must be wrapped into Singularity images which are then
    executed as isolated containers on an HPC cluster. Learn how to create,
    upload, and register such images in this article.

### Advanced topics

* [Error handling in SOAP services](service_implementation/advanced_error_handling.md):
  Explains how to gracefully handle errors inside SOAP services such that the
  outside world can process them.

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
  In this tutorial you will load, modify, and save an existing workflow using
  the graphical workflow editor.
  
* [Tutorial: Registration of new services](tutorials/workflows/basics_service_registration.md):
  Any newly created service needs to be registered properly to be usable in the
  CloudFlow platform. Learn about all details and caveats of service
  registration here.

### Using the HPC service
* [Overview over the generic HPC service](workflow_creation/HPC_service.md):
  Introduces the generic HPC service and showcases how it can be used to
  execute Singularity images on the available HPC resources.

* [Pre- and post-processor services](workflow_creation/HPC_prepost.md):
  Explains how one can interface with the generic HPC service by writing pre-
  and post-processor services.

### Available utility services
* [File selection using the FileChooser service](workflow_creation/utilities_filechooser.md):
  The FileChooser service is one of two ways to easily let the user upload and
  select files for a workflow. Learn how to integrate the file chooser into
  your workflows.

* [Automatic creation of graphical interfaces for user input](workflow_creation/utilities_auto_gui.md):
  Want an HTML form for user input at the start of a workflow? Then use this
  tool which automatically creates one for you with minimal input on your side.

* [DFKI’s utility services](workflow_creation/utilities_dfki.md):
  Want to show some HTML during a workflow? Need a user decision somewhere inside
  the workflow? DFKI's utility suite offers ready-made services just for that.

### Advanced topics
* [Using workflows inside workflows](workflow_creation/advanced_workflow_nesting.md):
  One of the great strengths of the CloudFlow workflow concepts is that one can
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
* [refissh](service_APIs/api_refissh.md)
