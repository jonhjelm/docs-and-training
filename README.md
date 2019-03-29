# Service and workflow development for the SemWES platform stack in CloudiFacturing
Welcome to the SemWES/CloudiFacturing service-development resources!

This repository is meant to be a center for documentation relevant for everyone
who develops services and workflows on the SemWES platform stack in
the CloudiFacturing project. Here, you will find everything from high-level
descriptions of the concepts behind the platform to step-by-step
tutorials for advanced topics in service development.

## Contents <!-- omit in toc -->
- [Documentation version](#documentation-version)
- [Contributing](#contributing)
- [Platform overview](#platform-overview)
- [Service implementation: concepts, examples, tutorials](#service-implementation-concepts-examples-tutorials)
  - [General concepts](#general-concepts)
  - [SemWES Synchronous services](#semwes-synchronous-services)
  - [SemWES Aynchronous services](#semwes-aynchronous-services)
  - [SemWES Applications](#semwes-applications)
  - [Service deployment](#service-deployment)
  - [SOAP services](#soap-services)
  - [File access](#file-access)
  - [Using HPC resources](#using-hpc-resources)
  - [Advanced topics](#advanced-topics)
- [Workflow creation, execution, and monitoring](#workflow-creation-execution-and-monitoring)
  - [Basic workflow editing](#basic-workflow-editing)
  - [Using the HPC service](#using-the-hpc-service)
  - [Available utility services](#available-utility-services)
  - [Workflow debugging](#workflow-debugging)
  - [Advanced topics](#advanced-topics)
- [Reference documentation of platform services](#reference-documentation-of-platform-services)

## Documentation version 
Current documentation version: `3.6.2`

See the [Changelog](CHANGELOG.md) for versioning details.

## Contributing
Everyone is *welcome* to contribute to this documentation center. Typos,
clarifications, interesting code examples, or also just questions – anything is
valuable. To contribute, choose one of the following options:
* Fork the repository, add your changes and create a pull request.
* Create an issue in the GitHub issue tracker.
* Write an email with your ideas to [Robert](mailto:robert.schittny@sintef.no)
  (discouraged, rather use one of the options above).

## Platform overview
New to the SemWES platform? Read all about its concepts and background here.

* [Getting access](infrastructure_overview/getting_access.md): Need access to
  the SemWES platform in CloudiFacturing? Look here.

* [Demos](infrastructure_overview/demos.md): If you want to get your hands
  dirty immediately and try out some demo workflows on the platform, look here.

* [Users, projects, and authentication](./infrastructure_overview/authentication.md):
  Gives a short overview of how user authentication and data-access restriction
  works on the SemWES platform.

* [Workflows and services in the SemWES cloud – an overview](infrastructure_overview/workflows_and_services.md):
  Gives a compact overview over the concepts behind SemWES and what services
  and workflows are and how they are executed. Also explains the nomenclature
  used in this repository.

* [The SemWES service types](infrastructure_overview/service_types.md):
  Description and requirements of synchronous services, asynchronous services,
  and applications. Read this if you're wondering what kind of service you
  need to develop for a certain use case.

* [Accessing cloud storage: Generic Storage Services (GSS)](infrastructure_overview/storage.md):
  On the SemWES platform, different cloud storages can be accessed in a
  simple, unified way. Learn about the basic concepts of the SemWES
  Generic Storage Services and the available storage solutions in
  CloudiFacturing.

## Service implementation: concepts, examples, tutorials
All workflows in the SemWES platform are basically a series of calls to
individual web services. This section provides information on how to develop
such web services in a way that they can be registered in the SemWES
platform.

All documentation here deals with things done "in code" (as opposed to via
the graphical tools provided on the portal).

### General concepts
* [Available parameters](./service_implementation/available_parameters.md):
  The workflow manager offers a set of "global" parameters which are available
  to every service. Here, we take a closer look at these parameters and their
  main use cases.

### SemWES Synchronous services
  * Check out the [SemWES service types](infrastructure_overview/service_types.md)
    for a high-level description of synchronous services and their required
    interface.
  * [Code example (Python): synchronous service](code_examples/Python/sync_calculator):
    A very simple synchronous calculator service implemented in Python
  * [Code example (Java): synchronous-service skeleton](code_examples/Java/skeleton_syncservice):
    Bare-bone skeleton of a synchronous service
  * [Tutorial: Deploy and modify synchronous calculator webservice](tutorials/services/python_sync_calculator.md):
    This tutorial teaches you how to deploy and modify one of the code examples,
    namely the synchronous Calculator webservice implemented in Python. Good as a
    starting point in the service development.


### SemWES Aynchronous services
  * Check out the [SemWES service types](infrastructure_overview/service_types.md)
    for a high-level description of asynchronous services and their required
    interface.
  * [Code example (Python): Waiter](code_examples/Python/async_waiter):
    An asynchronous service which does nothing but waiting
  * [Tutorial: Create a simple asynchronous service](tutorials/services/python_async_waiter.md):
    This tutorial guides you through the deployment steps of a simple
    asynchronous service. Starting from a simply Python script representing a
    long-running computation, we will wrap an asynchronous web service around it
    which can be deployed in the SemWES infrastructure stack.


### SemWES Applications
  * Check out the [SemWES service types](infrastructure_overview/service_types.md)
    for a high-level description of applications and their required interface.
  * [Code example (Python): Dialog](code_examples/Python/app_simple):
    Simplest possible example application containing a one-button dialog.
  * [Code example (Python): Debugger](code_examples/Python/app_debugger):
    Debug application for workflows; pauses a workflow and displays parameter
    contents.


### Service deployment
  * [Service-deployment concept](service_implementation/deployment_strategy.md):
  Learn about the SemWES deployment strategy here.

  * [Service-deployment manual](service_implementation/deployment_automated.md):
    Describes how services can be deployed in SemWES


### SOAP services
* [Testing SOAP services](service_implementation/basics_testing.md):
  Explains how deployed SOAP services can be tested without having to go
  through the workflow manager.

### File access
  * If you haven't done so already, it is recommended to read the general
    principles of [accessing cloud storage](infrastructure_overview/storage.md)
    on the SemWES platform.
  * [High-level file access using GSS libraries](service_implementation/basics_gss_libraries.md):
    While it is perfectly possible to directly interact with the GSS API, it is
    highly recommended to use the provided GSS client libraries for file access
    in SemWES. This article gives an overview over existing libraries and
    their usage.

### Using HPC resources
  * [HPC access through the SemWES platform](service_implementation/basics_hpc.md):
    The SemWES platform abstracts access of specific HPC resources with a
    generic API, making it possible to run computations on different HPC
    resources without any change to the computation code. This article explains
    the concepts and technical background of this solution.

  * [Packaging software in Singularity images](service_implementation/basics_singularity.md):
    All software that should be run on the HPC resources accessible through the
    SemWES platform must be wrapped into Singularity images which are then
    executed as isolated containers on an HPC cluster. Learn how to create,
    upload, and register such images in this article.

  * [Communicating with a running HPC job](service_implementation/advanced_hpc_notifications.md):
    Sometimes, communication with a running HPC job is important, for example to
    be able to control or abort a simulation if required. This article explains
    how to set up a Singularity image for this kind of communication.

  * [Debugging HPC applications](service_implementation/basics_hpc_logs.md):
    Debugging HPC applications in SemWES can be difficult due to many
    layers of abstraction between the running application and the user. This
    article gives some hints on debugging and loggin.

  * [Singularity and MPI applications](service_implementation/advanced_hpc_mpi.md):
    Learn how to prepare your Singularity image for parallel
    execution using MPI.

  * [GPU support for Singularity images](service_implementation/advanced_hpc_gpu.md):
    (not written yet) Learn how to prepare your Singularity image for access of
    underlying GPU cores.

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
* Don't forget to have a look at the [demo
  workflows](./infrastructure_overview/demos.md)
  to learn from some pre-defined workflow examples.

* [Tutorial: Overview over the portal GUI](tutorials/workflows/basics_portal_overview.md):
  In this tutorial you will get to know the portal GUI, start a workflow and
  inspect its results.
  
* [Tutorial: Basic workflow editing](tutorials/workflows/basics_editing.md):
  In this tutorial you will load, modify, and save an existing workflow using
  the graphical workflow editor.
  
* [Tutorial: Registration of new services](tutorials/workflows/basics_service_registration.md):
  Any newly created service needs to be registered properly to be usable in the
  SemWES platform. Learn about all details and caveats of service
  registration here.

* [Upgrading services](workflow_creation/service_upgrades.md): 
  Sometimes, an already deployed and registered service needs to be upgraded,
  possibly with changes to the input and output parameters. Read here what to
  keep in mind when performing such upgrades.

### Using the HPC service
* [Overview over the generic HPC service](workflow_creation/HPC_service.md):
  Introduces the generic HPC service and showcases how it can be used to
  execute Singularity images on the available HPC resources.

* [Converting from GSS URIs to file paths and back](workflow_creation/HPC_gss_conversion.md):
  Files and folders are handled using GSS URIs within the SemWES 
  platform, but on an HPC cluster, absolute paths are required. Learn how
  to convert between the two here.

* [Pre- and post-processor services](workflow_creation/HPC_prepost.md):
  Explains how one can interface with the generic HPC service by writing pre-
  and post-processor services.

* [Launching HPC jobs in the background](workflow_creation/HPC_background.md):
  Explains how HPC jobs can be launched in the background, such that other
  parts of the workflow can run in parallel.

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

### Workflow debugging

* [Parameter debugger](code_examples/Python/app_debugger/README.md):
  This simple application offers the option to pause a workflow and display any
  parameters that are currently in use. Great for debugging failing workflows
  or services. Offered as a code example with complete source code.

### Advanced topics
* [Using workflows inside workflows](workflow_creation/advanced_workflow_nesting.md):
  One of the great strengths of the SemWES workflow concepts is that one can
  use complete workflows as services inside another workflow. Learn about this
  workflow nesting here.

* [Branching and looping](workflow_creation/advanced_branching_looping.md):
  Read how you can implement basic branches and loops using only the workflow
  editor.

## Reference documentation of platform services
If you need information on a specific method of one of the platform services,
have a look at our API references:
* [Workflow manager](service_APIs/api_wfm.md)
* [Workflow editor](service_APIs/api_wfe.md)
* [Authentication manager](service_APIs/api_authentication.md)
* [GSS](service_APIs/api_gss.md)
* [refissh](service_APIs/api_refissh.md)
* [servicectl](service_APIs/api_servicectl.md)
