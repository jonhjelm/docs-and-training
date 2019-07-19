FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7

# Install dependencies
COPY requirements.txt /tmp
RUN apk add --update --virtual build-dep make gcc musl-dev python3-dev libxml2-dev libxslt-dev \
  && pip3 install -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt \
  && apk del build-dep \
  && rm -rf /var/cache/apk/*

ENV UWSGI_CHEAPER 1
ENV UWSGI_PROCESSES 2

# Copy app into container
COPY app/ /app
