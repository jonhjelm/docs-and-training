FROM tiangolo/uwsgi-nginx:python2.7-alpine3.7

# Install dependencies
COPY requirements.txt /tmp
RUN apk add --update --virtual build-dep make gcc musl-dev python-dev libxml2-dev linux-headers libxslt-dev \
  && pip install -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt \
  && apk del build-dep \
  && rm -rf /var/cache/apk/*

# Copy app into container
COPY app/ /app
COPY PythonTools/ PythonTools/
