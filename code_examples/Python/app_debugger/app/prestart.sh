#! /bin/bash

# Set uwsgi mount point to the defined context root
echo Configuring context root
: "${CONTEXT_ROOT:?Error, variable CONTEXT_ROOT unset or empty}"
sed -i "s#CONTEXT_ROOT#$CONTEXT_ROOT#g" /app/uwsgi.ini
