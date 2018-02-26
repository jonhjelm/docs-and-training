import os
from flask import Flask

app = Flask(__name__)

CONTEXT_ROOT = os.environ['CONTEXT_ROOT']


@app.route(CONTEXT_ROOT + '/')
def root():
    """Static page to avoid error 404"""
    return "Nothing to see here."
