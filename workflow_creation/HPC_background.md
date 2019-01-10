# Launching HPC jobs in the background
_Note:_ Launching an HPC job in the background is _not_ recommended unless you
know exactly what you are doing.

The HPC service offers a separate launcher interface for launching HPC jobs in
the background. The launch itself is identical to the standard foreground
launch, but the service will return once the job leaves the queue and reports
its first status.

The backgroun launcher has the following additional output arguments:
* `jobID`: HPC job ID, needed as input when terminating a running HPC job
* `hostName`: Meant to contain the host name of the compute node the job is
  running on. In reality, this simply returns the first status text the job
  reports. To make this the host name, set up your Singularity image to 
  execute the following: `uname -n > /service/status.html`

## Launching
Salomon launching method:
```
http://sintef/async/hpcBackgroundLaunch-4-Salomon.owl#hpcBackgroundLaunch_Service
```

Anselm launching method:
```
http://sintef/async/hpcBackgroundLaunch-4-Anselm.owl#hpcBackgroundLaunch_Service
```

## Terminating
Terminate an HPC job running in the background with the following methods.

Salomon:
```
http://sintef/sync/killBackgroundJob-4-salomon.owl#killBackgroundJob_Service
```

Anselm:
```
http://sintef/sync/killBackgroundJob-4-anselm.owl#killBackgroundJob_Service
```
