# Advanced workflow creation: Nesting workflows

Workflows can also be used as services within other workflows, which can ease the creation of more sophisticated workflows, as thereby complex workflows can be divided into different tool-chains or sub-workflows.

Nesting workflows allows you to re-use commonly used tool-chains without re-creating them everytime you need them. This additionally implies that whenever you need to update your tool-chain, you only need to perform those changes in one place.

To add a workflow as a service to your current workflow, just select it from the "Service URI" dropdown-menu and click on "append service to workflow". It will appear as one dark-green block in the graphical editor, featuring its respective inputs and outputs.

Remark: To add additional inputs and outputs to your workflow, you can use the "i" and "o" buttons below the "Service URI"-field.

![wfe_1.png](img_workflows/wfe_1.png)