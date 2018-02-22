FROM tiangolo/uwsgi-nginx-flask:python2.7

# Install required Python packages
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY app/ /app
