FROM python:3.6

# Install required Python packages
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
