# WARNING: This document is outdated!
This is the description of version 3 of the HPC service, which has been replaced
by version 4 in the meantime. This document only serves legacy purposes and will
be deleted soon.

# Overview over the generic HPC service
This document gives an overview over the CloudFlow HPC service and describes how
to use it to execute Singularity images on an HPC cluster.

_Note:_ You might want to read the [instructions on how to create and register
Singularity images](../service_implementation/basics_singularity.md) first.

## Integrating the generic HPC service in a workflow
There is a separate instance of the HPC service deployed for each of the
available HPC clusters. Use the following URIs in the workflow editors to add
one of them to your workflow:
* Anselm cluster: `http://www.cloudifacturing.eu/async/sintef/hpcLaunch_Anselm.owl#hpcLaunch_Service`
* Salomon cluster: `http://www.cloudifacturing.eu/async/sintef/hpcLaunch_Salomon.owl#hpcLaunch_Service`

The following screenshot shows the service inside the workflow editor:
<p align="center">
  <img src="img_hpc/wfe_screenshot_v3.png"
   alt="Minimal connections made to the file-chooser service" width="500px"/>
</p>

The complete set of input parameters is explained in the following table:

| Parameter name | Wiring required? | Description |
| -------------- | --------- | ----------- |
| `sessionToken` | yes | The session token used for authentication. Should be connected to the workflow input with the same name |
| `serviceID` | no | Provided automatically by the WFM, must be left open. |
| `imageName` | yes | Name of the Singularity image to execute. The image must have been registered before usage. |
| `commandline` | yes | The shell command to execute inside the Singularity image, without any parameters. |
| `parameters` | yes | The parameters to the command specified in `commandline`. |
| `queue` | yes | The cluster's queue to run the job on. |
| `numNodes` | yes | Number of nodes to reserve for the job. |
| `numCores` | yes | Number of CPUs to reserve on each node. Note that each cluster-queue combination has a minimum and maximum value for this parameter. |
| `maxDurationInMinutes` | yes | Maximum runtime after which a job will be aborted automatically. |

The above parameters are combined and passed to the queueing software on the
cluster. Note that the image name, command line, and parameters result in the
following Singularity execution command:
```shell
singularity exec --cleanenv [...] <imageName> <commandline> <parameters> [...]
```

**Example:**
If your Singularity execution call is `singularity exec my_image.simg python
/app/my_software.py inp.file -c 120`, the parameters should be:
* imageName: `my_image.simg`
* commandline: `python`
* parameters: `/app/my_software.py inp.file -c 120`

### Output arguments
| Parameter name | Wiring required? | Description |
| -------------- | --------- | ----------- |
| `status_base64` | no | Used by the workflow manager to query status reports. |
| `result` | yes | When the job finished, this argument will contain whatever the Singularity image has written into the file `/service/result.txt`. |

## Further reading
* _GSS &harr; file path conversion:_ Most likely, your HPC job will process some
  input files and create some output files as well. Since files are represented
  by GSS URIs on the CloudFlow platform but by ordinary file paths in the HPC
  environment, it is necessary to [convert between these two
  representations](HPC_gss_conversion.md).

* _Pre- and post-processing services:_ Also, hard-coding parameters like the
  command line and its parameters is often not practical (consider varying input
  file names). Therefore, it will most often be necessary to also create simple
  [pre- and post-processing services](HPC_prepost.md) alongside with a
  Singularity image.