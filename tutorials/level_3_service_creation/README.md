# Level 3: Creation of new services
This level of tutorials covers topics where actual code needs to be touched and
changed.

All tutorials are implemented using Python, which should be easy to read and
transport the right ideas also for non-Python programmers.

## Basic service creation: the different CAxMan service types
Learn how to implement synchronous services, asynchronous services, and
application.

* **[Tutorial 3-1: Deploy and modify synchronous calculator webservice](python_sync_calculator.md)**
  
  This tutorial teaches you how to deploy and modify one of the code examples,
  namely the synchronous Calculator webservice implemented in Python. Good as a
  starting point in the service development.

* **[Tutorial 3-2: Create a simple asynchronous service](python_async_waiter.md)**

  This tutorial guides you through the deployment steps of a simple
  asynchronous service. Starting from a simply Python script representing a
  long-running computation, we will wrap an asynchronous web service around it
  which can be deployed in the CAxMan infrastructure stack.

## Intermediate topics
* **[Tutorial 3-3: File access (showcased via a simple image converter)](python_imageconverter.md)**

  Learn how to programmatically access files via GSS by implementing a simple
  synchronous image conversion service.
