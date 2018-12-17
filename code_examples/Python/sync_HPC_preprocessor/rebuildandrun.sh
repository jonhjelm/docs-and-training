#!/bin/bash

cname=prep
port=80

docker kill $cname
docker rm $cname
docker build -t $cname .
docker run -d -p $port:80 --env-file=env --name $cname $cname
