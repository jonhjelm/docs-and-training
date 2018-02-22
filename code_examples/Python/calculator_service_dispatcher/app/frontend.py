import os
from flask import Flask
from flask import request

app = Flask(__name__)

CONTEXT_ROOT = os.environ['CONTEXT_ROOT']

@app.route(CONTEXT_ROOT + '/')
def root():
    response = "<h1>Hello World</h1>\n<h2>Request headers</h2>"
    for header in request.headers:
        response += "%s: %s<br/>" % (header[0], header[1])
    return response
