# Changelog

## On the versioning scheme
This document’s version number follows the pattern MAJOR.MINOR.PATCH following
the [semantic-versioning](https://semver.org/) scheme. In a nutshell,
* MAJOR is increased when large, incompatible changes are made. Examples are
  changes in the platform API, removal of components, deployment paths, etc.
* MINOR is increased when smaller, compatible changes are made. Examples are any
  additions which which don’t directly affect existing parts of the 
  documentation, .
* PATCH is increased after cosmetic or clarifying changes (wording, typos, etc.)
  or bugfixes of example code.

With each version, a git tag and an accompanying GitHub release will be created.

## Changelog
### 2019-03-29: Version 3.6.2
* (PATCH) Re-branded "CloudFlow" to "SemWES" throughout the documentation

### 2019-01-14: Version 3.6.1
* (PATCH) Added note on project names with underscores to the [deployment
  manual](./service_implementation/deployment_automated.md).

### 2019-01-11: Version 3.6.0
* (MINOR) Added point-cloud alignment workflow to [demo
  overview](./infrastructure_overview/demos.md).

### 2019-01-10: Version 3.5.0
* (MINOR) Added documentation on how to [launch background HPC jobs](./workflow_creation/HPC_background.md)

### 2019-01-10: Version 3.4.0
* (MINOR) Added code example for Fraunhofer's [input-GUI
  generation](./code_examples/Python/app_generic_gui)
  and [corresponding documentation](./workflow_creation/utilities_auto_gui.md).

### 2019-01-08: Version 3.3.0
* (MINOR) Added documentation of the clfpy CLI where appropriate.
* (MINOR) Added command-line-interface examples to the [deployment
  manual](./service_implementation/deployment_automated.md).
* (MINOR) Added input-GUI demo workflow to [demo
  overview](./infrastructure_overview/demos.md).

### 2018-12-17: Version 3.2.0
* (MINOR) Removed deprecated image-converter example and re-wrote info on GSS
  libraries.
* (MINOR) Added documentation of [in-service token validation](./service_implementation/advanced_authentication.md)
* (MINOR) Added [servicectl API documentation](./service_APIs/api_servicectl.md)
* (MINOR) Created new section on workflow debugging
* (MINOR) Added readme for the asynchronous-service code example
* (MINOR) Added overview page of [demo workflows](./infrastructure_overview/demos.md)
* (PATCH) Updated deployment path and port for debugger code example
* (PATCH) Removed remaining CAxMan elements from calculator tutorial
* (PATCH) Added token validation to code examples
* (PATCH) Removed note on dedicated VMs in [Getting Access](./infrastructure_overview/getting_access.md)
* (PATCH) Updated table of contents on the main page

### 2018-12-11: Version 3.1.0
* (MINOR) Updated [refissh API documentation](./service_APIs/api_refissh.md) to
  reflect latest refissh version

### 2018-12-10: Version 3.0.0
* (MAJOR) Service deployment is now fully automatic, see the [deployment
  manual](./service_implementation/deployment_automated.md).
  Manual deployment on dedicated VMs is now deprecated.

### 2018-12-07: Version 2.2.1
* (PATCH) Improved logging and updated an endpoint URL in the abortable-waiter
  Singularity code example

### 2018-11-30: Version 2.2.0
* (MINOR) Updated [refissh API documentation](./service_APIs/api_refissh.md) to
  reflect latest refissh version

### 2018-11-29: Version 2.1.1
* (PATCH) Updated endpoints of the HPC-service Images endpoint for registration
  of Singularity images.

### 2018-10-31: Version 2.1.0 – Addition of Nvidia support
* (MINOR) Singularity Nvidia support is now automatically activated when IT4I's
  `qviz` queue is selected.  See the [HPC-service
  documentation](./workflow_creation/HPC_service.md) for details.

### 2018-10-15: Version 2.0.0 – Addition of MPI support and Singularity versioning
* (MAJOR) The HPC service's launch method now has four more documented input
  parameters, one of them mandatory (`SingularityVersion`). The other three
  parameters allow the execution of MPI-enabled HPC jobs. See the [HPC-service
  documentation](./workflow_creation/HPC_service.md) for details.
* (MAJOR) Updated the [refissh API documentation](./service_APIs/api_refissh.md)
  to reflect MPI support and the change in mandatory parameters.
* (MINOR) Added basic information on [how to create MPI-ready Singularity
  images](./service_implementation/advanced_hpc_mpi.md).

### 2018-09-26: Version 1.3.3 – Clarify use of /service in Singularity
* (PATCH) Added clarification of the use of the /service mount in Singularity
  images. See article on [Singularity basics](./service_implementation/basics_singularity.md).

### 2018-09-12: Version 1.3.2 – Document wsdl peculiarity of Python spyne
* (PATCH) Added documentation of the peculiar mechanism of wsdl caching when
  using the Python spyne library. See article on [manual service deployment](./service_implementation/deployment_manual.md).

### 2018-08-07: Version 1.3.1 – Fixes refissh API docs
* (PATCH): Fixed parameter list for job submission in the [refissh API](./service_API/api_refissh.md).

### 2018-08-07: Version 1.3.0 – New code examples, description of global parameters
* (MINOR) Added a description of the ["global"
  parameters](./service_implementation/available_parameters.md) available for
  each service.
* (MINOR) Added the [workflow debugger](./code_examples/Python/app-debugger) 
  code example, which is deployed and ready to use for everyone.
* (PATH) Removed hard-coded WFM endpoint from [simple application code example](./code_examples/Python/app-simple).

### 2018-08-02: Version 1.2.1 – Corrected GSS API
* (PATCH) Updated the [GSS API](./service_APIs/api_gss.md) to clarify some 
  ambiguities in the construction of GSS URIs for new files and folders.

### 2018-07-02: Version 1.2.0 – HPC logs, sample preprocessor, service deployment
* (MINOR) Moved [deployment concept](./service_implementation/deployment_strategy.md) into separate deployment section.
* (MINOR) Added documentation of [manual service deployment](./service_implementation/deployment_manual.md)
* (MINOR) Added info on [service upgrades](./workflow_creation/service_upgrades.md)
  and their implications.
* (MINOR) Slight update of documentation on HPC pre- and post-processing services
* (MINOR) New [code example for HPC preprocessors](./code_examples/Python/sync_HPC_preprocessor)
* (MINOR) HPC jobs now expose their log files via GSS, see the [info on HPC
  debugging](./service_implementation/basics_hpc_logs.md) for details.
* (PATCH) Fixed broken link in v1.2.0 changelog
* (PATCH) Added missing part in refissh API reference

### 2018-06-28: Version 1.1.0 – Extends service-type descriptions
* (MINOR) Extends the service-type descriptions and adds the optional
  `notifyService` method to asynchronous services.

### 2018-05-31: Version 1.0.0 – Initial release
This is the initial release which introduces a versioning system for the
platform documentation. Consequently, no further changes are recorded in or
before this release.
