"""Main entrypoint of the Python-based SOAP webapp

Here, the dispatcher middleware is created and all required parts of the app
are "hooked in".
Adapt this file if you want to add new services to this app.
"""
import os

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from frontend import app as frontend
from Waiter import app as waiter

# Read deployment route from environment variable
CONTEXT_ROOT = os.environ['CONTEXT_ROOT']

# We use a simple, static frontend page and then "hook in" all sub-apps we like
# to have.
# Currently, this is only the calculator, for which we define the hosting
# location
app = DispatcherMiddleware(frontend, {
    CONTEXT_ROOT + '/waiter': waiter,
})


if __name__ == "__main__":
    # Only for debugging! (Will start the app in a simple Python thread
    # without nginx or uwsgi when main.py is directly executed.)
    run_simple('127.0.0.1', 8080, app, use_reloader=True)
