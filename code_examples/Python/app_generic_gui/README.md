Generic GUI Application
===

The _GenericGUIApplication_ is a configurable GUI web application. It allows for interactive parameter specification. When the application runs, it initially constructs appropriate GUI elements for the specified parameters. These GUI elements are incorporated into a web page, which will be presented to the user.

1 Requirements
---

You only require to have docker installed. The docker container installs all required packages automatically and runs the application.

2 Configuration
---
In order to configure the web application, three different configuration files are used. The following sections describe each of them.

#### 2.1 __Environment Variable File for Service Deployment Parameters:__ 
The _env_ file from the directory containing this README file specifies environment variables for the docker container. When the application runs, it reads these environment variables. The _env_ file contains all parameters for service deployment and also specifies the used configuration files for web site construction. The listing below shows a complete _env_ file for service deployment configuration.

```
# CONTEXT_ROOT defines the deployment location relative to the host.
# Set this variable such that it fits to the URL under which the VM hosting the
# app can be reached.
CONTEXT_ROOT=/gui-app

# Define deployment parameters and config file names
# Service name
SERVICE_NAME=GUIApp

# Target name space
TNS=tns

# Configuration file for layout
PAGE_CONFIG=GUIWebPageConfig.xml

# XLS sheet to specify GUI elements
XLS_PARAM_SHEET=GUIAppParameters.xlsx
```

#### 2.2 Configuration File for Web Page Layout:
The _app_ directory contains a configuration file for the web site layout parameters such as font size or title size. The listing below shows a complete layout configuration file. 

```XML
<pageConfiguration>
    <params>
        <param name="layout">top2bottom</param> <!-- Specify the order of GUI elements (top2bottom or left2right)-->
        <param name="orientation">single</param>
		<param name="margin">20</param>
		<param name="margin_direction">left</param>
		<param name="title_size">4</param> <!-- from 1 (large) to 6 (small) -->
		<param name="heading_size">5</param> <!-- from 1 (large) to 6 (small) -->
		<param name="font_size">14px</param> <!-- Size for text other than title and headings -->
    </params>
</pageConfiguration>
```

#### 2.3 Excel-Sheet for GUI Elements:
The _app_ directory also contains an excel sheet, which lists all gui elements. It allows to specify *element name*, *element type*, *unit of measurement*, *default value*, *min/max values*, *checked* state and the name of the *output parameter* for the workflow manager. The min/max parameters can be used to prevent users from specifying malicious parameters but are not mandatory. The checked state option is only used for checkable elements, i.e., checkboxes and radiobuttons. The unit of measurement option can be used to present the unit, e.g., milimeters, of the parameter to the user. Note that the unit of measurement option is mandatory for radiobuttons, since the application assigns radiobuttons of the same unit to the same group. For an complete example of a valid excel stylesheet checkout the *GUIAppParameters.xlsx* file in the *app* directory.

Currently the application supports the following data types:
+ **title**: The title of the web page. This shall be set first.
+ **heading**: Any heading to inform users about the semantics of GUI elements
+ **integer**: Integer input field
+ **decimal**: Float input field
+ **string**: String input field
+ **3 decimals**: Three contiguous decimal input fields
+ **6 decimals**: Six contiguous decimal input fields
+ **radiobutton**: A single radiobutton. To form groups of radiobuttons specify same unit of measurement. Set the value of the *checked* field to *YES* for an initially checked radiobutton.
+ **checkbox**: A single checkbox. Set the value of the *checked* field to *YES* for an initially checked checkbox.


3 Deployment
---
Before service deployment ensure that docker is installed and the service configuration is correct. The deployment of the application just amounts to building and starting the docker container. From the directory containing this README file execute the following:

```
docker build -t <container_name> .
docker run -d -p <host_port>:80 --env-file=env --name <container_name> <container_name>
```

The application runs automatically on the docker container.

Finally, connect the outputs of the GUI application with the input ports of the appropriate services.