# Service and workflow development in CAxMan
Welcome to the CAxMan service-development resources!

This repository is meant to be a center for CAxMan documentation relevant for
everyone who develops services and workflows in the CAxMan project. Here, you
will find everything from high-level descriptions of the concepts behind the
CAxMan infrastructure to step-by-step tutorials for advanced topics in CAxMan
service development.

## Infrastructure overview
* Workflows and services in the CAxMan cloud: an overview

* [CAxMan nomenclature](general_documentation/nomenclature.md): 
  A short description of the most important terms for CAxMan service
  development. Read this to understand what's written in the tutorials.

* [The CAxMan service types](general_documentation/service_types.md): 
  Description and requirements of synchronous services, asynchronous services,
  and applications. Read this if you're wondering what kind of service you 
  need to develop for a certain use case.

* [Deployment strategy](general_documentation/deployment_strategy.md): 
  Why do we recommend Docker for service deployment? How should I set up my
  VM(s)? How do I deploy several Docker containers when I have only a single
  available port? Learn about the CAxMan deployment strategy here.

## Service implementation: concepts, examples, tutorials

### Basics
* Implementation of a synchronous service

* Implementation of an asynchronous service

* Implementation of an application

* Testing SOAP services

* File access using GSS

* Using the HPC service: pre- and post-processor services

### Advanced topics

* [Error handling in SOAP services](general_documentation/error_handling.md):

  Explains how to gracefully handle errors inside SOAP services such that the
  outside world can process them.

* Beyond files: Using PLM for versioning and metadata

* Using the authentication manager inside a service

## Workflow creation, execution, and monitoring

### Basic workflow editing
* Workflow-editor overview

* Registration of new services

### Available utility services
* File selection using the FileChooser service

* Automatic creation of graphical interfaces for user input

* DFKI’s utility services

### Advanced topics
* Using the PLM web client

* Using workflows inside workflows

* Branching and looping

## Reference documentation of infrastructure services
* Workflow manager
* Workflow editor
* Authentication manager
* GSS
* HPC service

---
Old from here on!

## General documentation
Besides code examples and tutorials (see below), documentation is available on
some general topics which are beneficial for the understanding of why services
are developed in certain ways.


## Code examples
Have a look in the [code examples folder](code_examples). Currently, examples
are available for Python and for Java.

Start with a code example as a template for your own services, or just browse
the examples for clues on how certain things might work.

All examples should be well documented, self-contained, runnable without
modifications and should contain a short readme description.

The tutorials can and will build upon the code examples.

## Tutorials
The tutorials offer step-by-step descriptions of how to perform certain tasks
on the CAxMan infrastructure stack. They mostly build upon code examples but
all in all cover fewer topics.

The tutorials are currently divided into three levels:

[Level 1: Introduction to the portal GUI](tutorials/level_1_gui/)

[Level 2: Modifying workflows using the GUI](tutorials/level_2_modifying_workflows/)

[Level 3: Creating new services](tutorials/level_3_service_creation/)
