# Accessing cloud storage: Generic Storage Services (GSS)
There are plenty of different cloud-based file storage systems "out there", but
the more one wants to use at a time, the more challenging it gets. One will need
to manage several sets of credentials as well as several different access APIs.

The SemWES platform, however, provides the ability to use several different
storage solutions without having to worry about different APIs or credentials at
all. To accomplish this, Generic Storage Services or GSS have been introduced in
the SemWES project.

## Principles of GSS
The aim of GSS is to abstract all the specifics of different storage solutions
away and instead offer a single, unified entrypoint API for file access. GSS is
a SOAP web service which acts in two distinctly different ways:
1. GSS can act as a _middle man_ between a service on the SemWES platform
   which needs to access files and a storage provider. This means that the
   service which wants to access data calls a method of GSS, which then makes a
   call to the specific storage provider and subsequently delivers the response
   back to the service. Since all data is transported _through_ the GSS service,
   this scheme is only viable for small amounts of data such as file metadata or
   directory-content listings. File transfer, on the other hand, needs to happen
   directly without GSS "in the middle".
2. GSS can act as a _mediator_ between a data-accessing service and a storage
   provider. Here, instead of channeling data through GSS, the GSS service is
   merely providing the data-accessing service with standardized information on
   how to interact with a specific storage provider. Then, the data-accessing
   service can make a direct request to the storage provider, without having to
   know anything about this provider itself.

We provide you with [libraries](service_implementation/basics_gss_libraries.md)
to use GSS easily in your programs. Using those, you don't need to further worry
about how the two scenarios above work exactly. If you do want to gain a deeper
understanding though, have a look at the tutorial on [low-level file
access](tutorials/services/python_imageconverter.md) or take a closer look at
the source code of one of the libraries.

## File and folder representation on the SemWES platform
Any file or folder which is accessible via GSS on the SemWES platform is
identified by a URI of the following form:
```
<backend>://<location>
```
The `<backend>` part identifies the storage provider a file or folder is found
on, and the rest of the URI specifies the location on that specific provider.
Consequently, `<location>` must be unique within a specific provider, but not
across different providers.

Note that in most cases, you won't have to concern yourself with the anatomy of
a GSS URI. In your services, it will mostly just be a string which you use when
interacting with the GSS service.

## Available cloud storage in CloudiFacturing
Currently, the only cloud storage available in CloudiFacturing is the HPC
storage space provided by IT4I on their clusters Anselm and Salomon. (This is an
excellent example for the power of GSS, as HPC storage is conceptually not a
_cloud_ storage. GSS relieves you of the necessity to have your own SSH
credentials and perform file management over SSH.) The two clusters are
considered to be separate GSS backends, since one will usually keep files tied
to the cluster one runs simulations on. For each cluster, space on the `home`
storage as well as on the `scratch` storage is available via GSS.

IT4I's storage is available under the following GSS URI schemes:
* `it4i_anselm://home/<location>`: home storage on the Anselm cluster 
* `it4i_anselm://scratch/<location>`: scratch storage on the Anselm cluster
* `it4i_salomon://home/<location>`: home storage on the Salomon cluster
* `it4i_salomon://scratch/<location>`: scratch storage on the Salomon cluster

To browse any of the storage locations, you can use one of the pre-defined "File
Browser" workflows on the CloudiFacturing portal.

_Note:_ The data visible on IT4I's cluster storage is specific to the project a
user is identified with (i.e., the project one logs in with on the portal).
Users of other projects will not be able to view or edit this data. Similarly,
jobs running as [Singularity containers](service_implementation/basics_hpc.md)
on one of the clusters have access to the same project-specific files and
folders.

## GSS API reference
Read the [GSS API reference here](../service_APIs/api_gss.md).
