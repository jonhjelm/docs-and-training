# Converting from GSS URIs to HPC-cluster file paths and back
When services on the SemWES platform exchange files and folders, they do that
not by transferring data back and forth between web services. Instead, they
transfer only URIs which are understood by the Generic Storage Service GSS, and
GSS is utilized when interaction with the actual data becomes necessary.

On an HPC cluster, however, GSS URIs don't mean anything. Also, since the 
available storage in CloudiFacturing is this very HPC cluster's storage, taking
detours through GSS makes no sense. At the interface between SemWES services
(which handle GSS URIs) and HPC jobs (which handle absolute cluster file paths),
a conversion between the two concepts needs to be made. To do so, converter 
services are available for each HPC cluster.

## Usage
Use the workflow editor to include the services into your pre- and
post-processing steps of your HPC workflows. 

## Converters for the Anselm cluster
### GSS URI &rarr; cluster path
* Service URI: http://sintef/sync/convertGssToHpcPath_Anselm.owl#convertGssToHpcPath_Service
* Input arguments: `gssURI` (a valid Anselm GSS URI)
* Output arguments: `path` (corresponding Anselm path)

### cluster path &rarr; GSS URI
* Service URI: http://sintef/sync/convertHpcPathToGss_Anselm.owl#convertHpcPathToGss_Service
* Input arguments: `path` (absolute (starting with `/`) Anselm path)
* Output arguments: `gssURI` (corresponding GSS URI)

## Converters for the Salomon cluster
The same services are available for the Salomon cluster. Use the following
service URIs:
* GSS URI &rarr; cluster path: http://sintef/sync/convertGssToHpcPath_Salomon.owl#convertGssToHpcPath_Service
* cluster path &rarr; GSS URI: http://sintef/sync/convertHpcPathToGss_Salomon.owl#convertHpcPathToGss_Service
