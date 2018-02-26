# CloudFlow training resources
Welcome to the CloudFlow training resources!

Here, you will find code examples as well as tutorials for service development
on the CloudFlow infrastructure stack.

## General documentation
Besides code examples and tutorials (see below), documentation is available on
some general topics which are beneficial for the understanding of why services
are developed in certain ways.

* [CloudFlow nomenclature](general_documentation/nomenclature.md): 

  A short description of the most important terms for CloudFlow service
  development. Read this to understand what's written in the tutorials.

* [CloudFlow service types](general_documentation/service_types.md): 

  Description and requirements of synchronous services, asynchronous services,
  and applications. Read this if you're wondering what kind of service you 
  need to develop for a certain use case.

* [Error handling in SOAP services](general_documentation/error_handling.md):

  Explains how to gracefully handle errors inside SOAP services such that the
  outside world can process them.
  

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
on the CloudFlow infrastructure stack. They mostly build upon code examples but
all in all cover fewer topics.

The tutorials are currently divided into three levels:

[Level 1: Introduction to the portal GUI](tutorials/level_1_gui/)

[Level 2: Modifying workflows using the GUI](tutorials/level_2_modifying_workflows/)

[Level 3: Creating new services](tutorials/level_3_service_creation/)
