# Demo workflows
Try these demo workflows to get a quick impression of what can be done on the
CloudFlow platform.

Note: It is recommended to have a basic knowledge of the different [service
types](./service_types.md) on the CloudFlow platform when executing the demo
workflows, as it will lead to a better understanding of what these workflows
actually do.

## The demo project
Some of the workflows listed here require certain input files. For those
workflows, please log into the `demo` project with your usual username and
password.

Please make sure _not_ to delete or upload any data in the demo project or
perform any other changes.

## The workflows
Note: Feel free to open the workflows in the workflow editor and study them or
use them as the basis for your own workflows. However, please do _not_ modify
any of the workflows listed here.

### Calculator
**Workflow name and URI:** Demo_Calculator (http://demo/workflow/Demo_Calculator.owl#Demo_Calculator)<br/>
**Requires login with demo project:** No

This workflow showcases the multiplication of two numbers entered by the user.
It demonstrates simple user input as well as the usage of synchronous services.

Also see the accompanying [calculator
tutorial](../tutorials/services/python_sync_calculator.md) and full
[calculator code example](../code_examples/Python/sync_calculator).

### Waiter
**Workflow name and URI:** Demo_Waiter (http://demo/workflow/Demo_Waiter.owl#Demo_Waiter)<br/>
**Requires login with demo project:** No

This workflow demonstrates a simple asynchronous service, which does nothing
but waiting for a defined time. While not very spectacular in itself, it
showcases how asynchronous services can have detailed HTML status reports.

Also see the accompanying [waiter
tutorial](../tutorials/services/python_async_waiter.md) and full [waiter code
example](../code_examples/Python/async_waiter).

### Dialog
**Workflow name and URI:** Demo_Dialog (http://demo/workflow/Demo_Dialog.owl#Demo_Dialog)<br/>
**Requires login with demo project:** No

This workflow demonstrates a simple application service. It contains only a
button which, when clicked, will end the application (and therewith also the
workflow).

Also see the accompanying full [dialog code
example](../code_examples/Python/app_simple).

### HPC waiter
**Workflow name and URI:** Demo_HPC_Waiter (http://demo/workflow/Demo_HPC_Waiter.owl#Demo_HPC_Waiter)<br/>
**Requires login with demo project:** Yes (Singularity image registered with the demo project)

This workflow demonstrates CloudFlow's interface to an HPC cluster. It starts
a simple HPC job on IT4I's Anselm cluster and reports the job's status back to
the user. The job itself is not doing anything meaningful, as it is meant for
demonstration only.

The basics of creating Singularity images for HPC jobs are described
[here](../service_implementation/basics_singularity.md).  Also see the
accompanying [HPC waiter code example](../code_examples/Singularity/waiter).

### Abortable HPC waiter
**Workflow name and URI:** Demo_HPC_Abortable_Waiter (http://demo/workflow/Demo_HPC_Abortable_Waiter.owl#Demo_HPC_Abortable_Waiter)<br/>
**Requires login with demo project:** Yes (Singularity image registered with the demo project)

This workflow is very similar to the HPC waiter described above. But while the
HPC waiter only presents the status report from the HPC job, this abortable
waiter adds a communication channel back to the running HPC job, via which the
job can be aborted before the waiting time is over.

Again, the workflow in itself doesn't do anything meaningful, but it can be
seen as a blueprint for an HPC job with a control panel exposed to the user.

A detailed explanation of this additional communication channel can be found
[here](../service_implementation/advanced_hpc_notifications.md).  Also see the
accompanying [HPC abortable waiter code
example](../code_examples/Singularity/abortable_waiter).

### Abortable HPC waiter with pre-processor
**Workflow name and URI:** Demo_HPC_Abortable_Waiter_prep (http://demo/workflow/Demo_HPC_Abortable_Waiter_prep.owl#Demo_HPC_Abortable_Waiter_prep)<br/>
**Requires login with demo project:** Yes (Singularity image registered with the demo project)

This workflows does exactly the same as the abortable waiter described above.
Under the hood, however, it doesn't hard-code the input parameters to the HPC
service, but instead uses a dedicated pre-processor (synchronous) service. For
many HPC jobs where the input parameters depend on user input, such pre-processor
services are necessary.

See [here](../workflow_creation/HPC_prepost.md) for details on pre- and
post-processors. Also see the accompanying [HPC preprocessor code
example](../code_examples/Python/sync_HPC_preprocessor).
