# Workflows and services in the CloudFlow cloud
**TODO**: write content here

## CloudFlow nomenclature
This page describes some of the most important terms you will encounter while
developing services for the CloudFlow infrastructure stack.

* **webservice**: An application which is exposed to the internet, offering
  different webmethods to interact with

* **CloudFlow service**: A single method of a deployed webservice, registered
  with the CloudFlow infrastructure (more precisely, the workflow manager).

  Example: A "Calculator" webservice can have several webmethods, such as
  "add", "subtract", "multiply" etc. Each of those webmethods must be 
  registered as an individual CloudFlow service which to be used in
  CloudFlow workflows.

* **CloudFlow workflow**: A description of a set of CloudFlow services and how
  and when they are executed. Each workflow is executed by the workflow manager.

* **workflow manager**: The webservice responsible for the execution and
  monitoring of CloudFlow workflows. Part of the CloudFlow infrastructure
  stack.

* **workflow editor**: The webservice (not a GUI) responsible for the
  registration and modification of CloudFlow services and workflows. Part of
  the CloudFlow infrastructure stack.

* **workflow editor GUI**: Graphical interface to the workflow editor service.
  Ususally available through a website such as the CloudFlow portal.
