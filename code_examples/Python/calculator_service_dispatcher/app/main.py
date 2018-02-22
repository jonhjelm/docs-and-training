import os

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from frontend import app as frontend
from CalculatorService import app as calculator

CONTEXT_ROOT = os.environ['CONTEXT_ROOT']

app = DispatcherMiddleware(frontend, {
    CONTEXT_ROOT + '/calculator': calculator,
})


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
