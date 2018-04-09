# Parameter Extraction for CloudiFacturing Generic User Input asynchronous Web Application

Web applications used for priting often rely on end user input. However, the input parameters and their range have to be specified by the workflow provider to prevent malicious parameters.
One suitable way to provide these input parameters are files provided in the form of a spreadsheet (like xls, ods and xlsx).
These inputs provided in the file are extracted as parameters, converted to HTML5 tags and available for the end user via a web page. This GUI enables users to interactively change the values or check for correctness before submitting it for processing.

## Setting up the Web Application

This section describes how to configure the asynchronous web application for generation of GUI in CAxMan portal.

### Prerequisites

The module is developed and tested for python 2.7. So, a python environement for the execution is necessary.

In order to run this module we need to install the following python 2.7 listed in **requirements.txt**. This file is present under the project folder.
The dependencies can be installed using the following command:

```python
pip install -r requirements.txt
```
However, if **pip** is absent. It can installed using the following command:

```python
python get-pip.py
```

The application can also depend on the following helper files in the parent folder:

1. fileHelper.py - used to parse the spreadsheet and configuriation file
2. sessionHelper.py - used to validate the current session token

### Set Up

The first step is to set up the service in the CAxMAn WFM. The documenation of setting up a service is already available.

In addition, **extraParameters** has to be connected to the newly created service. Those parameters contian information about the location of the workflow manager.

Next, the user has to specify a configuration file written in .xml. This is used to initialize the server and attach the main application to this module.
The configuration file details are shown in the sample as follows:
```xml
<?xml version="1.0"?>
<config>
	<serverConfiguration>
		<location>http://localhost</location>
		<port>8080</port>
		<action>http://localhost</action>
		<namespace>default</namespace>
		<prefix>ns0</prefix>
		<trace>True</trace>
		<ns>True</ns>
		<name>Cavity Creation Configuration UI</name>
	</serverConfiguration>
	<serviceConfiguration>
		<file>CAxManPrintingParameters.xlsx</file>
		<script>webApp_UserInput</script>
	</serviceConfiguration>
</config>
```
In the tag **serverConfiguration** is used to read the *location*, *port*, *action*, *namespace*, *prefix*, *trace*, *ns*, *name*. These fields are used by the portal to identify the *service* before launching the application.

1. **location** : The URL of the service.
2. **port** : The port of the service.
3. **action** : Specfies where to lookUp the service using the URL.
4. **name**: Name of the Particular Service/Application.

The default values should be just fine for the rest of the fields.

The tag **serviceConfiguration** specifies the application module (here webApp_UserInput.py) and the spreadsheet (here CAxManPritingParameters.xlsx) that is needed to initialize the application.

### List of currently Supported Datatypes.

Mapping w.r.t to the types and dimensions( as specified in *Unit of Measurements* ) provided in the SpeadSheet.

1. **string** - string
2. **decimal** - integer or floating point based on default values
3. **3 decimals** - 3 fields having integer or floating point based on default values
4. **6 decimals** - 6 fields havaing integer or floating point based on default values

The web application is responsible for creation and validation of the fields. It also checks if the field is mandatory, minimum and maximum allowed values.

## Running the Application

The following steps are for using the the Generic Web Application interface for developing the CAxMan applications:

1. Fork or copy the module *Web_Application_Generic*.
2. Install the **Prerequisites**.
3. Check if the dependencies are present in the parent path *"/PythonTools"*.
4. Setting Up the *serverConfiguration* for the server.
5. Setting Up the *serviceConfiguration* for the Application. This includes providing the path to the application module in the **script** tag and input file if any in **file** tag.
6. Finally Launch the application service using the followingn command:
```python
python webAppInterface.py
```
7. The application when accessed in the CAxMan portal should display the generated GUI.
8. On submission it passes the parameters to the workflow manager. Parameter by parameter. Consequently, you can connect different parameters with different services. Submission **is only allowed, if** all parameters are in their allowed range.

