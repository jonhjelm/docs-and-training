# We base this on Python 2.7 since flask-spyne doesn't support Python 3
FROM python:2.7-stretch

# Install necessary Python packages
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

# Copy app into container
RUN mkdir /app
COPY app/ /app

EXPOSE 5000

WORKDIR /app

ENTRYPOINT ["./runscript.sh"]
