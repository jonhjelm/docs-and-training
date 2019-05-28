"""Main entrypoint of the Python-based SOAP webapp

Here, all required parts of the app are "hooked in". Adapt this file if you
want to add new services to this app.
"""
import logging
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter

import Cat

logging.basicConfig(level=logging.INFO)

# We use the wsgi mounter to hook up potentially more than one SOAP service
# inside a single app.
application = WsgiMounter({
    Cat.SERVICENAME: WsgiApplication(Cat.create_app())
})


if __name__ == '__main__':
    # Only for debugging! (Will start the app in a simple Python thread
    # without nginx or uwsgi when main.py is directly executed.)
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.INFO)

    server = make_server('0.0.0.0', 5000, application)
    server.serve_forever()
