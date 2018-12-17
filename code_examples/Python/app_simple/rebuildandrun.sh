#!/bin/bash

# Builds and runs the container locally (for testing purposes)

cname=app-simple
port=80

docker kill $cname
docker rm $cname
docker build -t $cname .
docker run -d -p $port:80 --env-file=env --name $cname $cname
