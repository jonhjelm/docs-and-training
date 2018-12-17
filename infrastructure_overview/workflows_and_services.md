# Workflows and services on the CloudFlow platform
In a nutshell, the CloudFlow platform is a _workflow execution engine_. Here,
a _workflow_ is defined as a set of calculations, simulations, or analytics
tasks which are executed for some specific user input. A typical workflow could
look like this:
1. The end user uploads his/her input to the workflow in the form of input
   files, for example a geometry definition to be used for a finite-element
   simulation task.
2. The user defines further input parameters such as simulation constraints
   through a web-based input mask.
3. A first software package (called _service_) creates a mesh from the input
   geometry and saves it to a mesh input file.
4. A second software package performs a simulation/calculation on the mesh file,
   possibly involving an optimization routine. Simulation results are saved to
   output files.
5. The final output files are interactively analyzed and visualized for the end
   user.

Translated to CloudFlow nomenclature, all points above are individual _steps_ in
a workflow. Behind each step, there stands a cloud-deployed software package
called a CloudFlow _service_. Each such service is a SOAP webservice which
defines a set of input and output parameters and which can be reused arbitrarily
often in any workflow. The CloudFlow _workflow manager_ calls the right service
with its input data for every step, and collects output data for the next
service in the workflow.

The following picture shows a simple workflow as displayed in the CloudFlow
workflow editor GUI (internally, all services as workflows are described and
stored using an xml data format):
<p align="center">
  <img src="workflows_and_services_img/workflow_example_annotated.png"
   alt="Execution diagram of a synchronous service" width="800px"/>
</p>

This particular workflow consists of three steps. Each step uses a CloudFlow
service which is represented by a gray-blue box with input ports on the
left-hand side and output ports on the right-hand side. The first two steps use
the same service (a file chooser application) to let the user interactively
select or upload two different input files. These input files are then passed to
the third step, the output of which constitutes the final workflow result. The
execution order of the different services is indicated by the dashed line.

Note again that each of the gray-blue service boxes represents a CloudFlow
service, meaning a cloud-deployed software package. More specifically, each
gray-blue box stands for a single webmethod of a SOAP webservice, with the
SOAP input and output arguments directly mapped to the input and output ports
at the sides of the boxes.

## CloudFlow platform services
To implement custom workflows on the CloudFlow platform, new custom services
will most likely have to be developed. However, there is a set of available
_platform services_ which provide many basic features needed by most workflows.
Click on the links to see detailed documentation on the individual services.

* [Generic Storage Services (GSS)](storage.md): Provides unified access to files
  and folders on different storage providers. 
* [FileChooser service](../workflow_creation/utilities_filechooser.md): Provides
  a graphical user interface to GSS, can be used to select or upload input files
  or folders.
* [HPC service](../README.md#using-hpc-resources): Provides unified access to
  computations on high-performance-computing clusters.
* [Workflow editor and its GUI](../README.md#basic-workflow-editing): The
  central entrypoint for registering new services and creating workflows.
* [DFKI workflow utilities](../workflow_creation/utilities_dfki.md): A set of
  small utility services to provide user interaction during workflow execution.
* [User-input GUI creation tool](../workflow_creation/utilities_auto_gui.md):
  Utility service which creates HTML user-input masks from a tabular description
  of required input parameters.
* Authentication services: Handles user management, authentication, and
  authorization on the CloudFlow platform.
* Workflow manager: The central workflow execution service. Invoked usually via
  the CloudFlow portal.

## CloudFlow nomenclature
This section describes some of the most important terms you will encounter while
developing services for the CloudFlow platform stack.

* **webservice**: An application which is exposed to the internet, offering
  different webmethods to interact with

* **CloudFlow service**: A single method of a deployed webservice, registered
  with the CloudFlow platform (more precisely, the workflow manager).

  Example: A "Calculator" webservice can have several webmethods, such as
  "add", "subtract", "multiply" etc. Each of those webmethods must be 
  registered as an individual CloudFlow service to be used in CloudFlow
  workflows.

* **CloudFlow workflow**: A description of a set of CloudFlow services and how
  and when they are executed. Each workflow is executed by the workflow manager.

* **workflow manager**: The webservice responsible for the execution and
  monitoring of CloudFlow workflows. Part of the CloudFlow platform
  stack.

* **workflow editor**: The webservice (not a GUI) responsible for the
  registration and modification of CloudFlow services and workflows. Part of
  the CloudFlow platform stack.

* **workflow editor GUI**: Graphical interface to the workflow editor service.
  Ususally available through a website such as the CloudFlow portal.
