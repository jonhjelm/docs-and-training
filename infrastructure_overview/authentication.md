# Users, projects, and authentication
This article collects some good-to-know facts about how user authentication and
data-access restriction works in CloudFlow.

## You always log into a project
Whenever you log into the portal or otherwise obtain a CloudFlow session token,
you lok in not only as a user, but also into a project. The same user can be
associated with several projects, but a login session is always associated
with only one project.

## Authentication is done via session tokens
During login, once your user credentials are validated, a _session token_ is
created which is valid for 24 hours. This session token also carries
information on the project you logged in with.

The session token is made available in all workflows, and all platform services
use the session token for authentication. In the same way, you can use the
session token to make sure that your own services deployed in CloudFlow can
only be used with a valid session token. See [authentication in
services](../service_implementation/advanced_authentication.md) for details.

## Data separation is done on a per-project basis
Users logged in to the same project can see and access the same data on file
storages, see the same registered HPC images, and see and modify the same
services deployed in CloudFlow. All this data cannot be seen when logged in
with another project.
