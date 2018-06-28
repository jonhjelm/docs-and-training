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

### Version 1.1.0 – Extends service-type descriptions
* (MINOR) Extends the service-type descriptions and adds the optional
  `notifyService` method to asynchronous services.

### Version 1.0.0 – Initial release
This is the initial release which introduces a versioning system for the
platform documentation. Consequently, no further changes are recorded in or
before this release.