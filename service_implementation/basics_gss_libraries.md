# Libraries for high-level GSS access
If you need to access files via GSS in your services, and if your services are
implemented in Python like most of the code examples here, it is highly
recommended to use the `clfpy` Python library
(https://github.com/CloudiFacturing/clfpy). The following paragraphs give a
minimal example of how to use `clfpy`, for more detailed examples, visit the
library's GitHub pages.

If you cannot use this library, you can of course also create your own library
which interfaces with the [GSS API](../service_APIs/api_gss.md). It's also
worth while to check out some of the [other client
libraries](https://github.com/CloudiFacturing/client_libs). However, most of
these are currently not maintained actively.

## File access in Python using clfpy
The following snippet gives you a quick idea of how file access can work inside
your services. The snippet assumes that
* a valid session token is available in the variable `token`,
* the GSS endpoint is stored in `gss_endpoint` (the GSS endpoint is one of the
  [_extraParameters_](../service_implementation/available_parameters.md) which
  is passed into any workflow),
* a GSS ID has been passed to the service and is stored in `gss_ID`.

```python
from clfpy import GssClient

# ...

gss = GssClient(gss_endpoint)
download_destination = "/tmp/newfile.bin"
gss.download_to_file(gss_ID, token, download_destination)
```

## Interactive file access using the clfpy CLI
The clfpy library comes with an interactive command-line interface (CLI) which
also includes a GSS client. To use this client, make sure you have the latest
version of clfpy installed (`pip install --upgrade clfpy`), start the CLI
(execute `clfpy_cli` from any console), and select the GSS client (`client gss`
in the CLI).
