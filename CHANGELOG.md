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

### 2018-10-15: Version 2.0.0 – Addition of MPI support
* (MAJOR) In line with major updates to two platform components (refissh and the
  HPC service), the documentation now includes a description of how to enable
  MPI for HPC jobs. Since the function signature for HPC-job launches changed,
  this is a major version upgrade.
* (MAJOR) Updated the [refissh API documentation](./service_APIs/api_refissh.md)
  to reflect MPI support and the change in mandatory parameters.

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