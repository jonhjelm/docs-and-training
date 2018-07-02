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

### 2018-07-02: Version 1.4.0 – Added info on service upgrades
* (MINOR) Added info on [service upgrades](./workflow_creation/service_upgrades.md)
  and their implications.

### 2018-07-02: Version 1.3.0 – Added sample preprocessor
* (MINOR) Slight update of documentation on HPC pre- and post-processing services
* (MINOR) New [code example for HPC preprocessors](./code_examples/Python/sync_HPC_preprocessor)
* (PATCH) Fixed broken link in v1.2.0 changelog
* (PATCH) Added missing part in refissh API reference

### 2018-07-02: Version 1.2.0 – New info on HPC logs and debugging
* (MINOR) HPC jobs now expose their log files via GSS, see the [info on HPC
  debugging](./service_implementation/basics_hpc_logs.md) for details.

### 2018-06-28: Version 1.1.0 – Extends service-type descriptions
* (MINOR) Extends the service-type descriptions and adds the optional
  `notifyService` method to asynchronous services.

### 2018-05-31: Version 1.0.0 – Initial release
This is the initial release which introduces a versioning system for the
platform documentation. Consequently, no further changes are recorded in or
before this release.